import tkinter as tk
from tkinter import ttk

from models.process import SimulationResult
from views.theme import (
    BG, BORDER, CYAN_DARK, GANTT_COLORS, GRAY, ROW_ALT, TEXT, TEXT_MUTED, WHITE
)


class ResultsPanelView(tk.Frame):
    """Renders Gantt chart and metrics table for a SimulationResult."""

    def __init__(self, parent):
        super().__init__(parent, bg=BG)

    def show(self, result: SimulationResult):
        for widget in self.winfo_children():
            widget.destroy()
        self._draw_gantt(result.gantt)
        self._draw_metrics(result.metrics, result.tme, result.tmt)

    def _draw_gantt(self, gantt):
        tk.Label(self, text="Gráfico de Gantt",
                 bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
                 anchor="w").pack(anchor="w", pady=(0, 6))
        tk.Frame(self, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

        card = tk.Frame(self, bg=WHITE, relief="solid", bd=1)
        card.pack(fill="x", pady=(0, 24))

        canvas = tk.Canvas(card, bg=WHITE, highlightthickness=0, height=80)
        h_scroll = ttk.Scrollbar(card, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side="bottom", fill="x")
        canvas.pack(fill="x", padx=16, pady=(12, 0))

        total = gantt[-1].end if gantt else 0
        UNIT = max(52, min(90, 700 // (total if total > 0 else 1)))
        canvas.configure(scrollregion=(0, 0, total * UNIT + 40, 80))

        BAR_Y1, BAR_Y2, TICK_Y = 8, 48, 56

        for g in gantt:
            x1 = g.start * UNIT
            x2 = g.end * UNIT
            bg_c, fg_c = GANTT_COLORS[g.color_idx % len(GANTT_COLORS)]
            canvas.create_rectangle(x1, BAR_Y1, x2, BAR_Y2,
                                    fill=bg_c, outline=CYAN_DARK, width=1)
            canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 - 6,
                                text=g.pid, fill=fg_c, font=("Segoe UI", 10, "bold"))
            canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 + 8,
                                text=f"{g.start}–{g.end}", fill=fg_c, font=("Segoe UI", 8))

        if gantt:
            ticks = sorted(set(g.start for g in gantt) | {gantt[-1].end})
            for t in ticks:
                x = t * UNIT
                canvas.create_line(x, BAR_Y2, x, TICK_Y - 2, fill=BORDER, width=1)
                canvas.create_text(x, TICK_Y, text=str(t),
                                   fill=TEXT_MUTED, font=("Segoe UI", 8))

    def _draw_metrics(self, metrics, tme: float, tmt: float):
        tk.Label(self, text="Métricas por Processo",
                 bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
                 anchor="w").pack(anchor="w", pady=(0, 6))
        tk.Frame(self, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

        card = tk.Frame(self, bg=WHITE, relief="solid", bd=1)
        card.pack(fill="x", pady=(0, 20))

        hdr = tk.Frame(card, bg=GRAY)
        hdr.pack(fill="x")
        for col in ["Processo", "Chegada", "Burst", "Conclusão", "Turnaround", "Espera"]:
            tk.Label(hdr, text=col, bg=GRAY, fg=WHITE,
                     font=("Segoe UI", 10, "bold"),
                     anchor="center", pady=10, width=12).pack(
                side="left", expand=True, fill="x")

        for idx, m in enumerate(metrics):
            bg_c = WHITE if idx % 2 == 0 else ROW_ALT
            row = tk.Frame(card, bg=bg_c)
            row.pack(fill="x")
            tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

            gc_bg, gc_fg = GANTT_COLORS[m.color_idx % len(GANTT_COLORS)]
            for i, val in enumerate([m.pid, m.arrival, m.burst, m.ct, m.tat, m.wt]):
                if i == 0:
                    f = tk.Frame(row, bg=bg_c)
                    f.pack(side="left", expand=True, fill="x", pady=8, padx=4)
                    tk.Label(f, text=str(val), bg=gc_bg, fg=gc_fg,
                             font=("Segoe UI", 10, "bold"),
                             padx=10, pady=2, relief="flat").pack()
                else:
                    tk.Label(row, text=str(val), bg=bg_c, fg=TEXT,
                             font=("Segoe UI", 10), anchor="center", width=12).pack(
                        side="left", expand=True, fill="x", pady=8)

        summary = tk.Frame(self, bg=BG)
        summary.pack(fill="x", pady=(4, 0))

        for label, val, desc, side_pad in [
            ("Tempo Médio de Espera (TME)", f"{tme:.2f}",
             "Média do tempo em fila de prontos", (0, 12)),
            ("Tempo Médio de Turnaround (TMT)", f"{tmt:.2f}",
             "Média do tempo total de conclusão", (0, 0)),
        ]:
            c = tk.Frame(summary, bg=WHITE, relief="solid", bd=1)
            c.pack(side="left", expand=True, fill="x", padx=side_pad, pady=4)
            tk.Label(c, text=label, bg=WHITE, fg=TEXT_MUTED,
                     font=("Segoe UI", 9, "bold"), anchor="w").pack(
                anchor="w", padx=16, pady=(14, 0))
            tk.Label(c, text=val, bg=WHITE, fg=CYAN_DARK,
                     font=("Segoe UI", 26, "bold"), anchor="w").pack(anchor="w", padx=16)
            tk.Label(c, text=desc, bg=WHITE, fg=TEXT_MUTED,
                     font=("Segoe UI", 9), anchor="w").pack(
                anchor="w", padx=16, pady=(0, 14))
