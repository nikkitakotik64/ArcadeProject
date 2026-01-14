import consts
from events_id import EventsID
from sprites.player import PlayerStatus
from data.savings import data
from screen import *
import arcade as ar
from sprites.world_wall import WorldWall
from sprites.player import Player
from game_types import Direction


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
        self.functional_objects = ar.SpriteList()
        self.decor = ar.SpriteList()

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
        self.functional_objects.draw()

    def events_update(self) -> None:
        if EventsID.left in self.events:
            if EventsID.right in self.events:
                self.player_sprite.change_x = 0
            else:
                self.player.set_direction(Direction.left)
                if self.player.status == PlayerStatus.siting:
                    self.player_sprite.change_x = -consts.SITING_SPEED * self.k
                elif self.player.status != PlayerStatus.laying:
                    self.player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.right in self.events:
            self.player.set_direction(Direction.right)
            if self.player.status == PlayerStatus.siting:
                self.player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.player.status != PlayerStatus.laying:
                self.player_sprite.change_x = consts.SPEED * self.k
        else:
            self.player_sprite.change_x = 0

        if self.player_sprite.change_y < 0:
            self.player.set_status(PlayerStatus.falling)
        if not self.player_sprite.change_y and self.player.get_status() == PlayerStatus.falling:
            self.player.set_status(PlayerStatus.normal)
        if EventsID.up in self.events and self.player.get_status() == PlayerStatus.normal:
            self.player_sprite.change_y = consts.JUMP_SPEED * self.k
            self.player.set_status(PlayerStatus.jumping)

        if EventsID.shoot in self.events:
            is_success, arr = self.player.shoot()
            if is_success:
                pass
                # TODO: shoot
        if EventsID.reload in self.events:
            self.player.reload()

    def on_update(self, delta_time: float) -> None:
        self.events_update()
        self.player.on_update(delta_time)
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
            if self.player.get_status() != PlayerStatus.siting and self.player.get_status() != PlayerStatus.laying:
                self.events.append(EventsID.up)
            else:
                self.player.up()
        if key == ar.key.D:
            self.events.append(EventsID.right)
        if key == ar.key.A:
            self.events.append(EventsID.left)
        if key == ar.key.S:
            self.player.down()
        if key == ar.key.SPACE:
            self.events.append(EventsID.shoot)
        if key == ar.key.R:
            self.events.append(EventsID.reload)

    def on_key_release(self, key: int, modifiers: int) -> None:
        try:
            if key == ar.key.A:
                self.events.remove(EventsID.left)
        except ValueError:
            pass
        try:
            if key == ar.key.D:
                self.events.remove(EventsID.right)
        except ValueError:
            pass
        try:
            if key == ar.key.W and EventsID.up in self.events:
                self.events.remove(EventsID.up)
        except ValueError:
            pass
        try:
            if key == ar.key.SPACE:
                self.events.remove(EventsID.shoot)
        except ValueError:
            pass
        try:
            if key == ar.key.R:
                self.events.remove(EventsID.reload)
        except ValueError:
            pass
