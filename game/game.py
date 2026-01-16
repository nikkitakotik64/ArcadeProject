import consts
from events_id import EventsID
from sprites.player import PlayerStatus
from data.savings import data
from screen import *
import arcade as ar
from sprites.world_wall import WorldWall
from sprites.player import Player
from game_types import Direction
from sprites.bullet import Bullet


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
        self.wall_list.extend(self.world_walls)
        self.functional_objects = ar.SpriteList()
        self.decor = ar.SpriteList()
        self.bullets = ar.SpriteList()
        self.enemies = ar.SpriteList()

        self.player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                             data.FILES['player_laying'], self.k / 6, 1, 10)
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)
        self.enemies_physics = [ar.PhysicsEnginePlatformer(enemy, self.wall_list,
                                                           gravity_constant=consts.GRAVITY * self.k)
                                for enemy in self.enemies]

        self.data_timer = data.get_data_timer()

    def update_enemies(self) -> None:
        self.enemies_physics = [ar.PhysicsEnginePlatformer(enemy, self.wall_list,
                                                           gravity_constant=consts.GRAVITY * self.k)
                                for enemy in self.enemies]

    def update_player_sprite(self) -> None:
        self.player_sprite = self.player.get_sprite()
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)

    def on_draw(self) -> None:
        self.clear()
        self.enemies.draw()
        self.player_list.draw()
        self.bullets.draw()
        self.wall_list.draw()
        self.functional_objects.draw()

    def events_update(self) -> None:
        if EventsID.left in self.events:
            if EventsID.right in self.events:
                self.player_sprite.change_x = 0
            else:
                self.player.set_direction(Direction.left)
                if self.player.get_status() == PlayerStatus.siting:
                    self.player_sprite.change_x = -consts.SITING_SPEED * self.k
                elif self.player.get_status() != PlayerStatus.laying:
                    self.player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.right in self.events:
            self.player.set_direction(Direction.right)
            if self.player.get_status() == PlayerStatus.siting:
                self.player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.player.get_status() != PlayerStatus.laying:
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
            bullets = self.player.shoot()
            if bullets:
                for x, y, bullet_characteristics, angle in bullets:
                    bullet = Bullet(x, y, bullet_characteristics, angle, 1 / 4, [self.player_sprite])
                    self.bullets.append(bullet)

        if EventsID.reload in self.events:
            self.player.reload()

    def bullets_update(self, delta_time: float) -> None:
        for bullet in self.bullets:
            bullet.on_update(delta_time)
            collision_list = ar.check_for_collision_with_list(bullet, self.wall_list)
            if collision_list:
                self.bullets.remove(bullet)
        sprites = ar.SpriteList()
        sprites.extend(self.enemies)
        sprites.append(self.player_sprite)
        for sprite in sprites:
            bullets = ar.check_for_collision_with_list(sprite, self.bullets)
            for bullet in bullets:
                if sprite in bullet.get_exceptions():
                    continue
                sprite.damage(bullet.get_damage())
                bullet.pierce(sprite)
                if not bullet.get_damage():
                    self.bullets.remove(bullet)
                if not sprite.get_hp():
                    try:
                        self.enemies.remove(sprite)
                    except ValueError:
                        print('Player dead')

    def on_update(self, delta_time: float) -> None:
        self.events_update()
        self.player.on_update(delta_time)
        self.player_physics.update()
        self.enemies.update()
        for physics in self.enemies_physics:
            physics.update()
        self.player_list.update(delta_time)
        self.wall_list.update(delta_time)
        self.bullets_update(delta_time)

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

    def on_key_release(self, key: int, _) -> None:
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


class PvP(Game):
    def __init__(self) -> None:
        super().__init__()
        self.second_player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                                    data.FILES['player_laying'], self.k / 6, 1, 12, is_second=True)
        self.second_player_sprite = self.second_player.get_sprite()
        self.second_player_list = ar.SpriteList()
        self.second_player_list.append(self.second_player_sprite)
        self.second_player_physics = ar.PhysicsEnginePlatformer(self.second_player_sprite, self.wall_list,
                                                                gravity_constant=consts.GRAVITY * self.k)

    def update_second_player_sprite(self) -> None:
        self.second_player_sprite = self.second_player.get_sprite()
        self.second_player_physics = ar.PhysicsEnginePlatformer(self.second_player_sprite, self.wall_list,
                                                                gravity_constant=consts.GRAVITY * self.k)
        self.second_player_list = ar.SpriteList()
        self.second_player_list.append(self.second_player_sprite)

    def events_update(self) -> None:
        super().events_update()
        if EventsID.sec_left in self.events:
            if EventsID.sec_right in self.events:
                self.second_player_sprite.change_x = 0
            else:
                self.second_player.set_direction(Direction.left)
                if self.second_player.get_status() == PlayerStatus.siting:
                    self.second_player_sprite.change_x = -consts.SITING_SPEED * self.k
                elif self.second_player.get_status() != PlayerStatus.laying:
                    self.second_player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.sec_right in self.events:
            self.second_player.set_direction(Direction.right)
            if self.second_player.get_status() == PlayerStatus.siting:
                self.second_player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.second_player.get_status() != PlayerStatus.laying:
                self.second_player_sprite.change_x = consts.SPEED * self.k
        else:
            self.second_player_sprite.change_x = 0

        if self.second_player_sprite.change_y < 0:
            self.second_player.set_status(PlayerStatus.falling)
        if not self.second_player_sprite.change_y and self.second_player.get_status() == PlayerStatus.falling:
            self.second_player.set_status(PlayerStatus.normal)
        if EventsID.sec_up in self.events and self.second_player.get_status() == PlayerStatus.normal:
            self.second_player_sprite.change_y = consts.JUMP_SPEED * self.k
            self.second_player.set_status(PlayerStatus.jumping)

        if EventsID.sec_shoot in self.events:
            bullets = self.second_player.shoot()
            if bullets:
                for x, y, bullet_characteristics, angle in bullets:
                    bullet = Bullet(x, y, bullet_characteristics, angle, 1 / 4, [self.second_player_sprite])
                    self.bullets.append(bullet)

        if EventsID.sec_reload in self.events:
            self.second_player.reload()

    def on_draw(self) -> None:
        self.clear()
        self.enemies.draw()
        self.player_list.draw()
        self.second_player_list.draw()
        self.bullets.draw()
        self.wall_list.draw()
        self.functional_objects.draw()

    def bullets_update(self, delta_time: float) -> None:
        for bullet in self.bullets:
            bullet.on_update(delta_time)
            collision_list = ar.check_for_collision_with_list(bullet, self.wall_list)
            if collision_list:
                self.bullets.remove(bullet)
        sprites = ar.SpriteList()
        sprites.extend(self.enemies)
        sprites.append(self.player_sprite)
        sprites.append(self.second_player_sprite)
        for sprite in sprites:
            bullets = ar.check_for_collision_with_list(sprite, self.bullets)
            for bullet in bullets:
                if sprite in bullet.get_exceptions():
                    continue
                sprite.damage(bullet.get_damage())
                bullet.pierce(sprite)
                if not bullet.get_damage():
                    self.bullets.remove(bullet)
                if not sprite.get_hp():
                    try:
                        self.enemies.remove(sprite)
                    except ValueError:
                        print('Player dead')

    def on_update(self, delta_time: float) -> None:
        self.events_update()
        self.player.on_update(delta_time)
        self.player_physics.update()
        self.second_player.on_update(delta_time)
        self.second_player_physics.update()
        self.enemies.update()
        for physics in self.enemies_physics:
            physics.update()
        self.wall_list.update(delta_time)
        self.bullets_update(delta_time)

        if self.data_timer <= 0:
            self.data_timer = data.get_data_timer()
            data.save()
        else:
            self.data_timer -= delta_time

    def on_key_press(self, key: int, modifiers: int) -> None:
        super().on_key_press(key, modifiers)
        if key == ar.key.UP:
            if (self.second_player.get_status() != PlayerStatus.siting
                    and self.second_player.get_status() != PlayerStatus.laying):
                self.events.append(EventsID.sec_up)
            else:
                self.second_player.up()
        if key == ar.key.RIGHT:
            self.events.append(EventsID.sec_right)
        if key == ar.key.LEFT:
            self.events.append(EventsID.sec_left)
        if key == ar.key.DOWN:
            self.second_player.down()

    def on_key_release(self, key: int, _) -> None:
        super().on_key_release(key, 0)
        try:
            if key == ar.key.LEFT:
                self.events.remove(EventsID.sec_left)
        except ValueError:
            pass
        try:
            if key == ar.key.RIGHT:
                self.events.remove(EventsID.sec_right)
        except ValueError:
            pass
        try:
            if key == ar.key.UP:
                self.events.remove(EventsID.sec_up)
        except ValueError:
            pass

    def on_mouse_press(self, _: int, __: int, button: int, ___: int) -> None:
        if button == ar.MOUSE_BUTTON_LEFT:
            self.events.append(EventsID.sec_shoot)
        if button == ar.MOUSE_BUTTON_RIGHT:
            self.events.append(EventsID.sec_reload)

    def on_mouse_release(self, _: int, __: int, button: int, ___: int) -> None:
        try:
            if button == ar.MOUSE_BUTTON_LEFT:
                self.events.remove(EventsID.sec_shoot)
        except ValueError:
            pass
        try:
            if button == ar.MOUSE_BUTTON_RIGHT:
                self.events.remove(EventsID.sec_reload)
        except ValueError:
            pass
