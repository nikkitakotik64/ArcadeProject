import arcade as ar
from data.savings import data
from math import sin, cos, pi
from screen import CELL_SIDE
from sprites.weapons import BulletCharacteristics


class Bullet(ar.sprite.Sprite):
    def __init__(self, x: float, y: float, characteristics: BulletCharacteristics,
                 angle: float, scale: float, exceptions: list[ar.sprite.Sprite]) -> None:
        super().__init__(data.FILES['bullet'], scale)
        self.speed = characteristics.get_bullet_speed()
        self.range = characteristics.get_normal_range()
        self.damage = characteristics.get_damage()
        self.armor_piercing = characteristics.get_armor_piercing()
        self.angle = angle * pi / 180
        self.center_x = x
        self.center_y = y
        self.exceptions = exceptions
        self.current_range = 0

    def on_update(self, delta_time: float) -> None:
        self.center_x += self.speed * delta_time * cos(self.angle)
        self.center_y += self.speed * delta_time * sin(self.angle)
        self.current_range += self.speed * delta_time

    def get_damage(self) -> float:
        damage = self.damage
        if self.current_range > self.range:
            damage -= (self.current_range - self.range) / CELL_SIDE / 3
        damage = max(0, damage)
        return damage

    def pierce(self, target: ar.sprite.Sprite) -> None:
        self.damage *= self.armor_piercing / 100
        self.exceptions.append(target)

    def get_exceptions(self) -> list[ar.sprite.Sprite]:
        return self.exceptions
