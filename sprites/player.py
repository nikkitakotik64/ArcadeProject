from enum import Enum
import arcade as ar
from screen import cell_center


class PlayerStatus(Enum):
    NORMAL = 0
    JUMPING = 1
    FALLING = 2
    SITING = 3
    LAYING = 4


class Player:
    def __init__(self, app, texture_staying: str, texture_siting: str, texture_laying: str,
                 scale: float, row: int, col: int) -> None:
        self.status = PlayerStatus.NORMAL
        self.sprite = ar.sprite.Sprite(texture_staying, scale)
        self.texture_staying = texture_staying
        self.texture_siting = texture_siting
        self.scale = scale
        self.app = app
        self.texture_laying = texture_laying
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)

    def move(self, row: int, col: int) -> None:
        self.sprite.center_x, self.sprite.center_y = cell_center(row, col)

    def update_texture(self, status: PlayerStatus) -> None:
        if status == PlayerStatus.SITING:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = ar.sprite.Sprite(self.texture_siting, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        elif status == PlayerStatus.LAYING:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = ar.sprite.Sprite(self.texture_laying, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        else:
            center_x, bottom = self.sprite.center_x, self.sprite.bottom
            self.sprite = ar.sprite.Sprite(self.texture_staying, self.scale)
            self.sprite.center_x, self.sprite.bottom = center_x, bottom
        self.app.update_player_sprite()

    def set_status(self, status: PlayerStatus) -> None:
        if self.status == PlayerStatus.SITING or self.status == PlayerStatus.LAYING:
            self.update_texture(status)
        self.status = status

    def get_status(self) -> PlayerStatus:
        return self.status

    def get_sprite(self) -> ar.sprite.Sprite:
        return self.sprite

    def down(self) -> None:
        match self.status:
            case PlayerStatus.NORMAL:
                self.status = PlayerStatus.SITING
                self.update_texture(self.status)
            case PlayerStatus.SITING:
                self.status = PlayerStatus.LAYING
                self.update_texture(self.status)

    def up(self) -> None:
        match self.status:
            case PlayerStatus.LAYING:
                self.status = PlayerStatus.SITING
                self.update_texture(self.status)
            case PlayerStatus.SITING:
                self.status = PlayerStatus.NORMAL
                self.update_texture(self.status)
