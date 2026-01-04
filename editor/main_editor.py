import arcade as ar
import arcade.gui
from Scroll_Area import *
from work_with_levels import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Редактор. Работа с уровнями"

class Level_Menu(ar.View):
    def __init__(self):
        super().__init__()
        self.manager = ar.gui.UIManager()
        self.level_list = List_of_Levels.get_levels()
        self.create_grid()

    def create_grid(self):
        self.scroll_area = UIScrollArea(
            width=600,
            height=400
        )
        grid = ar.gui.UIGridLayout(
            column_count=2, row_count=len(self.level_list), horizontal_spacing=20, vertical_spacing=20
        )
        for i, name in enumerate(self.level_list):
            # делаем кнопку уровня
            edit_btn = ar.gui.UIFlatButton(text=name, width=400)
            edit_btn.level_index = i
            edit_btn.on_click = self.on_edit_click
            grid.add(edit_btn, column = 0, row = i)
            # делаем кнопку удаления рядом
            del_btn = ar.gui.UIFlatButton(text="del", width=50)
            del_btn.level_index = i
            del_btn.on_click = self.on_delete_click
            grid.add(del_btn, column = 1, row = i)

        anchor_layout = self.manager.add(ar.gui.UIAnchorLayout())
        self.scroll_area.add(grid)
        anchor_layout.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.scroll_area
        )


# Запускается 1 раз при создании этого окна
    def on_show_view(self):
        ar.set_background_color(ar.color.EUCALYPTUS)
        self.manager.enable()
# Когда мы сворачиваем окно, менеджер перестает работать
    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()



    def on_edit_click(self, event):
        pass

    def on_delete_click(self, event):
        pass


def main():
    window = ar.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    Level_view = Level_Menu()
    window.show_view(Level_view)
    ar.run()

if __name__ == '__main__':
    main()
