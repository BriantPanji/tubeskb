# ============================================================
#  enemy.py  —  Entitas Musuh
#
#  Setiap musuh memegang salinan jalur A* dan menginterpolasi
#  dengan mulus di antara pusat sel. Saat pemain menempatkan
#  menara baru, GameState memanggil enemy.update_path() sehingga setiap
#  musuh yang hidup dengan mulus mengubah rute di sekitar rintangan —
#  menunjukkan perencanaan ulang A* secara real-time.
# ============================================================

import math
import pygame
from config import CELL_SIZE, ENEMY_TYPES


class Enemy:
    """
    Satu unit musuh yang mengikuti jalur komputasi A*.

    Atribut
    ----------
    alive        : True sampai HP mencapai 0 (dibunuh oleh menara → mendapatkan emas)
    reached_exit : True ketika musuh berjalan keluar dari tepi kanan (kehilangan nyawa)
    """

    def __init__(self, enemy_type: str, path: list):
        data = ENEMY_TYPES[enemy_type]

        # ── Statistik ──────────────────────────────────────────────
        self.type       = enemy_type
        self.name       = data['name']
        self.max_hp     = data['hp']
        self.hp         = data['hp']
        self.speed      = data['speed']     # px / frame
        self.reward     = data['reward']
        self.color      = data['color']
        self.radius     = data['radius']

        # ── Status bendera ────────────────────────────────────────
        self.alive        = True
        self.reached_exit = False

        # ── Jalur (list (kolom, baris) dari A*) ──────────────────
        self.path         = path            # jalur penuh
        self.waypoint_idx = 1               # indeks yang sedang kita tuju

        # ── Posisi piksel — mulai di tengah sel pertama ─────
        sc, sr      = path[0]
        self.x: float = sc * CELL_SIZE + CELL_SIZE / 2
        self.y: float = sr * CELL_SIZE + CELL_SIZE / 2

    # ----------------------------------------------------------
    def update_path(self, new_path: list):
        """
        Dipanggil saat menara ditempatkan dan A* mengembalikan rute baru.
        Mencari titik jalan terdekat di new_path ke sel grid musuh
        saat ini dan melanjutkannya dari sana.
        """
        if new_path is None:
            return  # tidak seharusnya terjadi (penempatan divalidasi terlebih dahulu)

        # Sel grid terdekat ke posisi piksel saat ini
        cur_col = int(self.x // CELL_SIZE)
        cur_row = int(self.y // CELL_SIZE)

        # Temukan titik gabung: titik jalan paling awal di new_path di pada atau di depan kita
        best_idx  = 1
        best_dist = float('inf')
        for i, (c, r) in enumerate(new_path):
            d = abs(c - cur_col) + abs(r - cur_row)
            if d < best_dist:
                best_dist = d
                best_idx  = i

        self.path         = new_path
        self.waypoint_idx = max(best_idx, 1)

    # ----------------------------------------------------------
    def take_damage(self, amount: float):
        if not self.alive:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp    = 0
            self.alive = False

    # ----------------------------------------------------------
    def update(self):
        if not self.alive or self.reached_exit:
            return

        # Semua titik jalan dikunjungi → musuh mencapai tujuan akhir
        if self.waypoint_idx >= len(self.path):
            self.reached_exit = True
            return

        # ── Bergerak menuju titik jalan saat ini ───────────────────────
        tc, tr   = self.path[self.waypoint_idx]
        target_x = tc * CELL_SIZE + CELL_SIZE / 2
        target_y = tr * CELL_SIZE + CELL_SIZE / 2

        dx    = target_x - self.x
        dy    = target_y - self.y
        dist  = math.hypot(dx, dy)

        if dist <= self.speed:
            # Pindah ke pusat titik jalan dan maju
            self.x = target_x
            self.y = target_y
            self.waypoint_idx += 1
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    # ----------------------------------------------------------
    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return

        cx, cy = int(self.x), int(self.y)
        r      = self.radius

        # ── Bayangan ─────────────────────────────────────────────
        shadow_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 80),
                           (r + 2, r + 4), r)
        surface.blit(shadow_surf, (cx - r - 2, cy - r - 2))

        # ── Tubuh ───────────────────────────────────────────────
        pygame.draw.circle(surface, self.color, (cx, cy), r)
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), r, 1)

        # ── Bar Darah ─────────────────────────────────────────
        bar_w  = r * 2 + 6
        bar_h  = 4
        bar_x  = cx - bar_w // 2
        bar_y  = cy - r - 9
        ratio  = max(self.hp / self.max_hp, 0)

        # Latar belakang
        pygame.draw.rect(surface, (60, 20, 20),
                         (bar_x, bar_y, bar_w, bar_h))
        # Isi — hijau → merah saat HP turun
        hp_color = (int(255 * (1 - ratio)), int(220 * ratio), 30)
        pygame.draw.rect(surface, hp_color,
                         (bar_x, bar_y, int(bar_w * ratio), bar_h))
        # Batas
        pygame.draw.rect(surface, (120, 120, 120),
                         (bar_x, bar_y, bar_w, bar_h), 1)
