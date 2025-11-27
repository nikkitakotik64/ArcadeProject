from screen import *
import consts
import events_id

# потом нормально сделаю комментарии для всего, ждите :)

class App(ar.Window):  # собственно окно
    def __init__(self) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)
        self.k = WIDTH / 800
        self.player_falling = 0
        self.events = list()
        self.player_sprite = ar.sprite.Sprite(data.FILES['player'], self.k / 10)
        self.player_sprite.center_x, self.player_sprite.center_y = cell_pos(1, 10)
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.wall_list = ar.SpriteList()
        wall = ar.sprite.Sprite(data.FILES['wall'], self.k)
        wall.center_x, wall.center_y = self.width // 2, 0
        self.wall_list.append(wall)
        # TODO: задать стены
        self.data_timer = data.get_data_timer()
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()
        self.wall_list.draw()

    def events_update(self) -> None:
        if events_id.LEFT in self.events:
            if events_id.RIGHT in self.events:
                self.player_sprite.change_x = 0
            else:
                self.player_sprite.change_x = -consts.SPEED * self.k
        elif events_id.RIGHT in self.events:
            self.player_sprite.change_x = consts.SPEED * self.k
        else:
            self.player_sprite.change_x = 0
        if events_id.UP in self.events and not self.player_falling:
            self.player_sprite.change_y = consts.JUMP_SPEED * self.k
            self.player_falling = 1
        if self.player_sprite.change_y < 0:
            self.player_falling = 2
        if not self.player_sprite.change_y and self.player_falling == 2:
            self.player_falling = 0

    def on_update(self, delta_time: float) -> None:
        self.events_update()
        self.player_physics.update()

        if self.data_timer <= 0:
            self.data_timer = data.get_data_timer()
            data.save()
        else:
            self.data_timer -= delta_time

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == ar.key.UP or key == ar.key.W:
            self.events.append(events_id.UP)
        if key == ar.key.RIGHT or key == ar.key.D:
            self.events.append(events_id.RIGHT)
        if key == ar.key.LEFT or key == ar.key.A:
            self.events.append(events_id.LEFT)
        if key == ar.key.SPACE:
            self.events.append(events_id.SHOOT)

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == ar.key.LEFT or key == ar.key.A:
            self.events.remove(events_id.LEFT)
        if key == ar.key.RIGHT or key == ar.key.D:
            self.events.remove(events_id.RIGHT)
        if key == ar.key.UP or key == ar.key.W:
            self.events.remove(events_id.UP)
        if key == ar.key.SPACE:
            self.events.remove(events_id.SHOOT)



if __name__ == "__main__":
    game = App()
    game.run()
