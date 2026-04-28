import tkinter as tk
from tkinter import messagebox
from typing import Callable, List, Tuple

from views.theme import BG
from views.components.header import HeaderView
from views.components.config_panel import ConfigPanelView
from views.components.process_table import ProcessTableView
from views.components.action_buttons import ActionButtonsView
from views.components.results_panel import ResultsPanelView
from models.process import SimulationResult


class MainWindow(tk.Tk):
    """Root window. Composes all view components and exposes a clean interface
    for the controller — no model imports beyond data transfer objects."""

    def __init__(self, algorithms: List[Tuple[str, bool]]):
        super().__init__()
        self.title("Simulador de Escalonamento de CPU")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(780, 500)

        header = HeaderView(self)
        header.pack(fill="x")

        scroll_frame = self._build_scrollable_body()

        self._config = ConfigPanelView(scroll_frame, algorithms)
        self._config.pack(fill="x", padx=28, pady=(24, 0))

        self._table = ProcessTableView(scroll_frame)
        self._table.pack(fill="x", padx=28, pady=(18, 0))

        self._buttons = ActionButtonsView(scroll_frame)
        self._buttons.pack(fill="x", padx=28, pady=(16, 0))

        self._results = ResultsPanelView(scroll_frame)
        self._results.pack(fill="x", padx=28, pady=(24, 32))

        self._table.add_row(0, 4)
        self._table.add_row(1, 3)
        self._table.add_row(2, 5)

    def _build_scrollable_body(self) -> tk.Frame:
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg=BG)
        fid = canvas.create_window((0, 0), window=frame, anchor="nw")

        canvas.bind("<Configure>", lambda e: canvas.itemconfig(fid, width=e.width))
        frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        return frame

    # ── Public interface for controller ────────────────────────────────────────

    def get_process_data(self) -> List[Tuple[str, str, str]]:
        return self._table.get_rows()

    def add_process_row(self):
        self._table.add_row()

    def get_algorithm_name(self) -> str:
        return self._config.get_algorithm_name()

    def get_quantum(self) -> str:
        return self._config.get_quantum()

    def show_results(self, result: SimulationResult):
        self._results.show(result)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def bind_add(self, callback: Callable):
        self._buttons.bind_add(callback)

    def bind_run(self, callback: Callable):
        self._buttons.bind_run(callback)
