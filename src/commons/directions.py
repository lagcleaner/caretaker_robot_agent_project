from random import randint, choice, shuffle
from typing import Tuple, List


class Directions:
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)
    #
    Northeast = (1, -1)
    Southeast = (1, 1)
    Southwest = (-1, 1)
    Northwest = (-1, -1)

    # Directions
    ALL = [North, East, South, West]
    # Directions [Extended]
    ALL_EXTENDED = [
        North, Northeast, East, Southeast,
        South, Southwest, West, Northwest,
    ]

    @staticmethod
    def rdir(cls, extended_directions=False) -> Tuple[int, int]:
        if extended_directions:
            directs = Directions.ALL_EXTENDED
        else:
            directs = Directions.ALL
        return choice(directs)

    @ staticmethod
    def rdirs(cls, extended_directions=False) -> List[Tuple[int, int]]:
        if extended_directions:
            directs = Directions.ALL_EXTENDED
        else:
            directs = Directions.ALL
        return shuffle(directs)
