import arcade as ar
import arcade.gui
from typing import Optional, Callable


class AddLevelDialog(ar.gui.UIMouseFilterMixin, ar.gui.UIAnchorLayout):
    """Всплывающее окно для добавления нового уровня"""

    def __init__(
            self,
            title: str = "Добавить новый уровень",
            on_ok_callback: Optional[Callable] = None,
            on_cancel_callback: Optional[Callable] = None
    ):
        super().__init__(size_hint=(1, 1))

        self.on_ok_callback = on_ok_callback
        self.on_cancel_callback = on_cancel_callback

        # основная рамка окна
        frame = self.add(
            ar.gui.UIAnchorLayout(
                width=400,
                height=200,
                size_hint=None
            )
        )
        frame.with_padding(all=20)

        frame.with_background(
            texture=ar.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=ar.load_texture(
                    ":resources:gui_basic_assets/window/grey_panel.png"
                )
            )
        )

        title_label = ar.gui.UILabel(
            text=title,
            align="center",
            font_size=18,
            multiline=False,
            width=350,
            text_color=ar.color.BLACK,
        )

        title_label_space = ar.gui.UISpace(height=15, color=ar.color.TRANSPARENT_BLACK)

        self.level_input = ar.gui.UIInputText(
            text="",
            width=350,
            height=40,
            font_size=14,
            text_color=ar.color.BLACK,
        ).with_border()

        button_layout = ar.gui.UIBoxLayout(vertical=False, space_between=20)

        ok_button = ar.gui.UIFlatButton(text="OK", width=150, height=40)
        ok_button.on_click = self._on_ok_click

        cancel_button = ar.gui.UIFlatButton(text="Отмена", width=150, height=40)
        cancel_button.on_click = self._on_cancel_click

        button_layout.add(ok_button)
        button_layout.add(cancel_button)

        widget_layout = ar.gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(title_label)
        widget_layout.add(title_label_space)
        widget_layout.add(self.level_input)
        widget_layout.add(button_layout)

        frame.add(
            child=widget_layout,
            anchor_x="center_x",
            anchor_y="top"
        )

    def _on_ok_click(self, event):
        level_name = self.level_input.text.strip()

        if not level_name:
            return

        if self.on_ok_callback:
            self.on_ok_callback(level_name)

        self.close_dialog()

    def _on_cancel_click(self, event):
        if self.on_cancel_callback:
            self.on_cancel_callback()

        self.close_dialog()

    def close_dialog(self):

        # Использует scheduled call для избежания проблем с гонкой событий
        def remove():
            if hasattr(self, 'parent') and self.parent:
                try:
                    self.parent.remove(self)
                except:
                    pass  # Игнорирует ошибки удаления

        ar.schedule_once(lambda dt: remove(), 0.05)


class NotificationDialog(ar.gui.UIMouseFilterMixin, ar.gui.UIAnchorLayout):
    """Универсальное всплывающее окно для уведомлений"""

    def __init__(
            self,
            title: str = "Уведомление",
            message: str = "",
            on_ok_callback: Optional[Callable] = None,
            width: int = 400,
            height: int = 200
    ):
        super().__init__(size_hint=(1, 1))

        self.on_ok_callback = on_ok_callback

        # основная рамка окна
        frame = self.add(
            ar.gui.UIAnchorLayout(
                width=width,
                height=height,
                size_hint=None
            )
        )
        frame.with_padding(all=20)

        frame.with_background(
            texture=ar.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=ar.load_texture(
                    ":resources:gui_basic_assets/window/grey_panel.png"
                )
            )
        )

        title_label = ar.gui.UILabel(
            text=title,
            align="center",
            font_size=18,
            multiline=False,
            width=width - 40,
            text_color=ar.color.BLACK,
        )

        message_label = ar.gui.UILabel(
            text=message,
            align="center",
            font_size=14,
            multiline=True,
            width=width - 40,
            text_color=ar.color.BLACK,
        )

        ok_button = ar.gui.UIFlatButton(text="OK", width=150, height=40)
        ok_button.on_click = self._on_ok_click

        widget_layout = ar.gui.UIBoxLayout(align="left", space_between=15)
        widget_layout.add(title_label)
        widget_layout.add(message_label)
        widget_layout.add(ok_button)

        frame.add(
            child=widget_layout,
            anchor_x="center_x",
            anchor_y="center_y"
        )

    def _on_ok_click(self, event):
        """Обработчик нажатия OK"""
        if self.on_ok_callback:
            self.on_ok_callback()

        # Безопасное закрытие окна
        self.close_dialog()

    def close_dialog(self):

        def remove():
            if hasattr(self, 'parent') and self.parent:
                try:
                    self.parent.remove(self)
                except:
                    pass  # Игнорирует ошибки удаления

        ar.schedule_once(lambda dt: remove(), 0.05)


class ManagerContainer:
    """Контейнер для хранения ссылки на UIManager"""

    _manager = None

    @classmethod
    def set_manager(cls, manager):
        cls._manager = manager

    @classmethod
    def get_manager(cls):
        return cls._manager
