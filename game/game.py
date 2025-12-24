import consts
from events_id import EventsID
from sprites.player import PlayerStatus
from data.savings import data
from screen import *
import arcade as ar
from sprites.world_wall import WorldWall
from sprites.player import Player


class Game(ar.Window):
    def __init__(self) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)
        self.k = CELL_SIDE / 16
        self.events = list()

        self.world_walls = set()
        self.world_walls.add(WorldWall(data.FILES['hor_world_wall'], self.width / 800, self.width / 2, -2))
        self.world_walls.add(WorldWall(data.FILES['hor_world_wall'], self.width / 800,
                                       self.width / 2, self.height + 2))
        self.world_walls.add(WorldWall(data.FILES['vert_world_wall'], self.height / 450,
                                       -CELL_SIDE / 2, self.height / 2))
        self.world_walls.add(WorldWall(data.FILES['vert_world_wall'], self.height / 450,
                                       self.width + CELL_SIDE / 2, self.height / 2))
        self.wall_list = ar.SpriteList()
        self.func_objects = ar.SpriteList()

        self.player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                             data.FILES['player_laying'], self.k / 6, 1, 10)
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

        self.data_timer = data.get_data_timer()

    def update_player_sprite(self) -> None:
        self.player_sprite = self.player.get_sprite()
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()
        self.wall_list.draw()
        self.func_objects.draw()

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
        if key == ar.key.D:
            self.events.append(EventsID.RIGHT)
        if key == ar.key.A:
            self.events.append(EventsID.LEFT)
        if key == ar.key.S:
            self.player.down()
        if key == ar.key.SPACE:
            self.events.append(EventsID.SHOOT)

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == ar.key.A:
            self.events.remove(EventsID.LEFT)
        if key == ar.key.D:
            self.events.remove(EventsID.RIGHT)
        if key == ar.key.W and EventsID.UP in self.events:
            self.events.remove(EventsID.UP)
        if key == ar.key.SPACE:
            self.events.remove(EventsID.SHOOT)
