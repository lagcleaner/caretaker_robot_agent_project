
from typing import List, Any, Iterator, Tuple, NamedTuple, Set
from random import randint, choice, shuffle, random

from .objects import Child
from ..commons import (
    distance, Directions,
    Dimensions, CellContent,
    Coordinates, Conclusion,
    SimulationResult, AgentAction,
    ChildAction
)
from ..agents import HouseAgent


class House:
    def __init__(
        self,
        dimensions: Dimensions,
        agent_model: HouseAgent,
        child_model=Child,
        number_of_house_agents: int = 1,
        number_of_dirtyCells: int = 0,
        number_of_obstacles: int = 0,
        dirtyCells_percent: int = None,
        obstacleCells_percent: int = None,
        number_of_children: int = 1,
        number_of_turns: int = None,
        t=3,
    ):
        total = dimensions.cols * dimensions.rows
        self.child_model = child_model
        self.agent_model = agent_model
        self.nagents = number_of_house_agents
        self.nchildren = number_of_children
        if dirtyCells_percent:
            self.ndirtyCells = total * dirtyCells_percent // 100
        else:
            self.ndirtyCells = number_of_dirtyCells

        if obstacleCells_percent:
            self.nobstacles = total * obstacleCells_percent // 100
        else:
            self.nobstacles = number_of_obstacles
        self.nturns = 100*t if number_of_turns is None else number_of_turns
        self.children = []
        self.agents = []
        self.dim: Dimensions = dimensions
        self.time_interval = t
        self.ctime = 0
        self.turn = 0
        self.floor: List[List[CellContent]] = None
        #
        self.build_field()

    # region Special Funcs
    def __getitem__(self, index: Coordinates):
        c, r = index
        return self.floor[c][r]

    def __setitem__(self, index: Coordinates, value):
        c, r = index
        self.floor[c][r] = value

    def __str__(self):
        turn = f'(turn: {self.turn}/{self.nturns})\n'
        res = ''
        for r in range(len(self.floor[0])):
            for c in range(len(self.floor)):
                content = None
                if self.floor[c][r] == CellContent.Empty:
                    content = '_'
                elif self.floor[c][r] == CellContent.Dirty:
                    content = '*'
                elif self.floor[c][r] == CellContent.Obstacle:
                    content = 'o'
                elif self.floor[c][r] == CellContent.Playpen:
                    content = 'U'
                #
                if any(ag.coord == (c, r) for ag in self.agents):
                    content = 'R'
                elif any(ch.coord == (c, r) for ch in self.children):
                    content = 'C'
                res += content
            res += '\n'
        return turn + res
    # endregion

    # region Build Field

    def build_field(self):
        self.floor = [
            [
                CellContent.Empty
                for _ in range(self.dim.rows)
            ]
            for _ in range(self.dim.cols)
        ]
        self.set_random_nplaypens(self.nchildren)
        self.set_random_nCellTypes(self.nobstacles, CellContent.Obstacle)
        self.set_random_nCellTypes(self.ndirtyCells, CellContent.Dirty)
        self.set_random_nagents(self.nagents, agentModel=self.agent_model)
        self.set_random_nchildren(self.nchildren, childModel=self.child_model)

    def set_random_nCellTypes(self, n, content_type: CellContent):
        for _ in range(n):
            while True:
                coord = Coordinates(
                    randint(0, self.dim.cols-1),
                    randint(0, self.dim.rows-1),
                )
                if self.floor[coord.col][coord.row] == CellContent.Empty and not self.occuped(coord):
                    self.floor[coord.col][coord.row] = content_type
                    if n == 1:
                        return coord
                    break

    def occuped(self, coord): return (
        any(a.coord == coord for a in self.agents) or
        any(ch.coord == coord for ch in self.children)
    )

    def set_random_nplaypens(self, n):
        initial = self.set_random_nCellTypes(1, CellContent.Playpen)
        self.floor[initial.col][initial.row] = CellContent.Playpen
        count = n-1
        connected = self.connected_cells(initial)
        ady: Coordinates = None
        for _ in range(count):
            try:
                ady = next(connected)
            except StopIteration:
                raise Exception('not enought space')
            self.floor[ady.col][ady.row] = CellContent.Playpen

    def set_random_nagents(self, n, agentModel=None, objs: List[HouseAgent] = None):
        assert agentModel or objs, 'invalid arguments'
        for _ in range(n):
            while True:
                coord = Coordinates(
                    randint(0, self.dim.cols-1),
                    randint(0, self.dim.rows-1),
                )
                if self.floor[coord.col][coord.row] in (CellContent.Empty, CellContent.Dirty) and not self.occuped(coord):
                    ag = None
                    if objs:
                        ag = objs.pop()
                        ag.coord = coord
                    else:
                        ag = agentModel(coord)
                    self.agents.append(ag)
                    break

    def set_random_nchildren(self, n, childModel=None, objs: List[Child] = None):
        assert childModel or objs, 'invalid arguments'
        for _ in range(n):
            while True:
                coord = Coordinates(
                    randint(0, self.dim.cols-1),
                    randint(0, self.dim.rows-1),
                )
                if self.floor[coord.col][coord.row] == CellContent.Empty and not self.occuped(coord):
                    ch = None
                    if objs:
                        ch = objs.pop()
                        ch.coordinates = coord
                    else:
                        ch = childModel(coord)
                    self.children.append(ch)
                    break

    # endregion

    # region Enviroment Change
    def randomize(self):
        old_floor = self.floor
        old_children = self.children
        self.floor = [
            [
                CellContent.Empty
                for _ in range(self.dim.rows)
            ]
            for _ in range(self.dim.cols)
        ]
        self.children = []
        free_children = []
        children_in_playpens = []

        ndirt = sum(
            cell == CellContent.Dirty
            for row in old_floor
            for cell in row
        )
        for child in old_children:
            if not (child.holded or child.in_playpen(old_floor)):
                free_children.append(child)
            if child.in_playpen(old_floor):
                children_in_playpens.append(child)
        playpens = self.set_random_nplaypens(self.nchildren)
        # set children
        selected = set()
        for child in children_in_playpens:
            while True:
                coord = choice(playpens)
                if coord in selected:
                    continue
                selected.add(coord)
                child.coord = coord
                break
        print('free_children: ', free_children)
        print('children_playpen: ', children_in_playpens)

        self.set_random_nCellTypes(self.nobstacles, CellContent.Obstacle)
        self.set_random_nCellTypes(ndirt, CellContent.Dirty)
        self.set_random_nagents(self.nagents, objs=self.agents)
        if free_children:
            self.set_random_nchildren(self.nchildren, objs=free_children)
    # endregion

    # region Flow

    def turn_cycle(self, verbose=False, stepbystep=False):
        while (
                self.turn < self.nturns and   # time end
                self.dirt_percent <= 60 and   # too dirty to continue
                not self.everythingIsClean()  # all children in playpens and all cells clean
        ):
            # agents actions
            # for agent in self.agents:
            #     action = agent.action(self)
            #     self.execute_agent_action(agent, action)

            # # children actions
            # for child in self.children:
            #     action = child.action(self)
            #     self.execute_child_action(child, action)

            # randomize environment
            if self.isRandomizeTime():
                self.randomize()

            if stepbystep or verbose:
                print(self)
            if stepbystep:
                input()
            self.turn += 1
        if self.everythingIsClean():
            return SimulationResult(conclusion=Conclusion.CompletedTask, dirt=0)
        elif self.dirt_percent > 60:
            return SimulationResult(conclusion=Conclusion.FailedTask, dirt=sum(cell == CellContent.Dirty for cell in row for row in self.floor))
        elif self.turn == self.nturns:
            return SimulationResult(conclusion=Conclusion.StabilizedHouse, dirt=sum(cell == CellContent.Dirty for cell in row for row in self.floor))
        else:
            raise Exception('undetermined status')

    def everythingIsClean(self):
        return (
            all(
                self[child.coord] == CellContent.Playpen
                for child in self.children
            )
            and not any(cell == CellContent.Dirty for cell in row for row in self.floor)
        )

    def isRandomizeTime(self):
        pass

    def execute_agent_action(self, agent, action):
        pass

    def execute_child_action(self, child, action):
        pass

    @ property
    def house_is_clean(self):
        return self.dirt_percent < 60

    @ property
    def dirt_percent(self):
        dirty_floor = 0
        empty_floor = 0
        for r, row in enumerate(self.floor):
            for c, cell in enumerate(row):
                if any(
                    ag.coord == (c, r)
                    for ag in self.agents
                ) and any(
                    ch.coord == (c, r)
                    for ch in self.children
                ):
                    continue
                dirty_floor += CellContent.Dirty == cell
                empty_floor += cell in (CellContent.Dirty,
                                        CellContent.Empty)

        return (100 * dirty_floor // empty_floor)

    @ property
    def clean_percent(self):
        return 100 - self.dirt_percent
    # endregion

    # region Commons

    def connected_cells(self, coord, extended=False):
        dirs = Directions.ALL_EXTENDED if extended else Directions.ALL
        adys = (
            Coordinates(coord.col + dc, coord.row + dr)
            for dc, dr in dirs
            if coord.col + dc < self.dim.cols and
            coord.row + dr < self.dim.rows
        )
        shuffle(adys)
        while adys:
            ady = adys.pop()
            yield ady
            adys += (
                Coordinates(ady.col + dc, ady.row + dr)
                for dc, dr in dirs
                if ady.col + dc < self.dim.cols and
                ady.row + dr < self.dim.rows
            )
            shuffle(adys)

    # endregion
