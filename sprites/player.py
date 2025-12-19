from enum import Enum
import arcade as ar
from screen import cell_center


class PlayerStatus(Enum):
    NORMAL = 0
    JUMPING = 1
    FALLING = 2


class Player:
    def __init__(self, texture: str, scale: float, row: int, col: int) -> None:
        self.status = PlayerStatus.NORMAL
        self.sprite = ar.sprite.Sprite(texture, scale)
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)

    def move(self, row: int, col: int) -> None:
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)

    def set_status(self, status: PlayerStatus) -> None:
        self.status = status

    def get_status(self) -> PlayerStatus:
        return self.status

    def get_sprite(self) -> ar.sprite.Sprite:
        return self.sprite
