from sprites.wall import Wall
from screen import cell_center
from game.game import Game as AbstractGame
import arcade as ar
from sprites.sign import Sign
from sprites.elevator import Elevator
from game_types import FunctionalObjectsTypes, Direction
from sprites.enemy import Enemy, EnemyType, EnemyTypeCodes, EnemyDirectionCodes
from errors import WrongEnemyTypeCodeError, WrongEnemyDirectionCodeError
from sprites.weapons import StartWeapon


class SingleGame(AbstractGame):
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
                case FunctionalObjectsTypes.sign:
                    self.functional_objects.append(Sign(self.k, row, col, add['text']))
                case FunctionalObjectsTypes.staying_enemy:
                    x, y = cell_center(row, col)
                    match add['type']:
                        case EnemyTypeCodes.laying:
                            tp = EnemyType.laying
                        case EnemyTypeCodes.siting:
                            tp = EnemyType.siting
                        case EnemyTypeCodes.staying:
                            tp = EnemyType.staying
                        case _:
                            raise WrongEnemyTypeCodeError(f'Incorrect enemy type code: {add['type']}')
                    match add['direction']:
                        case EnemyDirectionCodes.right:
                            dr = Direction.right
                        case EnemyDirectionCodes.left:
                            dr = Direction.left
                        case _:
                            raise WrongEnemyDirectionCodeError(f'Incorrect enemy direction code: {add["direction"]}')
                    self.enemies.append(Enemy(x, y, tp, dr))

        # TODO: delete
        self.enemies.append(Enemy(*cell_center(10, 5),
                                  EnemyType.staying, StartWeapon(), self.k / 6, Direction.right))
        self.enemies.append(Enemy(*cell_center(10, 8),
                                  EnemyType.staying, StartWeapon(), self.k / 6, Direction.right))
        self.enemies.append(Enemy(*cell_center(10, 11),
                                  EnemyType.staying, StartWeapon(), self.k / 6, Direction.right))
        self.enemies.append(Enemy(*cell_center(10, 14),
                                  EnemyType.staying, StartWeapon(), self.k / 6, Direction.right))

        for elev in level['rooms'][str(self.room)]['elevators']:
            pos, direction, room = elev['pos'], elev['direction'], elev['room']
            elevator = Elevator(self.k, pos, direction, room, level['background'])
            self.elevators.append(elevator)

        for elevator in self.elevators:
            for wall in elevator.get_walls():
                self.wall_list.append(wall)
            # TODO: add this code later (do textures)
            # self.functional_objects.append(elevator.get_button())
            # self.decor.append(elevator.get_mine())

        for wall in self.world_walls:
            self.wall_list.append(wall)

        self.update_player_sprite()
        self.update_enemies()

    def on_key_press(self, key: int, modifiers: int) -> None:
        super().on_key_press(key, modifiers)
        if key == ar.key.E:
            pass