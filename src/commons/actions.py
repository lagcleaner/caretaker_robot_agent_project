from enum import Enum
from .directions import Directions
from typing import Tuple


class AgentAction(Enum):
    MoveNorth = 1
    MoveEast = 2
    MoveSouth = 3
    MoveWest = 4
    #
    MoveNorthDouble = 5
    MoveEastDouble = 6
    MoveSouthDouble = 7
    MoveWestDouble = 8
    #
    CarryAChild = 9
    DropAChild = 10
    #
    Clean = 11
    #
    Stay = 12

    @staticmethod
    def todir(action) -> Tuple[int, int]:
        assert action.value < 9, 'No direction available'
        return Directions.ALL[action.value - 1 % 4]

    @staticmethod
    def steps(action) -> int:
        if action.value < 9:
            return action.value - 1 // 4 + 1
        else:
            return 0  # No direction


class ChildAction(Enum):
    MoveNorth = 1
    MoveEast = 2
    MoveSouth = 3
    MoveWest = 4
    #
    Stay = 5

    @staticmethod
    def todir(action):
        assert action.value < 5, 'No direction available'
        return Directions.ALL[action.value - 1]
