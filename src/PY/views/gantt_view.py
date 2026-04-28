import tkinter as tk
from tkinter import ttk
from views.theme import (
    GANTT_COLORS, BG, WHITE, TEXT, TEXT_MUTED, BORDER, CYAN_DARK, GRAY,
)


def draw_gantt(parent, gantt):
    tk.Label(parent, text="Gráfico de Gantt",
             bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
             anchor="w").pack(anchor="w", pady=(0, 6))
    tk.Frame(parent, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

    card = tk.Frame(parent, bg=WHITE, relief="solid", bd=1)
    card.pack(fill="x", pady=(0, 24))

    canvas = tk.Canvas(card, bg=WHITE, highlightthickness=0, height=80)
    h_scroll = ttk.Scrollbar(card, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=h_scroll.set)
    h_scroll.pack(side="bottom", fill="x")
    canvas.pack(fill="x", padx=16, pady=(12, 0))

    total = gantt[-1]["end"] if gantt else 0
    unit  = max(52, min(90, 700 // (total if total > 0 else 1)))
    canvas.configure(scrollregion=(0, 0, total * unit + 40, 80))

    BAR_Y1, BAR_Y2, TICK_Y = 8, 48, 56

    for g in gantt:
        x1 = g["start"] * unit
        x2 = g["end"]   * unit
        bg_c, fg_c = GANTT_COLORS[g["color_idx"] % len(GANTT_COLORS)]

        canvas.create_rectangle(x1, BAR_Y1, x2, BAR_Y2,
                                 fill=bg_c, outline=CYAN_DARK, width=1)
        canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 - 6,
                            text=g["pid"], fill=fg_c,
                            font=("Segoe UI", 10, "bold"))
        canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 + 8,
                            text=f"{g['start']}–{g['end']}", fill=fg_c,
                            font=("Segoe UI", 8))

    if gantt:
        ticks = sorted(set(g["start"] for g in gantt) | {gantt[-1]["end"]})
        for tick in ticks:
            x = tick * unit
            canvas.create_line(x, BAR_Y2, x, TICK_Y - 2, fill=BORDER, width=1)
            canvas.create_text(x, TICK_Y, text=str(tick),
                                fill=TEXT_MUTED, font=("Segoe UI", 8))
