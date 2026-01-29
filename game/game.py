import consts
from events_id import EventsID
from sprites.player import PlayerStatus
from data.savings import data
from screen import *
import arcade as ar
from sprites.decor import Decor
from sprites.wall import Wall
from sprites.world_wall import WorldWall
from sprites.player import Player
from game_types import Direction
from sprites.bullet import Bullet, ShotgunBullet
from main import game_settings
from sprites.weapons import weapons_dict, weapons_list, Shotgun, weapons_sounds
from random import choice
from enum import Enum


class GameStatus(Enum):
    normal = 1
    paused = 2
    ended = 3


class Game(ar.Window):
    def __init__(self, first_player_weapon: str) -> None:
        super().__init__(1, 1, 'Game', fullscreen=True)
        self.status = GameStatus.normal
        self.k = CELL_SIDE / 16
        self.events = list()
        label = ar.Sprite(data.FILES['label'], self.k)
        label.center_x, label.center_y = self.width / 2, self.height / 2
        self.label = ar.SpriteList()
        self.label.append(label)

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
                             data.FILES['player_laying'], self.k / 6, 1, 0,
                             weapons_dict[first_player_weapon]())
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)
        self.enemies_physics = [ar.PhysicsEnginePlatformer(enemy, self.wall_list,
                                                           gravity_constant=consts.GRAVITY * self.k)
                                for enemy in self.enemies]

        self.data_timer = data.get_data_timer()

    def restart(self, first_player_weapon: str = 'Glock-18') -> None:
        self.status = GameStatus.normal
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

        self.player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                             data.FILES['player_laying'], self.k / 6, 1, 0,
                             weapons_dict[first_player_weapon]())
        self.player_sprite = self.player.get_sprite()
        self.player_list = ar.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_physics = ar.PhysicsEnginePlatformer(self.player_sprite, self.wall_list,
                                                         gravity_constant=consts.GRAVITY * self.k)

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
            elif self.player.get_status() == PlayerStatus.laying:
                self.player_sprite.change_x = -consts.LAYING_SPEED * self.k
            elif self.player.get_status() != PlayerStatus.laying:
                self.player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.right in self.events:
            self.player.set_direction(Direction.right)
            if self.player.get_status() == PlayerStatus.siting:
                self.player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.player.get_status() == PlayerStatus.laying:
                self.player_sprite.change_x = consts.LAYING_SPEED * self.k
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
                if game_settings['sounds']:
                    ar.play_sound(weapons_sounds[self.first_player_weapon])
                if isinstance(self.player.get_weapon(), Shotgun):
                    for x, y, bullet_characteristics, angle in bullets:
                        bullet = ShotgunBullet(x, y, bullet_characteristics, angle, self.k / 12, [self.player])
                        self.bullets.append(bullet)
                else:
                    for x, y, bullet_characteristics, angle in bullets:
                        bullet = Bullet(x, y, bullet_characteristics, angle, self.k / 12, [self.player])
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
                        self.status = GameStatus.ended

    def on_update(self, delta_time: float) -> None:
        if self.status != GameStatus.normal:
            return
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

        if (self.player_sprite.left < 0 or self.player_sprite.right > W
                or self.player_sprite.top > H or self.player_sprite.bottom < 0):
            self.player_sprite.damage(200)

    def pause(self) -> None:
        self.status = GameStatus.paused

    def on_key_press(self, key: int, modifiers: int) -> None:
        if self.status != GameStatus.normal:
            if self.status == GameStatus.ended and key == ar.key.R:
                self.restart()
            return
        if key == ar.key.ESCAPE:
            self.pause()
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

    def close(self, ended: bool = True) -> None:
        if ended:
            game_settings['running'].set_false()
        super().close()

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
    sound_button_enabled = ar.Sprite(data.FILES['sound_button_game_enabled'], CELL_SIDE / 40)
    sound_button_disabled = ar.Sprite(data.FILES['sound_button_game_disabled'], CELL_SIDE / 40)

    def __init__(self, first_player_weapon: str, second_player_weapon: str, same_weapons: bool, level: str,
                 restart) -> None:
        self.first_player_weapon_mode = first_player_weapon
        if first_player_weapon == 'Random':
            self.first_player_weapon = choice(weapons_list)
        else:
            self.first_player_weapon = first_player_weapon
        if same_weapons:
            self.second_player_weapon = self.first_player_weapon
            self.second_player_weapon_mode = 'Same'
        elif second_player_weapon == 'Random':
            self.second_player_weapon_mode = second_player_weapon
            self.second_player_weapon = choice(weapons_list)
        else:
            self.second_player_weapon_mode = second_player_weapon
            self.second_player_weapon = second_player_weapon
        super().__init__(self.first_player_weapon)
        self.level = level
        if level == 'Random':
            editor_levels = data.get_levels_list()
            level = choice(list(data.LEVELS.values()) + editor_levels)
        elif level == 'Random_standard':
            level = choice(list(data.LEVELS.values()))
        elif level == 'Random_editor':
            editor_levels = data.get_levels_list()
            level = choice(editor_levels)
        level = data.load_level(level)
        for wall in level['walls']:
            r, c, txt = wall['row'], wall['col'], wall['texture']
            self.wall_list.append(Wall(txt, self.k / 8, r, c))
        for dec in level['decor']:
            r, c, txt = dec['row'], dec['col'], dec['texture']
            self.decor.append(Decor(txt, self.k / 8, r, c))

        if game_settings['sounds']:
            self.sound_button = ar.Sprite(data.FILES['sound_button_game_enabled'], self.k / 2.5)
        else:
            self.sound_button = ar.Sprite(data.FILES['sound_button_game_disabled'], self.k / 2.5)
        self.sound_button.center_x = W - CELL_SIDE * 2
        self.sound_button.center_y = H - CELL_SIDE * 2
        self.is_restart = restart
        self.second_player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                                    data.FILES['player_laying'], self.k / 6, 1, 47,
                                    weapons_dict[self.second_player_weapon](), is_second=True)
        self.second_player_sprite = self.second_player.get_sprite()
        self.second_player_list = ar.SpriteList()
        self.second_player_list.append(self.second_player_sprite)
        self.second_player_physics = ar.PhysicsEnginePlatformer(self.second_player_sprite, self.wall_list,
                                                                gravity_constant=consts.GRAVITY * self.k)

        self.pause_buttons = ar.SpriteList()
        self.continue_button = ar.Sprite(data.FILES['continue_button'], self.k)
        self.back_button = ar.Sprite(data.FILES['back_button'], self.k)
        self.continue_button.center_x, self.continue_button.center_y = W_OUTLINE + 3 * WIDTH / 4, H_OUTLINE + HEIGHT / 8
        self.back_button.center_x, self.back_button.center_y = W_OUTLINE + WIDTH / 4, H_OUTLINE + HEIGHT / 8
        self.pause_buttons.append(self.continue_button)
        self.pause_buttons.append(self.back_button)
        self.pause_buttons.append(self.sound_button)

        self.end_buttons = ar.SpriteList()
        self.restart_button = ar.Sprite(data.FILES['restart_button'], self.k)
        self.restart_button.center_x, self.restart_button.center_y = W_OUTLINE + 3 * WIDTH / 4, H_OUTLINE + HEIGHT / 8
        self.end_buttons.append(self.restart_button)
        self.end_buttons.append(self.back_button)
        self.change_weapon_button = ar.Sprite(data.FILES['change_weapon_button'], self.k)
        self.change_weapon_button.center_x, self.change_weapon_button.center_y = (W_OUTLINE + WIDTH / 2,
                                                                                  H_OUTLINE + HEIGHT / 3)
        self.end_buttons.append(self.change_weapon_button)

    def restart(self, **kwargs) -> None:
        if self.first_player_weapon_mode == 'Random':
            self.first_player_weapon = choice(weapons_list)
        else:
            self.first_player_weapon = self.first_player_weapon_mode
        if self.second_player_weapon_mode == 'Same':
            self.second_player_weapon = self.first_player_weapon
        elif self.second_player_weapon_mode == 'Random':
            self.second_player_weapon = choice(weapons_list)
        else:
            self.second_player_weapon = self.second_player_weapon_mode
        super().restart(self.first_player_weapon)
        level = self.level
        if level == 'Random':
            editor_levels = data.get_levels_list()
            level = choice(list(data.LEVELS.values()) + editor_levels)
        elif level == 'Random_standard':
            level = choice(list(data.LEVELS.values()))
        elif level == 'Random_editor':
            editor_levels = data.get_levels_list()
            level = choice(editor_levels)
        level = data.load_level(level)
        for wall in level['walls']:
            r, c, txt = wall['row'], wall['col'], wall['texture']
            self.wall_list.append(Wall(txt, self.k / 8, r, c))
        for dec in level['decor']:
            r, c, txt = dec['row'], dec['col'], dec['texture']
            self.decor.append(Decor(txt, self.k / 8, r, c))
        self.second_player = Player(self, data.FILES['player_staying'], data.FILES['player_siting'],
                                    data.FILES['player_laying'], self.k / 6, 1, 47,
                                    weapons_dict[self.second_player_weapon](), is_second=True)
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
            elif self.second_player.get_status() == PlayerStatus.laying:
                self.second_player_sprite.change_x = -consts.LAYING_SPEED * self.k
            elif self.second_player.get_status() != PlayerStatus.laying:
                self.second_player_sprite.change_x = -consts.SPEED * self.k
        elif EventsID.sec_right in self.events:
            self.second_player.set_direction(Direction.right)
            if self.second_player.get_status() == PlayerStatus.siting:
                self.second_player_sprite.change_x = consts.SITING_SPEED * self.k
            elif self.second_player.get_status() == PlayerStatus.laying:
                self.second_player_sprite.change_x = consts.LAYING_SPEED * self.k
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
                if game_settings['sounds']:
                    ar.play_sound(weapons_sounds[self.second_player_weapon])
                if isinstance(self.second_player.get_weapon(), Shotgun):
                    for x, y, bullet_characteristics, angle in bullets:
                        bullet = ShotgunBullet(x, y, bullet_characteristics, angle, self.k / 12,
                                               [self.second_player])
                        self.bullets.append(bullet)
                else:
                    for x, y, bullet_characteristics, angle in bullets:
                        bullet = Bullet(x, y, bullet_characteristics, angle, self.k / 12, [self.second_player])
                        self.bullets.append(bullet)

        if EventsID.sec_reload in self.events:
            self.second_player.reload()

    def on_draw(self) -> None:
        self.clear()
        self.bullets.draw()
        self.wall_list.draw()
        self.decor.draw()
        self.player_list.draw()
        self.second_player_list.draw()
        ar.draw_text('HP: ' + str(round(self.player.get_hp())), 16 * self.k, self.height - 16 * self.k, ar.color.RED,
                     12 * self.k)
        ar.draw_text('Weapon: ' + self.first_player_weapon, 16 * self.k, self.height - 40 * self.k, ar.color.RED,
                     12 * self.k)
        ar.draw_text('Ammo: ' + str(self.player.get_ammo()) + '/' + str(self.player.get_max_ammo()), 16 * self.k,
                     self.height - 64 * self.k, ar.color.RED, 12 * self.k)
        ar.draw_text('HP: ' + str(round(self.second_player.get_hp())), self.width - 160 * self.k,
                     self.height - 16 * self.k, ar.color.RED, 12 * self.k)
        ar.draw_text('Weapon: ' + self.second_player_weapon, self.width - 160 * self.k,
                     self.height - 40 * self.k, ar.color.RED, 12 * self.k)
        ar.draw_text('Ammo: ' + str(self.second_player.get_ammo()) + '/' + str(self.second_player.get_max_ammo()),
                     self.width - 160 * self.k, self.height - 64 * self.k, ar.color.RED, 12 * self.k)
        if self.status == GameStatus.paused:
            self.label.draw()
            ar.draw_text('PAUSE', self.center_x - 40 * self.k, self.height - 128 * self.k, ar.color.RED, 24 * self.k)
            self.pause_buttons.draw()
        elif self.status == GameStatus.ended:
            self.label.draw()
            if self.player.get_hp():
                text = 'First Player Won!'
            elif self.second_player.get_hp():
                text = 'Second Player Won!'
            else:
                text = 'Draw'
            ar.draw_text(text, self.center_x - 8 * self.k * len(text), self.center_y + HEIGHT / 3, ar.color.RED, 24 * self.k)
            self.end_buttons.draw()

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
                if sprite in map(lambda el: el.get_sprite(), bullet.get_exceptions()):
                    continue
                sprite.damage(bullet.get_damage())
                self.bullets.remove(bullet)
                if not sprite.get_hp():
                    self.status = GameStatus.ended

    def change_sound(self) -> None:
        game_settings['sounds'] = not game_settings['sounds']
        data.save_sound_settings(game_settings['sounds'])
        if game_settings['sounds']:
            self.sound_button.texture = self.sound_button_enabled.texture
        else:
            self.sound_button.texture = self.sound_button_disabled.texture

    def on_update(self, delta_time: float) -> None:
        if self.status != GameStatus.normal:
            return
        self.events_update()
        self.player.on_update(delta_time)
        self.player_physics.update()
        self.second_player.on_update(delta_time)
        self.second_player_physics.update()
        for physics in self.enemies_physics:
            physics.update()
        self.wall_list.update(delta_time)
        self.bullets_update(delta_time)

        if self.data_timer <= 0:
            self.data_timer = data.get_data_timer()
            data.save()
        else:
            self.data_timer -= delta_time

        if (self.player_sprite.left < 0 or self.player_sprite.right > W
                or self.player_sprite.top > H or self.player_sprite.bottom < 0):
            self.player_sprite.damage(200)
            self.status = GameStatus.ended

        if (self.second_player_sprite.left < 0 or self.second_player_sprite.right > W
                or self.second_player_sprite.top > H or self.second_player_sprite.bottom < 0):
            self.second_player_sprite.damage(200)
            self.status = GameStatus.ended

    def on_key_press(self, key: int, modifiers: int) -> None:
        super().on_key_press(key, modifiers)
        if self.status != GameStatus.normal:
            return
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

    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        if self.status != GameStatus.normal:
            if button == ar.MOUSE_BUTTON_LEFT:
                self.click(x, y)
            return
        if button == ar.MOUSE_BUTTON_LEFT:
            self.events.append(EventsID.sec_shoot)
        if button == ar.MOUSE_BUTTON_RIGHT:
            self.events.append(EventsID.sec_reload)

    def click(self, x: float, y: float) -> None:
        if (self.back_button.left <= x <= self.back_button.right
                and self.back_button.bottom <= y <= self.back_button.top):
            self.close(False)
        if self.status == GameStatus.paused:
            if (self.sound_button.left <= x <= self.sound_button.right
                    and self.sound_button.bottom <= y <= self.sound_button.top):
                self.change_sound()
            elif (self.continue_button.left <= x <= self.continue_button.right
                  and self.continue_button.bottom <= y <= self.continue_button.top):
                self.status = GameStatus.normal
        else:
            if (self.restart_button.left <= x <= self.restart_button.right
                    and self.restart_button.bottom <= y <= self.restart_button.top):
                self.restart()
            elif (self.change_weapon_button.left <= x <= self.change_weapon_button.right
                  and self.change_weapon_button.bottom <= y <= self.change_weapon_button.top):
                self.is_restart.set_true()
                self.close(False)

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
