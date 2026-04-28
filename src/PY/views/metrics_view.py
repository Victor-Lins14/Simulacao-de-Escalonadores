import tkinter as tk
from views.theme import (
    GANTT_COLORS, BG, WHITE, ROW_ALT, TEXT, TEXT_MUTED, BORDER, CYAN_DARK, GRAY,
)

_COLS = ["Processo", "Chegada", "Burst", "Conclusão", "Turnaround", "Espera"]


def draw_metrics(parent, metricas, tme, tmt):
    tk.Label(parent, text="Métricas por Processo",
             bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
             anchor="w").pack(anchor="w", pady=(0, 6))
    tk.Frame(parent, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

    card = tk.Frame(parent, bg=WHITE, relief="solid", bd=1)
    card.pack(fill="x", pady=(0, 20))

    hdr = tk.Frame(card, bg=GRAY)
    hdr.pack(fill="x")
    for col in _COLS:
        tk.Label(hdr, text=col, bg=GRAY, fg=WHITE,
                 font=("Segoe UI", 10, "bold"),
                 anchor="center", pady=10, width=12).pack(
            side="left", expand=True, fill="x")

    for idx, m in enumerate(metricas):
        bg_c = WHITE if idx % 2 == 0 else ROW_ALT
        row  = tk.Frame(card, bg=bg_c)
        row.pack(fill="x")
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

        gc_bg, gc_fg = GANTT_COLORS[m["color_idx"] % len(GANTT_COLORS)]
        values = [m["pid"], m["arrival"], m["burst"], m["ct"], m["tat"], m["wt"]]

        for i, val in enumerate(values):
            if i == 0:
                badge_frame = tk.Frame(row, bg=bg_c)
                badge_frame.pack(side="left", expand=True, fill="x",
                                  pady=8, padx=4)
                tk.Label(badge_frame, text=str(val), bg=gc_bg, fg=gc_fg,
                         font=("Segoe UI", 10, "bold"),
                         padx=10, pady=2, relief="flat").pack()
            else:
                tk.Label(row, text=str(val), bg=bg_c, fg=TEXT,
                         font=("Segoe UI", 10),
                         anchor="center", width=12).pack(
                    side="left", expand=True, fill="x", pady=8)

    _draw_summary(parent, tme, tmt)


def _draw_summary(parent, tme, tmt):
    summary = tk.Frame(parent, bg=BG)
    summary.pack(fill="x", pady=(4, 0))

    cards = [
        ("Tempo Médio de Espera (TME)",      f"{tme:.2f}",
         "Média do tempo em fila de prontos"),
        ("Tempo Médio de Turnaround (TMT)",  f"{tmt:.2f}",
         "Média do tempo total de conclusão"),
    ]

    for i, (label, val, desc) in enumerate(cards):
        padx = (0, 12) if i == 0 else 0
        c = tk.Frame(summary, bg=WHITE, relief="solid", bd=1)
        c.pack(side="left", expand=True, fill="x", padx=padx, pady=4)
        tk.Label(c, text=label, bg=WHITE, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(
            anchor="w", padx=16, pady=(14, 0))
        tk.Label(c, text=val, bg=WHITE, fg=CYAN_DARK,
                 font=("Segoe UI", 26, "bold"), anchor="w").pack(
            anchor="w", padx=16)
        tk.Label(c, text=desc, bg=WHITE, fg=TEXT_MUTED,
                 font=("Segoe UI", 9), anchor="w").pack(
            anchor="w", padx=16, pady=(0, 14))
