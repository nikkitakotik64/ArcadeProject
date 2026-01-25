import os
import arcade as ar
import json

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'



# Получает список названий уровней. Используется для создания списка кнопок в меню редактора. Может быть понадобится ещё для чего-то
def get_levels():
    with open(levels_folder + '/system_files' + '/Level_List', "r", encoding="utf-8") as f:
        level_list = f.readline().strip().split(";")[:-1]
    return level_list
# Добавляет в список названий уровней название нового уровня. Создает пустой файл уровня для редактора комнаты(уровня)
def add_level(level_name):
    with open(levels_folder + '/system_files' + '/Level_List', "a", encoding="utf-8") as f:
        f.write(f"{level_name};")

    with open(f"{levels_folder}/{level_name}.level", "w", encoding="utf-8") as f:
        # line = '{"room": {"walls": [], "decor": [], "functional_objects": []}}'
        # f.write(line)
        pass

# def get_rooms(level_name):
#     with open(levels_folder + '/system_files' + f'/{level_name}_rooms', "r", encoding="utf-8") as f:
#         level_list = f.readline().strip().split(";")[:-1]
#     return level_list

def load_level(level_name):
    path = levels_folder + level_name
    if os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        walls = level_data.get("walls", [])
        decor = level_data.get("decor", [])
        functional_objects = level_data.get("functional_objects", [])
    else:
        walls = []
        decor = []
        functional_objects = []

    return walls, decor, functional_objects

