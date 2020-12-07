from typing import List, Tuple, Any
from random import randint
from queue import Queue

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
        the tasks, once is choicing a target, the preference is setted like:

        `focus_child = True` then until the last kid out of the playpen does
        not set the next goal

        `focus_garbage = True` then until the last dirt was clean does not set
        the next goal
    '''

    def __init__(self, coord: Coordinates, focus_child=True, focus_garbage=False):
        super().__init__(coord)
        self.focus_child = focus_child or not focus_garbage
        self.goal: Coordinates = None
        self.directions_path: List[Tuple[int, int]] = None

    def action(self, env_info) -> [AgentAction]:
        if self.set_goal(env_info) is None:
            # if there is no goal available
            return [AgentAction.Stay]
        if self.coord == self.goal:
            # if t is in the goal cell
            return [self.action_on_cell(env_info)]
        # move to the goal
        moves = self.next_move(env_info, 1+self.double_steping_allowed)
        return moves if moves else [AgentAction.Stay]

    def next_move(self, env_info, steps=1):
        if not self.directions_path:
            return [AgentAction.Stay]
        actions = []
        cur_coord = self.coord
        # while all steps where defined and
        # still having positions movements to get to the goal
        while steps > 0 and self.directions_path:
            dr = self.directions_path.pop()
            cur_coord = Coordinates.on_direction(cur_coord, dr)
            cur_action = AgentAction(Directions.ALL.index(dr) + 1)
            if self.goal == cur_coord:
                return [cur_action]
            actions.append(cur_action)
            steps -= 1

        return actions

    def bfs_path(self, env_info, coord: Coordinates, condition) -> List[Coordinates]:
        if condition(env_info, coord):
            return coord
        queue = Queue()
        #
        queue.put(coord)
        path_d = {coord: (None, None)}
        #
        while not queue.empty():
            c = queue.get()
            #
            for dr in Directions.ALL:
                ca = Coordinates.on_direction(c, dr)
                if ca in path_d or not env_info.in_range(ca):
                    continue
                if condition(env_info, ca):
                    path = [dr]
                    step_c = c
                    while step_c == None:
                        step_c, dirct = path_d.get(step_c, (None, None))
                        if step_c == None:
                            break
                        path.append(dirct)

                        # build path of directions
                    return path
                path_d[ca] = c, dr
                queue.put(ca)
        return None

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
        return AgentAction.Stay

    def set_goal(self, env_info):
        self.goal = None
        self.directions_path = None
        #
        if self.focus_child:
            self.goal = self.set_next_child(env_info)
            if self.goal is None:
                self.goal = self.set_next_dirt(env_info)
        else:
            self.goal = self.set_next_dirt(env_info)
            if self.goal is None:
                self.goal = self.set_next_child(env_info)

        # build path if there is a goal
        if self.goal:
            self.directions_path = self.bfs_path(
                env_info, self.coord,
                lambda env, coord: coord == self.goal
            )
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
        return nearest_child

    def set_next_dirt(self, env_info):
        nearest_dirt = self.bfs(
            env_info, self.coord,
            lambda env, coord: env[coord] == CellContent.Dirty
        )
        return nearest_dirt
