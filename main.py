from screen import *
import consts
import events_id


class App(ar.Window):  # Собственно окно игры
    def __init__(self) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)  # окно именем "Game" на весь экран
        self.k = WIDTH / 800  # коэффицент отношения размеров к тем, под которые была сделана физика

        self.player_falling = 0  # переменная для обработки состояния игрока
        # TODO: вынести игрока в отдельный класс
        self.events = list()  # список событий
        self.player_sprite = ar.sprite.Sprite(data.FILES['player'], self.k / 10)  # Текстура игрока
        self.player_sprite.center_x, self.player_sprite.center_y = cell_pos(1, 10)
        # размещаем игрока во второй клетке по горизонтали и во второй по вертикали (если считать снизу)
        self.player_list = ar.SpriteList()  # группа спрайтов для игроков
        self.player_list.append(self.player_sprite)  # добавляем спрайт в группу

        self.wall_list = ar.SpriteList()  # список для стен
        wall = ar.sprite.Sprite(data.FILES['wall'], self.k)  # пол
        wall.center_x, wall.center_y = self.width // 2, 0
        self.wall_list.append(wall)
        # TODO: задать стены через отдельный класс по-нормальному

        self.data_timer = data.get_data_timer()  # создаём таймер для автосохранения
        # физика для игрока
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

    def on_draw(self) -> None:  # отрисовка
        # self.clear() обязательно, далее нужно отрисовать все необходимые списки спрайтов
        self.clear()
        self.player_list.draw()
        self.wall_list.draw()

    def events_update(self) -> None:  # обработка событий
        # Если нажата кнопка влево, то скорость с минусом, направо - с плюсом
        # Если сразу две кнопки или ни одной - то скорость 0
        if events_id.LEFT in self.events:
            if events_id.RIGHT in self.events:
                self.player_sprite.change_x = 0
            else:
                self.player_sprite.change_x = -consts.SPEED * self.k
        elif events_id.RIGHT in self.events:
            self.player_sprite.change_x = consts.SPEED * self.k
        else:
            self.player_sprite.change_x = 0

        # если игрок падает, то player_falling становится 2
        # если игрок упал на землю (то есть player_falling было 2), то player_falling становится 0
        # если игрок стоит на земле (player_falling == 0), то он может прыгнуть
        # если игрок прыгнул, то player_falling ставим 1 (он не падает, но при этом прыгать не может, летит крч)
        if self.player_sprite.change_y < 0:
            self.player_falling = 2
        if not self.player_sprite.change_y and self.player_falling == 2:
            self.player_falling = 0
        if events_id.UP in self.events and self.player_falling == 0:
            self.player_sprite.change_y = consts.JUMP_SPEED * self.k
            self.player_falling = 1

    def on_update(self, delta_time: float) -> None:
        # цикл обработки, вызывается +- 60 раз в секунду
        self.events_update()  # обрабатываем события
        self.player_physics.update()  # обновляем физику

        # проверяем, не нужно ли сделать автосэйв
        if self.data_timer <= 0:
            self.data_timer = data.get_data_timer()
            data.save()
        else:
            self.data_timer -= delta_time

    def on_key_press(self, key: int, modifiers: int) -> None:
        # обработка нажатия
        # по факту при нажатии кнопки в список добавляется соответвующее событие
        # таким образом можно узнать, нажаты ли две кнопки одновременно
        # мб это можно сделать проще, но я не ресёрчил настолько, мб потом займусь
        if key == ar.key.W:
            self.events.append(events_id.UP)
        if key == ar.key.D:
            self.events.append(events_id.RIGHT)
        if key == ar.key.A:
            self.events.append(events_id.LEFT)
        if key == ar.key.SPACE:
            self.events.append(events_id.SHOOT)

    def on_key_release(self, key: int, modifiers: int) -> None:
        # когда игрок отпускает кнопку, соответвующее событие удаляется из списка
        if key == ar.key.A:
            self.events.remove(events_id.LEFT)
        if key == ar.key.D:
            self.events.remove(events_id.RIGHT)
        if key == ar.key.W:
            self.events.remove(events_id.UP)
        if key == ar.key.SPACE:
            self.events.remove(events_id.SHOOT)



if __name__ == "__main__":
    # создание и запуск окна
    game = App()
    game.run()
