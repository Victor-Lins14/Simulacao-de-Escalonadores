import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple

from views.theme import BG, BORDER, GRAY, RED, ROW_ALT, TEXT, WHITE


class ProcessTableView(tk.Frame):
    """Manages the editable process rows."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG)

        hdr = tk.Frame(self, bg=GRAY)
        hdr.pack(fill="x")
        for col, w in [("Processo", 120), ("Tempo de Chegada", 260),
                       ("Tempo de Execução", 260), ("Ações", 80)]:
            tk.Label(hdr, text=col, bg=GRAY, fg=WHITE,
                     font=("Segoe UI", 10, "bold"),
                     width=w // 8, anchor="center",
                     pady=10).pack(side="left", expand=True, fill="x")

        self._rows_frame = tk.Frame(self, bg=WHITE, relief="solid", bd=1)
        self._rows_frame.pack(fill="x")

        self._rows: List[dict] = []

    def add_row(self, arrival="", burst=""):
        idx = len(self._rows)
        pid = f"P{idx + 1}"
        bg = WHITE if idx % 2 == 0 else ROW_ALT

        row_frame = tk.Frame(self._rows_frame, bg=bg)
        row_frame.pack(fill="x")
        sep = tk.Frame(self._rows_frame, bg=BORDER, height=1)
        sep.pack(fill="x")

        lbl_pid = tk.Label(row_frame, text=pid, bg=bg, fg=TEXT,
                           font=("Segoe UI", 11, "bold"), width=12, anchor="center")
        lbl_pid.pack(side="left", pady=8)

        arr_var = tk.StringVar(value=str(arrival))
        tk.Entry(row_frame, textvariable=arr_var,
                 font=("Segoe UI", 11), justify="center",
                 relief="solid", bd=1, width=18).pack(
            side="left", expand=True, fill="x", padx=12, pady=8)

        bst_var = tk.StringVar(value=str(burst))
        tk.Entry(row_frame, textvariable=bst_var,
                 font=("Segoe UI", 11), justify="center",
                 relief="solid", bd=1, width=18).pack(
            side="left", expand=True, fill="x", padx=12, pady=8)

        btn = tk.Button(row_frame, text="🗑", bg=bg, fg=RED,
                        font=("Segoe UI Emoji", 13), relief="flat",
                        cursor="hand2", width=3)
        btn.pack(side="left", padx=4)

        data = {"pid": pid, "arr_var": arr_var, "bst_var": bst_var,
                "row_frame": row_frame, "sep": sep, "lbl_pid": lbl_pid, "btn": btn}
        btn.config(command=lambda d=data: self._del_row(d))

        self._rows.append(data)
        self._reindex()

    def _del_row(self, data: dict):
        if len(self._rows) <= 1:
            messagebox.showwarning("Aviso", "É necessário pelo menos 1 processo.")
            return
        data["row_frame"].destroy()
        data["sep"].destroy()
        self._rows.remove(data)
        self._reindex()

    def _reindex(self):
        for i, row in enumerate(self._rows):
            pid = f"P{i + 1}"
            row["pid"] = pid
            row["lbl_pid"].config(text=pid)
            bg = WHITE if i % 2 == 0 else ROW_ALT
            row["row_frame"].config(bg=bg)
            row["lbl_pid"].config(bg=bg)
            row["btn"].config(bg=bg)

    def get_rows(self) -> List[Tuple[str, str, str]]:
        return [(r["pid"], r["arr_var"].get(), r["bst_var"].get()) for r in self._rows]

    def row_count(self) -> int:
        return len(self._rows)
