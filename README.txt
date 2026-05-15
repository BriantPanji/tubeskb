================================================================
  TOWER DEFENSE — MUSUH PINTAR
  Proyek Mata Kuliah AI  |  Python + Pygame
  Algoritma : Pencarian Jalur A* (A-Star)
================================================================

  Penulis    : Sudut Lain
  Mata Kuliah: Kecerdasan Buatan (Artificial Intelligence)
  Bahasa     : Python 3.10+
  Pustaka    : pygame >= 2.1.0
  Algoritma  : Pencarian A*  (Hart, Nilsson & Raphael, 1968)

================================================================
  DAFTAR ISI
================================================================

  1.  Gambaran Proyek
  2.  Cara Menjalankan
  3.  Kontrol Permainan
  4.  Struktur Proyek
  5.  Dokumentasi File (terperinci)
        5.1  config.py
        5.2  astar.py          ← File AI Inti
        5.3  enemy.py
        5.4  tower.py
        5.5  game_state.py     ← Di mana A* diterapkan
        5.6  renderer.py
        5.7  main.py
  6.  Mengapa Algoritma A*?
        6.1  Definisi Masalah
        6.2  Bagaimana A* Bekerja
        6.3  Mengapa Bukan BFS atau Dijkstra?
        6.4  A* dalam Permainan Ini — Dua Peran Utama
        6.5  Sifat Algoritma
        6.6  Referensi

================================================================
  1. GAMBARAN PROYEK
================================================================

  Tower Defense — Musuh Pintar adalah permainan strategi berbasis
  grid di mana pemain menempatkan menara pertahanan untuk mencegah
  gelombang unit musuh mencapai portal keluar.

  Fitur utama yang menjadikan ini proyek AI adalah BAGAIMANA
  musuh menavigasi grid. Alih-alih mengikuti jalur tetap yang 
  sudah digambar sebelumnya, setiap musuh menggunakan algoritma 
  pencarian jalur A* untuk menghitung dan memperbarui rutenya 
  secara dinamis dalam waktu nyata (real-time).

  Saat pemain menempatkan menara baru, SEMUA musuh yang masih hidup
  secara instan menghitung ulang jalur mereka di sekitar rintangan baru.
  Ini menciptakan ketegangan strategis yang nyata: pemain mencoba
  mengarahkan musuh ke zona mematikan, sementara AI beradaptasi 
  terhadap setiap keputusan penempatan.

  Permainan ini juga menggunakan A* sebagai VALIDATOR BATASAN — 
  penempatan menara ditolak jika itu akan memblokir sepenuhnya 
  semua jalur ke pintu keluar, memastikan permainan selalu dapat diselesaikan.

  Loop Inti Permainan:
    - Musuh muncul dari tepi KIRI (portal hijau).
    - Musuh mencoba mencapai tepi KANAN (portal merah).
    - Pemain menempatkan menara untuk memperlambat, mengarahkan, atau menghancurkan musuh.
    - Setiap musuh yang dibunuh menghasilkan emas untuk membeli lebih banyak menara.
    - Setiap musuh yang lolos mengurangi 1 nyawa (total 20 nyawa).
    - 8 gelombang dengan kesulitan yang meningkat harus dipertahankan untuk menang.

================================================================
  2. CARA MENJALANKAN
================================================================

  Langkah 1 — Aktifkan virtual environment Anda:
    Windows : venv\Scripts\activate
    Mac/Linux: source venv/bin/activate

  Langkah 2 — Instal pustaka yang diperlukan:
    pip install -r requirements.txt
      (atau: pip install pygame)

  Langkah 3 — Luncurkan permainan:
    python main.py

  Persyaratan:
    Python  3.10 atau lebih tinggi 
    pygame  2.1.0 atau lebih tinggi

================================================================
  3. KONTROL PERMAINAN
================================================================

  Klik Kanan di grid   Tempatkan menara yang dipilih di sel tersebut
  Klik Kiri di grid    Ganti menara yang dipilih
  1                    Pilih Menara Dasar (Basic)  (50g)
  2                    Pilih Menara Penembak Runduk (Sniper) (100g)
  3                    Pilih Menara Cepat (Rapid)   (75g)
  4                    Pilih Menara Bom (Bomb)    (125g)
  H                    Nyalakan/matikan sorotan jalur A*
  R                    Mulai ulang permainan
  P                    Jeda permainan
  ESC                  Keluar

  Tips UI:
    - Arahkan kursor ke sel untuk melihat jangkauan menara (cincin berwarna).
    - Sorotan hijau = penempatan valid.
    - Sorotan merah = tidak valid (sudah diblokir atau akan menjebak musuh).
    - Sel yang disorot biru menunjukkan jalur A* saat ini.

================================================================
  4. STRUKTUR PROYEK
================================================================

  tower_defense/
  │
  ├── main.py           Titik masuk. Loop permainan + penanganan kejadian.
  ├── config.py         Semua konstanta, nilai yang dapat disesuaikan, data permainan.
  ├── astar.py          Implementasi algoritma A* (AI inti).
  ├── enemy.py          Entitas musuh. Pergerakan + mengikuti jalur.
  ├── tower.py          Entitas Menara + Proyektil.
  ├── game_state.py     Logika permainan. Penempatan, gelombang, penggunaan A*.
  ├── renderer.py       Semua kode penggambaran Pygame.
  └── requirements.txt  Dependensi Python (pygame).

  Grafik dependensi (siapa mengimpor siapa):

    main.py
      ├── config.py
      ├── game_state.py
      │     ├── config.py
      │     ├── astar.py       ← AI digunakan di sini
      │     ├── enemy.py
      │     └── tower.py
      └── renderer.py
            └── config.py

================================================================
  5. DOKUMENTASI FILE
================================================================

----------------------------------------------------------------
  5.1  config.py
       Peran: Penyimpanan konfigurasi terpusat
----------------------------------------------------------------

  TUJUAN:
    Menyimpan setiap konstanta yang dapat disesuaikan di satu tempat.
    Tidak ada angka ajaib (magic numbers) yang tersebar di file lain —
    semua pengaturan diimpor dari sini. Ini memudahkan untuk menyesuaikan
    gameplay tanpa menyentuh kode logika.

  BAGIAN UTAMA:

    Layar & Grid
      CELL_SIZE = 40       Setiap sel grid berukuran 40×40 piksel.
      COLS = 20            Grid memiliki lebar 20 kolom.
      ROWS = 15            Grid memiliki tinggi 15 baris.
      SIDEBAR_W = 350      Lebar panel UI sisi kanan.
      SCREEN_W / SCREEN_H  Total dimensi jendela.
      FPS = 60             Target frame per detik.

    Titik Akhir Peta
      ENTRY = (0, 7)       Kemunculan musuh: tepi kiri, baris 7.
      EXIT  = (19, 7)      Tujuan musuh : tepi kanan, baris 7.
      Kedua sel ini selalu dijaga agar dapat dilewati oleh A*.

    Tipe Menara (dictionary TOWER_TYPES)
      Mendefinisikan 4 menara: basic, sniper, rapid, bomb.
      Setiap menara memiliki: biaya (cost), kerusakan (damage), jangkauan dalam sel (range), laju tembakan (fire_rate),
      kecepatan proyektil (proj_speed), warna (color), warna proyektil (proj_color), dan pintasan keyboard (key).

    Tipe Musuh (dictionary ENEMY_TYPES)
      Mendefinisikan 4 musuh: Grunt, Scout, Tank, Swarm.
      Setiap musuh memiliki: hp, kecepatan dalam px/frame (speed), hadiah emas (reward), warna (color).

    Jadwal Gelombang (list WAVES)
      8 gelombang, masing-masing berupa list berisi (tipe_musuh, jumlah, interval).
      Kelompok dalam satu gelombang muncul satu demi satu.
      Tingkat kesulitan meningkat: gelombang 1 murni Grunt,
      gelombang 8 mencampur keempat tipe dalam jumlah besar.

    WAVE_BREAK = 5.0
      Detik waktu persiapan antar gelombang.

  RELEVANSI AKADEMIK:
    Memisahkan konfigurasi dari logika adalah prinsip rekayasa 
    perangkat lunak standar (separation of concerns). Ini juga 
    memudahkan demonstrasi proyek — ubah angka di config.py 
    untuk menunjukkan perilaku AI yang berbeda secara langsung.

----------------------------------------------------------------
  5.2  astar.py
       Peran: Algoritma pencarian jalur A*  ← FILE AI INTI
----------------------------------------------------------------

  TUJUAN:
    Mengimplementasikan algoritma pencarian A* (A-Star) untuk 
    menemukan jalur optimal (terpendek) antara dua sel di 
    grid permainan, menavigasi di sekitar sel yang diblokir (menara).

    File ini adalah jantung akademik dari proyek ini.

  FUNGSI-FUNGSI:

    manhattan(a, b) -> int
      Menghitung heuristik jarak Manhattan antara dua
      sel grid (kolom, baris).

        h(n) = |col_a - col_b| + |row_a - row_b|

      Ini adalah fungsi heuristik h(n) yang digunakan oleh A*.
      Ini DAPAT DITERIMA (ADMISSIBLE) pada grid 4 arah (tidak pernah
      melebih-lebihkan) karena setiap langkah grid biayanya tepat 1
      dan pergerakan diagonal tidak diizinkan.

    astar(blocked, start, goal, cols, rows) -> list | None
      Fungsi A* utama. Mengembalikan jalur optimal sebagai list
      dari tuple (kolom, baris) dari awal ke tujuan, atau None jika
      tidak ada jalur yang ada.

      Struktur data internal:
        open_set   — antrean prioritas min-heap diurutkan berdasarkan f(n).
                     Format tuple: (f_score, g_score, node)
                     g_score digunakan sebagai pemecah seri (tie-breaker).
        came_from  — dictionary yang memetakan setiap node ke induknya,
                     digunakan untuk merekonstruksi jalur pada akhirnya.
        g_score    — dictionary yang memetakan setiap node yang dikunjungi ke
                     biaya termurah yang diketahui untuk mencapainya.

      Langkah-langkah algoritma (per iterasi):
        1. Pop node dengan f(n) terendah dari open_set.
        2. Jika itu adalah tujuan, rekonstruksi dan kembalikan jalur.
        3. Jika tidak, perluas 4 tetangganya (atas/bawah/kiri/kanan).
        4. Lewati tetangga yang di luar batas atau diblokir.
        5. Hitung tentative_g = g_score[current] + 1.
        6. Jika lebih murah dari g_score yang diketahui, perbarui catatan dan
           dorong (f, g, neighbour) ke dalam heap.

    astar_node_count(blocked, start, goal, cols, rows)
      -> tuple (path, nodes_expanded)
      Versi perluasan dari astar() yang juga menghitung berapa banyak
      node yang diperluas selama pencarian. Berguna untuk
      perbandingan akademik: Anda dapat memanggil ini bersama dengan implementasi 
      BFS dan menunjukkan bahwa A* memperluas jauh lebih sedikit node.

  FORMULA ALGORITMA:

        f(n) = g(n) + h(n)

        g(n)  =  biaya aktual dari awal ke node n
                 (setiap langkah grid = 1 unit)

        h(n)  =  Jarak Manhattan dari n ke tujuan
                 (perkiraan heuristik dari biaya yang tersisa)

        f(n)  =  perkiraan total biaya jalur yang melalui n

    A* selalu memperluas node dengan f(n) terendah terlebih dahulu,
    yang memandu pencarian menuju tujuan secara efisien sambil
    menjamin solusi optimal.

  KOMPLEKSITAS:
    Waktu : O(E log V)  — E tepi (edges), V simpul (vertices - sel grid)
    Ruang : O(V)        — open set dan came_from menyimpan paling banyak V node

  DIPANGGIL OLEH:
    game_state.py — untuk memvalidasi penempatan menara dan
                    untuk menghitung jalur baru setelah setiap penempatan.
    enemy.py      — menerima jalur yang dihitung untuk diikuti.

----------------------------------------------------------------
  5.3  enemy.py
       Peran: Kelas entitas Musuh
----------------------------------------------------------------

  TUJUAN:
    Mewakili satu unit musuh di grid. Menangani 
    pergerakan tingkat piksel yang mulus di sepanjang jalur yang dihitung A*, 
    menerima kerusakan dari proyektil menara, dan secara dinamis 
    memperbarui rutenya saat menara baru ditempatkan.

  KELAS: Enemy

    Konstruktor:  Enemy(enemy_type, path)
      enemy_type  — string kunci ke ENEMY_TYPES di config.py
      path        — list (kolom, baris) dari A* (awal → tujuan)

    Atribut Utama:
      hp / max_hp      Poin kesehatan (hit points) saat ini dan maksimum.
      speed            Pergerakan dalam piksel per frame.
      reward           Emas yang diberikan kepada pemain saat terbunuh.
      alive            False saat HP mencapai 0 (terbunuh).
      reached_exit     True saat musuh berjalan keluar tepi kanan.
      path             Jalur A* saat ini (list sel).
      waypoint_idx     Indeks sel yang sedang dituju.
      x, y             Posisi piksel (float untuk pergerakan mulus).

    Metode:

      update_path(new_path)
        Dipanggil oleh game_state.py setiap kali menara ditempatkan.
        Mencari sel terdekat di new_path ke posisi grid musuh
        saat ini dan melanjutkannya dari sana.
        Ini memungkinkan perutean ulang waktu nyata yang mulus — musuh
        tidak melompat atau berteleportasi, mereka dengan mulus melanjutkan 
        di rute optimal baru.

      take_damage(amount)
        Mengurangi HP. Mengatur alive = False saat HP mencapai 0.

      update()
        Dipanggil sekali per frame. Memindahkan musuh ke 
        titik jalan (waypoint) berikutnya di jalur hingga kecepatan `speed` piksel.
        Saat titik jalan tercapai, memajukan waypoint_idx.
        Saat semua titik jalan dikunjungi, mengatur reached_exit.

      draw(surface)
        Merender musuh sebagai lingkaran berwarna dengan
        bayangan, batas putih, dan bar kesehatan dinamis
        (hijau → merah saat HP berkurang).

  KONEKSI AI:
    enemy.py tidak memanggil A* secara langsung. Sebaliknya ia MENGIKUTI 
    jalur yang dihitung oleh astar.py dan diteruskan oleh 
    game_state.py. Metode update_path() adalah antarmuka utama 
    yang membuat perutean ulang memungkinkan pada saat runtime.

----------------------------------------------------------------
  5.4  tower.py
       Peran: Kelas entitas Menara dan Proyektil
----------------------------------------------------------------

  TUJUAN:
    Mewakili menara pertahanan yang ditempatkan oleh pemain dan
    proyektil yang mereka tembakkan. Menara secara otomatis 
    mengakuisisi target, memutar larasnya menghadap musuh, dan 
    menembak dengan laju yang dapat dikonfigurasi.

  KELAS: Projectile

    Peluru kendali yang ditembakkan oleh Menara.

    Konstruktor:  Projectile(x, y, target, damage, speed, color)
      Menyimpan referensi ke objek Enemy target.

    update()
      Bergerak menuju posisi piksel target musuh saat ini
      setiap frame (perilaku pelacak). Jika musuh mati
      sebelum proyektil tiba, proyektil
      dibuang (done = True).

    draw(surface)
      Merender proyektil sebagai lingkaran kecil dengan
      lingkaran cahaya bersinar semi-transparan untuk kejelasan visual.

  KELAS: Tower

    Konstruktor:  Tower(col, row, tower_type)
      tower_type  — string kunci ke TOWER_TYPES di config.py

    Atribut Utama:
      range_px     Jangkauan deteksi dan penembakan dalam piksel.
      fire_rate    Tembakan per detik.
      cooldown     Detik yang tersisa hingga tembakan berikutnya.
      target       Musuh saat ini yang sedang ditargetkan.
      projectiles  List objek Projectile yang aktif.
      angle        Sudut rotasi laras (derajat).

    Metode:

      update(enemies, dt)
        Pembaruan utama per-frame. Mengurangi cooldown,
        memperbarui semua proyektil, memvalidasi/mengakuisisi target,
        memutar laras, dan menembak saat cooldown mencapai 0.

      _find_target(enemies)
        Memindai semua musuh hidup dalam range_px dan memilih
        yang terdekat.

      _fire()
        Membuat Projectile baru yang ditujukan pada self.target dan
        menambahkannya ke self.projectiles.

      draw(surface, show_range)
        Merender dasar menara, laras yang berputar, titik pusat,
        hamparan cincin jangkauan opsional, dan semua proyektil.

  TIPE MENARA (didefinisikan dalam config.py):
    Basic   — Seimbang. 50g. Menara awal (starter) serba bisa yang bagus.
    Sniper  — Jarak jauh, kerusakan tinggi, laju tembakan sangat lambat.
    Rapid   — Jarak dekat, kerusakan rendah, laju tembakan sangat cepat.
    Bomb    — Jarak dekat, kerusakan masif, sangat lambat.

  CATATAN:
    Logika penempatan menara (tabrakan, validasi A*) berada di
    game_state.py, bukan di sini. Objek menara itu sendiri hanya
    menangani perilaku pertempuran.

----------------------------------------------------------------
  5.5  game_state.py
       Peran: Logika permainan inti  ← DI MANA A* DITERAPKAN
----------------------------------------------------------------

  TUJUAN:
    Koordinator pusat permainan. Memiliki state grid,
    mengelola validasi penempatan menara, menyiarkan pembaruan jalur
    ke musuh, mengontrol kemunculan gelombang, dan melacak semua
    sumber daya pemain.

  KELAS: GameState

    Konstruktor memanggil reset(), yang menginisialisasi semuanya
    baru — juga digunakan oleh tombol R (restart).

    Atribut Utama:
      gold, lives, score, wave_number   Sumber daya/kemajuan pemain.
      blocked                           Himpunan sel (kolom, baris)
                                        yang ditempati menara.
      current_path                      Jalur A* terbaru dari
                                        ENTRY ke EXIT.
      towers / enemies                  List entitas.
      wave_active, wave_queue           Status kemunculan gelombang.
      selected_type                     Menara yang sedang dipilih.
      hover_cell, hover_valid           Status pratinjau mouse.

    KASUS PENGGUNAAN A* 1 — Validasi Penempatan Menara:  _can_place()
      Sebelum membiarkan menara ditempatkan, permainan
      sementara menambahkan sel kandidat ke set yang diblokir
      dan memanggil A* untuk memeriksa apakah jalur masih ada:

        test_blocked = self.blocked | {(col, row)}
        return astar(test_blocked, ENTRY, EXIT, COLS, ROWS) is not None

      Jika A* mengembalikan None (tidak ada jalur), penempatan ditolak dan
      sel bersinar merah dalam pratinjau. Ini menjamin bahwa
      musuh selalu memiliki setidaknya satu rute pelarian — batasan 
      permainan adil (fair play) yang diberdayakan sepenuhnya oleh A*.

    KASUS PENGGUNAAN A* 2 — Perutean Ulang Pasca-Penempatan:  try_place_tower()
      Setelah penempatan yang valid dilakukan, A* berjalan lagi pada
      set yang diblokir yang diperbarui untuk mendapatkan jalur optimal baru.
      Jalur ini kemudian disiarkan ke SETIAP musuh yang hidup:

        new_path = astar(self.blocked, ENTRY, EXIT, COLS, ROWS)
        for e in self.enemies:
            if e.alive and not e.reached_exit:
                e.update_path(new_path)

      Ini adalah perilaku AI waktu nyata inti — musuh 
      melakukan perutean ulang di tengah pergerakan tanpa teleportasi atau 
      gangguan apa pun.

    KASUS PENGGUNAAN A* 3 — Kemunculan Musuh Baru:  _update_spawning()
      Setiap musuh yang baru muncul diberi salinan 
      current_path (hasil A* terbaru) untuk diikuti:

        enemy = Enemy(etype, list(self.current_path))

      Ini berarti musuh baru selalu mulai dengan jalur 
      optimal saat ini yang sudah memperhitungkan semua menara yang ditempatkan.

    Manajemen Gelombang:
      start_next_wave()  — memuat data gelombang dari config.WAVES.
      _update_spawning() — menghitung timer kemunculan, membuat musuh.
      Gelombang dimulai otomatis setelah detik WAVE_BREAK dari waktu persiapan.

    update(dt)
      Pembaruan utama per-frame yang dipanggil dari main.py.
      Urutan operasi setiap frame:
        1. Menjalankan timer tampilan pesan.
        2. Menangani hitung mundur gelombang atau kemunculan aktif.
        3. Memperbarui semua musuh (pergerakan + deteksi keluar).
        4. Mengumpulkan emas/skor dari musuh yang dibunuh.
        5. Menghapus musuh yang mati/keluar dari list.
        6. Memperbarui semua menara (penargetan + penembakan).
        7. Memeriksa apakah gelombang sepenuhnya selesai.

----------------------------------------------------------------
  5.6  renderer.py
       Peran: Semua kode penggambaran Pygame
----------------------------------------------------------------

  TUJUAN:
    Menangani setiap elemen visual di layar. Sepenuhnya
    baca-saja sehubungan dengan GameState — ia hanya membaca data,
    tidak pernah memodifikasinya. Pemisahan logika dan rendering ini
    adalah pola arsitektur permainan standar (gaya MVC).

  FUNGSI-FUNGSI UTAMA:

    init_fonts()
      Menginisialisasi font Consolas pada 5 ukuran yang digunakan di seluruh
      UI. Harus dipanggil sekali setelah pygame.init().

    draw_grid(surface, gs)
      Merender grid sel 20×15 dengan:
        - Sel latar belakang biru gelap.
        - Sel yang disorot biru sedikit lebih terang untuk
          jalur A* saat ini (jejak biru di layar).
        - Portal masuk hijau (tepi kiri).
        - Portal keluar merah (tepi kanan).

    draw_hover(surface, gs)
      Merender pratinjau penempatan di bawah kursor mouse:
        - Warna hijau + cincin jangkauan = penempatan valid.
        - Warna merah = penempatan tidak valid.
      Cincin jangkauan digambar menggunakan nilai jangkauan menara 
      yang dipilih, memberikan umpan balik visual yang akurat kepada pemain.

    draw_towers(surface, gs)
      Memanggil tower.draw() untuk setiap menara. Meneruskan show_range=True
      untuk menara yang saat ini berada di bawah kursor mouse sehingga 
      cincin jangkauannya selalu terlihat.

    draw_enemies(surface, gs)
      Memanggil enemy.draw() untuk setiap musuh yang hidup.

    draw_sidebar(surface, gs)
      Merender seluruh panel sisi kanan:
        - Judul permainan dan label algoritma.
        - Statistik langsung: emas, nyawa, gelombang, skor.
        - Empat tombol pemilihan menara (menyoroti yang aktif).
        - Hitung mundur gelombang atau teks status "gelombang aktif".
        - Pesan notifikasi yang memudar dari gs.notify().
        - Legenda kontrol di bagian bawah.

    draw_overlay(surface, gs)
      Menggelapkan area permainan dan menampilkan layar GAME OVER atau
      VICTORY yang besar ketika tanda yang sesuai diatur.

    draw_all(surface, gs, show_path)
      Fungsi utama yang dipanggil dari main.py sekali per frame.
      Memanggil semua yang ada di atas dalam urutan gambar yang benar:
        1. Isi latar belakang.
        2. Grid (termasuk sorotan jalur).
        3. Pratinjau hover.
        4. Menara.
        5. Musuh.
        6. Sidebar.
        7. Overlay (hanya jika permainan berakhir).

  CATATAN DESAIN:
    - Semua warna ditentukan dalam config.py sebagai konstanta C_*.
    - Alpha blending (pygame.SRCALPHA) digunakan untuk cincin
      jangkauan dan hamparan (overlay) game-over untuk tampilan yang halus.
    - Rotasi laras menara menggunakan math.atan2 untuk menghitung
      sudut ke target saat ini.

----------------------------------------------------------------
  5.7  main.py
       Peran: Titik masuk dan loop permainan
----------------------------------------------------------------

  TUJUAN:
    Skrip tingkat atas yang memulai aplikasi.
    Menginisialisasi Pygame, membuat status permainan dan jam (clock),
    dan menjalankan loop permainan utama pada 60 FPS.

  ALUR EKSEKUSI:

    1. pygame.init() + jendela + pembuatan jam.
    2. init_fonts() dipanggil sekali.
    3. GameState() dibuat (memanggil A* untuk jalur awal).
    4. Memasuki while True loop permainan:

       a. clock.tick(FPS) → dt dalam detik.

       b. PENANGANAN KEJADIAN (EVENT HANDLING)
            QUIT / ESC → keluar.
            K_r        → GameState baru (mulai ulang).
            K_h        → beralih sorotan jalur.
            K_1–K_4    → ubah tipe menara yang dipilih.
            MOUSEBUTTONDOWN klik kiri:
              - Periksa apakah klik mengenai tombol menara sidebar.
              - Jika tidak, panggil gs.try_place_tower(col, row).

       c. PEMBARUAN HOVER
            pixel_to_cell() mengonversi posisi mouse ke grid.
            gs.set_hover() menjalankan validasi A* untuk pratinjau.

       d. PEMBARUAN LOGIKA PERMAINAN
            gs.update(dt) menjalankan semua logika entitas dan gelombang.

       e. GAMBAR (DRAW)
            draw_all(screen, gs, show_path) merender frame.
            pygame.display.flip() menampilkannya.

  FUNGSI PEMBANTU:

    pixel_to_cell(mx, my) -> tuple | None
      Mengonversi koordinat piksel mentah menjadi sel grid
      (kolom, baris). Mengembalikan None jika mouse berada di atas sidebar
      atau di luar batas grid.

================================================================
  6. MENGAPA ALGORITMA A*?  (Justifikasi Akademik)
================================================================

----------------------------------------------------------------
  6.1  Definisi Masalah
----------------------------------------------------------------

  Tantangan AI inti dalam game ini adalah MASALAH JALUR TERPENDEK
  (SHORTEST PATH PROBLEM) pada grid 2D:

    "Diberikan sel grid di mana beberapa sel diblokir
     (menara), temukan jalur terpendek yang dapat dilalui dari
     sel masuk ke sel keluar."

  Ini adalah masalah klasik dalam Kecerdasan Buatan (AI) dan
  secara formal didefinisikan sebagai MASALAH PENCARIAN GRAF di mana:

    - Setiap sel grid adalah NODE dalam graf.
    - Kedekatan (atas/bawah/kiri/kanan) mendefinisikan EDGE (tepi).
    - Setiap tepi memiliki BIAYA seragam 1.
    - Sel yang diblokir (menara) cukup dihapus dari
      graf (tidak ada tepi yang mengarah ke sana).
    - Tujuannya adalah untuk menemukan jalur dari ENTRY ke EXIT
      dengan total biaya minimum (langkah paling sedikit).

  Kompleksitas tambahan: grid BERUBAH saat runtime.
  Setiap kali pemain menempatkan menara, tepi dihapus
  dari graf, dan jalur terpendek harus dihitung ulang.
  Ini membutuhkan algoritma yang efisien dan
  benar pada graf dinamis.

----------------------------------------------------------------
  6.2  Bagaimana A* Bekerja (Singkat)
----------------------------------------------------------------

  A* memelihara ANTREAN PRIORITAS (min-heap) dari node untuk dikunjungi,
  diurutkan berdasarkan skor f(n):

        f(n) = g(n) + h(n)

  Di mana:
    g(n)  =  Biaya pasti untuk mencapai node n dari awal.
             Ditambahkan dengan 1 untuk setiap langkah yang diambil.

    h(n)  =  Perkiraan heuristik dari biaya dari n ke tujuan.
             Dalam game ini: Jarak Manhattan.
             h(n) = |col_n - col_goal| + |row_n - row_goal|

    f(n)  =  Perkiraan total biaya dari jalur termurah
             yang melalui node n.

  Dengan selalu memperluas node dengan f(n) terendah, A*
  memprioritaskan node yang dekat dengan awal DAN
  dekat dengan tujuan — tidak seperti BFS (yang mengabaikan jarak
  ke tujuan) atau Pencarian Greedy (yang mengabaikan jarak dari awal).

  Ketika tujuan tercapai, jalur direkonstruksi dengan
  berjalan mundur melalui dictionary came_from.

----------------------------------------------------------------
  6.3  Mengapa Bukan BFS atau Dijkstra?
----------------------------------------------------------------

  BFS (Breadth-First Search):
    Mengeksplorasi semua node pada jarak 1, lalu jarak 2, dll.
    Itu LENGKAP dan OPTIMAL pada graf tak berbobot, tetapi
    TIDAK MEMILIKI heuristik — ia memperluas node ke segala arah
    secara merata, termasuk banyak sel yang jelas bergerak
    MENJAUH dari tujuan.

    Pada grid 20×15, BFS mungkin memperluas 200–300 node untuk menemukan
    jalur yang ditemukan A* dengan memperluas 40–80 node.

    Putusan: Benar, tapi boros.

  Algoritma Dijkstra:
    Optimal pada graf berbobot. Hanya menggunakan g(n), tidak ada heuristik.
    Pada grid dengan biaya seragam (semua tepi = 1), Dijkstra terdegradasi
    menjadi BFS. Tidak ada peningkatan di atas BFS dalam pengaturan game ini.

    Putusan: Benar, tapi setara dengan BFS di sini.

  A* (Algoritma Terpilih):
    Menggunakan h(n) = jarak Manhattan untuk MEMANDU pencarian menuju
    tujuan. Memperluas jauh lebih sedikit node daripada BFS/Dijkstra sambil
    tetap menjamin solusi OPTIMAL (karena
    heuristiknya dapat diterima — tidak pernah melebih-lebihkan).

    Ini menjadikan A* pilihan standar industri untuk pencarian jalur 
    grid dalam game, robotika, dan sistem navigasi.

    Putusan: Optimal DAN efisien. Paling cocok untuk game ini.

  Ringkasan Perbandingan:
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
  │  Algoritma   │  Lengkap?    │  Optimal?    │  Efisien?    │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
  │  BFS         │  Ya          │  Ya          │  Tidak       │
  │  Dijkstra    │  Ya          │  Ya          │  Tidak       │
  │  Greedy      │  Tidak       │  Tidak       │  Ya          │
  │  A*          │  Ya          │  Ya          │  Ya  ✓       │
  └──────────────┴──────────────┴──────────────┴──────────────┘

----------------------------------------------------------------
  6.4  A* dalam Permainan Ini — Dua Peran Utama
----------------------------------------------------------------

  PERAN 1: Navigasi Musuh Waktu Nyata (Real-Time)

    Setiap musuh mengikuti jalur yang dihitung A* dari ENTRY ke EXIT.
    Saat pemain menempatkan menara (menghapus sel dari
    graf yang dapat dilalui), A* dijalankan ulang dan semua musuh yang hidup
    diberikan jalur optimal baru melalui update_path().

    Ini menghasilkan perilaku "musuh pintar" yang mendefinisikan
    game ini: musuh tidak berjalan buta ke dinding, mereka
    secara cerdas beradaptasi dengan strategi pemain.

  PERAN 2: Validasi Batasan Penempatan

    Sebelum penempatan menara dilakukan, A* dijalankan pada
    kumpulan blok HIPOTESIS yang mencakup sel kandidat.
    Jika A* mengembalikan None (tidak ada jalur ke pintu keluar), penempatan
    ditolak dengan peringatan visual merah.

    Ini mencegah pemain dari menjebak musuh tanpa
    jalan keluar, yang akan merusak loop permainan.

    Ini adalah PENGGUNAAN BARU A* sebagai pemecah batasan waktu nyata,
    bukan hanya alat navigasi — poin diskusi yang kuat untuk
    laporan proyek Anda.

----------------------------------------------------------------
  6.5  Sifat Algoritma
----------------------------------------------------------------

  Admissibility (Dapat Diterima):
    Heuristik jarak Manhattan h(n) tidak pernah melebih-lebihkan
    jalur terpendek sebenarnya karena:
      - Setiap langkah biayanya tepat 1.
      - Jarak Manhattan menghitung jumlah langkah minimum
        yang dibutuhkan jika TIDAK ADA rintangan.
    Oleh karena itu h(n) <= biaya_sebenarnya(n, tujuan) untuk semua n.
    Ini menjamin A* mengembalikan jalur OPTIMAL.

  Completeness (Kelengkapan):
    A* akan selalu menemukan jalur jika ada, karena ia
    secara sistematis mengeksplorasi semua node yang dapat dijangkau dalam urutan
    peningkatan f(n). Ia akan mengembalikan None hanya ketika
    tidak ada jalur yang benar-benar memungkinkan.

  Consistency (Konsistensi):
    h(n) memenuhi ketidaksamaan segitiga:
      h(n) <= biaya(n, n') + h(n')  untuk setiap tetangga n'.
    Konsistensi menyiratkan admissibility dan memastikan node
    tidak pernah diperluas ulang — membuat A* maksimal efisien.

  Kompleksitas Waktu:  O(E log V)
    E = jumlah tepi grid yang dapat dilalui (~4 per sel)
    V = jumlah sel grid (COLS × ROWS = 300 dalam game ini)
    log V ≈ 8.2 untuk V = 300

  Kompleksitas Ruang: O(V)
    Open set (antrean prioritas) dan dictionary came_from masing-masing
    menyimpan paling banyak V entri.

----------------------------------------------------------------
  6.6  Referensi
----------------------------------------------------------------

  [1]  Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).
       A Formal Basis for the Heuristic Determination of
       Minimum Cost Paths.
       IEEE Transactions on Systems Science and Cybernetics.

  [2]  Russell, S., & Norvig, P. (2020).
       Artificial Intelligence: A Modern Approach (4th ed.).
       Chapter 3: Solving Problems by Searching.
       Pearson.

  [3]  Nilsson, N. J. (1971).
       Problem-Solving Methods in Artificial Intelligence.
       McGraw-Hill.

  [4]  Sturtevant, N. (2012).
       Benchmarks for Grid-Based Pathfinding.
       IEEE Transactions on Computational Intelligence
       and AI in Games.

================================================================
  AKHIR DOKUMENTASI
================================================================
