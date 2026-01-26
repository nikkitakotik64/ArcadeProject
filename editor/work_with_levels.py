import os
import arcade as ar
import json

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'



# Получает список названий уровней. Используется для создания списка кнопок в меню редактора. Может быть понадобится ещё для чего-то
def get_levels():
    level_list = []
    for filename in os.listdir(levels_folder):
        if filename.endswith('.level'):
            level_name = filename[:-6]
            level_list.append(level_name)
    return level_list
#  Создает пустой файл уровня для редактора комнаты(уровня)
def add_level(level_name):
    path = os.path.join(levels_folder, f"{level_name}.level")
    with open(path, "w", encoding="utf-8") as f:
        # line = '{"room": {"walls": [], "decor": [], "functional_objects": []}}'
        # f.write(line)
        pass
def delete_level(level_name):
    path = os.path.join(levels_folder, f"{level_name}.level")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def load_level(level_name):
    path = os.path.join(levels_folder, level_name)
    if os.path.getsize(path) > 0:
        with open(path, "r", encoding="utf-8") as f:
            level_data = json.load(f)

        walls = level_data.get("walls", [])
        decor = level_data.get("decor", [])
        # functional_objects = level_data.get("functional_objects", [])
    else:
        walls = []
        decor = []
        # functional_objects = []

    return walls, decor

def save_room(walls, decor, level_name):
    level_data = {
        "walls": walls,
        "decor": decor,
        # "functional_objects": functional_objects
        "background": "back"
    }
    path = os.path.join(levels_folder, level_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(level_data, f, ensure_ascii=False, indent=2)