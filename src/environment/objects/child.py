from random import choice, random
from ...commons import Coordinates, CellContent, ChildAction, Directions


class Child:
    '''
    Represents a child in the house.
    '''

    def __init__(self, coord: Coordinates):
        self.coord = coord
        self.holded = False

    def in_playpen(self, floor):
        assert isinstance(floor, list) and isinstance(floor[0], list)
        return not self.holded and floor[self.coord[0]][self.coord[1]] == CellContent.Playpen

    def __str__(self):
        return f'Child<{self.coord}, holded: {self.holded}>'
    __repr__ = __str__

    def action(self, env):
        if self.holded or self.in_playpen(env.floor) or random() < 1/2:
            return ChildAction.Stay
        directs = env.available_directions(self.coord)
        possible_directs = []
        for dr in directs:
            ci = Coordinates.on_direction(self.coord, dr)
            if (
                env[ci] in (CellContent.Empty, CellContent.Obstacle) and
                    not env.occuped(ci)
            ):
                possible_directs.append(dr)
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
