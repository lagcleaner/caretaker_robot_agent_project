from typing import List, Tuple, Sequence, Any
from queue import Queue

from ..commons.directions import Directions
from ..commons.coordinates import Coordinates
from ..commons.actions import AgentAction
from ..commons.cellcontent import CellContent


class HouseAgent:
    def __init__(self, coordinates: Coordinates = None):
        self.coord = coordinates
        self.carrying = None

    def __str__(self):
        return f'Agent<{self.coord}, carrying({self.carrying != None})>'
    __repr__ = __str__

    def action(self, env_info) -> [AgentAction]:
        raise NotImplementedError

    @property
    def double_steping_allowed(self) -> bool:
        return not (self.carrying is None)

    def adyacents(self, env, distance=1) -> Sequence[Coordinates]:
        return env.available_directions(self.coord, distance == 2)

    def bfs(self, env_info, coord: Coordinates, condition) -> Coordinates:
        if condition(env_info, coord):
            return coord
        queue = Queue()
        visited = set()
        #
        queue.put(coord)
        visited.add(coord)
        #
        while not queue.empty():
            c = queue.get()
            #
            for dr in Directions.ALL:
                ca = Coordinates.on_direction(c, dr)
                if ca in visited or not env_info.in_range(ca):
                    continue
                if condition(env_info, ca):
                    return ca
                visited.add(ca)
                queue.put(ca)
        return None
