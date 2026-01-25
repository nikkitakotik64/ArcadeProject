from enum import Enum
import arcade as ar
from screen import cell_center
from game_types import Direction
from sprites.weapons import Weapon
from errors import WrongPlayerDirectionError


class PlayerStatus(Enum):
    normal = 0
    jumping = 1
    falling = 2
    siting = 3
    laying = 4


class PlayerSprite(ar.sprite.Sprite):
    def __init__(self, texture: str, scale: float) -> None:
        super().__init__(texture, scale)
        self.hp = 200

    def get_hp(self) -> float:
        return self.hp

    def damage(self, damage: float) -> None:
        self.hp -= damage
        self.hp = max(0, self.hp)


class Player:
    def __init__(self, app, texture_staying: str, texture_siting: str, texture_laying: str,
                 scale: float, row: int, col: int, weapon: Weapon, is_second: bool = False) -> None:
        self.status = PlayerStatus.normal
        self.sprite = PlayerSprite(texture_staying, scale)
        self.texture_staying = texture_staying
        self.texture_siting = texture_siting
        self.scale = scale
        self.app = app
        self.texture_laying = texture_laying
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)
        self.direction = Direction.right
        self.weapon = weapon
        self.is_second = is_second
        self.hp = 200

    def get_hp(self) -> float:
        return self.sprite.get_hp()

    def move(self, row: int, col: int) -> None:
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)

    def update_texture(self, status: PlayerStatus) -> None:
        if status == PlayerStatus.siting:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = PlayerSprite(self.texture_siting, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        elif status == PlayerStatus.laying:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = PlayerSprite(self.texture_laying, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        else:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = PlayerSprite(self.texture_staying, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        if self.is_second:
            self.app.update_second_player_sprite()
        else:
            self.app.update_player_sprite()

    def set_status(self, status: PlayerStatus) -> None:
        if self.status == PlayerStatus.siting or self.status == PlayerStatus.laying:
            self.update_texture(status)
        self.status = status

    def get_status(self) -> PlayerStatus:
        return self.status

    def get_sprite(self) -> ar.sprite.Sprite:
        return self.sprite

    def down(self) -> None:
        match self.status:
            case PlayerStatus.normal:
                self.status = PlayerStatus.siting
                self.update_texture(self.status)
            case PlayerStatus.siting:
                self.status = PlayerStatus.laying
                self.update_texture(self.status)

    def up(self) -> None:
        match self.status:
            case PlayerStatus.laying:
                self.status = PlayerStatus.siting
                self.update_texture(self.status)
            case PlayerStatus.siting:
                self.status = PlayerStatus.normal
                self.update_texture(self.status)

    def set_direction(self, direction: Direction) -> None:
        if direction != Direction.right and direction != Direction.left:
            raise WrongPlayerDirectionError('Player can have only right or left direction')
        self.direction = direction

    def shoot(self) -> list:
        bullets = list()
        if self.weapon.can_shoot():
            for bullet_characteristics, angle in self.weapon.shoot(self.direction):
                x = -1
                match self.direction:
                    case Direction.right:
                        x = self.sprite.right
                    case Direction.left:
                        x = self.sprite.left
                bullets.append([x, self.sprite.center_y, bullet_characteristics, angle])
        return bullets

    def on_update(self, delta_time: float) -> None:
        self.weapon.on_update(delta_time)

    def reload(self) -> None:
        self.weapon.start_reload()
