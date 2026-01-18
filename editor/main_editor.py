import arcade as ar
import arcade.gui
from Scroll_Area import *
from work_with_levels import *
from Sub_Windows import AddLevelDialog

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Редактор. Работа с уровнями"

# TODO: доделать функционал доп окна и функций, исправить баги
class Level_Menu(ar.View):
    def __init__(self):
        super().__init__()
        self.manager = ar.gui.UIManager()
        self.level_list = List_of_Levels.get_levels()
        self.create_grid()
        self.dialog_open = False

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
            column_count=2, row_count=len(self.level_list), horizontal_spacing=150, vertical_spacing=20
        )
        for i, name in enumerate(self.level_list):
            # делаем кнопку уровня
            edit_btn = ar.gui.UIFlatButton(text=name, width=400)
            edit_btn.level_index = i
            edit_btn.on_click = self.on_edit_click
            grid.add(edit_btn, column=0, row=i)
            # делаем кнопку удаления рядом
            del_btn = ar.gui.UIFlatButton(text="del", width=50)
            del_btn.level_index = i
            del_btn.on_click = self.on_delete_click
            grid.add(del_btn, column=1, row=i)
        self.scroll_area.add(grid)
        main_layout.add(self.scroll_area)
        anchor_layout = self.manager.add(ar.gui.UIAnchorLayout())
        # создаем кнопку добавления
        add_btn = ar.gui.UIFlatButton(text="Добавить", width = 600)
        add_btn.on_click = self.on_add_click
        main_layout.add(add_btn)

        anchor_layout.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=main_layout
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

    def on_update_click(self, event):
        self.manager.clear()
        self.level_list = List_of_Levels.get_levels()
        self.rework_grid()

    def on_add_click(self, event):
        if self.dialog_open:
            return
        self.dialog_open = True

        dialog = AddLevelDialog(
            title="Добавить новый уровень",
            on_ok_callback=self._on_dialog_ok,
            on_cancel_callback=self._on_dialog_cancel
        )

        self.manager.add(dialog, layer=1)

    def _on_dialog_ok(self, level_name):

        List_of_Levels.add_level(level_name)

        self.dialog_open = False

    def _on_dialog_cancel(self):
        """Колбэк при нажатии Cancel в диалоге"""
        self.dialog_open = False

    def rework_grid(self):
        for child in list(self.scroll_area.children):
            self.scroll_area.remove(child)
        self.create_grid()
def main():
    window = ar.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    Level_view = Level_Menu()
    window.show_view(Level_view)
    ar.run()


if __name__ == '__main__':
    main()
