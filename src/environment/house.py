
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
        turn = f'(turn: {self.turn}/{self.nturns})'
        res = ''
        for r in range(len(self.floor[0])):
            res += '\n'
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
                elif any(ch.coord == (c, r) for ch in self.children if not ch.holded and not ch.in_playpen(self.floor)):
                    content = 'C'
                res += content
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
        playpens = [initial]
        for _ in range(count):
            try:
                ady = next(connected)
            except StopIteration:
                raise Exception('not enought space')
            self.floor[ady.col][ady.row] = CellContent.Playpen
            playpens.append(ady)
        return playpens

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
                        ch.coord = coord
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
        self.children: List[Child] = []
        free_children: List[Child] = []
        children_in_playpens: List[CellContent] = []

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

        self.set_random_nCellTypes(self.nobstacles, CellContent.Obstacle)
        self.set_random_nCellTypes(ndirt, CellContent.Dirty)
        self.set_random_nagents(self.nagents, objs=self.agents)
        if free_children:
            self.set_random_nchildren(len(free_children), objs=free_children)
    # endregion

    # region Flow

    def turn_cycle(self, verbose=False, stepbystep=False, warnings=False):
        print('Initialized...')
        while (
                self.turn < self.nturns and   # time end
                self.dirt_percent <= 60 and   # too dirty to continue
                not self.everythingIsClean()  # all children in playpens and all cells clean
        ):
            if stepbystep or verbose:
                # print('  <previus_status>')
                print(self)
                # print('children:', self.children)
                # print('agents:  ', self.agents)
            if stepbystep:
                input()

            if verbose or stepbystep:
                print('  <agents_actions>')
            for agent in self.agents:
                actions = agent.action(self)
                if verbose or stepbystep:
                    print(agent, actions)
                for action in actions:
                    if self.execute_agent_action(agent, action, warnings=warnings):
                        break
            if verbose or stepbystep:
                print('  <agents_actions/>')

            coords = []
            if verbose or stepbystep:
                print('  <child_actions>')
            for child in self.children:
                action = child.action(self)
                coord = self.execute_child_action(child, action)
                if verbose or stepbystep:
                    print(child, action)
                if self[coord] != CellContent.Playpen and not child.holded:
                    coords.append(coord)
                    coords.extend(self.get_adyacents(coord, extended=True))
            self.dirty(coords)
            if verbose or stepbystep:
                print('  <child_actions/>\n')

            # randomize environment
            if self.isRandomizeTime():
                if verbose or stepbystep:
                    print('  <environment_variation/>')
                self.randomize()

            self.turn += 1

        print('Concluded...')
        # Conclusion
        if self.everythingIsClean():
            return SimulationResult(conclusion=Conclusion.CompletedTask, dirt=0)
        elif self.dirt_percent > 60:
            return SimulationResult(conclusion=Conclusion.FailedTask, dirt=sum(cell == CellContent.Dirty for row in self.floor for cell in row))
        elif self.turn == self.nturns:
            return SimulationResult(conclusion=Conclusion.StabilizedHouse, dirt=sum(cell == CellContent.Dirty for row in self.floor for cell in row))
        else:
            raise Exception('undetermined status')

    def everythingIsClean(self):
        return (
            all(
                self[child.coord] == CellContent.Playpen
                for child in self.children
            )
            and not any(cell == CellContent.Dirty for row in self.floor for cell in row)
        )

    def isRandomizeTime(self):
        return not (self.turn % self.time_interval) and self.turn > 0

    def execute_agent_action(self, agent, action, warnings=False):
        if action == AgentAction.Stay:
            return False
        if action == AgentAction.Clean:
            if self[agent.coord] == CellContent.Dirty:
                self[agent.coord] = CellContent.Empty
                return False
            else:
                if warnings:
                    print('warning: attempting to clean in a clean cell')
                return False
        if action == AgentAction.CarryAChild:
            if agent.carrying is None:
                child_on_floor: Child = None
                for child in self.children:
                    if not child.holded and child.coord == agent.coord:
                        child_on_floor = child
                if child_on_floor is None:
                    if warnings:
                        print(
                            'warning: attempting to carry a child with not a single one')
                    return False
                child_on_floor.holded = True
                agent.carrying = child_on_floor
                return True
            else:
                if warnings:
                    print('warning: attempting to carry a child with one inside')
                return False
        if action == AgentAction.DropAChild:
            if not agent.carrying is None:
                child_in_playpen: Child = None
                for child in self.children:
                    if not child.holded and child.coord == agent.coord:
                        child_in_playpen = child
                        break
                if not child_in_playpen is None:
                    if warnings:
                        print(
                            'warning: attempting to drop a child with where is occuped')
                    return
                child = agent.carrying
                child.coord = agent.coord
                child.holded = False
                agent.carrying = None
                return True
            else:
                if warnings:
                    print(
                        'warning: attempting to drop a child with not a single one inside')
                return False
        new_coord = Coordinates.on_direction(
            agent.coord, AgentAction.todir(action)
        )
        if not self.in_range(new_coord):
            if warnings:
                print('warning: attempting to move out of the house limits')
            return False
        if (
            self[new_coord] == CellContent.Obstacle or (
                self[new_coord] == CellContent.Playpen and
                any(c for c in self.children if c.coord == new_coord)
            )
        ):
            if warnings:
                print('warning: attempting to move to a full playpen or obstacle')
            return False
        agent.coord = new_coord
        return False

    def available_directions(self, coord: Coordinates, double_stepping=False):
        dirs = []
        border = double_stepping + 1
        if coord.col < self.dim.cols-border:
            dirs.append(Directions.East)
        if coord.row < self.dim.rows-border:
            dirs.append(Directions.South)
        if coord.col > border-1:
            dirs.append(Directions.West)
        if coord.row > border-1:
            dirs.append(Directions.North)
        return dirs

    def execute_child_action(self, child, action):
        coord = child.coord
        if action == ChildAction.Stay:
            return coord
        if action.value < 5:  # Moving Actions
            direct = ChildAction.todir(action)
            next_coord = Coordinates.on_direction(child.coord, direct)

            if self[next_coord] == CellContent.Empty:
                child.coord = next_coord
                return coord
            elif self[next_coord] == CellContent.Obstacle and self.push_if_posible(next_coord, direct):
                child.coord = next_coord
                self[next_coord] = CellContent.Empty
                return coord
            else:
                return coord

    def push_if_posible(self, coord, direct):
        next_coord = Coordinates.on_direction(coord, direct)
        if not self.in_range(next_coord):
            return False
        if self[next_coord] == CellContent.Empty or (
            self[next_coord] == CellContent.Obstacle and
            self.push_if_posible(
                next_coord, direct)
        ):
            self[next_coord] = self[coord]
            return True
        else:
            return False

    def dirty(self, possible_dirt: List[Coordinates]):
        count = (
            1 if self.nchildren == 1 else
            3 if self.nchildren == 2 else 6
        )
        possible_dirt = [
            c for c in possible_dirt if self[c] == CellContent.Empty and not self.occuped(c)
        ]

        for c in possible_dirt:
            if count == 0:
                break
            if self[c] == CellContent.Empty and not self.occuped(c):
                messy = random() < 3 / 5
                self[c] = CellContent.Dirty if messy else self[c]
                count -= 1

    @property
    def house_is_clean(self):
        return self.dirt_percent < 60

    @property
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

    @property
    def clean_percent(self):
        return 100 - self.dirt_percent
    # endregion

    # region Commons
    def in_range(self, coord):
        return (0 <= coord[0] < self.dim.cols and 0 <= coord[1] < self.dim.rows)

    def get_adyacents(self, coord, extended=False):
        assert not (coord is None)
        dirs = Directions.rdirs(extended_directions=True)
        return (
            Coordinates.on_direction(coord, dr)
            for dr in dirs
            if 0 < coord.col + dr[0] < self.dim.cols-1 and
            0 < coord.row + dr[1] < self.dim.rows-1
        )

    def connected_cells(self, coord, extended=False):
        dirs = Directions.ALL_EXTENDED if extended else Directions.ALL
        adys = list(
            Coordinates.on_direction(coord, (dc, dr))
            for dc, dr in dirs
            if self.in_range((coord.col + dc, coord.row + dr))
        )
        shuffle(adys)
        while adys:
            ady = adys.pop()
            yield ady
            adys += list(
                Coordinates.on_direction(ady, (dc, dr))
                for dc, dr in dirs
                if self.in_range((ady.col + dc, ady.row + dr))
            )
            shuffle(adys)

    # endregion
