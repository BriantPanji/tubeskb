# ============================================================
#  main.py  —  Titik masuk & Loop Permainan
#
#  Jalankan:  python main.py
#
#  Kontrol
#  ─────────
#  Klik-kiri           → Tempatkan menara yang dipilih  /  Jatuhkan menara yang ditahan
#  Klik-kanan menara   → Ambil menara untuk direlokasi
#  ESC (saat pindah)   → Batalkan pindah, kembalikan menara ke asal
#  ESC (normal)        → Keluar
#  P                   → Jeda / Lanjutkan
#  1 / 2 / 3 / 4       → Pilih tipe menara
#  H                   → Beralih sorotan jalur
#  R                   → Mulai ulang permainan
# ============================================================

import sys
import pygame

from config      import SCREEN_W, SCREEN_H, FPS, TITLE, COLS, ROWS, CELL_SIZE, TOWER_ORDER
from game_state  import GameState
from renderer    import draw_all, init_fonts, get_tower_button_rects

GAME_W = COLS * CELL_SIZE


def pixel_to_cell(mx: int, my: int) -> tuple | None:
    """Ubah koordinat piksel mouse ke grid (kolom, baris), atau None."""
    if mx >= GAME_W or my < 0 or my >= ROWS * CELL_SIZE:
        return None
    col = mx // CELL_SIZE
    row = my // CELL_SIZE
    if 0 <= col < COLS and 0 <= row < ROWS:
        return col, row
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()

    init_fonts()

    gs = GameState()

    show_path = True      # beralih dengan H

    # ── Loop Utama ──────────────────────────────────────────────
    while True:
        dt = clock.tick(FPS) / 1000.0   # delta-time dalam detik

        # ── Penanganan kejadian ─────────────────────────────────────
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── Papan ketik ───────────────────────────────────────
            if event.type == pygame.KEYDOWN:

                # ESC: batalkan perpindahan dulu; jika tidak ada yang dibatalkan → keluar
                if event.key == pygame.K_ESCAPE:
                    if gs.moving_tower is not None:
                        gs.cancel_move()
                    else:
                        pygame.quit()
                        sys.exit()

                # P: jeda / lanjutkan
                if event.key == pygame.K_p:
                    gs.toggle_pause()

                if event.key == pygame.K_r:
                    gs = GameState()

                if event.key == pygame.K_h:
                    show_path = not show_path

                # Pemilihan menara: 1-4 (hanya saat tidak memindahkan menara)
                key_map = {
                    pygame.K_1: 'basic',
                    pygame.K_2: 'sniper',
                    pygame.K_3: 'rapid',
                    pygame.K_4: 'bomb',
                }
                if event.key in key_map and gs.moving_tower is None:
                    gs.selected_type = key_map[event.key]

            # ── Klik kiri mouse ───────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Periksa tombol tipe menara sidebar (hanya dalam mode normal)
                btn_rects   = get_tower_button_rects()
                clicked_btn = False
                if gs.moving_tower is None:
                    for i, rect in enumerate(btn_rects):
                        if rect.collidepoint(mx, my):
                            gs.selected_type = TOWER_ORDER[i]
                            clicked_btn = True
                            break

                if not clicked_btn and not gs.game_over and not gs.victory:
                    cell = pixel_to_cell(mx, my)
                    if cell:
                        if gs.moving_tower is not None:
                            # JATUHKAN menara yang ditahan ke sel ini
                            gs.drop_tower(cell[0], cell[1])
                        else:
                            # TEMPATKAN menara baru (mode normal)
                            gs.try_place_tower(cell[0], cell[1])

            # ── Klik kanan mouse → ambil menara ─────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not gs.game_over and not gs.victory:
                    mx, my = event.pos
                    cell = pixel_to_cell(mx, my)
                    if cell:
                        gs.pick_up_tower(cell[0], cell[1])

        # ── Mouse mengarah (setiap frame) ──────────────────────────
        mx, my = pygame.mouse.get_pos()
        cell = pixel_to_cell(mx, my)
        if cell and not gs.game_over and not gs.victory:
            gs.set_hover(cell[0], cell[1])
        else:
            gs.clear_hover()

        # ── Pembaruan logika permainan ──────────────────────────────────
        gs.update(dt)

        # ── Gambar ───────────────────────────────────────────────
        draw_all(screen, gs, show_path)
        pygame.display.flip()


if __name__ == '__main__':
    main()
