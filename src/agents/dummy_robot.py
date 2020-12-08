from typing import List, Tuple
from random import randint
from .agent import HouseAgent
from ..commons.directions import Directions
from ..commons.actions import AgentAction
from ..commons.coordinates import Coordinates
from ..commons.cellcontent import CellContent


class DummyRobot(HouseAgent):
    '''
        Moves randomly (double stepping if possible) whith none influence of the environment,
        takes the baby if is in the same cell, let him go if he is in a playpen, and collect
        the garbage if is on the way.
    '''

    def action(self, env_info) -> [AgentAction]:
        action_in_place = self.action_on_cell(env_info)
        if action_in_place:
            return [action_in_place]

        # double steping always is possible
        # choice a random direction (tuple if is double stepping enable)
        return self.next_move(env_info, self.coord, 1 + self.double_steping_allowed)

    def action_on_cell(self, env_info):
        if env_info[self.coord] == CellContent.Dirty:
            return AgentAction.Clean
        if any(
            child
            for child in env_info.children
            if child.coord == self.coord
        ):
            if env_info[self.coord] != CellContent.Playpen and self.carrying is None:
                return AgentAction.CarryAChild
        elif env_info[self.coord] == CellContent.Playpen and not self.carrying is None:
            return AgentAction.DropAChild

    def next_move(self, env_info, coord, count_steps):
        if not count_steps:
            return []
        c = Coordinates(-1, -1)
        while not env_info.in_range(c):
            action = self.choice_move(env_info, coord)
            dr = AgentAction.todir(action)
            c = Coordinates.on_direction(coord, dr)
        return [action] + self.next_move(env_info, c, count_steps-1)

    def choice_move(self, env_info, coord):
        return AgentAction(randint(1, 4))
