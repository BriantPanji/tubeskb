# ============================================================
#  game_state.py  —  Logika Inti Permainan
#
#  Tanggung Jawab
#  ─────────────────
#  • Memelihara grid (sel mana yang diblokir oleh menara)
#  • Memvalidasi penempatan menara melalui pemeriksaan jalur A*
#  • Menyiarkan jalur A* baru ke semua musuh yang hidup
#  • Mengelola antrean kemunculan gelombang
#  • Melacak emas, nyawa, skor, nomor gelombang
#  • Menjeda / melanjutkan permainan (Tombol P)
#  • Memindahkan (merelokasi) menara yang ditempatkan (klik kanan untuk mengambil,
#    klik kiri untuk menjatuhkan, ESC untuk membatalkan)
# ============================================================

import random

from config import (
    COLS, ROWS, ENTRY, EXIT, GOLD_START, LIVES_START,
    TOWER_TYPES, WAVES, WAVE_BREAK, CELL_SIZE,
)
from astar      import astar
from enemy      import Enemy
from tower      import Tower


class GameState:

    def __init__(self):
        self.reset()

    # ──────────────────────────────────────────────────────────
    def reset(self):
        # ── Sumber daya ──────────────────────────────────────────
        self.gold        = GOLD_START
        self.lives       = LIVES_START
        self.score       = 0
        self.wave_number = 0          # gelombang yang telah diselesaikan sejauh ini

        # ── Status bendera ──────────────────────────────────────────────
        self.game_over   = False
        self.victory     = False

        # ── Grid ─────────────────────────────────────────────────────────
        self.blocked: set   = set()
        self.obstacles: set = set()   # penghalang terrain awal (tidak bisa dibangun)
        self.current_path: list = []  # diisi oleh _place_random_obstacles

        # ── Daftar entitas ───────────────────────────────────────
        self.towers:  list[Tower] = []
        self.enemies: list[Enemy] = []

        # ── Gelombang / kemunculan ────────────────────────────────────
        self.wave_active    = False
        self.wave_queue:    list = []         # kelompok yang tersisa untuk dimunculkan
        self.active_group        = None       # [tipe, tersisa, interval]
        self.spawn_timer         = 0.0
        self.wave_countdown      = 3.0        # detik sebelum gelombang 1 mulai otomatis

        # ── UI / notifikasi ──────────────────────────────────
        self.selected_type   = 'basic'        # kursor tipe menara
        self.hover_cell      = None           # (kolom, baris) di bawah mouse
        self.hover_valid     = False          # bisakah kita menempatkannya di sini?
        self.message         = ""
        self.message_timer   = 0.0
        self.message_color   = (80, 220, 120)

        # ── Jeda ──────────────────────────────────────────────
        self.paused          = False

        # ── Mode pindah menara ────────────────────────────────────
        # Ketika tidak None, pemain telah mengambil menara dan
        # sedang memilih sel baru untuknya. Menara dihapus
        # dari self.towers dan self.blocked saat dalam perjalanan.
        self.moving_tower    = None    # Objek menara sedang dipindahkan
        self.moving_from     = None    # sel asli (kolom, baris)

        # ── Tempatkan penghalang acak & hitung jalur awal ────────────────
        self._place_random_obstacles()

    # ──────────────────────────────────────────────────────────
    #  Penghalang terrain acak
    # ──────────────────────────────────────────────────────────
    def _place_random_obstacles(self, count: int = 18):
        """
        Tempatkan penghalang terrain acak di awal permainan sehingga
        jalur musuh tidak selalu lurus dari kiri ke kanan.
        Setiap sel dicek dulu dengan A* agar path tetap valid.
        """
        ec, er = ENTRY
        xc, xr = EXIT

        # Lindungi area di sekitar pintu masuk dan keluar
        protected = {ENTRY, EXIT}
        for dc in range(1, 4):
            protected.add((ec + dc, er))
            protected.add((xc - dc, xr))

        placed   = 0
        attempts = 0
        while placed < count and attempts < 600:
            attempts += 1
            # Sedikit bias ke baris tengah agar jalur terpaksa naik/turun
            col = random.randint(1, COLS - 2)
            if random.random() < 0.55:
                row = random.randint(max(0, er - 5), min(ROWS - 1, er + 5))
            else:
                row = random.randint(1, ROWS - 2)
            cell = (col, row)
            if cell in protected or cell in self.blocked:
                continue
            test_blocked = self.blocked | {cell}
            if astar(test_blocked, ENTRY, EXIT, COLS, ROWS) is not None:
                self.blocked.add(cell)
                self.obstacles.add(cell)
                placed += 1

        self.current_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)

    # ──────────────────────────────────────────────────────────
    #  Fungsi bantuan publik
    # ──────────────────────────────────────────────────────────
    def notify(self, text: str, ok: bool = True):
        self.message       = text
        self.message_timer = 2.5
        self.message_color = (80, 220, 120) if ok else (220, 80, 60)

    def set_hover(self, col: int, row: int):
        """Dipanggil setiap frame dengan sel di bawah kursor mouse."""
        cell = (col, row)
        self.hover_cell  = cell
        if self.moving_tower is not None:
            # Dalam mode pindah: valid jika kita bisa menjatuhkan menara di sini
            self.hover_valid = self._can_drop(col, row)
        else:
            self.hover_valid = self._can_place(col, row)

    def clear_hover(self):
        self.hover_cell  = None
        self.hover_valid = False

    # ──────────────────────────────────────────────────────────
    #  Penempatan Menara
    # ──────────────────────────────────────────────────────────
    def _can_place(self, col: int, row: int) -> bool:
        """
        Menara dapat ditempatkan di (kolom, baris) jika dan hanya jika:
          1. Sel berada di dalam grid.
          2. Sel belum diblokir.
          3. Memblokir sel masih menyisakan jalur A* yang valid.

        Kondisi 3 adalah pemeriksaan AI yang kritis — ini mencegah
        pemain agar tidak sepenuhnya mengelilingi musuh tanpa jalan keluar.
        """
        if not (0 <= col < COLS and 0 <= row < ROWS):
            return False
        if (col, row) in self.blocked:
            return False
        # Blokir sementara dan periksa jalur
        test_blocked = self.blocked | {(col, row)}
        return astar(test_blocked, ENTRY, EXIT, COLS, ROWS) is not None

    def try_place_tower(self, col: int, row: int) -> bool:
        """Mencoba untuk menempatkan menara yang dipilih; mengembalikan True jika berhasil."""
        data = TOWER_TYPES[self.selected_type]
        cost = data['cost']

        if self.gold < cost:
            self.notify(f"Need {cost}g — only have {self.gold}g!", ok=False)
            return False

        if not self._can_place(col, row):
            self.notify("Can't place — would block path!", ok=False)
            return False

        # ── Konfirmasi penempatan ───────────────────────────────────
        self.blocked.add((col, row))
        new_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)
        self.current_path = new_path

        tower = Tower(col, row, self.selected_type)
        self.towers.append(tower)
        self.gold -= cost

        # ── Siarkan jalur baru ke semua musuh yang hidup ───────────
        for e in self.enemies:
            if e.alive and not e.reached_exit:
                e.update_path(new_path)

        self.notify(f"{data['name']} placed  (−{cost}g)")
        return True

    # ──────────────────────────────────────────────────────────
    #  Jeda
    # ──────────────────────────────────────────────────────────
    def toggle_pause(self):
        """Balik bendera jeda. Tidak melakukan apa pun jika permainan telah berakhir."""
        if self.game_over or self.victory:
            return
        self.paused = not self.paused
        if not self.paused:
            self.notify("Resumed!", ok=True)

    # ──────────────────────────────────────────────────────────
    #  Mode pindah menara
    # ──────────────────────────────────────────────────────────
    def pick_up_tower(self, col: int, row: int) -> bool:
        """
        Klik kanan pada sel yang berisi menara untuk mengambilnya.

        Menghapus menara dari self.towers dan membuka blokir selnya
        sehingga A* dapat merutekan melaluinya lagi — musuh segera merutekan ulang
        di sekitar celah yang sekarang terbuka.

        Mengembalikan True jika menara diambil.
        """
        if self.moving_tower is not None:
            # Sudah memegang satu — batalkan dulu
            self.cancel_move()
            return False

        # Temukan menara di (kolom, baris)
        target = None
        for t in self.towers:
            if t.col == col and t.row == row:
                target = t
                break

        if target is None:
            return False

        # Angkat menara dari grid
        self.towers.remove(target)
        self.blocked.discard((col, row))

        # Hitung ulang jalur dengan sel yang sekarang bebas
        self.current_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)
        for e in self.enemies:
            if e.alive and not e.reached_exit:
                e.update_path(self.current_path)

        self.moving_tower = target
        self.moving_from  = (col, row)
        self.notify(f"Picked up {target.name} — click to relocate, ESC to cancel")
        return True

    def _can_drop(self, col: int, row: int) -> bool:
        """
        Periksa apakah menara yang ditahan dapat dijatuhkan di (kolom, baris).
        Aturan yang sama dengan _can_place tetapi menggunakan grid yang sudah terbuka.
        """
        if not (0 <= col < COLS and 0 <= row < ROWS):
            return False
        if (col, row) in self.blocked:
            return False
        # Sel ENTRY dan EXIT harus tetap dapat dilewati
        if (col, row) == ENTRY or (col, row) == EXIT:
            return False
        test_blocked = self.blocked | {(col, row)}
        return astar(test_blocked, ENTRY, EXIT, COLS, ROWS) is not None

    def drop_tower(self, col: int, row: int) -> bool:
        """
        Tempatkan menara yang ditahan di (kolom, baris).

        Memblokir ulang sel, menjalankan ulang A*, dan menyiarkan rute baru
        ke semua musuh yang hidup.

        Mengembalikan True jika berhasil.
        """
        if self.moving_tower is None:
            return False

        if not self._can_drop(col, row):
            self.notify("Can't place there — path blocked!", ok=False)
            return False

        tower         = self.moving_tower
        tower.col     = col
        tower.row     = row
        tower.x       = col * CELL_SIZE + CELL_SIZE // 2
        tower.y       = row * CELL_SIZE + CELL_SIZE // 2
        # Atur ulang penargetan agar menara menarget ulang dengan bersih
        tower.target  = None

        self.blocked.add((col, row))
        self.current_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)
        for e in self.enemies:
            if e.alive and not e.reached_exit:
                e.update_path(self.current_path)

        self.towers.append(tower)
        self.moving_tower = None
        self.moving_from  = None

        moved_msg = ("Same spot." if (col, row) == self.moving_from
                     else f"Moved to ({col}, {row}).")
        self.notify(f"{tower.name} placed.  {moved_msg}")
        return True

    def cancel_move(self):
        """
        Kembalikan menara yang ditahan ke sel aslinya (ESC saat memindahkan).
        """
        if self.moving_tower is None:
            return

        col, row      = self.moving_from
        tower         = self.moving_tower
        tower.col     = col
        tower.row     = row
        tower.x       = col * CELL_SIZE + CELL_SIZE // 2
        tower.y       = row * CELL_SIZE + CELL_SIZE // 2
        tower.target  = None

        self.blocked.add((col, row))
        self.current_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)
        for e in self.enemies:
            if e.alive and not e.reached_exit:
                e.update_path(self.current_path)

        self.towers.append(tower)
        self.moving_tower = None
        self.moving_from  = None
        self.notify("Move cancelled — tower returned.", ok=True)

    # ──────────────────────────────────────────────────────────
    #  Manajemen gelombang
    # ──────────────────────────────────────────────────────────
    def start_next_wave(self):
        if self.wave_number >= len(WAVES):
            return  # semua gelombang selesai
        wave_data            = WAVES[self.wave_number]
        self.wave_queue      = [list(g) for g in wave_data]
        self.active_group    = None
        self.spawn_timer     = 0.0
        self.wave_active     = True
        self.wave_number    += 1
        self.notify(f"⚠  Wave {self.wave_number} incoming!")

    def _update_spawning(self, dt: float):
        self.spawn_timer -= dt

        # Muat grup berikutnya jika tidak ada yang aktif
        if self.active_group is None:
            if not self.wave_queue:
                return   # semua kelompok diberangkatkan
            self.active_group = self.wave_queue.pop(0)
            self.spawn_timer  = 0.0   # munculkan segera

        if self.spawn_timer <= 0:
            etype, count, interval = self.active_group
            if count > 0:
                # Munculkan satu musuh mengikuti jalur A* saat ini
                enemy = Enemy(etype, list(self.current_path))
                self.enemies.append(enemy)
                self.active_group[1] -= 1
                self.spawn_timer = interval
            if self.active_group[1] <= 0:
                self.active_group = None

    # ──────────────────────────────────────────────────────────
    #  Pembaruan utama (dipanggil sekali per frame)
    # ──────────────────────────────────────────────────────────
    def update(self, dt: float):
        if self.game_over or self.victory:
            return
        if self.paused:
            return   # bekukan semua logika game; rendering terus berlanjut

        # ── Timer pesan ──────────────────────────────────────
        self.message_timer = max(0.0, self.message_timer - dt)

        # ── Jeda antar gelombang ────────────────────────────────────────
        if not self.wave_active:
            self.wave_countdown -= dt
            if self.wave_countdown <= 0:
                self.wave_countdown = WAVE_BREAK
                self.start_next_wave()
        else:
            self._update_spawning(dt)

        # ── Musuh ────────────────────────────────────────────
        for e in self.enemies:
            e.update()
            if e.reached_exit:
                self.lives -= 1
                e.alive = False     # tandai untuk dihapus
                if self.lives <= 0:
                    self.lives     = 0
                    self.game_over = True

        # Kumpulkan hadiah dari musuh yang terbunuh (bukan yang melarikan diri)
        for e in self.enemies:
            if not e.alive and not e.reached_exit:
                self.gold  += e.reward
                self.score += e.reward * 10

        # Bersihkan musuh yang mati / keluar
        self.enemies = [e for e in self.enemies
                        if e.alive and not e.reached_exit]

        # ── Menara ─────────────────────────────────────────────
        for t in self.towers:
            t.update(self.enemies, dt)

        # ── Periksa penyelesaian gelombang ───────────────────────────────
        if (self.wave_active
                and self.active_group is None
                and not self.wave_queue
                and not self.enemies):
            self.wave_active    = False
            self.wave_countdown = WAVE_BREAK

            if self.wave_number >= len(WAVES):
                self.victory = True
                self.notify("All waves cleared — VICTORY!", ok=True)
            else:
                self.notify(f"Wave {self.wave_number} cleared! +Prep time")
