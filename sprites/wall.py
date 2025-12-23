import arcade as ar
from data.savings import data


class Wall(ar.sprite.Sprite):
    def __init__(self, texture_id: int, scale: float, center_x: float, center_y: float) -> None:
        texture = data.FILES[f'wall{texture_id}']
        super().__init__(texture, scale)
        self.center_x, self.center_y = center_x, center_y
