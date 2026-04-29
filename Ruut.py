import pygame
import sys

# ── Värvid ─────────────────────────────────────────────────────────────────
COLORS = [
    (74, 222, 128), (96, 165, 250), (249, 115, 22), (244, 114, 182),
    (250, 204, 21), (167, 139, 250), (52, 211, 153), (251, 113, 133),
    (148, 163, 184), (253, 230, 138),
]
RAINBOW = [
    (248, 113, 113), (251, 146, 60), (250, 204, 21),
    (74, 222, 128),  (56, 189, 248), (129, 140, 248), (232, 121, 249),
]

PANEL_H   = 90
BG_COLOR  = (15, 15, 35)
UI_BG     = (25, 25, 50)
UI_BORDER = (60, 60, 100)
TEXT_COL  = (200, 200, 220)
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)

# ── Seadistusekraan ──────────────────────────────────────────────────────────

SETUP_W, SETUP_H = 500, 520
SETUP_BG    = (12, 12, 28)
CARD_BG     = (22, 22, 48)
CARD_BORDER = (55, 55, 95)
ACCENT      = (99, 102, 241)
ACCENT_DARK = (67, 70, 180)
MUTED       = (120, 120, 160)
INPUT_BG    = (30, 30, 60)
INPUT_FOCUS = (50, 50, 90)


class Slider:
    def __init__(self, x, y, w, min_val, max_val, val, label, suffix=""):
        self.rect   = pygame.Rect(x, y, w, 6)
        self.min_val = min_val
        self.max_val = max_val
        self.val     = val
        self.label   = label
        self.suffix  = suffix
        self.dragging = False
        self.handle_r = 10

    @property
    def handle_x(self):
        t = (self.val - self.min_val) / (self.max_val - self.min_val)
        return int(self.rect.x + t * self.rect.w)

    def handle_rect(self):
        hx = self.handle_x
        return pygame.Rect(hx - self.handle_r, self.rect.centery - self.handle_r,
                           self.handle_r * 2, self.handle_r * 2)

    def on_mouse_down(self, pos):
        if self.handle_rect().collidepoint(pos) or self.rect.inflate(0, 20).collidepoint(pos):
            self.dragging = True
            self._update(pos[0])

    def on_mouse_up(self):
        self.dragging = False

    def on_mouse_move(self, pos):
        if self.dragging:
            self._update(pos[0])

    def _update(self, mx):
        t = max(0.0, min(1.0, (mx - self.rect.x) / self.rect.w))
        self.val = round(self.min_val + t * (self.max_val - self.min_val))

    def draw(self, surf, font_sm, font_lbl):
        # Silt + väärtus
        lbl = font_lbl.render(self.label, True, MUTED)
        surf.blit(lbl, (self.rect.x, self.rect.y - 24))
        val_txt = font_sm.render(f"{self.val}{self.suffix}", True, WHITE)
        surf.blit(val_txt, (self.rect.right - val_txt.get_width(), self.rect.y - 24))
        # Riba taust
        pygame.draw.rect(surf, INPUT_BG, self.rect, border_radius=3)
        # Täidetud osa
        filled = pygame.Rect(self.rect.x, self.rect.y,
                             self.handle_x - self.rect.x, self.rect.h)
        pygame.draw.rect(surf, ACCENT, filled, border_radius=3)
        # Käepide
        hx = self.handle_x
        hy = self.rect.centery
        pygame.draw.circle(surf, ACCENT, (hx, hy), self.handle_r)
        pygame.draw.circle(surf, WHITE, (hx, hy), self.handle_r - 3)


class ColorPicker:
    """Väike värviriba joonevärvile."""
    PRESETS = [
        (180, 30, 30), (30, 120, 180), (30, 160, 80),
        (160, 100, 30), (120, 30, 160), (60, 60, 60), (200, 200, 200),
    ]

    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.selected = 0
        self.r = 11
        self.rects = []
        for i, _ in enumerate(self.PRESETS):
            self.rects.append(pygame.Rect(x + i * 30, y, self.r * 2, self.r * 2))

    @property
    def color(self):
        return self.PRESETS[self.selected]

    def on_click(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.inflate(4, 4).collidepoint(pos):
                self.selected = i

    def draw(self, surf, font_lbl):
        lbl = font_lbl.render(self.label, True, MUTED)
        surf.blit(lbl, (self.x, self.y - 22))
        for i, (rect, col) in enumerate(zip(self.rects, self.PRESETS)):
            pygame.draw.circle(surf, col, rect.center, self.r)
            if i == self.selected:
                pygame.draw.circle(surf, WHITE, rect.center, self.r + 2, 2)


def run_setup():
    pygame.init()
    screen = pygame.display.set_mode((SETUP_W, SETUP_H))
    pygame.display.set_caption("Ruudustiku Mäng — Seadistused")
    clock = pygame.time.Clock()

    font_title  = pygame.font.SysFont("segoeui", 22, bold=True)
    font_sub    = pygame.font.SysFont("segoeui", 13)
    font_btn    = pygame.font.SysFont("segoeui", 15, bold=True)
    font_lbl    = pygame.font.SysFont("segoeui", 12)
    font_sm     = pygame.font.SysFont("segoeui", 13, bold=True)

    PAD = 40

    slider_w   = SETUP_W - PAD * 2

    s_sw  = Slider(PAD, 110, slider_w, 320, 1600, 640,  "Akna laius",   " px")
    s_sh  = Slider(PAD, 180, slider_w, 240, 1000, 480,  "Akna kõrgus",  " px")
    s_cs  = Slider(PAD, 250, slider_w, 5,   80,   20,   "Ruudu suurus", " px")
    s_lw  = Slider(PAD, 320, slider_w, 0,   3,    1,    "Joone laius",  "")
    sliders = [s_sw, s_sh, s_cs, s_lw]

    cp = ColorPicker(PAD, 390, "Joone värv")

    btn_rect = pygame.Rect(PAD, 455, SETUP_W - PAD * 2, 44)
    btn_hover = False

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        btn_hover = btn_rect.collidepoint(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sl in sliders:
                    sl.on_mouse_down((mx, my))
                cp.on_click((mx, my))
                if btn_rect.collidepoint(mx, my):
                    return s_sw.val, s_sh.val, s_cs.val, cp.color, s_lw.val

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for sl in sliders:
                    sl.on_mouse_up()

            elif event.type == pygame.MOUSEMOTION:
                for sl in sliders:
                    sl.on_mouse_move((mx, my))

        # Joonistamine
        screen.fill(SETUP_BG)

        # Kaart
        card = pygame.Rect(20, 20, SETUP_W - 40, SETUP_H - 40)
        pygame.draw.rect(screen, CARD_BG, card, border_radius=16)
        pygame.draw.rect(screen, CARD_BORDER, card, 1, border_radius=16)

        # Pealkiri
        title = font_title.render("Ruudustiku Mäng", True, WHITE)
        screen.blit(title, (PAD, 44))
        sub = font_sub.render("Seadista parameetrid enne mängu alustamist", True, MUTED)
        screen.blit(sub, (PAD, 72))

        # Liugrid
        for sl in sliders:
            sl.draw(screen, font_sm, font_lbl)

        # Värvilugeja arvutus
        cols = s_sw.val // s_cs.val
        rows = (s_sh.val - PANEL_H) // s_cs.val
        info = font_sub.render(f"Ruudustik: {cols} × {rows}  ({cols * rows} lahtrit)", True, MUTED)
        screen.blit(info, (PAD, 352))

        # Värvivaija
        cp.draw(screen, font_lbl)

        # Nupp
        btn_col = ACCENT_DARK if btn_hover else ACCENT
        pygame.draw.rect(screen, btn_col, btn_rect, border_radius=10)
        btn_txt = font_btn.render("Alusta mängu  →", True, WHITE)
        screen.blit(btn_txt, btn_txt.get_rect(center=btn_rect.center))

        pygame.display.flip()


# ── Mängu funktsioonid ───────────────────────────────────────────────────────

def draw_grid(surface, grid, cell, rows, cols, line_color, line_w):
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color:
                pygame.draw.rect(surface, color,
                                 (c * cell, PANEL_H + r * cell, cell, cell))
    if line_w > 0:
        for r in range(rows + 1):
            y = PANEL_H + r * cell
            pygame.draw.line(surface, line_color, (0, y), (cols * cell, y), line_w)
        for c in range(cols + 1):
            x = c * cell
            pygame.draw.line(surface, line_color, (x, PANEL_H),
                             (x, PANEL_H + rows * cell), line_w)


def flood_fill(grid, r, c, target, replacement, rows, cols):
    if target == replacement:
        return
    stack = [(r, c)]
    while stack:
        rr, cc = stack.pop()
        if rr < 0 or rr >= rows or cc < 0 or cc >= cols:
            continue
        if grid[rr][cc] != target:
            continue
        grid[rr][cc] = replacement
        stack += [(rr-1,cc),(rr+1,cc),(rr,cc-1),(rr,cc+1)]


def paint_cell(grid, r, c, mode, color, rainbow_idx, rows, cols):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return rainbow_idx
    if mode == "erase":
        grid[r][c] = None
    elif mode == "fill":
        flood_fill(grid, r, c, grid[r][c], color, rows, cols)
    elif mode == "rainbow":
        grid[r][c] = RAINBOW[rainbow_idx % len(RAINBOW)]
        rainbow_idx += 1
    else:
        grid[r][c] = color
    return rainbow_idx


def get_cell(mx, my, cell):
    if my < PANEL_H:
        return -1, -1
    return (my - PANEL_H) // cell, mx // cell


def pct(grid, rows, cols):
    filled = sum(1 for r in range(rows) for c in range(cols) if grid[r][c])
    total  = rows * cols
    return filled, total, int(filled / total * 100) if total else 0


# ── Peamäng ──────────────────────────────────────────────────────────────────

def main(screen_w, screen_h, cell_size, line_color, line_w):
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Ruudustiku Mäng")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("segoeui", 15)
    small = pygame.font.SysFont("segoeui", 12)

    cols = screen_w // cell_size
    rows = (screen_h - PANEL_H) // cell_size
    grid = [[None] * cols for _ in range(rows)]

    cur_color   = COLORS[0]
    mode        = "paint"
    rainbow_idx = 0
    is_drawing  = False

    MODES       = ["paint", "erase", "fill", "rainbow"]
    MODE_LABELS = ["✏ Joonista", "⌫ Kustuta", "🪣 Täida", "🌈 Vikerkaar"]

    COLOR_R = 12
    color_rects = [pygame.Rect(10 + i * 30, 8, COLOR_R*2, COLOR_R*2)
                   for i in range(len(COLORS))]

    mode_rects = [pygame.Rect(10 + i * 115, 36, 108, 24)
                  for i in range(len(MODES))]

    CLEAR_RECT = pygame.Rect(screen_w - 90, 8,  80, 24)
    SAVE_RECT  = pygame.Rect(screen_w - 90, 36, 80, 24)

    toast_msg   = ""
    toast_timer = 0

    def show_toast(msg):
        nonlocal toast_msg, toast_timer
        toast_msg   = msg
        toast_timer = 120

    def draw_ui():
        pygame.draw.rect(screen, UI_BG, (0, 0, screen_w, PANEL_H))
        pygame.draw.line(screen, UI_BORDER, (0, PANEL_H), (screen_w, PANEL_H), 1)

        for i, (rect, col) in enumerate(zip(color_rects, COLORS)):
            pygame.draw.circle(screen, col, rect.center, COLOR_R)
            if col == cur_color:
                pygame.draw.circle(screen, WHITE, rect.center, COLOR_R + 2, 2)

        for i, (rect, label) in enumerate(zip(mode_rects, MODE_LABELS)):
            active = MODES[i] == mode
            bg = (80, 80, 160) if active else (40, 40, 80)
            pygame.draw.rect(screen, bg, rect, border_radius=6)
            pygame.draw.rect(screen, UI_BORDER, rect, 1, border_radius=6)
            txt = small.render(label, True, WHITE if active else TEXT_COL)
            screen.blit(txt, txt.get_rect(center=rect.center))

        pygame.draw.rect(screen, (60, 20, 20), CLEAR_RECT, border_radius=6)
        pygame.draw.rect(screen, UI_BORDER, CLEAR_RECT, 1, border_radius=6)
        ct = small.render("✕ Tühjenda", True, (255, 120, 120))
        screen.blit(ct, ct.get_rect(center=CLEAR_RECT.center))

        pygame.draw.rect(screen, (20, 60, 40), SAVE_RECT, border_radius=6)
        pygame.draw.rect(screen, UI_BORDER, SAVE_RECT, 1, border_radius=6)
        st = small.render("💾 Salvesta", True, (120, 255, 160))
        screen.blit(st, st.get_rect(center=SAVE_RECT.center))

        filled, total, p = pct(grid, rows, cols)
        info = font.render(f"Värvitud: {filled}/{total}  ({p}%)", True, TEXT_COL)
        screen.blit(info, (10, 68))

    def save_screenshot():
        fname = "ruudustik_pilt.png"
        pygame.image.save(screen, fname)
        show_toast(f"Salvestatud: {fname}")

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_c:
                    grid[:] = [[None]*cols for _ in range(rows)]
                    show_toast("Lõuend tühjendatud!")
                elif event.key == pygame.K_s:
                    save_screenshot()
                elif event.key == pygame.K_1: mode = "paint"
                elif event.key == pygame.K_2: mode = "erase"
                elif event.key == pygame.K_3: mode = "fill"
                elif event.key == pygame.K_4: mode = "rainbow"
                elif event.key == pygame.K_RIGHT:
                    idx = COLORS.index(cur_color)
                    cur_color = COLORS[(idx + 1) % len(COLORS)]
                elif event.key == pygame.K_LEFT:
                    idx = COLORS.index(cur_color)
                    cur_color = COLORS[(idx - 1) % len(COLORS)]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect, col in zip(color_rects, COLORS):
                        if rect.collidepoint(mx, my):
                            cur_color = col; mode = "paint"; break
                    for i, rect in enumerate(mode_rects):
                        if rect.collidepoint(mx, my):
                            mode = MODES[i]; break
                    if CLEAR_RECT.collidepoint(mx, my):
                        grid[:] = [[None]*cols for _ in range(rows)]
                        show_toast("Lõuend tühjendatud!")
                    elif SAVE_RECT.collidepoint(mx, my):
                        save_screenshot()
                    elif my >= PANEL_H:
                        r, c = get_cell(mx, my, cell_size)
                        rainbow_idx = paint_cell(grid, r, c, mode, cur_color,
                                                  rainbow_idx, rows, cols)
                        is_drawing = True
                elif event.button == 3:
                    if my >= PANEL_H:
                        r, c = get_cell(mx, my, cell_size)
                        if 0 <= r < rows and 0 <= c < cols:
                            grid[r][c] = None

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    is_drawing = False

            elif event.type == pygame.MOUSEMOTION:
                if is_drawing and my >= PANEL_H:
                    r, c = get_cell(mx, my, cell_size)
                    rainbow_idx = paint_cell(grid, r, c, mode, cur_color,
                                              rainbow_idx, rows, cols)

        screen.fill(BG_COLOR)
        draw_grid(screen, grid, cell_size, rows, cols, line_color, line_w)
        draw_ui()

        if toast_timer > 0:
            toast_timer -= 1
            surf = font.render(toast_msg, True, WHITE)
            bg   = pygame.Surface((surf.get_width() + 20, surf.get_height() + 10),
                                   pygame.SRCALPHA)
            bg.fill((0, 0, 0, 160))
            screen.blit(bg,   bg.get_rect(center=(screen_w//2, PANEL_H + 20)))
            screen.blit(surf, surf.get_rect(center=(screen_w//2, PANEL_H + 20)))

        hint = small.render(
            "1-Joonista  2-Kustuta  3-Täida  4-Vikerkaar  ←→ värvid  "
            "S-salvesta  C-tühjenda  ESC-sulge", True, (80, 80, 120))
        screen.blit(hint, (4, screen_h - 16))

        pygame.display.flip()


# ── Käivitamine ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pygame.init()
    sw, sh, cs, lc, lw = run_setup()
    main(sw, sh, cs, lc, lw)