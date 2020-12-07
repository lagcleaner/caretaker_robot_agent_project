from typing import NamedTuple
from .directions import Directions


def build_coordinates(coord_t: tuple):
    return Coordinates(col=coord_t[0], row=coord_t[1])


class Coordinates(NamedTuple):
    col: int
    row: int

    @staticmethod
    def on_direction(coord, dr: Directions):
        return build_coordinates((coord[0] + dr[0], coord[1] + dr[1]))
