from enum import Enum
from .directions import Directions
from typing import Tuple


class AgentAction(Enum):
    MoveNorth = 1
    MoveEast = 2
    MoveSouth = 3
    MoveWest = 4
    #
    CarryAChild = 5
    DropAChild = 6
    #
    Clean = 7
    #
    Stay = 8

    @staticmethod
    def todir(action) -> Tuple[int, int]:
        assert 1 <= action.value <= 4, 'No direction available'
        return Directions.ALL[action.value - 1]


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
