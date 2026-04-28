import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from views.theme import BG, TEXT_MUTED


class ConfigPanelView(tk.Frame):
    """Algorithm selector + optional quantum field.

    algorithms: list of (name, requires_quantum) pairs — injected by MainWindow
    so this component has zero dependency on the model layer.
    """

    def __init__(self, parent, algorithms: List[Tuple[str, bool]]):
        super().__init__(parent, bg=BG)
        self._requires_quantum = {name: req for name, req in algorithms}
        names = [name for name, _ in algorithms]

        left = tk.Frame(self, bg=BG)
        left.pack(side="left", fill="x", expand=True, padx=(0, 16))
        tk.Label(left, text="Algoritmo de Escalonamento", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        self._alg_var = tk.StringVar(value=names[0])
        cb = ttk.Combobox(left, textvariable=self._alg_var,
                          values=names, state="readonly",
                          font=("Segoe UI", 11))
        cb.pack(fill="x", pady=(4, 0), ipady=4)
        cb.bind("<<ComboboxSelected>>", self._on_alg_change)

        self._quantum_frame = tk.Frame(self, bg=BG, width=200)
        self._quantum_frame.pack(side="right", fill="y")
        self._quantum_frame.pack_propagate(False)
        tk.Label(self._quantum_frame, text="Quantum", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self._quantum_var = tk.StringVar(value="2")
        tk.Entry(self._quantum_frame, textvariable=self._quantum_var,
                 font=("Segoe UI", 11), justify="left",
                 relief="solid", bd=1).pack(fill="x", pady=(4, 0), ipady=4)

    def _on_alg_change(self, _=None):
        if self._requires_quantum.get(self._alg_var.get(), False):
            self._quantum_frame.pack(side="right", fill="y")
        else:
            self._quantum_frame.pack_forget()

    def get_algorithm_name(self) -> str:
        return self._alg_var.get()

    def get_quantum(self) -> str:
        return self._quantum_var.get()
