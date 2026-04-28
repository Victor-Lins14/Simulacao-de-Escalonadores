from collections import deque
from typing import List

from models.process import Process, GanttBlock, ProcessMetrics, SimulationResult
from services.base_scheduler import IScheduler


class RoundRobinScheduler(IScheduler):
    def __init__(self, quantum: int):
        self._quantum = quantum

    @property
    def name(self) -> str:
        return "Round Robin"

    @property
    def requires_quantum(self) -> bool:
        return True

    def run(self, processes: List[Process]) -> SimulationResult:
        lista = [
            {"pid": p.pid, "arrival": p.arrival, "burst": p.burst,
             "remaining": p.burst, "color_idx": p.color_idx}
            for p in processes
        ]
        lista.sort(key=lambda x: x["arrival"])

        fila, in_fila = deque(), set()
        gantt: List[GanttBlock] = []
        ct: dict = {}
        t, done, i = 0, 0, 0

        while done < len(lista):
            while i < len(lista) and lista[i]["arrival"] <= t:
                if lista[i]["pid"] not in in_fila:
                    fila.append(lista[i])
                    in_fila.add(lista[i]["pid"])
                i += 1

            if not fila:
                t = lista[i]["arrival"]
                continue

            p = fila.popleft()
            ex = min(self._quantum, p["remaining"])
            gantt.append(GanttBlock(p["pid"], t, t + ex, p["color_idx"]))
            t += ex
            p["remaining"] -= ex

            while i < len(lista) and lista[i]["arrival"] <= t:
                if lista[i]["pid"] not in in_fila:
                    fila.append(lista[i])
                    in_fila.add(lista[i]["pid"])
                i += 1

            if p["remaining"] > 0:
                fila.append(p)
            else:
                ct[p["pid"]] = t
                done += 1

        metrics = []
        for p in processes:
            tat = ct[p.pid] - p.arrival
            wt = tat - p.burst
            metrics.append(ProcessMetrics(p.pid, p.arrival, p.burst, ct[p.pid], tat, wt, p.color_idx))

        tme = sum(m.wt for m in metrics) / len(metrics) if metrics else 0.0
        tmt = sum(m.tat for m in metrics) / len(metrics) if metrics else 0.0

        return SimulationResult(gantt, metrics, tme, tmt)
