# ============================================================
#  config.py  —  Tower Defense: Musuh Pintar
#  Semua konstanta permainan ada di sini. Edit nilai untuk menyesuaikan gameplay.
# ============================================================

# ── Layar & Grid ────────────────────────────────────────────
CELL_SIZE   = 40            # piksel per sel grid
COLS        = 20            # kolom grid
ROWS        = 15            # baris grid
SIDEBAR_W   = 350           # lebar sidebar dalam piksel
SCREEN_W    = COLS * CELL_SIZE + SIDEBAR_W   # 1020
SCREEN_H    = ROWS * CELL_SIZE               # 600
FPS         = 60
TITLE       = "Tower Defense"

# ── Titik akhir peta ────────────────────────────────────────────
ENTRY = (0, 7)              # tempat muncul musuh (tepi kiri, baris tengah)
EXIT  = (COLS - 1, 7)       # tujuan musuh (tepi kanan)

# ── Sumber daya awal ───────────────────────────────────────
GOLD_START  = 500
LIVES_START = 20

# ── Palet Warna (tema taktis-gelap) ─────────────────────
C_BG          = (10,  15,  25)
C_GRID        = (18,  26,  40)
C_GRID_LINE   = (28,  40,  58)
C_PATH        = (30,  46,  68)
C_ENTRY       = (50, 200,  90)
C_EXIT        = (200,  70,  50)
C_SIDEBAR     = (14,  20,  34)
C_SIDEBAR_HDR = (20,  30,  50)
C_TEXT        = (190, 205, 225)
C_TEXT_DIM    = (100, 120, 150)
C_GOLD        = (255, 200,  50)
C_LIVES       = (220,  80,  60)
C_WAVE        = (100, 180, 255)
C_BTN         = (28,  44,  70)
C_BTN_SEL     = (45,  95, 158)
C_BTN_HOV     = (38,  60,  95)
C_MSG_OK      = ( 80, 220, 120)
C_MSG_ERR     = (220,  80,  60)
C_OBSTACLE    = ( 42,  28,  18)   # warna sel penghalang terrain
C_OBSTACLE_BD = ( 75,  52,  30)   # border penghalang terrain

# ── Definisi Menara ─────────────────────────────────────────
#   range      → radius deteksi dalam sel
#   fire_rate  → tembakan per detik
#   proj_speed → kecepatan peluru dalam px/frame
TOWER_TYPES = {
    'basic': {
        'name':       'Basic',
        'desc':       'Balanced all-rounder',
        'cost':        50,
        'damage':      15,
        'range':       3.5,
        'fire_rate':   1.0,
        'proj_speed':  5.0,
        'color':      (70, 130, 200),
        'proj_color': (140, 195, 255),
        'key':         '1',
    },
    'sniper': {
        'name':       'Sniper',
        'desc':       'Long range, high damage',
        'cost':        100,
        'damage':      60,
        'range':       7.0,
        'fire_rate':   0.4,
        'proj_speed': 12.0,
        'color':      (200, 165,  50),
        'proj_color': (255, 220, 100),
        'key':         '2',
    },
    'rapid': {
        'name':       'Rapid',
        'desc':       'Fast fire, low damage',
        'cost':        75,
        'damage':       8,
        'range':       2.5,
        'fire_rate':   4.0,
        'proj_speed':  7.0,
        'color':      (70, 190, 120),
        'proj_color': (130, 255, 170),
        'key':         '3',
    },
    'bomb': {
        'name':       'Bomb',
        'desc':       'Slow but devastating',
        'cost':        125,
        'damage':      100,
        'range':       3.0,
        'fire_rate':   0.25,
        'proj_speed':  3.0,
        'color':      (200,  75,  75),
        'proj_color': (255, 140,  80),
        'key':         '4',
    },
}
TOWER_ORDER = ['basic', 'sniper', 'rapid', 'bomb']   # urutan tampilan

# ── Definisi Musuh ─────────────────────────────────────────
#   speed  → pergerakan dalam px/frame
#   reward → emas yang diberikan saat terbunuh
ENEMY_TYPES = {
    'basic': {
        'name':   'Grunt',
        'hp':      100,
        'speed':   1.2,
        'reward':  10,
        'color':  (220,  85,  60),
        'radius':  10,
    },
    'fast': {
        'name':   'Scout',
        'hp':       60,
        'speed':   2.8,
        'reward':  15,
        'color':  (225, 205,  55),
        'radius':   8,
    },
    'tank': {
        'name':   'Tank',
        'hp':      450,
        'speed':   0.7,
        'reward':  40,
        'color':  (160,  65, 220),
        'radius':  15,
    },
    'swarm': {
        'name':   'Swarm',
        'hp':       40,
        'speed':   2.2,
        'reward':   8,
        'color':  (60,  210, 200),
        'radius':   7,
    },
}

# ── Jadwal Gelombang ─────────────────────────────────────────────
#   Setiap gelombang = list (tipe_musuh, jumlah, interval_muncul_detik)
#   Beberapa kelompok dalam satu gelombang muncul secara berurutan.
WAVES = [
    # 1
    [('basic', 8, 1.5)],
    # 2
    [('basic', 10, 1.2), ('fast', 5, 0.9)],
    # 3
    [('basic', 8, 1.0), ('fast', 6, 0.8), ('tank', 2, 4.0)],
    # 4
    [('fast', 12, 0.7), ('tank', 3, 3.0)],
    # 5
    [('basic', 15, 0.8), ('swarm', 12, 0.5), ('tank', 3, 2.5)],
    # 6
    [('swarm', 20, 0.4), ('fast', 12, 0.6), ('tank', 5, 2.0)],
    # 7
    [('tank', 8, 1.5), ('swarm', 18, 0.35), ('fast', 15, 0.5)],
    # 8
    [('basic', 20, 0.5), ('swarm', 25, 0.3), ('tank', 10, 1.5), ('fast', 18, 0.4)],
]

WAVE_BREAK = 5.0    # detik waktu persiapan antar gelombang
