# 🧠 Penjelasan Simpel: Algoritma A* dan Project Tower Defense

---

## Bayangkan Kamu Tersesat di Labirin...

Kamu berdiri di pintu masuk sebuah **labirin raksasa**. Di ujung sana ada pintu keluar. Kamu harus cari jalan keluar secepat mungkin.

Nah, ada beberapa cara kamu bisa cari jalan keluar:

---

## 🐢 Cara 1: BFS — "Si Penakut yang Cek Semua Arah"

Bayangin kamu **takut salah jalan**, jadi kamu kirim "kloningan" dirimu ke **semua arah sekaligus** — kiri, kanan, atas, bawah. Setiap kloningan juga kirim kloningan lagi ke semua arah.

Hasilnya? Kamu **pasti** ketemu pintu keluar. Tapi masalahnya:
- Kamu kirim kloningan ke arah yang jelas-jelas **salah** (misalnya ke arah dinding, atau malah balik ke pintu masuk)
- **Buang-buang tenaga dan waktu** karena eksplorasi ke mana-mana tanpa arah

> 🐢 BFS itu kayak orang yang nyari kunci mobil di **seluruh rumah** — padahal dia terakhir ingat taruh di meja dapur. Tetap dicari di kamar mandi, di gudang, di atap...

---

## 🦊 Cara 2: Greedy — "Si Sok Tau"

Bayangin kamu **selalu jalan ke arah yang TERLIHAT paling dekat** ke pintu keluar. Kalau pintu keluar di kanan, ya kamu belok kanan terus.

Masalahnya? Kadang **jalan buntu!** Kamu mentok di tembok karena terlalu fokus ke arah tujuan tanpa peduli ada halangan. Kadang jalur yang kelihatan lebih jauh justru lebih cepat sampai.

> 🦊 Greedy itu kayak orang yang pake Google Maps tapi **cuma lihat garis lurus ke tujuan** — tanpa peduli ada sungai, gedung, atau jalan tol yang harus diputar dulu.

---

## 🐌 Cara 3: Dijkstra — "Si Teliti yang Nggak Tau Arah"

Dijkstra itu versi **upgrade-nya BFS**. Bedanya gimana?

Bayangin kamu di sebuah kota di mana **setiap jalan punya panjang yang beda-beda**. Ada jalan tol (cepat tapi mahal), ada jalan kampung (murah tapi lama), ada jalan biasa.

BFS nggak peduli perbedaan itu — dia anggap semua jalan sama. Dijkstra **lebih teliti**: dia catat **biaya persis** yang sudah dikeluarkan buat sampai ke setiap titik, dan selalu pilih titik yang biayanya **paling murah dulu**.

Kedengarannya bagus kan? Masalahnya:
- Dijkstra **nggak tau arah tujuan**. Dia tetap cek ke **semua arah** — kiri, kanan, atas, bawah — sama kayak BFS
- Dia cuma lebih teliti soal **biaya** yang sudah dikeluarkan, tapi **nggak punya tebakan** arah mana yang lebih menjanjikan

> 🐌 Dijkstra itu kayak **kurir paket yang sangat teliti ngitung ongkos kirim** ke setiap alamat di kota. Dia pastiin nggak ada jalan yang lebih murah. Tapi dia **nggak pernah lihat peta** — jadi dia tetap cek semua gang dan jalan buntu sebelum akhirnya sampai ke alamat tujuan.

**Dan di game kita?** Semua langkah di grid biayanya **sama** (1 langkah = 1 biaya). Nggak ada jalan yang lebih mahal atau murah. Jadi ketelitian Dijkstra **nggak ada gunanya** — dia jadi persis sama kayak BFS. Kayak bawa kalkulator canggih ke ujian yang soalnya cuma 1+1.

---

## 🧠 Cara 4: A* — "Si Cerdas yang Mikir Dua Langkah"

Nah, A* itu **gabungan terbaik dari semuanya**. Dia punya ketelitian Dijkstra, TAPI ditambah "insting arah" yang nggak dimiliki BFS dan Dijkstra. Dia mikir pakai 2 pertanyaan sekaligus:

### Pertanyaan 1: "Sudah sejauh apa aku jalan dari awal?"
> Ini namanya **g(n)** — biaya yang sudah dikeluarkan.
> 
> Kayak ngitung: "Aku sudah jalan 5 langkah dari pintu masuk."

### Pertanyaan 2: "Kira-kira masih seberapa jauh ya ke tujuan?"
> Ini namanya **h(n)** — tebakan/perkiraan jarak ke tujuan.
> 
> Kayak ngeliat dari jauh: "Hmm, pintu keluarnya kayaknya masih sekitar 8 langkah lagi kalau lurus."

### Lalu dia jumlahkan keduanya:
> **f(n) = g(n) + h(n)**
> 
> "Total perkiraan jarak perjalananku = 5 + 8 = 13"

A* selalu **pilih jalan yang total perkiraannya paling kecil**. Jadi dia nggak asal belok kanan kayak Greedy, tapi juga nggak buang waktu cek semua arah kayak BFS.

> 🧠 A* itu kayak orang yang nyari jalan ke mall — dia **tau arah mall di mana** (pakai perkiraan), tapi dia juga **ingat sudah jalan sejauh apa** dan **pilih jalan yang paling masuk akal secara total**.

---

## 📏 Manhattan Distance — "Si Penghitung Blok Kota"

Nah, tebakan jarak yang dipakai A* di game ini namanya **Manhattan Distance**. Kenapa namanya Manhattan?

Bayangin kamu di kota New York (Manhattan). Jalanannya **kotak-kotak** kayak grid. Kamu **nggak bisa jalan diagonal** nembus gedung — kamu cuma bisa jalan ke kiri/kanan/atas/bawah.

Jadi kalau kamu di titik A dan mau ke titik B:

```
  A . . . .
  . . . . .
  . . . . B
```

Kamu nggak bisa jalan diagonal langsung (kayak burung terbang ✈️). Kamu harus jalan:
- **4 langkah ke kanan** + **2 langkah ke bawah** = **6 langkah**

Itu Manhattan Distance-nya: **hitung berapa blok horizontal + berapa blok vertikal**.

> 📏 Manhattan Distance = |selisih kolom| + |selisih baris|

**Kenapa ini bagus buat game kita?** Karena musuh di game kita juga cuma bisa gerak 4 arah (atas/bawah/kiri/kanan), persis kayak jalan di kota Manhattan! Jadi tebakan jaraknya selalu **masuk akal** — nggak pernah terlalu lebay, nggak pernah terlalu pesimis.

---

## 🎮 Bagaimana A* Bekerja di Game Tower Defense Kita?

Oke, sekarang masuk ke game kita. Bayangin grid permainan kita itu sebuah **kota kotak-kotak**:

### Ceritanya begini:

Ada **monster** (musuh) yang muncul dari **pintu hijau** (kiri). Mereka mau kabur ke **pintu merah** (kanan). Tugas kamu sebagai pemain: **taruh menara** di grid buat halangi dan tembak mereka.

### Nah, monster-monster ini **pintar**. Mereka punya GPS (A*)!

#### Langkah 1 — Monster Pertama Muncul
Monster pertama muncul di pintu hijau. Dia langsung **jalanin A*** di otaknya:

> *"Oke, aku di kiri. Pintu keluar di kanan. Nggak ada halangan. Aku jalan lurus aja."*

```
  🟩 → → → → → → → → → → → → → → → → → → 🟥
```
Simpel, jalur lurus.

#### Langkah 2 — Pemain Taruh Menara
Kamu taruh menara di tengah jalan! Sekarang ada **tembok** yang menghalangi.

Semua monster yang masih hidup langsung **hitung ulang jalur** pakai A*:

> *"Wah, jalan lurus diblokir! Aku hitung ulang... oke, aku muter lewat atas!"*

```
          → → → → ↓
          ↑       ↓
  🟩 → → ↑  🏰   ↓ → → → → → 🟥
```

Monster **nggak bingung, nggak nabrak tembok**. Mereka langsung tau jalan tercepat yang baru.

#### Langkah 3 — Pemain Taruh Menara Lagi
Kamu taruh menara lagi! Monster hitung ulang lagi:

> *"Jalan atas juga diblokir? Oke, aku lewat bawah aja!"*

Ini terjadi **setiap kamu taruh menara baru**. Semua monster langsung update GPS-nya.

#### Langkah 4 — Kalau Kamu Coba Blokir Semua Jalan?
Kamu iseng mau blokir SEMUA jalan biar monster nggak bisa lewat? 

**Nggak bisa!** Game-nya juga pakai A* buat ngecek:

> *"Kalau menara ditaruh di sini... [jalanin A*]... hasilnya: NGGAK ADA JALUR. Berarti nggak boleh taruh di sini!"*

Sel-nya langsung jadi **merah** dan penempatan ditolak. Ini supaya game tetap adil — selalu ada jalan buat monster.

---

## 🏆 Jadi, Kenapa Pilih A*?

Bayangin lagi analogi labirin tadi. Kalau kamu jadi monster di game ini:

| Algoritma | Analogi | Punya "Insting Arah"? | Optimal? | Masalah |
|-----------|---------|----------------------|----------|---------|
| **BFS** | Kloningan ke **semua arah** | ❌ Tidak | ✅ Ya | Lambat — cek jalur yang jelas salah arah |
| **Dijkstra** | Kurir teliti yang **ngitung ongkos** tapi nggak lihat peta | ❌ Tidak | ✅ Ya | Di game kita = BFS, ketelitiannya percuma |
| **Greedy** | Selalu belok ke arah **yang kelihatan paling dekat** | ✅ Ya | ❌ Tidak | Kadang mentok! Bisa dapet jalur bukan terpendek |
| **A\*** ✅ | **Tau arah tujuan** DAN **ingat sudah jalan sejauh apa** | ✅ Ya | ✅ Ya | Nggak ada! Cepat DAN selalu dapet jalur terpendek |

### Rangkuman kenapa A* menang:

1. **Selalu dapet jalur terpendek** (optimal) — monster selalu ambil rute tercepat ✅
2. **Lebih cepat dari BFS** — karena pakai "tebakan arah" (Manhattan Distance), nggak perlu cek semua arah ✅
3. **Nggak mentok kayak Greedy** — karena tetap ingat jarak yang sudah dilewati ✅
4. **Lebih berguna dari Dijkstra** — Dijkstra teliti ngitung biaya tapi di grid game kita semua biaya sama, jadi ketelitiannya sia-sia. A* tambah "insting arah" yang bikin dia jauh lebih cepat ✅
5. **Cocok buat grid game** — Manhattan Distance itu "tebakan" yang sempurna buat grid 4-arah ✅
6. **Bisa jalan berkali-kali dengan cepat** — penting karena di game ini A* dipanggil setiap kali menara ditaruh ✅

---

## 🔍 Siapa yang Ngecek Halangan? A* atau Fungsi Lain?

Ini pertanyaan penting! Jawabannya: **dua-duanya kerja bareng**, tapi tugasnya beda.

### A* itu cuma "Si Navigator"

A* itu **cuma bisa satu hal**: dikasih peta, terus cari jalan terpendek. Dia **nggak tau** tentang aturan game, nggak tau soal emas, nggak tau soal menara. Dia cuma tau:

> *"Ini peta. Kotak-kotak ini diblokir. Cariin jalan dari A ke B. Kalau ada, kasih jalannya. Kalau nggak ada, bilang 'None'."*

**A* nggak pernah ngecek sendiri.** Dia cuma **menjawab kalau ditanya**.

### Yang "Nanya" ke A* itu Fungsi `_can_place()`

Di file `game_state.py`, ada fungsi bernama **`_can_place()`**. Fungsi ini yang bertugas jadi **satpam** — dia yang nentuin boleh atau nggak taruh menara di suatu tempat.

Bayangin kayak gini:

> 🏗️ **Pemain** = tukang bangunan yang mau taruh tembok  
> 👮 **`_can_place()`** = satpam proyek yang jaga aturan  
> 🗺️ **A\*** = arsitek yang bisa gambar jalur di peta  

Alurnya:

1. **Pemain** bilang: *"Aku mau taruh menara di sini!"*
2. **Satpam (`_can_place`)** cek dulu hal-hal dasar:
   - Sel-nya di dalam grid nggak? ❓
   - Sel-nya udah ada menara belum? ❓
   - Sel-nya bukan pintu masuk/keluar kan? ❓
3. Kalau lolos semua, satpam **belum langsung izinin**. Dia tanya ke arsitek dulu:
   - Satpam bikin **peta percobaan**: *"Kalau misalnya kotak ini ditutup..."*
   - Satpam kasih peta percobaan itu ke **A\***: *"Bro, kalau peta-nya gini, masih ada jalan nggak?"*
4. **A\*** cek peta percobaan itu dan jawab:
   - ✅ *"Masih ada jalan kok!"* → Satpam izinin, sel jadi **hijau**
   - ❌ *"Nggak ada jalan sama sekali!"* → Satpam tolak, sel jadi **merah**

### Jadi pembagian tugasnya jelas:

| Siapa | Tugasnya | File |
|-------|----------|------|
| **`_can_place()`** | Satpam — cek aturan dasar + tanya A* | `game_state.py` |
| **A\*** | Arsitek — cari jalur di peta yang dikasih | `astar.py` |
| **Pemain** | Tukang bangunan — mau taruh menara | Klik mouse |

> A* **nggak pernah bilang "boleh" atau "nggak boleh"**. Dia cuma bilang "ada jalan" atau "nggak ada jalan". Yang **memutuskan** boleh/nggak itu `_can_place()`.

---

## 🚧 Bagaimana Cara Mencegah Pemain Blokir Semua Jalan?

Oke, sekarang kamu udah tau siapa yang ngecek. Sekarang kita lihat **step-by-step** gimana pencegahannya bekerja.

### Skenario: Kamu Mau Blokir Satu-Satunya Jalan Tersisa

Bayangin kondisi grid kayak gini — cuma ada **satu jalan sempit** yang tersisa buat monster:

```
  🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
  🟩 → → → → → → → → → 🟥    ← satu-satunya jalan
  🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
```

Kamu iseng mau taruh menara **di tengah jalan itu** (sel yang ada panah →).

### Apa yang Terjadi di Balik Layar?

**Langkah 1 — Pemain klik sel**
> Kamu klik kiri di sel tengah jalan.

**Langkah 2 — Satpam (`_can_place`) cek dasar**
> *"Sel-nya di grid? ✅ Belum ada menara? ✅ Bukan pintu masuk/keluar? ✅"*
> *"Oke, cek dasar lolos. Tapi aku harus tanya arsitek dulu..."*

**Langkah 3 — Satpam bikin peta percobaan**
> Satpam **nggak langsung taruh menara**. Dia bikin **salinan peta** dan **pura-pura** taruh menara di situ:

```
  🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
  🟩 → → → → 🏰? → → → → 🟥    ← "kalau ditaruh di sini..."
  🏰 🏰 🏰 🏰 🏰 🏰 🏰 🏰
```

**Langkah 4 — Satpam tanya A\***
> *"Bro, kalau peta-nya kayak gini, masih ada jalan dari hijau ke merah nggak?"*

**Langkah 5 — A\* cek dan jawab**
> A* coba cari jalan... atas diblokir 🏰, bawah diblokir 🏰, lurus diblokir 🏰?...
> *"Nggak ada jalan sama sekali. Jawaban: **None**."*

**Langkah 6 — Satpam tolak penempatan**
> *"A* bilang nggak ada jalan. Berarti aku TOLAK!"*
> Sel langsung jadi **🟥 merah**, menara **nggak jadi ditaruh**, emas **nggak berkurang**.

### Kuncinya: Peta Percobaan (Simulasi)

Yang bikin sistem ini cerdas adalah: **nggak ada yang beneran ditaruh dulu**. Satpam bikin **peta percobaan** (simulasi), tanya A*, baru putusin. Kalau jawabannya "nggak ada jalan", semuanya dibatalin — seolah-olah nggak pernah terjadi.

Dalam kode aslinya, ini cuma **2 baris**:

```python
test_blocked = self.blocked | {(col, row)}   # peta percobaan: "kalau ditaruh..."
return astar(test_blocked, ...) is not None   # "masih ada jalan nggak?"
```

> Baris pertama = bikin peta percobaan  
> Baris kedua = tanya A*, kalau jawabannya bukan None (= ada jalan), berarti boleh

### Kalau Penempatan Diizinkan?

Nah kalau A* bilang **"masih ada jalan"**, baru deh menara beneran ditaruh. Tapi ceritanya belum selesai! Setelah menara ditaruh:

1. A* dijalankan **lagi** untuk dapetin jalur baru yang optimal
2. Jalur baru itu langsung **dikirim ke SEMUA monster** yang masih hidup
3. Semua monster **langsung belok** ngikutin jalur baru — kayak GPS yang re-route

Jadi A* dipanggil **2 kali** setiap penempatan menara:
- **Panggilan 1**: *"Masih ada jalan nggak kalau ditaruh di sini?"* (simulasi, untuk izin)
- **Panggilan 2**: *"Oke udah ditaruh. Sekarang jalan terbaiknya yang mana?"* (beneran, untuk navigasi)

---

## 🔄 Kesimpulan Super Singkat

> **A* itu kayak GPS pintar buat monster.** Dia tau arah tujuan (pakai Manhattan Distance), dia ingat sudah jalan sejauh apa, dan dia selalu pilih jalan yang **total perkiraannya paling pendek**. Kalau ada jalan baru diblokir? Langsung hitung ulang rute terbaik dalam sekejap.

> Di game kita, A* dipakai buat **dua hal**: (1) kasih jalan ke monster supaya mereka "pintar", dan (2) **dijadikan "penasehat"** oleh fungsi `_can_place()` untuk cek apakah pemain boleh taruh menara di suatu tempat atau nggak.

> Yang **memutuskan** boleh/nggak itu bukan A* — tapi **`_can_place()`** yang berperan sebagai satpam. A* cuma ditanya: *"masih ada jalan nggak?"*

---

*Analogi final:* Kalau BFS itu **lampu sorot yang nyinarin semua arah**, Dijkstra itu **lampu sorot yang sama tapi sambil bawa kalkulator**, Greedy itu **senter yang cuma ngarah ke tujuan**, maka **A* itu senter yang ngarah ke tujuan TAPI sambil bawa kalkulator DAN sesekali nengok kiri-kanan** buat mastiin nggak ada jalan yang lebih bagus. 🔦
