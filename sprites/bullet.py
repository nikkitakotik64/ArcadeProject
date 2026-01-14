import arcade as ar
from data.savings import data
from math import sin, cos, pi


class Bullet(ar.sprite.Sprite):
    def __init__(self, x: float, y: float, bullet_speed: float, angle: float, scale: float, parent) -> None:
        super().__init__(data.FILES['bullet'], scale)
        self.speed = bullet_speed
        self.angle = angle * pi / 180
        self.center_x = x
        self.center_y = y

    def on_update(self, delta_time: float) -> None:
        self.center_x += self.speed * delta_time * cos(self.angle)
        self.center_y += self.speed * delta_time * sin(self.angle)
