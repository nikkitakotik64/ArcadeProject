class LevelError(Exception):
    pass


class WrongLevelTypeError(LevelError):
    pass


class WeaponError(Exception):
    pass


class WeaponCanNotShootError(WeaponError):
    pass


class WrongWeaponDirectionError(WeaponError):
    pass
