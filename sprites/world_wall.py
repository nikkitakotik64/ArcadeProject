import arcade as ar


class WorldWall(ar.sprite.Sprite):
    def __init__(self, texture: str, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(texture, scale)
        self.center_x, self.center_y = center_x, center_y
