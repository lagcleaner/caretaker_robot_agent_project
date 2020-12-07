from random import choice
from ...commons import Coordinates, CellContent, ChildAction, Directions


class Child:
    '''
    Represents a child in the house.
    '''

    def __init__(self, coord: Coordinates):
        self.coord = coord
        self.holded = False

    def in_playpen(self, floor):
        return not self.holded and floor[self.coord[0]][self.coord[1]] == CellContent.Playpen

    def __str__(self):
        return f'Child<{self.coord}, holded: {self.holded}>'
    __repr__ = __str__

    def action(self, env):
        if self.holded or self.in_playpen(env.floor):
            return ChildAction.Stay
        directs = env.available_directions(self.coord)
        possible_directs = [
            dr for dr in directs
            if env[Coordinates.on_direction(self.coord, dr)] in
            (CellContent.Empty, CellContent.Obstacle)
        ]
        if possible_directs:
            direct = choice(possible_directs)
            if direct == Directions.North:
                return ChildAction.MoveNorth
            if direct == Directions.South:
                return ChildAction.MoveSouth
            if direct == Directions.West:
                return ChildAction.MoveWest
            if direct == Directions.East:
                return ChildAction.MoveEast
        else:
            return ChildAction.Stay
