import arcade as ar

W, H = ar.get_display_size()
CELL_H, CELL_W = 27, 48
CELL_SIDE = min(H / CELL_H, W / CELL_W)
WIDTH = CELL_SIDE * CELL_W
HEIGHT = CELL_SIDE * CELL_H
W_OUTLINE = W - WIDTH
H_OUTLINE = H - HEIGHT
W_OUTLINE /= 2
H_OUTLINE /= 2

# W, H - размеры окна
# CELL_SIDE - размер одной клетки
# WIDTH, HEIGHT - размер игровой зоны
# W_OUTLINE, H_OUTLINE - отступы от краёв экрана


def pos(x, y) -> tuple[float, float]:
    return x + W_OUTLINE // 2, y + H_OUTLINE


def get_size() -> tuple[float, float]:
    return WIDTH, HEIGHT


def get_screen_size() -> tuple[float, float]:
    return W, H


def cell_pos(r: int, c: int) -> tuple[float, float]:
    return c * CELL_SIDE + W_OUTLINE, (CELL_H - r - 1) * CELL_SIDE + H_OUTLINE

def cell_center(r: int, c: int) -> tuple[float, float]:
    x, y = cell_pos(CELL_H - r - 1, c)
    return x + CELL_SIDE / 2, y + CELL_SIDE / 2
