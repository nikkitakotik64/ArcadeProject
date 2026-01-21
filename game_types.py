from enum import Enum


class Direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4


class FunctionalObjectsTypes:
    pass


class Running:
    def __init__(self) -> None:
        self.running = True

    def set_false(self) -> None:
        self.running = False

    def set_true(self) -> None:
        self.running = True

    def is_running(self) -> bool:
        return self.running
