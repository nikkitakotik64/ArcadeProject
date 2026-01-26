import os
import arcade as ar
import json
from editor.sub_Windows import NotificationDialog, ManagerContainer

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'


def show_notification(title, message, ui_manager=None):
    manager = ui_manager or ManagerContainer.get_manager()
    if manager:
        dialog = NotificationDialog(title=title, message=message)
        manager.add(dialog, layer=1)


# Получает список названий уровней. Используется для создания списка кнопок в меню редактора. Может быть понадобится ещё для чего-то
def get_levels():
    level_list = []
    for filename in os.listdir(levels_folder):
        if filename.endswith('.level'):
            level_name = filename[:-6]
            level_list.append(level_name)
    return level_list


#  Создает пустой файл уровня для редактора комнаты(уровня)
def add_level(level_name, ui_manager=None):
    path = os.path.join(levels_folder, f"{level_name}.level")
    if os.path.exists(path):
        show_notification(
            "Ошибка",
            "Такой уровень уже существует,"
            " придумайте другое название",
            ui_manager
        )
        return False
    try:
        with open(path, "w", encoding="utf-8") as f:
            # line = '{"room": {"walls": [], "decor": [], "functional_objects": []}}'
            # f.write(line)
            pass
        show_notification(
            "Успешно",
            f"Уровень '{level_name}' успешно создан",
            ui_manager
        )
        return True

    except Exception as e:
        show_notification(
            "Ошибка",
            f"Не удалось создать уровень: {str(e)}",
            ui_manager
        )
        return False


def delete_level(level_name, ui_manager=None):
    path = os.path.join(levels_folder, f"{level_name}.level")

    if not os.path.exists(path):
        show_notification(
            "Ошибка",
            f"Уровень '{level_name}' не найден",
            ui_manager
        )
        return False

    try:
        os.remove(path)
        show_notification(
            "Успешно",
            f"Уровень '{level_name}' успешно удален",
            ui_manager
        )
        return True

    except Exception as e:
        show_notification(
            "Ошибка",
            f"Не удалось удалить уровень: {str(e)}",
            ui_manager
        )
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


def save_room(walls, decor, level_name, ui_manager=None):
    level_data = {
        "walls": walls,
        "decor": decor,
        # "functional_objects": functional_objects
        "background": "back"
    }
    path = os.path.join(levels_folder, level_name)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(level_data, f, ensure_ascii=False, indent=2)
        show_notification(
            "Успешно!",
            "Уровень успешно сохранен",
            ui_manager
        )
        return True

    except Exception as e:
        show_notification(
            "Ошибка",
            f"При сохранении произошла ошибка: {str(e)}",
            ui_manager
        )
        return False
