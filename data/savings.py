import os

data_folder = os.path.dirname(__file__)


class Data:  # класс, читающий и записывающий данные
    FILES = {
        'player': data_folder + '/player.png',
        'wall': data_folder + '/wall.png'
    }

    def __init__(self) -> None:
        # TODO: сделать нормальное чтение и запись в файл
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:
        return self.data_timer

    def save(self) -> None:
        # сохранить данные в файл
        pass


data = Data()
