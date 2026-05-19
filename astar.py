# ============================================================
#  astar.py  —  Algoritma Pencarian Jalur A*
#
#  A* (Hart, Nilsson & Raphael, 1968) adalah algoritma pencarian
#  terinformasi yang menemukan jalur terpendek antara dua node
#  dalam graf berbobot menggunakan:
#
#      f(n) = g(n) + h(n)
#
#  di mana:
#      g(n) = biaya aktual dari awal ke node n
#      h(n) = perkiraan heuristik dari n ke tujuan
#             (Jarak Manhattan untuk peta grid)
#
#  A* bersifat LENGKAP (selalu menemukan jalur jika ada)
#  dan OPTIMAL (menemukan jalur terpendek) asalkan h(n)
#  adalah *admissible* (dapat diterima) — tidak pernah melebih-lebihkan biaya sebenarnya.
#
#  Jarak Manhattan dapat diterima pada grid 4-arah
#  karena pergerakan diagonal tidak diizinkan.
#
#  Kompleksitas waktu : O(E log V)  di mana E = tepi, V = node
#  Kompleksitas ruang: O(V)        untuk himpunan open/closed
# ============================================================

import heapq


def manhattan(a: tuple, b: tuple) -> int:
    """
    Heuristik h(n): Jarak Manhattan antara dua sel grid.
    Dapat diterima karena setiap langkah berbiaya tepat 1.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(blocked: set, start: tuple, goal: tuple,
          cols: int, rows: int) -> list | None:
    """
    Mencari jalur terpendek pada grid 2D menggunakan A*.

    Parameter
    ----------
    blocked : himpunan tuple (kolom, baris) yang tidak dapat dilewati (sel menara)
    start   : (kolom, baris) — sel awal
    goal    : (kolom, baris) — sel tujuan
    cols    : lebar grid
    rows    : tinggi grid

    Kembalian
    -------
    list (kolom, baris) dari start → goal (inklusif), atau None jika tidak ada jalur.
    """
    # ── Antrean prioritas: (f_score, tie_breaker, node) ──────────
    # tie_breaker (g) memastikan urutan FIFO untuk skor f yang sama
    open_set: list = []
    heapq.heappush(open_set, (manhattan(start, goal), 0, start))

    came_from: dict  = {}          # catatan rute
    g_score:   dict  = {start: 0}  # biaya termurah yang diketahui untuk mencapai setiap node
    
    while open_set:
        _f, _g, current = heapq.heappop(open_set)

        # ── Tujuan tercapai → rekonstruksi jalur ───────────────────
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        col, row = current

        # ── Perluas tetangga (4-arah) ─────────────────
        
        for dc, dr in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nc, nr   = col + dc, row + dr
            neighbor = (nc, nr)

            # Pemeriksaan batas
            if not (0 <= nc < cols and 0 <= nr < rows):
                continue
            # Pemeriksaan dapat dilewati
            if neighbor in blocked:
                continue

            tentative_g = g_score[current] + 1   # biaya tepi seragam = 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                # Menemukan jalur yang lebih murah ke tetangga ini
                came_from[neighbor]  = current
                g_score[neighbor]    = tentative_g
                f                    = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))

    return None   # Tidak ada jalur yang ada
