from ...commons import Coordinates


class Child:
    '''
    Represents a child in the house.
    '''

    def __init__(self, coord: Coordinates):
        self.coord = coord
        self.holded = False
        self.in_playpen = False
    def __str__(self):
        return f'Child<{self.coord}, holded: {self.holded}>'
    __repr__ = __str__

    def action(self, env):
        pass
