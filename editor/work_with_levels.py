import os
import arcade as ar
import arcade.gui

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'

class List_of_Levels:
    def __init__(self):
        pass

    def get_levels(self):
        with open(levels_folder + '/Level_List', "r", encoding="utf-8") as f:
            self.level_list = f.readline().strip().split(";")[:-1]
        return self.level_list

    def add_level(self, level_name):
        with open(levels_folder + '/Level_List', "a", encoding="utf-8") as f:
            f.write(f"{level_name};")
        with open(f"{levels_folder}/{level_name}.level", "w", encoding="utf-8") as f:
            pass



List_of_Levels = List_of_Levels()