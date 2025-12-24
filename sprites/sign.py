import arcade as ar
from data.savings import data
from screen import cell_center


class Sign(ar.sprite.Sprite):
    def __init__(self, scale: float, row: int, col: int, text: str) -> None:
        texture = data.FILES[f'sign']
        super().__init__(texture, scale)
        self.center_x, self.center_y = cell_center(row, col)
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_type(self) -> str:
        return 'sign'
