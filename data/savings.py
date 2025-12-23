import os

data_folder = os.path.dirname(__file__)
# TODO: сделать нормальное чтение и запись в файл


class Data:
    FILES = {
        'player_staying': data_folder + '/player.png',
        'player_siting': data_folder + '/sit.png',
        'player_laying': data_folder + '/lay.png',
        'wall-1': data_folder + '/wall.png',  # тестовая стена без текстуры !
        'data': data_folder + '/data.game',
        'hor_world_wall': data_folder + '/hor_world_wall.png',
        'vert_world_wall': data_folder + '/vert_world_wall.png'
    }

    def __init__(self) -> None:
        self.data_timer = 60 * 5

    def get_data_timer(self) -> float:
        return self.data_timer

    def save(self) -> None:
        pass


data = Data()
