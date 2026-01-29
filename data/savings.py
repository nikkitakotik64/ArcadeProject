import os
import json
from editor.work_with_levels import levels_folder as editor_levels_folder

data_folder = os.path.dirname(__file__)
image_folder = data_folder + '/images'
levels_folder = data_folder + '/levels'
file_folder = data_folder + '/files'
sounds_folder = data_folder + '/sounds'


class Data:
    FILES = {
        'player_staying': image_folder + '/player.png',
        'player_siting': image_folder + '/sit.png',
        'player_laying': image_folder + '/lay.png',
        'wall-1': image_folder + '/wall.png',  # тестовая стена без текстуры, станет кирпичной!
        'wall-2': image_folder + '/wall2.png', # будет металлическая(если будет)
        'torch': image_folder + '/torch.png',
        'tree': image_folder + '/tree.png',
        'vase': image_folder + '/vase.png',
        'door': image_folder + '/door.png',
        'chest': image_folder + '/chest.png',
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
        'random_button_all': image_folder + '/random_button_all.png',
        'random_button_editor': image_folder + '/random_button_editor.png',
        'random_button_standard': image_folder + '/random_button_standard.png',
        'player_button': image_folder + '/player_button.png',
        'shotgun_bullet': image_folder + '/shotgun_bullet.png',
        'label': image_folder + '/label.png',
        'continue_button': image_folder + '/continue_button.png',
        'back_button': image_folder + '/back_button.png',
        'sound_button_game_enabled': image_folder + '/sound_button_game_enabled.png',
        'sound_button_game_disabled': image_folder + '/sound_button_game_disabled.png',
        'change_weapon_button': image_folder + '/change_weapon_button.png',
        'restart_button': image_folder + '/restart_button.png',
        'level_button': image_folder + '/level_button.png',
        'creator_button': image_folder + '/creator_button.png',
        'paradigm_button': image_folder + '/paradigm_button.png',
        'battle_button': image_folder + '/battle_button.png',
    }

    LEVELS = {
        'Battle Of Everything': levels_folder + '/Battle Of Everything',
        'Paradigm': levels_folder + '/Paradigm',
        'Creator': levels_folder + '/Creator',
    }

    SOUNDS = {
        'glock-18': sounds_folder + '/glock-18.mp3',
        'p250': sounds_folder + '/p250.mp3',
        'USP-S': sounds_folder + '/usp-s.mp3',
        'Dual Berrettas': sounds_folder + '/dual_berrettas.mp3',
        'Revolver R8': sounds_folder + '/revolver.mp3',
        'Desert Eagle': sounds_folder + '/deagle.mp3',
        'MP5': sounds_folder + '/mp5.mp3',
        'MP7': sounds_folder + '/mp7.mp3',
        'MP9': sounds_folder + '/mp9.mp3',
        'UZI': sounds_folder + '/uzi.mp3',
        'P90': sounds_folder + '/p90.mp3',
        'M249': sounds_folder + '/m249.mp3',
        'XM1014': sounds_folder + '/xm1014.mp3',
        'MAG-7': sounds_folder + '/mag7.mp3',
        'M4A4': sounds_folder + '/m4a4.mp3',
        'SCAR20': sounds_folder + '/scar20.mp3',
        'FAMAS': sounds_folder + '/famas.mp3',
        'AUG': sounds_folder + '/aug.mp3',
        'SSG-08': sounds_folder + '/ssg08.mp3',
        'AWP': sounds_folder + '/awp.mp3',
        'SVD': sounds_folder + '/svd.mp3',
        'AK47': sounds_folder + '/ak47.mp3',
    }

    def __init__(self) -> None:
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:
        return self.data_timer

    def save(self) -> None:
        pass

    @staticmethod
    def check_level(level: str) -> bool:
        try:
            with open(level) as file:
                js = json.loads(file.read())
            walls, decor, _ = js['walls'], js['decor'], js['background']
            for wall in walls:
                _ = wall['row'], wall['col'], wall['texture']
            for dec in decor:
                _ = dec['row'], dec['col'], dec['texture']
            return True
        except:
            return False

    @staticmethod
    def load_level(level: str):
        with open(level + '.level') as file:
            js = json.loads(file.read())
            return js

    def get_levels_list(self) -> list[str]:
        files = os.listdir(editor_levels_folder)
        levels = list()
        for name in files:
            if name.endswith('.level') and self.check_level(name):
                levels.append(name)
        return levels

    def check_levels(self, levels: list[str]) -> list[str]:
        new_levels = list()
        for level in levels:
            if self.check_level(level):
                new_levels.append(level)
        return new_levels

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
