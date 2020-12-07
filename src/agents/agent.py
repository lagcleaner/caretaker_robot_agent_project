from typing import List, Tuple, Sequence
from ..commons.directions import Directions
from ..commons.coordinates import Coordinates
from ..commons.actions import AgentAction


class HouseAgent:
    def __init__(self, coordinates: Coordinates = None):
        self.coord = coordinates
        self.carrying = None

    def __str__(self):
        return f'Agent<{self.coord}, carrying({self.carrying != None})>'
    __repr__ = __str__

    def action(self, env_info) -> AgentAction:
        raise NotImplementedError

    @property
    def doble_steping_allowed(self) -> bool:
        raise NotImplementedError

    def adyacents(self, house):
        pass
        # c, r = self.coord
        # adyacent_pos = [
        #     (dc + c, dr + r)
        #     for dc, dr in DIRECTIONS
        #     if 0 <= dc + c < house.dim.cols and 0 <= dr + r < house.dim.rows
        # ]
        # if self.doble_steping:
        #     adyacent_pos.extend([
        #         (2*dc + c, 2*dr + r)
        #         for dc, dr in DIRECTIONS
        #         if 0 <= 2*dc + c < house.dim.cols and 0 <= 2*dr + r < house.dim.rows
        #     ])
        # return adyacent_pos

    def move_to(self, house, direction=(1, 0)):
        pass
        # c, r = self.coord
        # nc, nr = c + direction[0], r + direction[1]
        # if house.field[nc][nr].can_hold(self):
        #     house.field[nc][nr].hold(self)
        #     house.field[c][r].release(self)
        #     return True
        # else:
        #     return False
