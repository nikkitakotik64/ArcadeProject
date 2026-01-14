from enum import Enum
from random import randint
from errors import WeaponCanNotShootError, WrongWeaponDirectionError
from game_types import Direction


class WeaponStatus(Enum):
    normal = 0
    reloading = 1
    shooting = 2
    no_ammo = 3
    preparing = 4


class Weapon:
    def __init__(self, count_of_ammo: int, count_of_magazines: int,
                 damage: int, normal_range: float, armor_piercing: int,
                 spread_angle: int, rate_of_fire: float, reloading_time: float,
                 bullet_speed: float, preparing_time: float) -> None:
        self.preparing_time = preparing_time
        self.count_of_ammo = count_of_ammo
        self.magazines_ammo = count_of_magazines * count_of_ammo
        self.damage = damage
        self.normal_range = normal_range
        self.armor_piercing = armor_piercing
        self.now_ammo = count_of_ammo
        self.status = WeaponStatus.preparing
        self.spread_angle = spread_angle
        self.timer = 0
        self.rate_of_fire = rate_of_fire
        self.reloading_time = reloading_time
        self.bullet_speed = bullet_speed

    def can_shoot(self) -> bool:
        if (self.status == WeaponStatus.reloading or self.status == WeaponStatus.shooting
                or self.status == WeaponStatus.preparing):
            return False
        if not self.now_ammo:
            self.start_reload()
            return False
        return True

    def shoot(self, direction: Direction) -> list[tuple[float, float]]:
        if not self.can_shoot():
            match self.status:
                case WeaponStatus.shooting:
                    raise WeaponCanNotShootError('Weapon is already shot, wait')
                case WeaponStatus.reloading:
                    raise WeaponCanNotShootError('Weapon can not shoot when reloading')
                case WeaponStatus.preparing:
                    raise WeaponCanNotShootError('Weapon can not shot when preparing')
        match direction:
            case Direction.up:
                raise WrongWeaponDirectionError('Weapon can not shoot up')
            case Direction.down:
                raise WrongWeaponDirectionError('Weapon can not shoot down')
            case Direction.left:
                self.status = WeaponStatus.shooting
                self.now_ammo -= 1
                return [(self.bullet_speed, 180 + randint(-self.spread_angle, self.spread_angle))]
            case Direction.right:
                self.status = WeaponStatus.shooting
                self.now_ammo -= 1
                return [(self.bullet_speed, 0 + randint(-self.spread_angle, self.spread_angle) % 360)]

    def start_reload(self) -> None:
        if not self.magazines_ammo:
            self.status = WeaponStatus.no_ammo
            return
        if self.status != WeaponStatus.normal or self.now_ammo == self.count_of_ammo:
            return
        self.status = WeaponStatus.reloading
        self.timer = 0

    def end_reload(self) -> None:
        self.status = WeaponStatus.normal
        self.timer = 0
        self.magazines_ammo -= self.count_of_ammo - self.now_ammo
        self.now_ammo = self.count_of_ammo
        while self.magazines_ammo < 0:
            self.magazines_ammo += 1
            self.now_ammo -= 1

    def on_update(self, delta_time: float) -> None:
        match self.status:
            case WeaponStatus.shooting:
                self.timer += delta_time
                if self.timer >= self.rate_of_fire:
                    self.timer = 0
                    self.status = WeaponStatus.normal
            case WeaponStatus.reloading:
                self.timer += delta_time
                if self.timer >= self.reloading_time:
                    self.timer = 0
                    self.status = WeaponStatus.normal
                    self.end_reload()
            case WeaponStatus.preparing:
                self.timer += delta_time
                if self.timer >= self.preparing_time:
                    self.timer = 0
                    self.status = WeaponStatus.normal

    def get_status(self) -> WeaponStatus:
        return self.status


class StartWeapon(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 100000, 5, 10, 40,
                         4, 2.5 / 60, 2.5, 1500, 1.5)

# can be added more weapon
