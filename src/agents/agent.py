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

    def adyacents(self, env, distance=1) -> Sequence[Coordinates]:
        return env.available_directions(self.coord, distance == 2)
