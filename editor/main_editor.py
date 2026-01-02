import arcade as ar


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Редактор. Работа с уровнями"

class Level_Menu(ar.View):
    def __init__(self):
        super().__init__()
        self.manager = ar.gui.UIManager()

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


def main():
    window = ar.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    Level_view = Level_Menu()
    window.show_view(Level_view)
    ar.run()

if __name__ == '__main__':
    main()
