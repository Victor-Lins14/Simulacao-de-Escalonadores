from typing import List

from models.process import Process, GanttBlock, ProcessMetrics, SimulationResult
from services.base_scheduler import IScheduler


class SRTFScheduler(IScheduler):
    @property
    def name(self) -> str:
        return "SRTF (Shortest Remaining Time First)"

    @property
    def requires_quantum(self) -> bool:
        return False

    def run(self, processes: List[Process]) -> SimulationResult:
        lista = [
            {"pid": p.pid, "arrival": p.arrival, "burst": p.burst,
             "remaining": p.burst, "color_idx": p.color_idx}
            for p in processes
        ]

        t, done, n = 0, 0, len(lista)
        gantt: List[GanttBlock] = []
        ct: dict = {}
        current_pid, block_start, current_color = None, 0, 0

        while done < n:
            available = [p for p in lista if p["arrival"] <= t and p["remaining"] > 0]

            if not available:
                if current_pid is not None:
                    gantt.append(GanttBlock(current_pid, block_start, t, current_color))
                    current_pid = None
                t = min(p["arrival"] for p in lista if p["remaining"] > 0)
                continue

            available.sort(key=lambda x: (x["remaining"], x["arrival"]))
            shortest = available[0]

            if shortest["pid"] != current_pid:
                if current_pid is not None:
                    gantt.append(GanttBlock(current_pid, block_start, t, current_color))
                current_pid = shortest["pid"]
                block_start = t
                current_color = shortest["color_idx"]

            shortest["remaining"] -= 1
            t += 1

            if shortest["remaining"] == 0:
                gantt.append(GanttBlock(current_pid, block_start, t, current_color))
                ct[shortest["pid"]] = t
                current_pid = None
                done += 1

        metrics = []
        for p in processes:
            tat = ct[p.pid] - p.arrival
            wt = tat - p.burst
            metrics.append(ProcessMetrics(p.pid, p.arrival, p.burst, ct[p.pid], tat, wt, p.color_idx))

        tme = sum(m.wt for m in metrics) / len(metrics) if metrics else 0.0
        tmt = sum(m.tat for m in metrics) / len(metrics) if metrics else 0.0

        return SimulationResult(gantt, metrics, tme, tmt)
