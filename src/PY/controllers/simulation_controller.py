from models.process import Process
from services.registry import build_scheduler, get_algorithm_info
from views.theme import GANTT_COLORS


class SimulationController:
    """Wires view events to model logic.

    Depends on the view's public interface only — never touches Tkinter widgets
    directly. Depends on IScheduler via the registry abstraction (D in SOLID).
    """

    def __init__(self, view):
        self._view = view
        self._algorithm_info = {name: req for name, req in get_algorithm_info()}
        view.bind_add(self._on_add)
        view.bind_run(self._on_run)

    def _on_add(self):
        self._view.add_process_row()

    def _on_run(self):
        processes = self._parse_processes()
        if processes is None:
            return

        alg_name = self._view.get_algorithm_name()
        quantum = None

        if self._algorithm_info.get(alg_name, False):
            quantum = self._parse_quantum()
            if quantum is None:
                return

        scheduler = build_scheduler(alg_name, quantum)
        result = scheduler.run(processes)
        self._view.show_results(result)

    def _parse_processes(self):
        rows = self._view.get_process_data()
        processes = []
        for i, (pid, arrival_str, burst_str) in enumerate(rows):
            try:
                arrival = int(arrival_str)
                burst = int(burst_str)
                if arrival < 0 or burst < 1:
                    raise ValueError
            except ValueError:
                self._view.show_error(
                    "Erro",
                    f"{pid}: valores inválidos.\nChegada ≥ 0 e Burst ≥ 1."
                )
                return None
            processes.append(Process(pid, arrival, burst, i % len(GANTT_COLORS)))
        return processes

    def _parse_quantum(self):
        try:
            quantum = int(self._view.get_quantum())
            if quantum < 1:
                raise ValueError
            return quantum
        except ValueError:
            self._view.show_error("Erro", "Quantum deve ser um inteiro ≥ 1.")
            return None
