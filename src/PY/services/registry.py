from typing import Callable, Dict, List, Tuple

from services.base_scheduler import IScheduler
from services.round_robin_scheduler import RoundRobinScheduler
from services.srtf_scheduler import SRTFScheduler

# To add a new algorithm: add an entry here and a new IScheduler subclass.
# No other file needs to change.
_REGISTRY: Dict[str, dict] = {
    "Round Robin": {
        "factory": lambda quantum: RoundRobinScheduler(quantum),
        "requires_quantum": True,
    },
    "SRTF (Shortest Remaining Time First)": {
        "factory": lambda _: SRTFScheduler(),
        "requires_quantum": False,
    },
}


def get_algorithm_info() -> List[Tuple[str, bool]]:
    return [(name, entry["requires_quantum"]) for name, entry in _REGISTRY.items()]


def build_scheduler(name: str, quantum: int) -> IScheduler:
    entry = _REGISTRY[name]
    return entry["factory"](quantum)
