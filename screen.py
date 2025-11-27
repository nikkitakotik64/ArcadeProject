import arcade as ar
from data.savings import data

W, H = ar.get_display_size()
CELL_SIDE = min(H // 27, W // 48)
WIDTH = CELL_SIDE * 48
HEIGHT = CELL_SIDE * 27
W_OUTLINE = W - WIDTH
H_OUTLINE = H - HEIGHT

# W, H - размеры окна
# CELL_SIDE - размер одной клетки
# WIDTH, HEIGHT - размер игровой зоны
# W_OUTLINE, H_OUTLINE - отступы от краёв экрана


def pos(x, y) -> tuple[int, int]:  # позиция точки на экране по игровым координатам
    return x + W_OUTLINE // 2, y + H_OUTLINE


def get_size() -> tuple[int, int]:  # размер игровой области
    return WIDTH, HEIGHT


def get_screen_size() -> tuple[int, int]:  # размер экрана
    return W, H


def cell_pos(r: int, c: int) -> tuple[int, int]:  # координаты левого верхнего угла клетки по ряду и колонке
    return c * CELL_SIDE + W_OUTLINE, r * CELL_SIDE + H_OUTLINE

def cell_center(r: int, c: int) -> tuple[int, int]:
    x, y = cell_pos(r, c)
    return x + CELL_SIDE / 2, y + CELL_SIDE / 2
