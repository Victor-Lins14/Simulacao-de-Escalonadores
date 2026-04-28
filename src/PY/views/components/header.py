import tkinter as tk
from views.theme import GRAY, WHITE


class HeaderView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=GRAY, height=56)
        self.pack_propagate(False)

        tk.Label(self, text="⚙", bg=GRAY, fg=WHITE,
                 font=("Segoe UI Emoji", 20)).pack(side="left", padx=(18, 8), pady=10)
        tk.Label(self, text="Simulador de Escalonamento de CPU",
                 bg=GRAY, fg=WHITE,
                 font=("Segoe UI", 14, "bold")).pack(side="left", pady=10)
