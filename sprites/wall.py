import arcade as ar
from data.savings import data
from screen import cell_center


class Wall(ar.sprite.Sprite):
    def __init__(self, texture_id: int, scale: float, row: int, col: int) -> None:
        texture = data.FILES[f'wall{texture_id}']
        super().__init__(texture, scale)
        self.center_x, self.center_y = cell_center(row, col)
