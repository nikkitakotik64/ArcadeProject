import arcade as ar
import arcade.gui
# TODO: переделать в классе добавления окна реализацию заднего фона
class AddLevelDialog(ar.gui.UIWidget):
    def __init__(self, width=400, height=200, on_ok_callback=None, on_cancel_callback=None):
        super().__init__(x=0, y=0, width=width, height=height)
        self.on_ok_callback = on_ok_callback
        self.on_cancel_callback = on_cancel_callback

        self.bg_rect = ar.SpriteSolidColor(width, height, ar.color.GRAY)

        window_layout = ar.gui.UIBoxLayout(vertical=True, space_between=15)

        title_label = ar.gui.UILabel(text="Добавить новый уровень", width=350, height=30, font_size=18, align="center")
        window_layout.add(title_label)

        # Поле ввода

        input_layout = ar.gui.UIBoxLayout(vertical=False, space_between=10)
        input_label = ar.gui.UILabel(text="Название:", width=100, height=30)
        self.level_input = ar.gui.UIInputText(
            text="",
            width=250,
            height=40,
            font_size=14
        )
        input_layout.add(input_label)
        input_layout.add(self.level_input)
        window_layout.add(input_layout)

        # Кнопки Ок и Закрыть
        button_layout = ar.gui.UIBoxLayout(vertical=False, space_between=20)
        ok_button = ar.gui.UIFlatButton(text="Ок", width=120, height=40)
        ok_button.on_click = self.on_ok_click
        cancel_button = ar.gui.UIFlatButton(text="Отмена", width=120, height=40)
        cancel_button.on_click = self.on_cancel_click

        button_layout.add(ok_button)
        button_layout.add(cancel_button)
        window_layout.add(button_layout)

        # Центрируем окно
        anchor_layout = ar.gui.UIAnchorLayout(width=width, height=height)
        anchor_layout.add(
            child=window_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.add(anchor_layout)

    def on_ok_click(self, event):
        level_name = self.level_input.text.strip()
        if level_name and self.on_ok_callback:
            self.on_ok_callback(level_name)

        self.parent.remove(self)

    def on_cancel_click(self, event):
        if self.on_cancel_callback:
            self.on_cancel_callback()

        self.parent.remove(self)

    def on_draw(self):
        self.bg_rect.draw()
        super.on_draw()