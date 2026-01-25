import arcade as ar
import arcade.gui

from work_with_levels import *
from data.savings import data

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Редактор комнаты"

OBJECT_TYPES = {
    "walls": "Стены",
    "decor": "Декор",
    "functional_objects": "Функциональные"
}

TEXTURE_MAP = {
    "Кирпичная": "wall-1",
    "Металлическая": "wall-2",
    "Факел": "torch",
    "Дерево": "tree",
    "Ваза": "vase",
    "Сундук": "chest",
    "Дверь": "door"
}

TEXTURE_TO_NAME = {
    "wall-1": "Кирпичная",
    "wall-2": "Металлическая",
    "torch": "Факел",
    "tree": "Дерево",
    "vase": "Ваза",
    "chest": "Сундук",
    "door": "Дверь"
}

class RoomEditor(ar.View):
    def __init__(self, level_name="Test_level.level"):
        super().__init__()
        self.level_name = level_name
        self.grid_width = 48
        self.grid_height = 27
        self.cell_size = 20
        self.selected_tool = None
        self.texture_id = None
        self.option_name = None
        self.manager = arcade.gui.UIManager()

        self.walls = []
        self.decor = []
        self.functional = []
        self.background = 1

        self.textures = {}
        self.load_textures()

        self.walls, self.decor, self.functional = load_level(level_name)

    def load_textures(self):
        for key, id in TEXTURE_MAP.items():
            if id in data.FILES:
                self.textures[id] = ar.load_texture(data.FILES[id])

    def on_show_view(self):
        ar.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
        self.setup()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        self.manager.clear()

        # Панель инструментов
        right_panel = ar.gui.UIBoxLayout(vertical=True, space_between=20)

        # создание секций выпадающий список+кнопка
        walls_section = self.create_tool_section("Стены", ["Кирпичная", "Металлическая"])
        right_panel.add(walls_section)
        decor_section = self.create_tool_section("Декор", ["Факел", "Дерево", "Ваза"])
        right_panel.add(decor_section)
        functional_section = self.create_tool_section("Функциональные", ["Сундук", "Дверь"])
        right_panel.add(functional_section)

        save_button = ar.gui.UIFlatButton(
            text="Сохранить уровень",
            width=250,
            height=50,
        )
        save_button.on_click = self.on_save_click
        right_panel.add(save_button)

        # Позиционируем панель в правой части
        container = ar.gui.UIAnchorLayout()
        container.add(
            child=right_panel,
            anchor_x="right",
            anchor_y="center_y"
        )

        self.manager.add(container)

    def create_tool_section(self, title, options):
        section = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
        section.with_background(color=ar.color.LIGHT_APRICOT)
        section.with_border(color=arcade.color.DARK_BROWN)
        section.with_padding(all=10)

        section_title = ar.gui.UILabel(
            text=title,
            font_size=18,
            width=250,
            height=30,
            align="center",
            text_color=ar.color.BLACK
        )
        section.add(section_title)

        dropdown = arcade.gui.UIDropdown(
            default=options[0],
            options=options,
            width=250,
            height=35,
        )
        dropdown.section_title = title
        section.add(dropdown)

        select_button = ar.gui.UIFlatButton(
            text="Выбрать",
            width=250,
            height=40
        )
        select_button.section_title = title
        select_button.dropdown = dropdown  # Связываем кнопку с выпадающим списком
        select_button.on_click = self.on_tool_select
        section.add(select_button)

        return section

    def on_tool_select(self, event):
        """Какой инструмент выбран"""
        button = event.source
        section_title = button.section_title
        selected_option = button.dropdown.value

        if section_title == "Стены":
            self.selected_tool = "walls"
        elif section_title == "Декор":
            self.selected_tool = "decor"
        elif section_title == "Функциональные":
            self.selected_tool = "functional_objects"

        self.texture_id = TEXTURE_MAP[selected_option]
        self.option_name = selected_option


    def on_draw(self):
        self.clear()

        # 1. Рисуем фон правой панели
        panel_rect = ar.rect.XYWH(
            SCREEN_WIDTH * 0.85,  # 70% + половина от 30% = 85%
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH * 0.3,
            SCREEN_HEIGHT
        )
        ar.draw_rect_filled(panel_rect, arcade.color.APRICOT)

        # 2. Рисуем сетку
        self.draw_grid()

        self.manager.draw()

    def draw_grid(self):
        """Рисует сетку 48x27 в левой части экрана"""
        # Вычисляем размеры сетки в пикселях
        grid_pixel_width = self.grid_width * self.cell_size
        grid_pixel_height = self.grid_height * self.cell_size

        # Вычисляем позицию сетки (центрируем в левой панели)
        left_panel_width = SCREEN_WIDTH * 0.7
        start_x = (left_panel_width - grid_pixel_width) / 2
        start_y = (SCREEN_HEIGHT - grid_pixel_height) / 2

        # Сохраняем для использования в других методах
        self.grid_start_x = start_x
        self.grid_start_y = start_y
        self.grid_pixel_width = grid_pixel_width
        self.grid_pixel_height = grid_pixel_height

        grid_rect = ar.rect.XYWH(
            start_x + grid_pixel_width / 2,  # center_x
            start_y + grid_pixel_height / 2,  # center_y
            grid_pixel_width,  # width
            grid_pixel_height  # height
        )
        ar.draw_rect_filled(grid_rect, ar.color.BLACK)

        # Белые линии сетки
        # Вертикальные линии
        for x in range(self.grid_width + 1):
            line_x = start_x + x * self.cell_size
            ar.draw_line(
                line_x, start_y,
                line_x, start_y + grid_pixel_height,
                ar.color.WHITE, 1
            )

        # Горизонтальные линии
        for y in range(self.grid_height + 1):
            line_y = start_y + y * self.cell_size
            ar.draw_line(
                start_x, line_y,
                start_x + grid_pixel_width, line_y,
                ar.color.WHITE, 1
            )

    def on_save_click(self):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def is_mouse_in_grid(self, mouse_x, mouse_y):
        pass

    def get_cell_from_mouse(self, mouse_x, mouse_y):
        pass

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)

    editor = RoomEditor()
    window.show_view(editor)
    ar.run()

if __name__ == "__main__":
    main()