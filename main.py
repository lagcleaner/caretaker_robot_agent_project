from src.environment.house import House
from src.commons.dimensions import Dimensions
from src.commons.cellcontent import CellContent
from src.agents import DummyRobot, FocusedRobot


def runNtimes(N: int, agentModels: dict, dimension: Dimensions, **kwrgs):
    all_conclusions = {modelName: None for modelName in agentModels}
    for modelName, model in agentModels.items():
        conclusions = []
        for _ in range(N):
            house = House(dimension, model, **kwrgs)
            conclusion = house.turn_cycle()
            conclusions.append(conclusion)
        all_conclusions[modelName] = conclusions
    #
    return all_conclusions
if __name__ == "__main__":
    house = House(
        Dimensions(15, 15), HouseAgent,
        dirtyCells_percent=0, obstacleCells_percent=30,
        number_of_children=3
    )
    conclusion = house.turn_cycle(stepbystep=True)
    print(conclusion)
