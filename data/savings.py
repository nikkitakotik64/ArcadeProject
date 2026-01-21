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
        'bullet': image_folder + '/bullet.png',
        'start_button': image_folder + '/start_button.png',
        'editor_button': image_folder + '/editor_button.png',
        'quit_button': image_folder + '/quit_button.png',
        'sound_button_enabled': image_folder + '/sound_button_enabled.png',
        'sound_button_disabled': image_folder + '/sound_button_disabled.png',
    }

    LEVELS = {
        -1: levels_folder + '/test.level',
    }

    def __init__(self) -> None:
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:
        return self.data_timer

    def save(self) -> None:
        pass

    def get_level_info(self, level_id: int) -> tuple[dict, LevelType]:
        with open(self.LEVELS[level_id], 'r') as file:
            level = json.loads(file.read())
        level_type = LevelType(level['type'])
        return level, level_type

    def get_sound_settings(self) -> bool:
        return True


data = Data()
