from dataclasses import dataclass
from typing import List


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    color_idx: int = 0


@dataclass
class GanttBlock:
    pid: str
    start: int
    end: int
    color_idx: int


@dataclass
class ProcessMetrics:
    pid: str
    arrival: int
    burst: int
    ct: int
    tat: int
    wt: int
    color_idx: int


@dataclass
class SimulationResult:
    gantt: List[GanttBlock]
    metrics: List[ProcessMetrics]
    tme: float
    tmt: float
