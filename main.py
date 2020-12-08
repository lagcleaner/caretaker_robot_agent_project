from src.environment.house import House
from src.commons.dimensions import Dimensions
from src.commons.cellcontent import CellContent
from src.agents import DummyRobot, FocusedRobot

if __name__ == "__main__":
    house = House(
        Dimensions(15, 15), HouseAgent,
        dirtyCells_percent=0, obstacleCells_percent=30,
        number_of_children=3
    )
    conclusion = house.turn_cycle(stepbystep=True)
    print(conclusion)
