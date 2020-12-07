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
    def to_string(dr: Tuple[int, int]):
        if Directions.North == dr:
            return 'North'
        if Directions.South == dr:
            return 'South'
        if Directions.West == dr:
            return 'West'
        if Directions.East == dr:
            return 'East'
        if Directions.Northeast == dr:
            return 'Northeast'
        if Directions.Northwest == dr:
            return 'Northwest'
        if Directions.Southeast == dr:
            return 'Southeast'
        if Directions.Southwest == dr:
            return 'Southwest'
        else:
            return f'Undef: {dr}'

    @staticmethod
    def rdir(extended_directions=False) -> Tuple[int, int]:
        if extended_directions:
            directs = Directions.ALL_EXTENDED
        else:
            directs = Directions.ALL
        return choice(directs)

    @ staticmethod
    def rdirs(extended_directions=False) -> List[Tuple[int, int]]:
        if extended_directions:
            directs = Directions.ALL_EXTENDED.copy()
        else:
            directs = Directions.ALL.copy()
        shuffle(directs)
        return directs
