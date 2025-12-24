import arcade as ar
from data.savings import data
from screen import cell_center


class ElevatorDoor(ar.sprite.Sprite):
    pass


class ElevatorWall(ar.sprite.Sprite):
    pass


class ElevatorButton(ar.sprite.Sprite):
    pass


class Elevator:
    def __init__(self, scale: float, pos: int, direction: int, room: int) -> None:
        self.direction = direction
        self.room = room

    def get_type(self) -> str:
        return 'elevator'
