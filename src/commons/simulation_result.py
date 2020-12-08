from typing import NamedTuple
from enum import Enum


class Conclusion(Enum):
    CompletedTask = 1
    StabilizedHouse = 2
    FailedTask = 3


class SimulationResult(NamedTuple):
    conclusion: Conclusion
    dirt: float


class SimulationCompiledResult(NamedTuple):
    conclusion: Conclusion
    dirtyAverage: float
    failedTaskAverage: float
    completedTaskAverage: float
