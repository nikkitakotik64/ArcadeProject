import os
import arcade as ar
import arcade.gui

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'

# TODO: предполагаю, что необходимо уничтожить класс List_of_Levels и вынести все его методы в отдельные функции. Либо переименовать класс
class List_of_Levels:
    def __init__(self):
        pass

    def get_levels(self):
        with open(levels_folder + '/system_files' + '/Level_List', "r", encoding="utf-8") as f:
            self.level_list = f.readline().strip().split(";")[:-1]
        return self.level_list

    def add_level(self, level_name):
        with open(levels_folder + '/system_files' + '/Level_List', "a", encoding="utf-8") as f:
            f.write(f"{level_name};")

        # with open(levels_folder + '/system_files' + f'/{level_name}_rooms', "w", encoding="utf-8") as f:
        #     pass

        with open(f"{levels_folder}/{level_name}.level", "w", encoding="utf-8") as f:
            line = '{"room": {"walls": [], "decor": [], "functional_objects": []}}'
            f.write(line)

    def get_rooms(self, level_name):
        with open(levels_folder + '/system_files' + f'/{level_name}_rooms', "r", encoding="utf-8") as f:
            level_list = f.readline().strip().split(";")[:-1]
        return level_list


List_of_Levels = List_of_Levels()
