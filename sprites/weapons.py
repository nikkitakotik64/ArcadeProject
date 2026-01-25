from enum import Enum
from random import randint
from errors import WeaponCanNotShootError, WrongWeaponDirectionError
from game_types import Direction
from screen import CELL_SIDE


class WeaponStatus(Enum):
    normal = 0
    reloading = 1
    shooting = 2


class BulletCharacteristics:
    def __init__(self, damage: float, normal_range: float, armor_piercing: int,
                 bullet_speed: float) -> None:
        self.damage = damage
        self.normal_range = normal_range
        self.armor_piercing = armor_piercing
        self.bullet_speed = bullet_speed

    def get_damage(self) -> int:
        return self.damage

    def get_normal_range(self) -> float:
        return self.normal_range

    def get_armor_piercing(self) -> int:
        return self.armor_piercing

    def get_bullet_speed(self) -> float:
        return self.bullet_speed


class Weapon:
    def __init__(self, count_of_ammo: int, damage: float, normal_range: float, armor_piercing: int,
                 spread_angle: int, rate_of_fire: float, reloading_time: float,
                 bullet_speed: float) -> None:
        self.count_of_ammo = count_of_ammo
        self.now_ammo = count_of_ammo
        self.status = WeaponStatus.normal
        self.spread_angle = spread_angle
        self.timer = 0
        self.rate_of_fire = rate_of_fire
        self.reloading_time = reloading_time
        self.bullet_characteristics = BulletCharacteristics(damage, normal_range, armor_piercing, bullet_speed)

    def can_shoot(self) -> bool:
        if self.status == WeaponStatus.reloading or self.status == WeaponStatus.shooting:
            return False
        if not self.now_ammo:
            self.start_reload()
            return False
        return True

    def shoot(self, direction: Direction) -> list[tuple[BulletCharacteristics, float]]:
        if not self.can_shoot():
            match self.status:
                case WeaponStatus.shooting:
                    raise WeaponCanNotShootError('Weapon is already shot, wait')
                case WeaponStatus.reloading:
                    raise WeaponCanNotShootError('Weapon can not shoot when reloading')
        match direction:
            case Direction.up:
                raise WrongWeaponDirectionError('Weapon can not shoot up')
            case Direction.down:
                raise WrongWeaponDirectionError('Weapon can not shoot down')
            case Direction.left:
                self.status = WeaponStatus.shooting
                self.now_ammo -= 1
                return [(self.bullet_characteristics, 180 + randint(-self.spread_angle, self.spread_angle))]
            case Direction.right:
                self.status = WeaponStatus.shooting
                self.now_ammo -= 1
                return [(self.bullet_characteristics, 0 + randint(-self.spread_angle, self.spread_angle) % 360)]

    def start_reload(self) -> None:
        if self.status != WeaponStatus.normal or self.now_ammo == self.count_of_ammo:
            return
        self.status = WeaponStatus.reloading
        self.timer = 0

    def end_reload(self) -> None:
        self.status = WeaponStatus.normal
        self.timer = 0
        self.now_ammo = self.count_of_ammo

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

    def get_status(self) -> WeaponStatus:
        return self.status


class Glock18(Weapon):
    def __init__(self) -> None:
        super().__init__(20, 5, CELL_SIDE, 5, 3,
                         20 / 60, 1, 1000)


class P250(Weapon):
    def __init__(self) -> None:
        super().__init__(13, 10, CELL_SIDE * 2.5, 5, 8,
                         20 / 60, 1, 1000)


class USP(Weapon):
    def __init__(self) -> None:
        super().__init__(12, 7, CELL_SIDE * 2.5, 5, 2,
                         20 / 60, 1, 1000)


class DualBerrettas(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 6, CELL_SIDE * 1.5, 5, 5,
                         10 / 60, 3, 1000)


class Revolver(Weapon):
    def __init__(self) -> None:
        super().__init__(8, 90, CELL_SIDE * 6, 5, 3,
                         30 / 60, 2, 1000)


class Deagle(Weapon):
    def __init__(self) -> None:
        super().__init__(7, 55, CELL_SIDE, 5, 1,
                         20 / 60, 1.5, 1000)


class MP9(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 8, CELL_SIDE, 5, 10,
                         2 / 60, 2, 1500)


class MP7(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 10, CELL_SIDE, 5, 8,
                         3 / 60, 2.5, 1000)


class UZI(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 8, CELL_SIDE, 5, 10,
                         2.5 / 60, 2.5, 1000)


class MP5(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 9, CELL_SIDE, 5, 6,
                         3.5 / 60, 2.5, 1000)


class P90(Weapon):
    def __init__(self) -> None:
        super().__init__(50, 8, CELL_SIDE, 5, 8,
                         2 / 60, 3.5, 1500)


class M249(Weapon):
    def __init__(self) -> None:
        super().__init__(100, 8, CELL_SIDE, 5, 10,
                         2.5 / 60, 6, 1000)


class Shotgun(Weapon):
    def __init__(self, count_of_ammo: int, damage: int, normal_range: float, armor_piercing: int,
                 spread_angle: int, rate_of_fire: float, reloading_time: float,
                 bullet_speed: float, count_of_pierces) -> None:
        super().__init__(count_of_ammo * count_of_pierces, damage / count_of_pierces, normal_range,
                         armor_piercing, spread_angle, rate_of_fire, reloading_time, bullet_speed)
        self.count_of_pierces = count_of_pierces

    def shoot(self, direction: Direction) -> list[tuple[BulletCharacteristics, float]]:
        bullets = []
        for i in range(self.count_of_pierces):
            self.status = WeaponStatus.normal
            bullets += super().shoot(direction)
        return bullets


class XM1014(Shotgun):
    def __init__(self) -> None:
        super().__init__(7, 100, CELL_SIDE, 5, 15,
                         20 / 60, 10, 1000, 20)


class MAG7(Shotgun):
    def __init__(self) -> None:
        super().__init__(5, 210, CELL_SIDE, 5, 20,
                         80 / 60, 3, 1000, 30)


class M4A4(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 30, CELL_SIDE * 3, 5, 3,
                         4 / 60, 3, 1500)


class AK47(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 40, CELL_SIDE * 4.5, 5, 6,
                         4 / 60, 3, 1500)


class SCAR20(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 30, CELL_SIDE * 6, 5, 3,
                         5 / 60, 3, 1500)


class FAMAS(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 25, CELL_SIDE * 3, 5, 3,
                         4 / 60, 3, 1500)


class AUG(Weapon):
    def __init__(self) -> None:
        super().__init__(30, 30, CELL_SIDE * 5, 5, 3,
                         4 / 60, 4.5, 1500)


class SSG08(Weapon):
    def __init__(self) -> None:
        super().__init__(10, 90, CELL_SIDE * 8, 5, 0,
                         80 / 60, 5, 1500)


class AWP(Weapon):
    def __init__(self) -> None:
        super().__init__(5, 200, CELL_SIDE * 5, 5, 0,
                         120 / 60, 5, 1500)


class SVD(Weapon):
    def __init__(self) -> None:
        super().__init__(20, 50, CELL_SIDE, 5, 1,
                         17 / 60, 7, 1000)


weapons_list = ['Glock-18', 'P250', 'USP-S', 'Dual Berrettas', 'Revolver R8', 'Desert Eagle',
                'MP9', 'MP7', 'UZI', 'MP5', 'P90', 'M249', 'XM1014', 'MAG-7',
                'M4A4', 'AK-47', 'SCAR-20', 'FAMAS', 'AUG',
                'SSG-08', 'AWP', 'SVD']
weapons_dict = {'Glock-18': Glock18, 'P250': P250, 'USP-S': USP, 'Dual Berrettas': DualBerrettas,
                'Revolver R8': Revolver, 'Desert Eagle': Deagle, 'MP9': MP9, 'MP7': MP7,
                'UZI': UZI, 'MP5': MP5, 'P90': P90, 'M249': M249, 'XM1014': XM1014, 'MAG-7': MAG7,
                'M4A4': M4A4, 'AK-47': AK47, 'SCAR-20': SCAR20, 'FAMAS': FAMAS, 'AUG': AUG,
                'SSG-08': SSG08, 'AWP': AWP, 'SVD': SVD}
