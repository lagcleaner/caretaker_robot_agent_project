from typing import List, Tuple, Any
from random import randint

from .agent import HouseAgent
from ..commons.directions import Directions
from ..commons.distance import distance
from ..commons.actions import AgentAction
from ..commons.coordinates import Coordinates
from ..commons.cellcontent import CellContent
from .utils import Infinite


class FocusedRobot(HouseAgent):
    '''
        As the name describes focus the attention and dont stop until finish,
        the tasks, once is choicing a target the preference is setted:

        `focus_child = True` then until the last kid out of the playpen does
        not set the next goal

        `focus_garbage = True` then until the last dirt was clean does not set
        the next goal
    '''

    def __init__(self, coord: Coordinates, focus_child=True, focus_garbage=False):
        super().__init__(coord)
        self.focus_child = focus_child or not focus_garbage
        self.goal: Coordinates = None

    def action(self, env_info) -> AgentAction:
        if self.goal is None and self.set_next_goal(env_info) is None:
            # if there is no goal available
            return AgentAction.Stay
        if self.coord == self.goal:
            return self.action_on_cell(env_info)
        move = self.next_move(env_info)

    def next_move(self, env_info):
        visited_on_dfs_s = set()
        for dr in Directions.ALL:
            adyc = Coordinates.on_direction(self.coord, dr)
            if env_info.in_range(adyc):
                continue
            if self.dfs(
                env_info, adyc, visited_on_dfs_s,
                lambda env, coord: env[coord] == self.goal
            ):
                if self.carrying:
                    # double stepping if possible
                    sec_degre_ady = Coordinates.on_direction(adyc, dr)
                    if env_info.in_range(sec_degre_ady) and env_info[sec_degre_ady] in (CellContent.Empty, CellContent.Dirty):

                if self.coord

    def action_on_cell(self, env_info):
        if env_info[self.coord] == CellContent.Dirty:
            return AgentAction.Clean
        if env_info[self.coord] == CellContent.Playpen and not self.carrying is None:
            return AgentAction.DropAChild
        if any(
            child for child in env_info.childen
            if child.coord == self.coord
        ):
            return AgentAction.CarryAChild

    def set_next_goal(self, env_info):
        if self.focus_child:
            self.goal = self.set_next_child(env_info)
            if self.goal is None:
                self.goal = self.set_next_dirt(env_info)
        else:
            self.goal = self.set_next_dirt(env_info)
            if self.goal is None:
                self.goal = self.set_next_child(env_info)
        return self.goal

    def set_next_child(self, env_info):
        nearest_child = None
        best_dist = Infinite()
        for child in env_info.children:
            if not child.in_playpen(env_info) and not child.holded:
                dist = distance(self.coord, child.coord)
                nearest_child, best_dist = (
                    (child.coord, dist)
                    if best_dist > dist
                    else (nearest_child, best_dist)
                )
        self.next_move = self.bfs(
            env_info, self.coord,
            lambda env, coord: coord == nearest_child.coord
        )
        return nearest_child

    def set_next_dirt(self, env_info):
        nearest_dirt = self.bfs(
            env_info, self.coord,
            lambda env, coord: env[coord] == CellContent.Dirty
        )
        return nearest_dirt
