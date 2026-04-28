import tkinter as tk
from typing import Callable

from views.theme import BG, CYAN, GRAY, WHITE


class ActionButtonsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        self._btn_add = tk.Button(self, text="＋  Adicionar Processo",
                                  bg=CYAN, fg=WHITE,
                                  font=("Segoe UI", 12, "bold"),
                                  relief="flat", cursor="hand2", pady=12)
        self._btn_add.pack(fill="x", pady=(0, 10))

        self._btn_run = tk.Button(self, text="▶  Executar Simulação",
                                  bg=GRAY, fg=WHITE,
                                  font=("Segoe UI", 12, "bold"),
                                  relief="flat", cursor="hand2", pady=12)
        self._btn_run.pack(fill="x")

        self._btn_add.bind("<Enter>", lambda e: self._btn_add.config(bg="#424242"))
        self._btn_add.bind("<Leave>", lambda e: self._btn_add.config(bg=CYAN))
        self._btn_run.bind("<Enter>", lambda e: self._btn_run.config(bg="#60d3e8"))
        self._btn_run.bind("<Leave>", lambda e: self._btn_run.config(bg=GRAY))

    def bind_add(self, callback: Callable):
        self._btn_add.config(command=callback)

    def bind_run(self, callback: Callable):
        self._btn_run.config(command=callback)
