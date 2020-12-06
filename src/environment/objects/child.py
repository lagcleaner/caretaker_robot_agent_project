from ...commons import Coordinates


class Child:
    '''
    Represents a child in the house.
    '''

    def __init__(self, coord: Coordinates):
        self.coord = coord
        self.holded = False
        self.in_playpen = False

    def action(self, env):
        pass
