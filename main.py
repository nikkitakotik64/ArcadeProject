from game.rooms_game import SingleGame as SingleRoomGame
from game.game import PvP as Arena
from data.savings import data
from level_types import LevelType
from errors import WrongLevelTypeError
from game_types import Running


def main():
    running = Running()
    # level_id = -1
    # level, level_type = data.get_level_info(level_id)
    # flag = False
    # match level_type:
        # case LevelType.rooms:
            # flag = True
            # game = SingleRoomGame(level)
            # game.run()
        # case LevelType.long_way:
            # flag = True
        # case LevelType.boss_fight:
            # flag = True
    # if not flag:
        # raise WrongLevelTypeError(f'Level type {level_type} is not supported')
    while running.is_running():
        game = Arena(running)
        game.run()


if __name__ == '__main__':
    main()
