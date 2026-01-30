import arcade as ar
import arcade.gui as gui
from main import game_settings
from data.savings import data
from screen import CELL_SIDE, W_OUTLINE, WIDTH, H_OUTLINE, HEIGHT, H
from sprites.weapons import weapons_list
from game.game import PvP as Game
from game_types import Running
from enum import Enum

restart = Running()


def create_tool_section(title: str, options: list[str], x: int, y: int, width: int, height: int):
    k = CELL_SIDE / 16
    section = gui.UIBoxLayout(vertical=True, space_between=10, x=x, y=y, height=height, width=width)
    section.with_background(color=ar.color.BLACK)
    section.with_padding(all=10)

    section_title = gui.UILabel(
        text=title,
        font_size=CELL_SIDE // 16 * 16,
        width=80 * k,
        height=50 * k,
        align="center",
        text_color=ar.color.DARK_RED
    )
    section.add(section_title)

    fnt_size = CELL_SIDE // 16 * 9
    dropdown_style = {
        "normal": gui.UIFlatButton.UIStyle(bg=ar.color.BLACK, font_color=ar.color.DARK_RED, font_size=fnt_size),
        "hover": gui.UIFlatButton.UIStyle(bg=(80, 80, 80, 255), font_color=ar.color.DARK_RED, font_size=fnt_size),
        "press": gui.UIFlatButton.UIStyle(bg=(80, 80, 80, 255), font_color=ar.color.DARK_RED, font_size=fnt_size),
    }
    active_dropdown_style = {
        "normal": gui.UIFlatButton.UIStyle(bg=ar.color.BLACK, font_color=ar.color.RED, font_size=fnt_size),
        "hover": gui.UIFlatButton.UIStyle(bg=(80, 80, 80, 255), font_color=ar.color.RED, font_size=fnt_size),
        "press": gui.UIFlatButton.UIStyle(bg=(80, 80, 80, 255), font_color=ar.color.RED, font_size=fnt_size),
    }

    dropdown = gui.UIDropdown(
        default=options[0],
        options=options,
        width=80 * k,
        height=13 * k,
        primary_style=active_dropdown_style,
        dropdown_style=dropdown_style,
        active_style=active_dropdown_style,
    )
    dropdown.section_title = title
    section.add(dropdown)

    section_title = gui.UILabel(
        text='',
        font_size=CELL_SIDE // 16 * 16,
        width=80 * k,
        height=300 * k,
        align="center",
        text_color=ar.color.DARK_RED
    )
    section.add(section_title)

    return section, dropdown


class StartGameMenuModes(Enum):
    normal = 0
    level_changing = 1
    editor_levels_change = 2


class StartGameMenu(ar.Window):
    random_button_all = ar.Sprite(data.FILES['random_button_all'], CELL_SIDE / 40)
    random_button_editor = ar.Sprite(data.FILES['random_button_editor'], CELL_SIDE / 40)
    random_button_standard = ar.Sprite(data.FILES['random_button_standard'], CELL_SIDE / 40)
    random_button_disabled = ar.Sprite(data.FILES['random_button_disabled'], CELL_SIDE / 40)
    same_button_enabled = ar.Sprite(data.FILES['same_button_enabled'], CELL_SIDE / 40)
    same_button_disabled = ar.Sprite(data.FILES['same_button_disabled'], CELL_SIDE / 40)

    def __init__(self) -> None:
        self.k = CELL_SIDE / 16
        self.stop = False
        self.texts = [''] * 4
        super().__init__(1, 1, 'Game', fullscreen=True)
        self.editor_levels = data.get_levels_list()
        ar.set_background_color(ar.color.DARK_RED)
        self.buttons = ar.SpriteList()
        self.mode = StartGameMenuModes.normal
        self.page = 0

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
        self.random_button = ar.Sprite(data.FILES['random_button_all'], self.k / 2.5)
        self.random_button.center_x = WIDTH / 2 + W_OUTLINE
        self.random_button.center_y = HEIGHT / 2 + H_OUTLINE
        self.buttons.append(self.random_button)

        self.level = data.LEVELS['Creator']
        self.level_button = ar.Sprite(data.FILES['level_button'], self.k)
        self.level_button.center_x = WIDTH / 2 + W_OUTLINE
        self.level_button.center_y = H - H_OUTLINE - 1.2 * HEIGHT / 5
        self.buttons.append(self.level_button)

        self.level_change_buttons = ar.SpriteList()
        self.creator_button = ar.Sprite(data.FILES['creator_button'], self.k)
        self.creator_button.center_x = WIDTH / 4 + W_OUTLINE
        self.creator_button.center_y = 3 * HEIGHT / 4 + H_OUTLINE
        self.level_change_buttons.append(self.creator_button)

        self.paradigm_button = ar.Sprite(data.FILES['paradigm_button'], self.k)
        self.paradigm_button.center_x = 3 * WIDTH / 4 + W_OUTLINE
        self.paradigm_button.center_y = 3 * HEIGHT / 4 + H_OUTLINE
        self.level_change_buttons.append(self.paradigm_button)

        self.battle_button = ar.Sprite(data.FILES['battle_button'], self.k)
        self.battle_button.center_x = WIDTH / 4 + W_OUTLINE
        self.battle_button.center_y = HEIGHT / 2 + H_OUTLINE
        self.level_change_buttons.append(self.battle_button)

        self.room_button = ar.Sprite(data.FILES['room_button'], self.k)
        self.room_button.center_x = 3 * WIDTH / 4 + W_OUTLINE
        self.room_button.center_y = HEIGHT / 2 + H_OUTLINE
        self.level_change_buttons.append(self.room_button)

        self.editor_button = ar.Sprite(data.FILES['editor_levels_button'], self.k)
        self.editor_button.center_x = WIDTH / 2 + W_OUTLINE
        self.editor_button.center_y = HEIGHT / 4 + H_OUTLINE
        self.level_change_buttons.append(self.editor_button)

        self.editor_buttons = ar.SpriteList()
        self.first_button = ar.Sprite(data.FILES['button'], self.k)
        self.first_button.center_x = WIDTH / 4 + W_OUTLINE
        self.first_button.center_y = 3 * HEIGHT / 4 + H_OUTLINE

        self.second_button = ar.Sprite(data.FILES['button'], self.k)
        self.second_button.center_x = 3 * WIDTH / 4 + W_OUTLINE
        self.second_button.center_y = 3 * HEIGHT / 4 + H_OUTLINE

        self.third_button = ar.Sprite(data.FILES['button'], self.k)
        self.third_button.center_x = WIDTH / 4 + W_OUTLINE
        self.third_button.center_y = HEIGHT / 2 + H_OUTLINE

        self.fourth_button = ar.Sprite(data.FILES['button'], self.k)
        self.fourth_button.center_x = 3 * WIDTH / 4 + W_OUTLINE
        self.fourth_button.center_y = HEIGHT / 2 + H_OUTLINE

        self.next_button = ar.Sprite(data.FILES['next_button'], self.k)
        self.next_button.center_x = 3 * WIDTH / 4 + W_OUTLINE
        self.next_button.center_y = HEIGHT / 4 + H_OUTLINE

        self.prev_button = ar.Sprite(data.FILES['prev_button'], self.k)
        self.prev_button.center_x = WIDTH / 4 + W_OUTLINE
        self.prev_button.center_y = HEIGHT / 4 + H_OUTLINE

        first_player_selection, self.first_dropdown = create_tool_section('First player', ['Random'] + weapons_list,
                                                                          W_OUTLINE + WIDTH / 8 - 128 * self.k / 2,
                                                                          H_OUTLINE + HEIGHT / 2 - 345 * self.k / 2,
                                                                          128 * self.k, 345 * self.k)
        self.manager1 = gui.UIManager()
        self.manager1.add(first_player_selection)
        self.manager1.enable()

        second_player_selection, self.second_dropdown = create_tool_section('Second player',
                                                                            ['Random'] + weapons_list,
                                                                            W_OUTLINE + 7 * WIDTH / 8 - 128 * self.k / 2,
                                                                            H_OUTLINE + HEIGHT / 2 - 345 * self.k / 2,
                                                                            128 * self.k, 345 * self.k)
        self.manager2 = gui.UIManager()
        self.manager2.add(second_player_selection)
        self.manager2.enable()

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

    def on_update(self, _: float) -> None:
        if self.stop:
            return
        if self.same:
            self.manager2.disable()
            self.second_dropdown.value = self.first_dropdown.value
        else:
            self.manager2.enable()
        if self.first_button in self.editor_buttons and self.mode != StartGameMenuModes.editor_levels_change:
            self.editor_buttons = ar.SpriteList()

    def close(self, ended: bool = True) -> None:
        self.manager1.disable()
        self.manager2.disable()
        self.manager.disable()
        if ended:
            game_settings['running'].set_false()
        super().close()

    def on_draw(self) -> None:
        self.clear()
        match self.mode:
            case StartGameMenuModes.normal:
                self.buttons.draw()
                self.manager.draw()
                self.manager1.draw()
                self.manager2.draw()
            case StartGameMenuModes.level_changing:
                self.level_change_buttons.draw()
            case StartGameMenuModes.editor_levels_change:
                self.editor_buttons.draw()
                if self.first_button not in self.editor_buttons:
                    ar.draw_text('No levels in editor', self.width / 2 - 19 * 11 * self.k, self.height / 2,
                                 ar.color.BLACK, 40 * self.k)
                else:
                    if self.fourth_button in self.editor_buttons:
                        ar.draw_text(self.texts[3], 3 * WIDTH / 4 + W_OUTLINE - len(self.texts[3]) * 4 * self.k,
                                     self.height / 2, ar.color.RED, 20 * self.k)
                    if self.third_button in self.editor_buttons:
                        ar.draw_text(self.texts[2], WIDTH / 4 + W_OUTLINE - len(self.texts[2]) * 4 * self.k, self.height / 2,
                                     ar.color.RED, 20 * self.k)
                    if self.second_button in self.editor_buttons:
                        ar.draw_text(self.texts[1], 3 * WIDTH / 4 + W_OUTLINE - len(self.texts[1]) * 4 * self.k,
                                     3 * self.height / 4, ar.color.RED, 20 * self.k)
                    ar.draw_text(self.texts[0], WIDTH / 4 + W_OUTLINE - len(self.texts[0]) * 4 * self.k, 3 * self.height / 4,
                                 ar.color.RED, 20 * self.k)

    def on_key_press(self, key: int, _: int) -> None:
        if key == ar.key.ESCAPE:
            self.close(False)

    def update_editor_levels(self) -> None:
        self.editor_buttons = ar.SpriteList()
        self.mode = StartGameMenuModes.editor_levels_change
        levels = data.get_levels_list()
        ln = len(levels)
        cnt = ln // 4 if ln % 4 else ln // 4 - 1
        if self.page > cnt != -1:
            self.page = cnt
        if cnt != -1:
            match ln - self.page * 4:
                case 1:
                    self.editor_buttons.append(self.first_button)
                    self.texts[0] = levels[-1]
                case 2:
                    self.editor_buttons.append(self.first_button)
                    self.editor_buttons.append(self.second_button)
                    self.texts[0], self.texts[1] = levels[-2], levels[-1]
                case 3:
                    self.editor_buttons.append(self.first_button)
                    self.editor_buttons.append(self.second_button)
                    self.editor_buttons.append(self.third_button)
                    self.texts[0], self.texts[1], self.texts[2] = levels[-3], levels[-2], levels[-1]
                case _:
                    self.editor_buttons.append(self.first_button)
                    self.editor_buttons.append(self.second_button)
                    self.editor_buttons.append(self.third_button)
                    self.editor_buttons.append(self.fourth_button)
                    fst, snd, trd, fth = self.page * 4, self.page * 4 + 1, self.page * 4 + 2, self.page * 4 + 3
                    self.texts[0], self.texts[1], self.texts[2], self.texts[3] = (levels[fst], levels[snd],
                                                                              levels[trd], levels[fth])
        if self.page:
            self.editor_buttons.append(self.prev_button)
        if self.page != cnt and cnt != -1:
            self.editor_buttons.append(self.next_button)
        self.editor_levels = levels

    def start_game(self) -> None:
        self.close(False)
        first_player = self.first_dropdown.value
        second_player = self.second_dropdown.value

        level = self.level
        match self.random:
            case 0:
                level = 'Random'
            case 1:
                level = 'Random_standard'
            case 2:
                level = 'Random_editor'
        self.stop = True
        restart.set_false()
        game = Game(first_player, second_player, self.same, level, restart)
        game.run()

    def change_same(self) -> None:
        self.same = not self.same
        if self.same:
            self.same_button.texture = self.same_button_enabled.texture
        else:
            self.same_button.texture = self.same_button_disabled.texture

    def normal_click(self, x: float, y: float) -> None:
        if (self.start_button.right >= x >= self.start_button.left
                and self.start_button.top >= y >= self.start_button.bottom):
            self.start_game()
        elif (self.same_button.right >= x >= self.same_button.left
              and self.same_button.top >= y >= self.same_button.bottom):
            self.change_same()
        elif (self.random_button.right >= x >= self.random_button.left
              and self.random_button.top >= y >= self.random_button.bottom):
            self.change_random()
        elif (self.level_button.right >= x >= self.level_button.left
              and self.level_button.top >= y >= self.level_button.bottom):
            self.change_level()

    def change_level(self) -> None:
        if self.random == 3:
            self.mode = StartGameMenuModes.level_changing

    def change_random(self) -> None:
        self.random += 1
        self.random %= 4
        match self.random:
            case 0:
                self.random_button.texture = self.random_button_all.texture
            case 1:
                if self.editor_levels:
                    self.random_button.texture = self.random_button_standard.texture
                else:
                    self.change_random()
            case 2:
                if self.editor_levels:
                    self.random_button.texture = self.random_button_editor.texture
                else:
                    self.change_random()
            case 3:
                self.random_button.texture = self.random_button_disabled.texture

    def level_click(self, x: float, y: float) -> None:
        self.mode = StartGameMenuModes.normal
        if (self.creator_button.right >= x >= self.creator_button.left
                and self.creator_button.top >= y >= self.creator_button.bottom):
            self.level = data.LEVELS['Creator']
        elif (self.paradigm_button.right >= x >= self.paradigm_button.left
              and self.paradigm_button.top >= y >= self.paradigm_button.bottom):
            self.level = data.LEVELS['Paradigm']
        elif (self.battle_button.right >= x >= self.battle_button.left
              and self.battle_button.top >= y >= self.battle_button.bottom):
            self.level = data.LEVELS['Battle Of Everything']
        elif (self.room_button.right >= x >= self.room_button.left
              and self.room_button.top >= y >= self.room_button.bottom):
            self.level = data.LEVELS['Room']
        elif (self.editor_button.right >= x >= self.editor_button.left
              and self.editor_button.top >= y >= self.editor_button.bottom):
            self.update_editor_levels()

    def editor_levels_click(self, x: float, y: float) -> None:
        self.mode = StartGameMenuModes.normal
        if (self.first_button in self.editor_buttons
                and self.first_button.right >= x >= self.first_button.left
                and self.first_button.top >= y >= self.first_button.bottom):
            self.level = data.get_editor_level_path(self.editor_levels[self.page * 4])
            self.page = 0
        elif (self.second_button in self.editor_buttons
              and self.second_button.right >= x >= self.second_button.left
              and self.second_button.top >= y >= self.second_button.bottom):
            self.level = data.get_editor_level_path(self.second_level[self.page * 4 + 1])
            self.page = 0
        elif (self.third_button in self.editor_buttons
              and self.third_button.right >= x >= self.third_button.left
              and self.third_button.top >= y >= self.third_button.bottom):
            self.level = data.get_editor_level_path(self.third_level[self.page * 4 + 2])
            self.page = 0
        elif (self.fourth_button in self.editor_buttons
              and self.fourth_button.right >= x >= self.fourth_button.left
              and self.fourth_button.top >= y >= self.fourth_button.bottom):
            self.level = data.get_editor_level_path(self.fourth[self.page * 4 + 3])
            self.page = 0
        elif (self.prev_button in self.editor_buttons
              and self.prev_button.right >= x >= self.prev_button.left
              and self.prev_button.top >= y >= self.prev_button.bottom):
            self.page -= 1
            self.update_editor_levels()
        elif (self.next_button in self.editor_buttons
              and self.next_button.right >= x >= self.next_button.left
              and self.next_button.top >= y >= self.next_button.bottom):
            self.page += 1
            self.update_editor_levels()

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            match self.mode:
                case StartGameMenuModes.normal:
                    self.normal_click(x, y)
                case StartGameMenuModes.level_changing:
                    self.level_click(x, y)
                case StartGameMenuModes.editor_levels_change:
                    self.editor_levels_click(x, y)
