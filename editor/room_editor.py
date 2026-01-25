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


class GameObject(ar.Sprite):
    """Класс для игровых объектов в редакторе"""

    def __init__(self, row, col, texture_id, cell_size=20):
        self.texture_id = texture_id
        self.row = row
        self.col = col
        self.cell_size = cell_size
        # self.alpha = 0.0
        super().__init__(scale=1.0)

    def update_position(self, grid_start_x, grid_start_y):
        """Обновляет позицию спрайта на основе координат сетки"""
        self.center_x = grid_start_x + self.col * self.cell_size + self.cell_size // 2
        self.center_y = grid_start_y + self.row * self.cell_size + self.cell_size // 2
        scale = self.cell_size / max(self.width, self.height) * 0.8
        self.scale = scale


class RoomEditor(ar.View):
    def __init__(self, level_name="Test_Level.level"):
        super().__init__()
        self.level_name = level_name
        self.grid_width = 48
        self.grid_height = 27
        self.cell_size = 20

        self.selected_tool = None
        self.selected_texture_id = None
        self.selected_option_name = None

        self.manager = arcade.gui.UIManager()

        self.walls_sprites = ar.SpriteList()
        self.decor_sprites = ar.SpriteList()
        self.functional_sprites = ar.SpriteList()

        self.walls_data = []
        self.decor_data = []
        self.functional_data = []

        self.background = 1

        self.textures = {}
        self.load_textures()

        self.load_level_data(level_name)

    def load_textures(self):
        for key, texture_id in TEXTURE_MAP.items():
            if texture_id in data.FILES:
                self.textures[texture_id] = ar.load_texture(data.FILES[texture_id])

    def load_level_data(self, level_name):
        """Загружает данные уровня и создает спрайты"""
        walls_data, decor_data, functional_data = load_level(level_name)

        self.walls_data = walls_data
        self.decor_data = decor_data
        self.functional_data = functional_data

        # Создаем спрайты для загруженных данных
        for wall in walls_data:
            self.create_sprite_from_data(wall, "walls")
        for decor in decor_data:
            self.create_sprite_from_data(decor, "decor")
        for functional in functional_data:
            self.create_sprite_from_data(functional, "functional_objects")

    def create_sprite_from_data(self, obj_data, obj_type):
        """Создает спрайт из данных объекта"""
        row = obj_data.get("row", 0)
        col = obj_data.get("col", 0)
        texture_id = obj_data.get("texture_id", "")

        texture = self.textures.get(texture_id)
        if texture:
            sprite = GameObject(row, col, texture_id, self.cell_size)
            sprite.texture = texture

            # Сохраняем исходные данные в спрайте
            sprite.obj_type = obj_type
            sprite.texture_id = texture_id

            # Добавляем в соответствующий список
            if obj_type == "walls":
                self.walls_sprites.append(sprite)
            elif obj_type == "decor":
                self.decor_sprites.append(sprite)
            elif obj_type == "functional_objects":
                self.functional_sprites.append(sprite)

    def on_show_view(self):
        ar.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.manager.enable()
        self.setup()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        self.manager.clear()

        right_panel = ar.gui.UIBoxLayout(vertical=True, space_between=20)

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
        select_button.dropdown = dropdown
        select_button.on_click = self.on_tool_select
        section.add(select_button)

        return section

    def on_tool_select(self, event):
        button = event.source
        section_title = button.section_title
        selected_option = button.dropdown.value

        if section_title == "Стены":
            self.selected_tool = "walls"
        elif section_title == "Декор":
            self.selected_tool = "decor"
        elif section_title == "Функциональные":
            self.selected_tool = "functional_objects"

        self.selected_texture_id = TEXTURE_MAP[selected_option]
        self.selected_option_name = selected_option

    def on_draw(self):
        self.clear()

        panel_rect = ar.rect.XYWH(
            SCREEN_WIDTH * 0.85,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH * 0.3,
            SCREEN_HEIGHT
        )
        ar.draw_rect_filled(panel_rect, arcade.color.APRICOT)

        self.draw_grid()
        self.draw_objects()
        self.draw_selected_tool()

        self.manager.draw()

    def draw_grid(self):
        grid_pixel_width = self.grid_width * self.cell_size
        grid_pixel_height = self.grid_height * self.cell_size

        left_panel_width = SCREEN_WIDTH * 0.7
        start_x = (left_panel_width - grid_pixel_width) / 2
        start_y = (SCREEN_HEIGHT - grid_pixel_height) / 2

        self.grid_start_x = start_x
        self.grid_start_y = start_y
        self.grid_pixel_width = grid_pixel_width
        self.grid_pixel_height = grid_pixel_height

        grid_rect = ar.rect.XYWH(
            start_x + grid_pixel_width / 2,
            start_y + grid_pixel_height / 2,
            grid_pixel_width,
            grid_pixel_height
        )
        ar.draw_rect_filled(grid_rect, ar.color.BLACK)

        for x in range(self.grid_width + 1):
            line_x = start_x + x * self.cell_size
            ar.draw_line(
                line_x, start_y,
                line_x, start_y + grid_pixel_height,
                ar.color.WHITE, 1
            )

        for y in range(self.grid_height + 1):
            line_y = start_y + y * self.cell_size
            ar.draw_line(
                start_x, line_y,
                start_x + grid_pixel_width, line_y,
                ar.color.WHITE, 1
            )

    def draw_objects(self):
        # Обновляем позиции всех спрайтов перед отрисовкой
        for sprite in self.walls_sprites:
            sprite.update_position(self.grid_start_x, self.grid_start_y)
        for sprite in self.decor_sprites:
            sprite.update_position(self.grid_start_x, self.grid_start_y)
        for sprite in self.functional_sprites:
            sprite.update_position(self.grid_start_x, self.grid_start_y)

        # Рисуем спрайты
        self.walls_sprites.draw()
        self.decor_sprites.draw()
        self.functional_sprites.draw()

        # Рисуем рамки
        self.draw_borders()

    def draw_borders(self):
        """Рисует рамки вокруг объектов"""
        for sprite in self.walls_sprites:
            self.draw_sprite_border(sprite, ar.color.RED)
        for sprite in self.decor_sprites:
            self.draw_sprite_border(sprite, ar.color.GREEN)
        for sprite in self.functional_sprites:
            self.draw_sprite_border(sprite, ar.color.BLUE)

    def draw_sprite_border(self, sprite, color):
        """Рисует рамку вокруг спрайта"""
        half_width = self.cell_size * 0.9 / 2
        half_height = self.cell_size * 0.9 / 2

        left = sprite.center_x - half_width
        right = sprite.center_x + half_width
        bottom = sprite.center_y - half_height
        top = sprite.center_y + half_height

        ar.draw_lrbt_rectangle_outline(
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            color=color,
            border_width=1
        )

    def draw_selected_tool(self):
        if self.selected_tool and self.selected_option_name:
            text = f"Выбран: {self.selected_option_name}"
            color = ar.color.RED if self.selected_tool == "walls" else (
                ar.color.GREEN if self.selected_tool == "decor" else ar.color.BLUE
            )
            ar.draw_text(
                text, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - 30, color, 18, anchor_x="center", bold=True
            )

    def on_save_click(self, event):
        """Сохранение уровня в файл"""
        try:
            # Обновляем данные из спрайтов
            self.update_data_from_sprites()

            level_data = {
                "walls": self.walls_data,
                "decor": self.decor_data,
                "functional_objects": self.functional_data
            }

            path = levels_folder + '/' + self.level_name
            with open(path, "w", encoding="utf-8") as f:
                json.dump(level_data, f, ensure_ascii=False, indent=2)

            print(f"Уровень {self.level_name} успешно сохранен!")

        except Exception as e:
            print(f"Ошибка при сохранении уровня: {e}")

    def update_data_from_sprites(self):
        """Обновляет данные из спрайтов перед сохранением"""
        self.walls_data = []
        self.decor_data = []
        self.functional_data = []

        for sprite in self.walls_sprites:
            self.walls_data.append({
                "row": sprite.row,
                "col": sprite.col,
                "texture_id": sprite.texture_id
            })

        for sprite in self.decor_sprites:
            self.decor_data.append({
                "row": sprite.row,
                "col": sprite.col,
                "texture_id": sprite.texture_id
            })

        for sprite in self.functional_sprites:
            self.functional_data.append({
                "row": sprite.row,
                "col": sprite.col,
                "texture_id": sprite.texture_id
            })

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.is_mouse_in_grid(x, y):
            return
        cell = self.get_cell_from_mouse(x, y)
        if not cell:
            return
        row, col = cell
        if button == ar.MOUSE_BUTTON_LEFT and self.selected_tool:
            self.add_object(row, col)
        elif button == ar.MOUSE_BUTTON_RIGHT:
            self.remove_object(row, col)

    def is_mouse_in_grid(self, mouse_x, mouse_y) -> bool:
        if not hasattr(self, "grid_start_x"):
            return False

        return (self.grid_start_x <= mouse_x <= self.grid_start_x + self.grid_pixel_width and
                self.grid_start_y <= mouse_y <= self.grid_start_y + self.grid_pixel_height)

    def get_cell_from_mouse(self, mouse_x, mouse_y):
        if not self.is_mouse_in_grid(mouse_x, mouse_y):
            return None
        col = int((mouse_x - self.grid_start_x) // self.cell_size)
        row = int((mouse_y - self.grid_start_y) // self.cell_size)

        if 0 <= col < self.grid_width and 0 <= row < self.grid_height:
            return (row, col)
        return None

    def add_object(self, row, col):
        """Добавление объекта в указанную клетку"""
        if not self.selected_tool or not self.selected_texture_id:
            return

        # Проверяем столкновения
        if self.selected_tool == "walls":
            # Проверяем функциональные объекты
            for sprite in self.functional_sprites:
                if sprite.row == row and sprite.col == col:
                    return
            # Удаляем существующую стену в этой клетке
            self.remove_existing_object(row, col, self.walls_sprites)

        elif self.selected_tool == "functional_objects":
            # Проверяем стены
            for sprite in self.walls_sprites:
                if sprite.row == row and sprite.col == col:
                    return
            # Удаляем существующий функциональный объект
            self.remove_existing_object(row, col, self.functional_sprites)

        elif self.selected_tool == "decor":
            # Декор можно размещать где угодно, просто удаляем существующий
            self.remove_existing_object(row, col, self.decor_sprites)

        # Создаем новый спрайт
        texture = self.textures.get(self.selected_texture_id)
        if texture:
            sprite = GameObject(row, col, self.selected_texture_id, self.cell_size)
            sprite.texture = texture
            sprite.texture_id = self.selected_texture_id
            sprite.obj_type = self.selected_tool

            # Добавляем в соответствующий список
            if self.selected_tool == "walls":
                self.walls_sprites.append(sprite)
            elif self.selected_tool == "decor":
                self.decor_sprites.append(sprite)
            elif self.selected_tool == "functional_objects":
                self.functional_sprites.append(sprite)

    def remove_existing_object(self, row, col, sprite_list):
        """Удаляет существующий объект из списка спрайтов"""
        for i, sprite in enumerate(sprite_list):
            if sprite.row == row and sprite.col == col:
                sprite_list.pop(i)
                return True
        return False

    def remove_object(self, row, col):
        """Удаление объекта из указанной клетки"""
        # Удаляем из всех списков
        self.remove_existing_object(row, col, self.walls_sprites)
        self.remove_existing_object(row, col, self.decor_sprites)
        self.remove_existing_object(row, col, self.functional_sprites)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)

    editor = RoomEditor()
    window.show_view(editor)
    ar.run()


if __name__ == "__main__":
    main()