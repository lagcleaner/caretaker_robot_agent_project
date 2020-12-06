from enum import Enum


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


class ChildAction(Enum):
    MoveNorth = 1
    MoveEast = 2
    MoveSouth = 3
    MoveWest = 4
    #
    Stay = 5
