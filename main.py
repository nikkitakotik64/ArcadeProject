from game.rooms_game import SingleGame as SingleRoomGame
from data.savings import data
from level_types import LevelType
from errors import WrongLevelTypeError


def main():
    level_id = -1
    level, level_type = data.get_level_info(level_id)
    flag = False
    match level_type:
        case LevelType.rooms:
            flag = True
            game = SingleRoomGame(level)
            game.run()
        case LevelType.long_way:
            flag = True
        case LevelType.boss_fight:
            flag = True
    if not flag:
        raise WrongLevelTypeError(f'Level type {level_type} is not supported')


if __name__ == '__main__':
    main()
