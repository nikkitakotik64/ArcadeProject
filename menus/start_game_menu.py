import arcade as ar
import arcade.gui as gui
from main import game_settings
from data.savings import data
from screen import CELL_SIDE, W_OUTLINE, WIDTH, H_OUTLINE, HEIGHT
from sprites.weapons import weapons_list

changing = [False, False]


def create_tool_section(title: str, options: list[str], x: int, y: int):
    section = gui.UIBoxLayout(vertical=True, space_between=10, x=x, y=y)
    section.with_background(color=ar.color.BLACK)
    section.with_padding(all=10)
    k = CELL_SIDE / 16

    section_title = gui.UILabel(
        text=title,
        font_size=CELL_SIDE // 16 * 16,
        width=80 * k,
        height=50 * k,
        align="center",
        text_color=ar.color.DARK_RED
    )
    section.add(section_title)

    # TODO: сделать стили
    dropdown = gui.UIDropdown(
        default=options[0],
        options=options,
        width=80 * k,
        height=15 * k,
    )
    dropdown.section_title = title
    section.add(dropdown)

    return section, dropdown


def stop_change_first_player(_) -> None:
    changing[0] = False


def stop_change_second_player(_) -> None:
    changing[1] = False


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
        self.changing = changing

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

        self.first_player = 'Random'
        self.first_player_button = ar.Sprite(data.FILES['player_button'], self.k)
        self.first_player_button.center_x = W_OUTLINE + WIDTH / 8
        self.first_player_button.center_y = H_OUTLINE + HEIGHT / 2
        self.for_first_player = ar.SpriteList()
        self.for_first_player.append(self.first_player_button)

        self.second_player = 'Random'
        self.second_player_button = ar.Sprite(data.FILES['player_button'], self.k)
        self.second_player_button.center_x = W_OUTLINE + 7 * WIDTH / 8
        self.second_player_button.center_y = H_OUTLINE + HEIGHT / 2
        self.for_second_player = ar.SpriteList()
        self.for_second_player.append(self.second_player_button)

        first_player_selection, self.first_dropdown = create_tool_section('First player', ['Random'] + weapons_list,
                                                                          W_OUTLINE + WIDTH / 16,
                                                                          H_OUTLINE + 3 * HEIGHT / 4)
        self.first_dropdown.on_change = stop_change_first_player
        self.manager1 = gui.UIManager()
        self.manager1.enable()
        self.manager1.add(first_player_selection)

        second_player_selection, self.second_dropdown = create_tool_section('Second player',
                                                                            ['Random'] + weapons_list,
                                                                            W_OUTLINE + 51 * WIDTH / 64,
                                                                            H_OUTLINE + 3 * HEIGHT / 4)
        self.second_dropdown.on_change = stop_change_second_player
        self.manager2 = gui.UIManager()
        self.manager2.enable()
        self.manager2.add(second_player_selection)

        text = 'The same weapons'
        lay = gui.UIBoxLayout(vertical=True, space_between=10, x=W_OUTLINE + CELL_SIDE * 2.75 + WIDTH / 4,
                              y=H_OUTLINE + 1.75 * HEIGHT / 5)
        section = gui.UILabel(
            text=text,
            font_size=CELL_SIDE // 16 * 16,
            width=80 * self.k,
            height=50 * self.k,
            align="center",
            text_color=ar.color.BLACK,
        )
        lay.add(section)

        self.manager = gui.UIManager()
        self.manager.enable()
        self.manager.add(lay)

    def on_update(self, delta_time: float) -> None:
        self.first_player = self.first_dropdown.value
        self.second_player = self.second_dropdown.value

    def close(self, ended: bool = True) -> None:
        if ended:
            self.manager1.disable()
            self.manager2.disable()
            game_settings['running'].set_false()
        super().close()

    def on_draw(self) -> None:
        self.clear()
        self.buttons.draw()
        self.manager.draw()
        if self.changing[0]:
            self.manager1.draw()
        else:
            self.for_first_player.draw()
        if self.changing[1]:
            self.manager2.draw()
        else:
            self.for_second_player.draw()

    def on_key_press(self, key: int, _: int) -> None:
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
        self.changing[0] = True
        self.changing[1] = False

    def change_second_player(self) -> None:
        if self.same:
            return
        self.changing[1] = True
        self.changing[0] = False

    def change_random(self) -> None:
        self.random = not self.random
        if self.random:
            self.random_button.texture = self.random_button_enabled.texture
        else:
            self.random_button.texture = self.random_button_disabled.texture

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            self.click(x, y)
