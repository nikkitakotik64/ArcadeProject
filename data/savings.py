import os
import json

data_folder = os.path.dirname(__file__)
image_folder = data_folder + '/images'
levels_folder = data_folder + '/levels'
file_folder = data_folder + '/files'


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
        'sound_settings': file_folder + '/sounds_settings.txt',
        'same_button_disabled': image_folder + '/same_button_disabled.png',
        'same_button_enabled': image_folder + '/same_button_enabled.png',
        'random_button_disabled': image_folder + '/random_button_disabled.png',
        'random_button_enabled': image_folder + '/random_button_enabled.png',
        'player_button': image_folder + '/player_button.png',
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

    def get_level_info(self, level_id: int):
        with open(self.LEVELS[level_id], 'r') as file:
            level = json.loads(file.read())
            return level

    def get_sound_settings(self) -> bool:
        try:
            with open(self.FILES['sound_settings'], 'r') as file:
                if file.readline() == '1':
                    return True
                return False
        except FileNotFoundError:
            return True

    def save_sound_settings(self, value: bool) -> None:
        with open(self.FILES['sound_settings'], 'w') as file:
            if value:
                file.write('1')
            else:
                file.write('0')


data = Data()
