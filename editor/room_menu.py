import arcade as ar
import arcade.gui
from PIL.ImageWin import Window

from scroll_Area import *
from work_with_levels import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Редактор. Создание комнат"


class Room_Menu(ar.View):
    def __init__(self):
        super().__init__()
        self.manager = ar.gui.UIManager()
        self.room_list = List_of_Levels.get_rooms("Test_Level")
        self.check_rooms()

    def check_rooms(self):
        if len(self.room_list) == 0:
            self.start_add_menu()
        else:
            self.create_grid()

    def create_grid(self):
        # главный Box для всего окна
        main_layout = ar.gui.UIBoxLayout(vertical=True, space_between=10)
        # создаем кнопку обновления
        update_list_btn = ar.gui.UIFlatButton(text="Обновить", width=600)
        update_list_btn.on_click = self.on_update_click
        main_layout.add(update_list_btn)
        self.scroll_area = UIScrollArea(
            width=600,
            height=400
        )
        grid = ar.gui.UIGridLayout(
            column_count=2, row_count=len(self.room_list), horizontal_spacing=150, vertical_spacing=20
        )
        for i, name in enumerate(self.room_list):
            # делаем кнопку комнаты
            room_btn = ar.gui.UIFlatButton(text=name, width=400)
            room_btn.level_index = i
            room_btn.on_click = self.on_edit_click
            grid.add(room_btn, column=0, row=i)
        self.scroll_area.add(grid)
        main_layout.add(self.scroll_area)
        anchor_layout = self.manager.add(ar.gui.UIAnchorLayout())
        # создаем кнопку добавления
        add_btn = ar.gui.UIFlatButton(text="Добавить", width=600)
        add_btn.on_click = self.on_add_click
        main_layout.add(add_btn)
        # кнопка возврата в гл.меню
        back_to_menu_btn = ar.gui.UIFlatButton(text="В Главное меню", width=600)
        back_to_menu_btn.on_click = self.on_back_click
        main_layout.add(back_to_menu_btn)

        anchor_layout.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=main_layout
        )

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

    def on_add_click(self, event):
        pass

    def on_back_click(self, event):
        pass

    def on_update_click(self, event):
        pass

def main():
    window = ar.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    List_of_rooms = Room_Menu()
    window.show_view(List_of_rooms)
    ar.run()

if __name__ == '__main__':
    main()