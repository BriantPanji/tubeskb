# ============================================================
#  tower.py  —  Entitas Menara & Proyektil
# ============================================================

import math
import pygame
from config import CELL_SIZE, TOWER_TYPES


# ── Projectile ────────────────────────────────────────────────
class Projectile:
    """
    Peluru kendali yang ditembakkan oleh Menara.
    Mengejar musuh targetnya sampai mengenai atau musuh mati.
    """

    def __init__(self, x: float, y: float, target,
                 damage: float, speed: float, color: tuple, tower_ref):
        self.x         = x
        self.y         = y
        self.target    = target      # Referensi musuh
        self.damage    = damage
        self.speed     = speed
        self.color     = color
        self.done      = False
        self.size      = 4
        self.tower_ref = tower_ref   # Referensi menara penembak

    def update(self):
        # Target sudah hilang
        if self.done or not self.target.alive:
            self.done = True
            return

        dx   = self.target.x - self.x
        dy   = self.target.y - self.y
        dist = math.hypot(dx, dy)

        if dist <= self.speed:
            was_alive = self.target.alive
            self.target.take_damage(self.damage)
            if was_alive and not self.target.alive:
                self.tower_ref.kills += 1
            self.done = True
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, surface: pygame.Surface):
        if self.done:
            return
        cx, cy = int(self.x), int(self.y)

        # Lingkaran cahaya bersinar
        glow = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*self.color, 55),
                           (self.size * 3, self.size * 3), self.size * 3)
        surface.blit(glow, (cx - self.size * 3, cy - self.size * 3))

        # Inti
        pygame.draw.circle(surface, self.color, (cx, cy), self.size)
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), self.size, 1)


# ── Menara ─────────────────────────────────────────────────────
class Tower:
    """
    Unit pertahanan statis yang ditempatkan oleh pemain.

    Perilaku
    ---------
    Setiap frame menara:
      1. Mengurangi timer cooldown-nya.
      2. Memilih musuh hidup terdekat dalam jangkauan.
      3. Memutar larasnya ke arah target.
      4. Menembakkan Proyektil saat cooldown mencapai 0.
    """

    def __init__(self, col: int, row: int, tower_type: str):
        data = TOWER_TYPES[tower_type]

        # ── Konfigurasi ─────────────────────────────────────────────
        self.col        = col
        self.row        = row
        self.type       = tower_type
        self.name       = data['name']
        self.cost       = data['cost']
        self.damage     = data['damage']
        self.range_px   = data['range'] * CELL_SIZE   # jangkauan dalam piksel
        self.fire_rate  = data['fire_rate']            # tembakan / detik
        self.proj_speed = data['proj_speed']
        self.color      = data['color']
        self.proj_color = data['proj_color']

        # ── Posisi (pusat piksel) ────────────────────────────
        self.x = col * CELL_SIZE + CELL_SIZE // 2
        self.y = row * CELL_SIZE + CELL_SIZE // 2

        # ── Status waktu proses ──────────────────────────────────────
        self.cooldown    = 0.0          # detik hingga tembakan berikutnya
        self.target      = None         # referensi Musuh saat ini
        self.projectiles: list = []
        self.kills       = 0
        self.angle       = 0.0          # rotasi laras (derajat)

    # ----------------------------------------------------------
    def _find_target(self, enemies: list):
        """Pilih musuh hidup terdekat di dalam jangkauan."""
        best, best_d = None, float('inf')
        for e in enemies:
            if not e.alive or e.reached_exit:
                continue
            d = math.hypot(e.x - self.x, e.y - self.y)
            if d <= self.range_px and d < best_d:
                best, best_d = e, d
        self.target = best

    # ----------------------------------------------------------
    def _target_valid(self) -> bool:
        if self.target is None:
            return False
        if not self.target.alive or self.target.reached_exit:
            return False
        d = math.hypot(self.target.x - self.x, self.target.y - self.y)
        return d <= self.range_px

    # ----------------------------------------------------------
    def update(self, enemies: list, dt: float):
        # Majukan cooldown
        self.cooldown = max(0.0, self.cooldown - dt)

        # Bersihkan proyektil yang selesai
        self.projectiles = [p for p in self.projectiles if not p.done]

        # Perbarui proyektil
        for proj in self.projectiles:
            proj.update()

        # Dapatkan / validasi target
        if not self._target_valid():
            self._find_target(enemies)

        if self.target:
            # Putar laras
            self.angle = math.degrees(
                math.atan2(self.target.y - self.y, self.target.x - self.x)
            )
            # Tembak
            if self.cooldown == 0.0:
                self._fire()
                self.cooldown = 1.0 / self.fire_rate

    # ----------------------------------------------------------
    def _fire(self):
        proj = Projectile(
            self.x, self.y,
            self.target,
            self.damage,
            self.proj_speed,
            self.proj_color,
            tower_ref=self,
        )
        self.projectiles.append(proj)

    # ----------------------------------------------------------
    def draw(self, surface: pygame.Surface, show_range: bool = False):
        # ── Cincin jangkauan (saat diarahkan / dipilih) ───────────────
        if show_range:
            r   = int(self.range_px)
            rs  = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(rs, (*self.color, 22), (r, r), r)
            pygame.draw.circle(rs, (*self.color, 65), (r, r), r, 1)
            surface.blit(rs, (self.x - r, self.y - r))

        cx, cy   = int(self.x), int(self.y)
        half     = CELL_SIZE // 2 - 4

        # ── Basis (persegi terisi) ───────────────────────────────
        dark = tuple(max(0, c - 60) for c in self.color)
        base = pygame.Rect(cx - half, cy - half, half * 2, half * 2)
        pygame.draw.rect(surface, dark,       base, border_radius=4)
        pygame.draw.rect(surface, self.color, base, 2, border_radius=4)

        # ── Laras (garis diputar) ──────────────────────────────
        rad     = math.radians(self.angle)
        blen    = half + 5
        bx      = cx + math.cos(rad) * blen
        by      = cy + math.sin(rad) * blen
        pygame.draw.line(surface, self.color, (cx, cy), (int(bx), int(by)), 3)

        # ── Titik pusat ─────────────────────────────────────────
        pygame.draw.circle(surface, (230, 235, 245), (cx, cy), 3)

        # ── Proyektil ────────────────────────────────────────
        for proj in self.projectiles:
            proj.draw(surface)
