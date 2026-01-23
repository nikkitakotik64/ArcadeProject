import arcade as ar
import arcade.gui as gui
from main import game_settings
from data.savings import data
from screen import CELL_SIDE, W_OUTLINE, WIDTH, H_OUTLINE, HEIGHT
from sprites.weapons import weapons_list


def create_tool_section(title: str, options: list[str], x: int, y: int):
    section = gui.UIBoxLayout(vertical=True, space_between=10, x=x, y=y)
    section.with_background(color=ar.color.LIGHT_APRICOT)
    section.with_border(color=ar.color.DARK_BROWN)
    section.with_padding(all=10)

    section_title = gui.UILabel(
        text=title,
        font_size=18,
        width=250,
        height=30,
        align="center",
        text_color=ar.color.BLACK
    )
    section.add(section_title)

    dropdown = gui.UIDropdown(
        default=options[0],
        options=options,
        width=250,
        height=35,
    )
    dropdown.section_title = title
    section.add(dropdown)

    return section


class StartGameMenu(ar.Window):
    random_button_enabled = ar.Sprite(data.FILES['random_button_enabled'], CELL_SIDE / 40)
    random_button_disabled = ar.Sprite(data.FILES['random_button_disabled'], CELL_SIDE / 40)
    same_button_enabled = ar.Sprite(data.FILES['same_button_enabled'], CELL_SIDE / 40)
    same_button_disabled = ar.Sprite(data.FILES['same_button_disabled'], CELL_SIDE / 40)

    def __init__(self) -> None:
        self.k = CELL_SIDE / 16
        super().__init__(1, 1, 'Game', fullscreen=True)
        ar.set_background_color(ar.color.DARK_RED)
        self.buttons = ar.SpriteList()
        self.changing = [False, False]

        self.start_button = ar.Sprite(data.FILES['start_button'], self.k)
        self.start_button.center_x = WIDTH / 2 + W_OUTLINE
        self.start_button.center_y = HEIGHT / 5 + H_OUTLINE
        self.buttons.append(self.start_button)

        self.same = False
        self.same_button = ar.Sprite(data.FILES['same_button_disabled'], self.k / 2.5)
        self.same_button.center_x = W_OUTLINE + CELL_SIDE * 1.25 + WIDTH / 4
        self.same_button.center_y = H_OUTLINE + 1.9 * HEIGHT / 5
        self.buttons.append(self.same_button)

        self.random = False
        self.random_button = ar.Sprite(data.FILES['random_button_enabled'], self.k / 2.5)
        self.random_button.center_x = CELL_SIDE * 1.25 + WIDTH / 4 + W_OUTLINE
        self.random_button.center_y = HEIGHT / 2 + H_OUTLINE
        self.buttons.append(self.random_button)

        self.first_player = 'Glock-18'
        self.first_player_button = ar.Sprite(data.FILES['player_button'], self.k)
        self.first_player_button.center_x = W_OUTLINE + WIDTH / 8
        self.first_player_button.center_y = H_OUTLINE + HEIGHT / 2
        self.buttons.append(self.first_player_button)

        self.second_player = 'Glock-18'
        self.second_player_button = ar.Sprite(data.FILES['player_button'], self.k)
        self.second_player_button.center_x = W_OUTLINE + 7 * WIDTH / 8
        self.second_player_button.center_y = H_OUTLINE + HEIGHT / 2
        self.buttons.append(self.second_player_button)

        first_player_selection = create_tool_section(self.first_player, weapons_list,
                                                     W_OUTLINE + WIDTH / 8, H_OUTLINE + HEIGHT / 2)
        self.manager1 = gui.UIManager()
        self.manager1.enable()
        self.manager1.add(first_player_selection)

    def close(self, ended: bool = True) -> None:
        if ended:
            self.manager1.disable()
            game_settings['running'].set_false()
        super().close()

    def on_draw(self) -> None:
        self.clear()
        self.buttons.draw()
        if self.changing[0]:
            self.manager1.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == ar.key.ESCAPE:
            self.close(False)

    def start_game(self) -> None:
        pass

    def change_same(self) -> None:
        self.same = not self.same
        if self.same:
            self.same_button.texture = self.same_button_enabled.texture
        else:
            self.same_button.texture = self.same_button_disabled.texture

    def click(self, x: float, y: float) -> None:
        if (self.start_button.right >= x >= self.start_button.left
                and self.start_button.top >= y >= self.start_button.bottom):
            self.start_game()
        elif (self.same_button.right >= x >= self.same_button.left
              and self.same_button.top >= y >= self.same_button.bottom):
            self.change_same()
        elif (self.random_button.right >= x >= self.random_button.left
              and self.random_button.top >= y >= self.random_button.bottom):
            self.change_random()
        elif (self.first_player_button.right >= x >= self.first_player_button.left
              and self.first_player_button.top >= y >= self.first_player_button.bottom):
            self.change_first_player()
        elif (self.second_player_button.right >= x >= self.second_player_button.left
              and self.second_player_button.top >= y >= self.second_player_button.bottom):
            self.change_second_player()

    def change_first_player(self) -> None:
        if self.random:
            return
        self.changing[0] = True

    def change_second_player(self) -> None:
        if self.random and self.same:
            return

    def change_random(self) -> None:
        self.random = not self.random
        if self.random:
            self.random_button.texture = self.random_button_enabled.texture
        else:
            self.random_button.texture = self.random_button_disabled.texture

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            self.click(x, y)
