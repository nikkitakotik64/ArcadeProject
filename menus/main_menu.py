from game.game import PvP as Arena
from main import game_settings
import arcade as ar
from screen import CELL_SIDE, W, H
from data.savings import data
from editor.main_editor import main as editor_start


class MainMenu(ar.Window):
    k = CELL_SIDE / 16
    sound_button_enabled = ar.Sprite(data.FILES['sound_button_enabled'], CELL_SIDE / 40)
    sound_button_disabled = ar.Sprite(data.FILES['sound_button_disabled'], CELL_SIDE / 40)

    def __init__(self) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)
        ar.set_background_color(ar.color.DARK_RED)
        self.buttons = ar.SpriteList()

        self.start_button = ar.Sprite(data.FILES['start_button'], self.k)
        self.start_button.center_x = W / 2
        self.start_button.center_y = 3 * H / 5
        self.buttons.append(self.start_button)

        self.editor_button = ar.Sprite(data.FILES['editor_button'], self.k)
        self.editor_button.center_x = W / 2
        self.editor_button.center_y = 2 * H / 5
        self.buttons.append(self.editor_button)

        self.quit_button = ar.Sprite(data.FILES['quit_button'], self.k)
        self.quit_button.center_x = W / 2
        self.quit_button.center_y = H / 5
        self.buttons.append(self.quit_button)

        if game_settings['sounds']:
            self.sound_button = ar.Sprite(data.FILES['sound_button_enabled'], self.k / 2.5)
        else:
            self.sound_button = ar.Sprite(data.FILES['sound_button_disabled'], self.k / 2.5)
        self.sound_button.center_x = W - CELL_SIDE * 2
        self.sound_button.center_y = H - CELL_SIDE * 2
        self.buttons.append(self.sound_button)

    def on_draw(self) -> None:
        self.clear()
        self.buttons.draw()

    def change_sound(self) -> None:
        game_settings['sounds'] = not game_settings['sounds']
        data.save_sound_settings(game_settings['sounds'])
        if game_settings['sounds']:
            self.sound_button.texture = self.sound_button_enabled.texture
        else:
            self.sound_button.texture = self.sound_button_disabled.texture

    def start_game(self) -> None:
        self.close(False)
        # TODO
        # start = StartGameMenu()
        # start.run()

    def start_editor(self) -> None:
        self.close(False)
        editor_start()

    def click(self, x: float, y: float) -> None:
        if (self.start_button.right >= x >= self.start_button.left
                and self.start_button.top >= y >= self.start_button.bottom):
            self.start_game()
        elif (self.editor_button.right >= x >= self.editor_button.left
              and self.editor_button.top >= y >= self.editor_button.bottom):
            self.start_editor()
        elif (self.quit_button.right >= x >= self.quit_button.left
              and self.quit_button.top >= y >= self.quit_button.bottom):
            self.close()
        elif (self.sound_button.right >= x >= self.sound_button.left
              and self.sound_button.top >= y >= self.sound_button.bottom):
            self.change_sound()

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            self.click(x, y)

    def close(self, ended: bool = True) -> None:
        if ended:
            game_settings['running'].set_false()
        super().close()


def main():
    while game_settings['running'].is_running():
        game = MainMenu()
        game.run()


if __name__ == '__main__':
    main()
