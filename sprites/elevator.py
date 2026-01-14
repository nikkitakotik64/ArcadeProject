import arcade as ar
from data.savings import data
from screen import cell_center
from consts import ELEVATOR_DOORS_SPEED
from enum import Enum


class ElevatorDoorStatus(Enum):
    OPENED = 0
    CLOSED = 1
    OPENING = 2
    CLOSING = 3


class ElevatorDoor(ar.sprite.Sprite):
    def __init__(self, texture_id: int, scale: float, col0: int,
                 row: int, col: int) -> None:
        texture = data.FILES[f'elevator_wall{texture_id}']
        super().__init__(texture, scale)
        self.pos = cell_center(row, col)[1]
        self.center_x, self.center_y = cell_center(row, col0)
        self.start_pos = self.center_y
        self.status = ElevatorDoorStatus.OPENED
        self.direction = False if self.pos > self.center_y else True
        self.block = ElevatorBlock(self.scale, self.row, self.col0)

    def close(self) -> None:
        self.status = ElevatorDoorStatus.CLOSING
        self.block.move(self.center_x, self.pos)

    def on_update(self, delta_time: float) -> None:
        if self.status == ElevatorDoorStatus.CLOSING:
            if self.direction:
                self.center_y = max(self.pos, self.center_y - delta_time * ELEVATOR_DOORS_SPEED)
                if self.center_y == self.pos:
                    self.status = ElevatorDoorStatus.CLOSED
            else:
                self.center_y = min(self.pos, self.center_y + delta_time * ELEVATOR_DOORS_SPEED)
                if self.center_y == self.pos:
                    self.status = ElevatorDoorStatus.CLOSED
        elif self.status == ElevatorDoorStatus.OPENING:
            if self.direction:
                self.center_y = min(self.start_pos, self.center_y + delta_time * ELEVATOR_DOORS_SPEED)
                if self.center_y == self.start_pos:
                    self.status = ElevatorDoorStatus.OPENED
            else:
                self.center_y = max(self.start_pos, self.center_y - delta_time * ELEVATOR_DOORS_SPEED)
                if self.center_y == self.start_pos:
                    self.status = ElevatorDoorStatus.OPENED
            self.block.move(self.center_x, self.center_y)

    def open(self) -> None:
        self.status = ElevatorDoorStatus.OPENING

    def get_block(self) -> ar.sprite.Sprite:
        return self.block


class ElevatorBlock(ar.sprite.Sprite):
    def __init__(self, scale: float, row: int, col: int) -> None:
        texture = data.FILES['invisible_wall']
        super().__init__(texture, scale)
        self.center_x, self.center_y = cell_center(row, col)

    def move(self, x: float, y: float) -> None:
        self.center_x, self.center_y = x, y


class ElevatorButton(ar.sprite.Sprite):
    def __init__(self, texture_id: int, scale: float, row: int, col: int, elevator: Elevator) -> None:
        texture = data.FILES[f'elevator_button{texture_id}']
        super().__init__(texture, scale)
        self.center_x, self.center_y = cell_center(row, col)
        self.elevator = elevator

    def get_elevator(self) -> Elevator:
        return self.elevator

    def get_type(self) -> str:
        return 'elevator_button'


class ElevatorMine(ar.sprite.Sprite):
    def __init__(self, texture_id: int, scale: float, row: int, col: int) -> None:
        texture = data.FILES[f'elevator_mine{texture_id}']
        super().__init__(texture, scale)
        self.center_x, self.center_y = cell_center(row, col)


class Elevator:
    def __init__(self, scale: float, pos: int, direction: int, room: int, background: int) -> None:
        self.direction = direction
        self.room = room
        self.walls = []
        self.doors = []
        self.mine = ElevatorMine(-1, -1, -1, -1)  # TODO
        self.button = ElevatorButton(-1, -1, -1, -1, self)  # TODO

    def get_walls(self) -> list[ar.sprite.Sprite]:
        walls = []
        for wall in self.walls:
            wall.append(wall)
        for door in self.doors:
            for wall in door.get_block():
                walls.append(wall)
        return walls

    def get_mine(self) -> ar.sprite.Sprite:
        return self.mine

    def get_button(self) -> ar.sprite.Sprite:
        return self.button
