from screen import *
import consts
from events_id import EventsID
from sprites.player import Player, PlayerStatus
from sprites.world_wall import WorldWall
from sprites.wall import Wall
from data.savings import data
from level_types import LevelType


class App(ar.Window):
    def __init__(self, level_id: int = -1) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)
        self.k = CELL_SIDE / 16
        self.events = list()

        self.wall_list = ar.SpriteList()
        self.wall_list.append(WorldWall(data.FILES['hor_world_wall'], self.k, self.width / 2, -1))
        self.wall_list.append(WorldWall(data.FILES['hor_world_wall'], self.k, self.width / 2, self.height + 1))
        self.wall_list.append(WorldWall(data.FILES['vert_world_wall'], self.k, -CELL_SIDE / 2, self.height / 2))
        self.wall_list.append(WorldWall(data.FILES['vert_world_wall'], self.k, self.width + CELL_SIDE / 2, self.height / 2))
        if level_id == -1:  # TODO: тестовый вариант, удалить !
            self.wall_list.append(Wall(-1, self.k / 8, 2, 2))
            self.wall_list.append(Wall(-1, self.k / 8, 0, 2))
            self.wall_list.append(Wall(-1, self.k / 8, 1, 2))
            self.level_type = LevelType.ROOMS
        else:
            level, level_type = data.get_level_info(level_id)
            # TODO: сделать


        self.player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                             data.FILES['player_laying'], self.k / 6, 1, 10)
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

        self.data_timer = data.get_data_timer()
        self.setup()

    def update_player_sprite(self) -> None:
        self.player_sprite = self.player.get_sprite()
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

    def setup(self) -> None:
        self.events = list()
        self.player.move(1, 10)
        self.player_sprite.center_x, self.player_sprite.center_y = cell_center(1, 10)
        self.data_timer = data.get_data_timer()

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()
        self.wall_list.draw()

    def events_update(self) -> None:
        if EventsID.LEFT in self.events:
            if EventsID.RIGHT in self.events:
                self.player_sprite.change_x = 0
            else:
                if self.player.status == PlayerStatus.SITING:
                    self.player_sprite.change_x = -consts.SITING_SPEED * self.k
                elif self.player.status != PlayerStatus.LAYING:
                    self.player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.RIGHT in self.events:
            if self.player.status == PlayerStatus.SITING:
                self.player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.player.status != PlayerStatus.LAYING:
                self.player_sprite.change_x = consts.SPEED * self.k
        else:
            self.player_sprite.change_x = 0

        if self.player_sprite.change_y < 0:
            self.player.set_status(PlayerStatus.FALLING)
        if not self.player_sprite.change_y and self.player.get_status() == PlayerStatus.FALLING:
            self.player.set_status(PlayerStatus.NORMAL)
        if EventsID.UP in self.events and self.player.get_status() == PlayerStatus.NORMAL:
            self.player_sprite.change_y = consts.JUMP_SPEED * self.k
            self.player.set_status(PlayerStatus.JUMPING)

    def on_update(self, delta_time: float) -> None:
        self.events_update()
        self.player_physics.update()
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_list.update(delta_time)
        self.wall_list.update(delta_time)

        if self.data_timer <= 0:
            self.data_timer = data.get_data_timer()
            data.save()
        else:
            self.data_timer -= delta_time

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == ar.key.ESCAPE:
            ar.exit()
        if key == ar.key.W:
            if self.player.get_status() != PlayerStatus.SITING and self.player.get_status() != PlayerStatus.LAYING:
                self.events.append(EventsID.UP)
            else:
                self.player.up()
                self.player_sprite = self.player.get_sprite()
                self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                                 gravity_constant=consts.GRAVITY * self.k)
        if key == ar.key.D:
            self.events.append(EventsID.RIGHT)
        if key == ar.key.A:
            self.events.append(EventsID.LEFT)
        if key == ar.key.S:
            self.player.down()
            self.player_sprite = self.player.get_sprite()
            self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                             gravity_constant=consts.GRAVITY * self.k)
        if key == ar.key.SPACE:
            self.events.append(EventsID.SHOOT)

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == ar.key.A:
            self.events.remove(EventsID.LEFT)
        if key == ar.key.D:
            self.events.remove(EventsID.RIGHT)
        if key == ar.key.W:
            self.events.remove(EventsID.UP)
        if key == ar.key.SPACE:
            self.events.remove(EventsID.SHOOT)


if __name__ == "__main__":
    game = App()
    game.run()
