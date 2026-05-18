# ============================================================
#  renderer.py  —  Semua kode penggambaran Pygame
#
#  Akses baca-saja secara ketat ke GameState. Tidak ada logika di sini.
# ============================================================

import pygame
import math
from config import (
    CELL_SIZE, COLS, ROWS, SIDEBAR_W, SCREEN_W, SCREEN_H,
    TOWER_TYPES, TOWER_ORDER, WAVES, WAVE_BREAK,
    C_BG, C_GRID, C_GRID_LINE, C_PATH, C_ENTRY, C_EXIT,
    C_SIDEBAR, C_SIDEBAR_HDR, C_TEXT, C_TEXT_DIM,
    C_GOLD, C_LIVES, C_WAVE, C_BTN, C_BTN_SEL, C_BTN_HOV,
    C_MSG_OK, C_MSG_ERR, C_OBSTACLE, C_OBSTACLE_BD,
)

GAME_W = COLS * CELL_SIZE   # lebar piksel area grid


# ── Inisialisasi font (panggil sekali setelah pygame.init()) ──────
_fonts: dict = {}

def init_fonts():
    _fonts['title'] = pygame.font.SysFont('consolas', 16, bold=True)
    _fonts['ui']    = pygame.font.SysFont('consolas', 14)
    _fonts['small'] = pygame.font.SysFont('consolas', 12)
    _fonts['big']   = pygame.font.SysFont('consolas', 28, bold=True)
    _fonts['huge']  = pygame.font.SysFont('consolas', 42, bold=True)


def _txt(surface, text, font_key, color, x, y, center=False):
    surf = _fonts[font_key].render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(surf, rect)
    return rect


# ═══════════════════════════════════════════════════════════════
#  GRID
# ═══════════════════════════════════════════════════════════════
def draw_grid(surface: pygame.Surface, gs, show_path: bool = True):
    """Gambar sel latar belakang, sorotan jalur, penanda masuk/keluar."""

    path_set = set(gs.current_path) if (gs.current_path and show_path) else set()

    for row in range(ROWS):
        for col in range(COLS):
            rx = col * CELL_SIZE
            ry = row * CELL_SIZE
            cell = pygame.Rect(rx, ry, CELL_SIZE, CELL_SIZE)

            if (col, row) in path_set:
                color = C_PATH
            else:
                color = C_GRID
            pygame.draw.rect(surface, color, cell)
            pygame.draw.rect(surface, C_GRID_LINE, cell, 1)

    # ── Penghalang terrain ────────────────────────────────────────
    for (oc, or_) in gs.obstacles:
        rx = oc * CELL_SIZE
        ry = or_ * CELL_SIZE
        pygame.draw.rect(surface, C_OBSTACLE, (rx, ry, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, C_OBSTACLE_BD, (rx, ry, CELL_SIZE, CELL_SIZE), 1)
        m = 9
        pygame.draw.line(surface, C_OBSTACLE_BD,
                         (rx + m, ry + m), (rx + CELL_SIZE - m, ry + CELL_SIZE - m), 2)
        pygame.draw.line(surface, C_OBSTACLE_BD,
                         (rx + CELL_SIZE - m, ry + m), (rx + m, ry + CELL_SIZE - m), 2)

    # Portal masuk
    ec, er = gs.entry
    pygame.draw.rect(surface, C_ENTRY,
                     (ec * CELL_SIZE, er * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    _txt(surface, '▶', 'small', (10, 10, 10),
         ec * CELL_SIZE + 12, er * CELL_SIZE + 12)

    # Portal keluar
    xc, xr = gs.exit
    pygame.draw.rect(surface, C_EXIT,
                     (xc * CELL_SIZE, xr * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    _txt(surface, '✕', 'small', (10, 10, 10),
         xc * CELL_SIZE + 12, xr * CELL_SIZE + 12)


# ═══════════════════════════════════════════════════════════════
#  PRATINJAU ARAHAN (HOVER)
# ═══════════════════════════════════════════════════════════════
def draw_hover(surface: pygame.Surface, gs):
    if gs.hover_cell is None:
        return
    col, row = gs.hover_cell
    rx = col * CELL_SIZE
    ry = row * CELL_SIZE

    # Dalam mode pindah gunakan warna oranye; dalam mode tempat gunakan hijau/merah
    if gs.moving_tower is not None:
        valid_color   = (255, 165,  40)   # oranye = relokasi
        invalid_color = (220,  60,  60)
        fill_alpha    = 90
    else:
        valid_color   = ( 80, 220, 120)   # hijau = tempatkan
        invalid_color = (220,  60,  60)
        fill_alpha    = 80

    alpha_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    if gs.hover_valid:
        alpha_surf.fill((*valid_color, fill_alpha))
    else:
        alpha_surf.fill((*invalid_color, fill_alpha))
    surface.blit(alpha_surf, (rx, ry))

    border_color = valid_color if gs.hover_valid else invalid_color
    pygame.draw.rect(surface, border_color,
                     (rx, ry, CELL_SIZE, CELL_SIZE), 2)

    # Pratinjau cincin jangkauan
    if gs.hover_valid:
        # Gunakan statistik menara yang dipindahkan dalam mode pindah, tipe yang dipilih sebaliknya
        if gs.moving_tower is not None:
            tower_color = gs.moving_tower.color
            r_px        = int(gs.moving_tower.range_px)
        else:
            data        = TOWER_TYPES[gs.selected_type]
            tower_color = data['color']
            r_px        = int(data['range'] * CELL_SIZE)

        cx = rx + CELL_SIZE // 2
        cy = ry + CELL_SIZE // 2
        rs = pygame.Surface((r_px * 2, r_px * 2), pygame.SRCALPHA)
        pygame.draw.circle(rs, (*tower_color, 20), (r_px, r_px), r_px)
        pygame.draw.circle(rs, (*tower_color, 60), (r_px, r_px), r_px, 1)
        surface.blit(rs, (cx - r_px, cy - r_px))


# ═══════════════════════════════════════════════════════════════
#  MENARA
# ═══════════════════════════════════════════════════════════════
def draw_towers(surface: pygame.Surface, gs):
    hover = gs.hover_cell

    # Gambar garis luar hantu pudar di sel asli saat memindahkan
    if gs.moving_tower is not None and gs.moving_from is not None:
        gc, gr = gs.moving_from
        gx = gc * CELL_SIZE + 4
        gy = gr * CELL_SIZE + 4
        gh = CELL_SIZE - 8
        ghost = pygame.Surface((gh, gh), pygame.SRCALPHA)
        ghost.fill((*gs.moving_tower.color, 40))
        pygame.draw.rect(ghost, (*gs.moving_tower.color, 120),
                         (0, 0, gh, gh), 2, border_radius=4)
        surface.blit(ghost, (gx, gy))

    for tower in gs.towers:
        show = (hover is not None and
                abs(tower.col - hover[0]) + abs(tower.row - hover[1]) == 0)
        tower.draw(surface, show_range=show)


# ═══════════════════════════════════════════════════════════════
#  MUSUH
# ═══════════════════════════════════════════════════════════════
def draw_enemies(surface: pygame.Surface, gs):
    for enemy in gs.enemies:
        enemy.draw(surface)


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
_BTN_H  = 68
_BTN_W  = SIDEBAR_W - 20
_BTN_X  = GAME_W + 10

def get_tower_button_rects() -> list[pygame.Rect]:
    rects = []
    for i in range(len(TOWER_ORDER)):
        y = 190 + i * (_BTN_H + 6)
        rects.append(pygame.Rect(_BTN_X, y, _BTN_W, _BTN_H))
    return rects


def draw_sidebar(surface: pygame.Surface, gs):
    # Latar belakang
    pygame.draw.rect(surface, C_SIDEBAR,
                     (GAME_W, 0, SIDEBAR_W, SCREEN_H))
    pygame.draw.line(surface, C_GRID_LINE,
                     (GAME_W, 0), (GAME_W, SCREEN_H), 2)

    x = GAME_W

    # ── Header ─────────────────────────────────────────────────
    pygame.draw.rect(surface, C_SIDEBAR_HDR, (x, 0, SIDEBAR_W, 42))
    _txt(surface, 'TOWER DEFENSE', 'title', C_WAVE,
         x + SIDEBAR_W // 2, 14, center=True)
    _txt(surface, 'with A* Algorithm', 'small', C_TEXT_DIM,
         x + SIDEBAR_W // 2, 28, center=True)

    # ── Statistik ──────────────────────────────────────────────────
    sy = 52
    stats = [
        ('GOLD',  f'{gs.gold}g',                    C_GOLD),
        ('LIVES', str(gs.lives),                     C_LIVES),
        ('WAVE',  f'{gs.wave_number}/{len(WAVES)}',  C_WAVE),
        ('SCORE', str(gs.score),                     C_TEXT),
    ]
    for i, (label, value, color) in enumerate(stats):
        ry = sy + i * 22
        pygame.draw.rect(surface, color, (x + 12, ry + 3, 10, 10))
        _txt(surface, label, 'small', color, x + 28, ry + 1)
        _txt(surface, value, 'ui',    color, x + 110, ry)

    # ── Pembatas ────────────────────────────────────────────────
    pygame.draw.line(surface, C_GRID_LINE,
                     (x + 10, 135), (x + SIDEBAR_W - 10, 135), 1)

    # ── Label menara ────────────────────────────────────────────
    _txt(surface, 'TOWERS  [1-4]', 'small', C_TEXT_DIM,
         x + SIDEBAR_W // 2, 148, center=True)

    # ── Tombol menara ──────────────────────────────────────────
    rects = get_tower_button_rects()
    for i, ttype in enumerate(TOWER_ORDER):
        data = TOWER_TYPES[ttype]
        rect = rects[i]
        selected = (ttype == gs.selected_type)
        bg_color = C_BTN_SEL if selected else C_BTN
        pygame.draw.rect(surface, bg_color, rect, border_radius=6)
        if selected:
            pygame.draw.rect(surface, data['color'], rect, 2, border_radius=6)
        else:
            pygame.draw.rect(surface, C_GRID_LINE, rect, 1, border_radius=6)

        # Titik warna menara
        dot_x = rect.x + 18
        dot_y = rect.y + rect.height // 2
        pygame.draw.circle(surface, data['color'], (dot_x, dot_y), 8)
        pygame.draw.circle(surface, (255, 255, 255), (dot_x, dot_y), 8, 1)

        # Nama + kunci
        _txt(surface, f"[{data['key']}] {data['name']}",
             'ui', C_TEXT, rect.x + 34, rect.y + 8)
        _txt(surface, data['desc'],
             'small', C_TEXT_DIM, rect.x + 34, rect.y + 26)
        _txt(surface, f"Cost:{data['cost']}g  Rng:{data['range']}c  Rate:{data['fire_rate']}/s",
             'small', C_TEXT_DIM, rect.x + 34, rect.y + 44)

    # ── Hitung mundur gelombang / status ────────────────────────────────
    pygame.draw.line(surface, C_GRID_LINE,
                     (x + 10, 480), (x + SIDEBAR_W - 10, 480), 1)

    if not gs.wave_active and not gs.victory and not gs.game_over:
        remaining = max(0, gs.wave_countdown)
        if gs.wave_number < len(WAVES):
            msg = f"Next wave in {remaining:.1f}s"
        else:
            msg = "Final wave done!"
        _txt(surface, msg, 'small', C_WAVE,
             x + SIDEBAR_W // 2, 492, center=True)
    elif gs.wave_active:
        _txt(surface, f'Wave {gs.wave_number} active', 'small', C_MSG_ERR,
             x + SIDEBAR_W // 2, 492, center=True)

    # ── Spanduk mode pindah ───────────────────────────────────────
    if gs.moving_tower is not None:
        banner = pygame.Rect(x + 6, 505, SIDEBAR_W - 12, 28)
        pygame.draw.rect(surface, (120, 70, 10), banner, border_radius=5)
        pygame.draw.rect(surface, (255, 165, 40), banner, 1, border_radius=5)
        _txt(surface, f'MOVING: {gs.moving_tower.name}',
             'small', (255, 200, 80), x + SIDEBAR_W // 2, 512, center=True)
        _txt(surface, 'L-click=drop  ESC=cancel',
             'small', (200, 160, 60), x + SIDEBAR_W // 2, 525, center=True)
    else:
        # ── Pemberitahuan pesan (disembunyikan saat pause) ───────────
        if gs.message_timer > 0 and not gs.paused:
            alpha    = min(255, int(gs.message_timer * 120))
            msg_surf = _fonts['small'].render(gs.message, True, gs.message_color)
            msg_surf.set_alpha(alpha)
            mr = msg_surf.get_rect(centerx=x + SIDEBAR_W // 2, y=512)
            surface.blit(msg_surf, mr)

    # ── Indikator jeda ────────────────────────────────────────
    if gs.paused:
        pause_banner = pygame.Rect(x + 6, 536, SIDEBAR_W - 12, 20)
        pygame.draw.rect(surface, (40, 40, 80), pause_banner, border_radius=4)
        pygame.draw.rect(surface, (100, 100, 220), pause_banner, 1, border_radius=4)
        _txt(surface, 'PAUSED  —  press P to resume',
             'small', (160, 160, 255), x + SIDEBAR_W // 2, 546, center=True)

    # ── Legenda kontrol ────────────────────────────────────────
    legend_y = 558
    _txt(surface, 'L-click = Place  R-click = Move', 'small', C_TEXT_DIM, x + 10, legend_y)
    _txt(surface, '1-4 = Tower  H = Path  P = Pause', 'small', C_TEXT_DIM, x + 10, legend_y + 14)
    _txt(surface, 'R = Restart  ESC = Cancel/Quit',   'small', C_TEXT_DIM, x + 10, legend_y + 28)


# ═══════════════════════════════════════════════════════════════
#  TAMPILAN JEDA
# ═══════════════════════════════════════════════════════════════
def draw_pause_overlay(surface: pygame.Surface):
    """Penggelapan halus + panel PAUSED di tengah area grid."""
    dark = pygame.Surface((GAME_W, SCREEN_H), pygame.SRCALPHA)
    dark.fill((0, 0, 20, 140))
    surface.blit(dark, (0, 0))

    cx, cy = GAME_W // 2, SCREEN_H // 2

    panel_w, panel_h = 300, 130
    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((8, 12, 42, 238))
    surface.blit(panel, (cx - panel_w // 2, cy - panel_h // 2))
    pygame.draw.rect(surface, (75, 90, 215),
                     (cx - panel_w // 2, cy - panel_h // 2, panel_w, panel_h),
                     2, border_radius=12)

    # Ikon pause — dua batang di-tengah tepat di atas teks PAUSED
    bar_col = (155, 170, 255)
    pygame.draw.rect(surface, bar_col, (cx - 18, cy - 52, 14, 28), border_radius=3)
    pygame.draw.rect(surface, bar_col, (cx +  4, cy - 52, 14, 28), border_radius=3)

    _txt(surface, 'PAUSED',              'big', (155, 170, 255), cx, cy,  center=True)
    _txt(surface, 'Press  P  to resume', 'ui',  (105, 125, 205), cx, cy + 30, center=True)


# ═══════════════════════════════════════════════════════════════
#  TAMPILAN LAYAR
# ═══════════════════════════════════════════════════════════════
def draw_overlay(surface: pygame.Surface, gs):
    """Gambar tampilan game-over atau kemenangan di atas area permainan."""
    if not gs.game_over and not gs.victory:
        return

    # Gelapkan area permainan
    dark = pygame.Surface((GAME_W, SCREEN_H), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 160))
    surface.blit(dark, (0, 0))

    cx, cy = GAME_W // 2, SCREEN_H // 2

    if gs.victory:
        title = "VICTORY!"
        color = (100, 255, 140)
        sub   = f"All {len(WAVES)} waves defeated!"
    else:
        title = "GAME OVER"
        color = (255, 80, 60)
        sub   = "The enemies broke through!"

    _txt(surface, title, 'huge', color, cx, cy - 50, center=True)
    _txt(surface, sub,   'big',  C_TEXT, cx, cy + 10, center=True)
    _txt(surface, f'Score: {gs.score}', 'big', C_GOLD, cx, cy + 55, center=True)
    _txt(surface, 'Press  R  to restart', 'ui', C_TEXT_DIM, cx, cy + 100, center=True)


# ═══════════════════════════════════════════════════════════════
#  PANGGILAN GAMBAR UTAMA
# ═══════════════════════════════════════════════════════════════
def draw_all(surface: pygame.Surface, gs, show_path: bool = True):
    surface.fill(C_BG)
    draw_grid(surface, gs, show_path)
    draw_hover(surface, gs)
    draw_towers(surface, gs)
    draw_enemies(surface, gs)
    draw_sidebar(surface, gs)
    draw_overlay(surface, gs)
    # Tampilan jeda digambar terakhir sehingga berada di atas segalanya
    if gs.paused and not gs.game_over and not gs.victory:
        draw_pause_overlay(surface)
