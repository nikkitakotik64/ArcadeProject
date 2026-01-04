import os
import arcade as ar
import arcade.gui

editor_folder = os.path.dirname(__file__)
levels_folder = editor_folder + '/editor_levels'

class List_of_Levels:
    def __init__(self):
        with open(levels_folder + '/Level_List', "r", encoding="utf-8") as f:
            self.level_list = f.readline().strip().split(";")[:-1]

    def get_levels(self):
        return self.level_list



List_of_Levels = List_of_Levels()