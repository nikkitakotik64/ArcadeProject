from sprites.wall import Wall
from game.game import Game as AbstractGame


class Game(AbstractGame):
    def __init__(self, level: dict) -> None:
        super().__init__()
        self.level = level

        self.room = 0
        for wall in level['rooms'][str(self.room)]['walls']:
            row, col, texture_id = wall['row'], wall['col'], wall['texture_id']
            self.wall_list.append(Wall(texture_id, self.k / 8, row, col))
        for wall in self.world_walls:
            self.wall_list.append(wall)
