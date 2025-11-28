import arcade as ar
from data.savings import data

W, H = ar.get_display_size()
CELL_H, CELL_W = 27, 48
CELL_SIDE = min(H // CELL_H, W // CELL_W)
WIDTH = CELL_SIDE * CELL_W
HEIGHT = CELL_SIDE * CELL_H
W_OUTLINE = W - WIDTH
H_OUTLINE = H - HEIGHT

# W, H - размеры окна
# CELL_SIDE - размер одной клетки
# WIDTH, HEIGHT - размер игровой зоны
# W_OUTLINE, H_OUTLINE - отступы от краёв экрана


def pos(x, y) -> tuple[float, float]:  # позиция точки на экране по игровым координатам
    return x + W_OUTLINE // 2, y + H_OUTLINE


def get_size() -> tuple[float, float]:  # размер игровой области
    return WIDTH, HEIGHT


def get_screen_size() -> tuple[float, float]:  # размер экрана
    return W, H


def cell_pos(r: int, c: int) -> tuple[float, float]:  # координаты левого верхнего угла клетки по ряду и колонке
    return c * CELL_SIDE + W_OUTLINE, (CELL_H - r - 1) * CELL_SIDE + H_OUTLINE

def cell_center(r: int, c: int) -> tuple[float, float]:  # центр клетки
    x, y = cell_pos(r, c)
    y = CELL_H - y - 1
    return x + CELL_SIDE / 2, y + CELL_SIDE / 2
