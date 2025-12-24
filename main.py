from game.rooms_game import Game as RoomGame
from data.savings import data
from level_types import LevelType
from errors import WrongLevelTypeError


def main():
    level_id = -1
    level, level_type = data.get_level_info(level_id)
    flag = False
    match level_type:
        case LevelType.ROOMS:
            flag = True
            game = RoomGame(level)
            game.run()
        case LevelType.LONG_WAY:
            flag = True
        case LevelType.BOSS_FIGHT:
            flag = True
    if not flag:
        raise WrongLevelTypeError(f'Level type {level_type} is not supported')


if __name__ == '__main__':
    main()
