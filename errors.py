class LevelError(Exception):
    pass


class WeaponError(Exception):
    pass


class WeaponCanNotShootError(WeaponError):
    pass


class WrongWeaponDirectionError(WeaponError):
    pass


class EnemyError(Exception):
    pass


class WrongEnemyDirectionError(EnemyError):
    pass


class WrongEnemyTypeCodeError(EnemyError, LevelError):
    pass


class WrongEnemyDirectionCodeError(EnemyError, LevelError):
    pass


class PlayerError(Exception):
    pass


class WrongPlayerDirectionError(PlayerError):
    pass
