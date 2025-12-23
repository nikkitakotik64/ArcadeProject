import os
import json

data_folder = os.path.dirname(__file__)
image_folder = data_folder + '/images'
levels_folder = data_folder + '/levels'
# TODO: сделать нормальное чтение и запись в файл


class Data:
    FILES = {
        'player_staying': image_folder + '/player.png',
        'player_siting': image_folder + '/sit.png',
        'player_laying': image_folder + '/lay.png',
        'wall-1': image_folder + '/wall.png',  # тестовая стена без текстуры !
        'data': data_folder + '/data.game',
        'hor_world_wall': image_folder + '/hor_world_wall.png',
        'vert_world_wall': image_folder + '/vert_world_wall.png',
    }

    LEVELS = {
        0: levels_folder + '/level0.level',
    }

    with open(data_folder + '/level_types.game', 'r') as file:
        LEVEL_TYPES = json.loads(file.read())

    def __init__(self) -> None:
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:
        return self.data_timer

    def save(self) -> None:
        pass

    def get_level_info(self, level_id: int) -> tuple[dict, int]:
        level = dict()
        # TODO: считать json !
        level_type = self.LEVEL_TYPES[str(level_id)]
        return level, int(level_type)


data = Data()
