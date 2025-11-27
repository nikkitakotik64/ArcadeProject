import os

data_folder = os.path.dirname(__file__)
# TODO: сделать нормальное чтение и запись в файл


class Data:  # класс, читающий и записывающий данные
    FILES = {
        'player': data_folder + '/player.png',
        'wall': data_folder + '/wall.png'
    }

    def __init__(self) -> None:
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:  # Время до автосохранения данных
        return self.data_timer

    def save(self) -> None:
        # сохранить данные в файл
        pass


data = Data()
