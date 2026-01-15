from enum import Enum
from sprites.weapons import Weapon
from data.savings import data
from game_types import Direction
from errors import WrongEnemyDirectionError
import arcade as ar
from consts import ENEMY_SPEED


class EnemyDirectionCodes:
    left = 0
    right = 1


class EnemyType(Enum):
    staying = 0
    laying = 1
    siting = 2


class EnemyTypeCodes:
    staying = 0
    laying = 1
    siting = 2


class LayingType:
    def __init__(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass


class SitingType:
    def __init__(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass


class StayingType:
    def __init__(self) -> None:
        pass

    def on_update(self, delta_time: float) -> None:
        pass


class Enemy(ar.sprite.Sprite):
    def __init__(self, x: float, y: float, enemy_type: EnemyType, weapon: Weapon, scale: float,
                 direction: Direction, hp: int = 200) -> None:
        match enemy_type:
            case EnemyType.staying:
                texture = data.FILES['enemy_staying']
                self.type = StayingType()
            case EnemyType.siting:
                texture = data.FILES['enemy_siting']
                self.type = SitingType()
            case EnemyType.laying:
                texture = data.FILES['enemy_laying']
                self.type = LayingType()
        super().__init__(texture, scale)
        self.center_x = x
        self.center_y = y
        self.weapon = weapon
        self.hp = hp
        if direction != Direction.right and direction != Direction.left:
            raise WrongEnemyDirectionError('Enemy can have only right or left direction')
        self.direction = direction

    def update(self, delta_time: float) -> None:
        self.on_update(delta_time)

    def on_update(self, delta_time: float) -> None:
        self.weapon.on_update(delta_time)
        self.type.on_update(delta_time)

    # TODO: доделать
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

    def get_hp(self) -> float:
        return self.hp

    def damage(self, damage: float) -> None:
        self.hp = max(self.hp - damage, 0)
