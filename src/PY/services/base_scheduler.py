from abc import ABC, abstractmethod
from typing import List
from models.process import Process, SimulationResult


class IScheduler(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def requires_quantum(self) -> bool: ...

    @abstractmethod
    def run(self, processes: List[Process]) -> SimulationResult: ...
