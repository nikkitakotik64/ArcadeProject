import arcade as ar
from main import game_settings
from data.savings import data
from screen import CELL_SIDE, W_OUTLINE, WIDTH, H_OUTLINE, HEIGHT


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

        self.first_player_button = ar.Sprite(data.FILES['player_button'], self.k)
        self.first_player_button.center_x = W_OUTLINE + WIDTH / 8
        self.first_player_button.center_y = H_OUTLINE + HEIGHT / 2
        self.buttons.append(self.first_player_button)

    def close(self, ended: bool = True) -> None:
        if ended:
            game_settings['running'].set_false()
        super().close()

    def on_draw(self) -> None:
        self.clear()
        self.buttons.draw()

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

    def change_random(self) -> None:
        self.random = not self.random
        if self.random:
            self.random_button.texture = self.random_button_enabled.texture
        else:
            self.random_button.texture = self.random_button_disabled.texture

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            self.click(x, y)
