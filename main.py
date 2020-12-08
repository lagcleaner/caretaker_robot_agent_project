from src.environment.house import House, Child
from src.commons.dimensions import Dimensions
from src.commons.cellcontent import CellContent
from src.commons.simulation_result import Conclusion, SimulationResult, SimulationCompiledResult
from src.agents import DummyRobot, FocusedRobot
from pprint import pprint

TESTS = (
    (
        Dimensions(10, 10), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 3,
            'dirtyCells_percent': 0,
            'obstacleCells_percent': 0,
            't': 10,
        }
    ),
    (
        Dimensions(15, 15), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 2,
            'dirtyCells_percent': 15,
            'obstacleCells_percent': 5,
            't': 16,
        }
    ),
    (
        Dimensions(20, 20), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 1,
            'dirtyCells_percent': 25,
            'obstacleCells_percent': 2,
            't': 11,
        }
    ),
    (
        Dimensions(15, 15), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 6,
            'dirtyCells_percent': 0,
            'obstacleCells_percent': 0,
            't': 12,
        }
    ),
    (
        Dimensions(20, 20), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 6,
            'dirtyCells_percent': 12,
            'obstacleCells_percent': 5,
            't': 12,
        }
    ),
    (
        Dimensions(20, 20), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 1,
            'dirtyCells_percent': 5,
            'obstacleCells_percent': 20,
            't': 14,
        }
    ),
    (
        Dimensions(10, 10), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 1,
            'dirtyCells_percent': 20,
            'obstacleCells_percent': 5,
            't': 14,
        }
    ),
    (
        Dimensions(15, 15), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 4,
            'dirtyCells_percent': 2,
            'obstacleCells_percent': 0,
            't': 10,
        }
    ),
    (
        Dimensions(20, 20), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 4,
            'dirtyCells_percent': 3,
            'obstacleCells_percent': 1,
            't': 14,
        }
    ),
    (
        Dimensions(25, 25), {
            'child_model': Child,
            'number_of_house_agents': 1,
            'number_of_children': 5,
            'dirtyCells_percent': 5,
            'obstacleCells_percent': 4,
            't': 15,
        }
    ),
)


def runNtimes(N: int, agentModels: dict, dimension: Dimensions, **kwrgs):
    all_results = {modelName: None for modelName in agentModels}
    for modelName, model in agentModels.items():
        results = []
        for _ in range(N):
            house = House(dimension, model, **kwrgs,)
            result = house.turn_cycle()
            # print(modelName, result)
            results.append(result)
        all_results[modelName] = results
    #
    return {model: process_results(results) for model, results in all_results.items()}


def process_results(results: list) -> SimulationCompiledResult:
    completed = 0
    stabilized = 0
    failed = 0
    #
    dirty_amounts = 0
    #
    for res in results:
        completed += res.conclusion == Conclusion.CompletedTask
        failed += res.conclusion == Conclusion.FailedTask
        stabilized += res.conclusion == Conclusion.StabilizedHouse
        dirty_amounts += res.dirt

    _, concl = max(
        (completed, Conclusion.CompletedTask),
        (stabilized, Conclusion.StabilizedHouse),
        (failed, Conclusion.FailedTask), key=lambda elm: elm[0]
    )
    return SimulationCompiledResult(
        conclusion=concl,
        dirtyAverage=dirty_amounts/len(results),
        failedTasksPercent=100*failed/len(results),
        completedTasksPercent=100*completed/len(results),
    )


def print_board_params(dim, **kwargs):
    print(dim, ',', ', '.join([f'{k}: {a}' for k, a in kwargs.items()]))


if __name__ == "__main__":
    N = 30

    agentModels = {
        'ShortPerception     (DummyRobot)': DummyRobot,
        'LongTermPerception(FocusedRobot)': FocusedRobot
    }
    print('-'*60)

    for dim, kwargs in TESTS:
        results = runNtimes(N, agentModels, dim, **kwargs)
        print_board_params(dim, **kwargs)
        print()
        for model, res in results.items():
            print(model, ': ')
            print(res)
        print('-'*60)
