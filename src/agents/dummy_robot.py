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

    def action(self, env_info) -> AgentAction:
        if env_info[self.coord] == CellContent.Dirty:
            # clean the floor if it is dirty
            return AgentAction.Clean

        if self.carrying is None:
            # pickup a child if there is one in the same cell
            ch = None
            for child in env_info.children:
                # dont pickup if is in a playpen
                if child.coord == self.coord and env_info[self.coord] != CellContent.Playpen:
                    ch = child
                    break
            if not (ch is None):
                return AgentAction.CarryAChild

        elif env_info[self.coord] == CellContent.Playpen:
            # drop the child carried if is in a playpen
            return AgentAction.DropAChild

        # double steping always is possible
        double = self.double_steping_allowed

        # choice a random direction
        return AgentAction(randint(1, 4) + (double * 4))
