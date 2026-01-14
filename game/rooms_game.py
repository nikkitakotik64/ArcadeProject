from sprites.wall import Wall
from game.game import Game as AbstractGame
import arcade as ar
from sprites.sign import Sign
from sprites.elevator import Elevator


class Game(AbstractGame):
    def __init__(self, level: dict) -> None:
        super().__init__()
        self.level = level
        self.room = 0
        self.elevators = []
        self.memory = dict()

        for wall in level['rooms'][str(self.room)]['walls']:
            row, col, texture_id = wall['row'], wall['col'], wall['texture_id']
            self.wall_list.append(Wall(texture_id, self.k / 8, row, col))

        for obj in level['rooms'][str(self.room)]['functional_objects']:
            row, col, obj_type, add = obj['row'], obj['col'], obj['type'], obj['additionally']
            match obj_type:
                case 1:
                    self.func_objects.append(Sign(self.k, row, col, add['text']))

        for elev in level['rooms'][str(self.room)]['elevators']:
            pos, direction, room = elev['pos'], elev['direction'], elev['room']
            elevator = Elevator(self.k, pos, direction, room, level['background'])
            self.elevators.append(elevator)

        for elevator in self.elevators:
            for wall in elevator.get_walls():
                self.wall_list.append(wall)
            self.functional_objects.append(elevator.get_button())
            self.decor.append(elevator.get_mine())

        for wall in self.world_walls:
            self.wall_list.append(wall)

        self.update_player_sprite()

    def on_key_press(self, key: int, modifiers: int) -> None:
        super().on_key_press(key, modifiers)
        if key == ar.key.E:
            pass