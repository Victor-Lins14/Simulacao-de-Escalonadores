import tkinter as tk
from tkinter import ttk, messagebox

# Importa os algoritmos dos arquivos separados
from round_robin import round_robin
from srtf import srtf

# ── Paleta de cores ────────────────────────────────────────────────────────────
CYAN        = "#00bcd4"
CYAN_DARK   = "#0097a7"
CYAN_LIGHT  = "#e0f7fa"
ORANGE      = "#ff9800"
WHITE       = "#ffffff"
BG          = "#f5f7fa"
ROW_ALT     = "#f0f4f8"
TEXT        = "#1a2533"
TEXT_MUTED  = "#607080"
BORDER      = "#d0dce8"
RED         = "#e53935"
RED_LIGHT   = "#ffebee"
GRAY        = "#515151"

GANTT_COLORS = [
    ("#b2ebf2", "#006064"),
    ("#c8e6c9", "#1b5e20"),
    ("#ffe0b2", "#bf360c"),
    ("#e1bee7", "#4a148c"),
    ("#fce4ec", "#880e4f"),
    ("#fff9c4", "#f57f17"),
    ("#b3e5fc", "#01579b"),
    ("#dcedc8", "#33691e"),
]

# ── Aplicação principal ────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Escalonamento de CPU")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(780, 500)

        self.process_rows = []   

        self._build_header()
        self._build_body()
        self._add_default_rows()

    # ── Header ─────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=GRAY, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="Simulador de Escalonamento de CPU",
                 bg=GRAY, fg=WHITE,
                 font=("Segoe UI", 14, "bold")).pack(side="left", pady=10)

    # ── Corpo principal ─────────────────────────────────────────────────────────
    def _build_body(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(canvas, bg=BG)
        self.sf_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(self.sf_id, width=e.width)
        canvas.bind("<Configure>", _on_resize)

        def _update_scroll(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scroll_frame.bind("<Configure>", _update_scroll)

        def _mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _mousewheel)

        self._build_config(self.scroll_frame)
        self._build_table(self.scroll_frame)
        self._build_buttons(self.scroll_frame)
        self._build_results(self.scroll_frame)

    # ── Config: algoritmo + quantum ─────────────────────────────────────────────
    def _build_config(self, parent):
        frm = tk.Frame(parent, bg=BG)
        frm.pack(fill="x", padx=28, pady=(24, 0))

        # Algoritmo
        left = tk.Frame(frm, bg=BG)
        left.pack(side="left", fill="x", expand=True, padx=(0, 16))
        tk.Label(left, text="Algoritmo de Escalonamento", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        self.alg_var = tk.StringVar(value="Round Robin")
        cb = ttk.Combobox(left, textvariable=self.alg_var,
                          values=["Round Robin", "SRTF (Shortest Remaining Time First)"], state="readonly",
                          font=("Segoe UI", 11))
        cb.pack(fill="x", pady=(4, 0), ipady=4)
        cb.bind("<<ComboboxSelected>>", self._on_alg_change)

        # Quantum
        self.quantum_frame = tk.Frame(frm, bg=BG, width=200)
        self.quantum_frame.pack(side="right", fill="y")
        self.quantum_frame.pack_propagate(False)
        tk.Label(self.quantum_frame, text="Quantum", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.quantum_var = tk.StringVar(value="2")
        self.quantum_entry = tk.Entry(self.quantum_frame, textvariable=self.quantum_var,
                                      font=("Segoe UI", 11), justify="left",
                                      relief="solid", bd=1)
        self.quantum_entry.pack(fill="x", pady=(4, 0), ipady=4)

    def _on_alg_change(self, event=None):
        """Oculta o frame do Quantum caso o algoritmo selecionado seja SRTF"""
        if self.alg_var.get() == "SRTF (Shortest Remaining Time First)":
            self.quantum_frame.pack_forget()
        else:
            self.quantum_frame.pack(side="right", fill="y")

    # ── Tabela de processos ─────────────────────────────────────────────────────
    def _build_table(self, parent):
        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(fill="x", padx=28, pady=(18, 0))

        hdr = tk.Frame(wrap, bg=GRAY)
        hdr.pack(fill="x")
        for col, w in [("Processo", 120), ("Tempo de Chegada", 260),
                       ("Tempo de Execução", 260), ("Ações", 80)]:
            tk.Label(hdr, text=col, bg=GRAY, fg=WHITE,
                     font=("Segoe UI", 10, "bold"),
                     width=w // 8, anchor="center",
                     pady=10).pack(side="left", expand=True, fill="x")

        self.rows_frame = tk.Frame(wrap, bg=WHITE, relief="solid", bd=1)
        self.rows_frame.pack(fill="x")

    def _add_row(self, arrival="", burst=""):
        # Começamos com valores padrão, mas o _update_rows vai arrumar tudo
        idx = len(self.process_rows)
        pid = f"P{idx + 1}"
        bg  = WHITE if idx % 2 == 0 else ROW_ALT

        row_frame = tk.Frame(self.rows_frame, bg=bg)
        row_frame.pack(fill="x")

        sep = tk.Frame(self.rows_frame, bg=BORDER, height=1)
        sep.pack(fill="x")

        lbl_pid = tk.Label(row_frame, text=pid, bg=bg, fg=TEXT,
                           font=("Segoe UI", 11, "bold"),
                           width=12, anchor="center")
        lbl_pid.pack(side="left", pady=8)

        arr_var = tk.StringVar(value=str(arrival))
        arr_entry = tk.Entry(row_frame, textvariable=arr_var,
                             font=("Segoe UI", 11), justify="center",
                             relief="solid", bd=1, width=18)
        arr_entry.pack(side="left", expand=True, fill="x", padx=12, pady=8)

        bst_var = tk.StringVar(value=str(burst))
        bst_entry = tk.Entry(row_frame, textvariable=bst_var,
                             font=("Segoe UI", 11), justify="center",
                             relief="solid", bd=1, width=18)
        bst_entry.pack(side="left", expand=True, fill="x", padx=12, pady=8)

        btn = tk.Button(row_frame, text="🗑", bg=bg, fg=RED,
                        font=("Segoe UI Emoji", 13), relief="flat",
                        cursor="hand2", width=3)
        btn.pack(side="left", padx=4)

        data = {"pid": pid, "arr_var": arr_var, "bst_var": bst_var,
                "row_frame": row_frame, "sep": sep, "lbl_pid": lbl_pid, "btn": btn}

        btn.config(command=lambda d=data: self._del_row(d))

        self.process_rows.append(data)
        self._update_rows()

    def _del_row(self, data):
        if len(self.process_rows) <= 1:
            messagebox.showwarning("Aviso", "É necessário pelo menos 1 processo.")
            return
        
        data["row_frame"].destroy()
        data["sep"].destroy()
        self.process_rows.remove(data)
        
        # Assim que deletar, chamamos a função para reenumerar tudo!
        self._update_rows()

    def _update_rows(self):
        """Re-organiza a numeração de todos os processos e as cores da tabela"""
        for i, row in enumerate(self.process_rows):
            new_pid = f"P{i + 1}"
            row["pid"] = new_pid
            row["lbl_pid"].config(text=new_pid)
            
            # Arrumar o fundo alternado caso algum do meio tenha sido removido
            bg_color = WHITE if i % 2 == 0 else ROW_ALT
            row["row_frame"].config(bg=bg_color)
            row["lbl_pid"].config(bg=bg_color)
            row["btn"].config(bg=bg_color)

    def _add_default_rows(self):
        self._add_row(0, 4)
        self._add_row(1, 3)
        self._add_row(2, 5)

    # ── Botões ──────────────────────────────────────────────────────────────────
    def _build_buttons(self, parent):
        frm = tk.Frame(parent, bg=BG)
        frm.pack(fill="x", padx=28, pady=(16, 0))

        btn_add = tk.Button(frm, text="＋  Adicionar Processo",
                            bg=CYAN, fg=WHITE,
                            font=("Segoe UI", 12, "bold"),
                            relief="flat", cursor="hand2", pady=12,
                            command=lambda: self._add_row())
        btn_add.pack(fill="x", pady=(0, 10))

        btn_run = tk.Button(frm, text="▶  Executar Simulação",
                            bg=GRAY, fg=WHITE,
                            font=("Segoe UI", 12, "bold"),
                            relief="flat", cursor="hand2", pady=12,
                            command=self._run)
        btn_run.pack(fill="x")

        for btn, normal, hover in [(btn_add, GRAY, "#424242"),
                                   (btn_run, CYAN, "#60d3e8")]:
            btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, n=normal: b.config(bg=n))

    # ── Área de resultados ──────────────────────────────────────────────────────
    def _build_results(self, parent):
        self.results_frame = tk.Frame(parent, bg=BG)
        self.results_frame.pack(fill="x", padx=28, pady=(24, 32))

    # ── Executar simulação ──────────────────────────────────────────────────────
    def _run(self):
        processos = []
        for i, row in enumerate(self.process_rows):
            try:
                arr = int(row["arr_var"].get())
                bst = int(row["bst_var"].get())
                if arr < 0 or bst < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro",
                    f"{row['pid']}: valores inválidos.\n"
                    "Chegada ≥ 0 e Burst ≥ 1.")
                return
            processos.append({"pid": row["pid"], "arrival": arr,
                               "burst": bst, "color_idx": i % len(GANTT_COLORS)})

        algoritmo = self.alg_var.get()
        
        if algoritmo == "Round Robin":
            try:
                quantum = int(self.quantum_var.get())
                if quantum < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Quantum deve ser um inteiro ≥ 1.")
                return
            gantt, metricas, tme, tmt = round_robin(processos, quantum)
        
        elif algoritmo == "SRTF (Shortest Remaining Time First)":
            gantt, metricas, tme, tmt = srtf(processos)

        # Limpa resultados anteriores
        for w in self.results_frame.winfo_children():
            w.destroy()

        self._draw_gantt(gantt)
        self._draw_metrics(metricas, tme, tmt)

    # ── Gráfico de Gantt ────────────────────────────────────────────────────────
    def _draw_gantt(self, gantt):
        tk.Label(self.results_frame, text="Gráfico de Gantt",
                 bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
                 anchor="w").pack(anchor="w", pady=(0, 6))
        tk.Frame(self.results_frame, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

        card = tk.Frame(self.results_frame, bg=WHITE, relief="solid", bd=1)
        card.pack(fill="x", pady=(0, 24))

        canvas = tk.Canvas(card, bg=WHITE, highlightthickness=0, height=80)
        h_scroll = ttk.Scrollbar(card, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=h_scroll.set)
        h_scroll.pack(side="bottom", fill="x")
        canvas.pack(fill="x", padx=16, pady=(12, 0))

        total = gantt[-1]["end"] if gantt else 0
        UNIT  = max(52, min(90, 700 // (total if total > 0 else 1)))
        W     = total * UNIT + 40
        canvas.configure(scrollregion=(0, 0, W, 80))

        BAR_Y1, BAR_Y2 = 8, 48
        TICK_Y         = 56

        for g in gantt:
            x1 = g["start"] * UNIT
            x2 = g["end"]   * UNIT
            bg_c, fg_c = GANTT_COLORS[g["color_idx"] % len(GANTT_COLORS)]

            canvas.create_rectangle(x1, BAR_Y1, x2, BAR_Y2, fill=bg_c, outline=CYAN_DARK, width=1)
            canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 - 6, text=g["pid"], fill=fg_c, font=("Segoe UI", 10, "bold"))
            canvas.create_text((x1 + x2) / 2, (BAR_Y1 + BAR_Y2) / 2 + 8, text=f"{g['start']}–{g['end']}", fill=fg_c, font=("Segoe UI", 8))

        if gantt:
            ticks = sorted(set(g["start"] for g in gantt) | {gantt[-1]["end"]})
            for t in ticks:
                x = t * UNIT
                canvas.create_line(x, BAR_Y2, x, TICK_Y - 2, fill=BORDER, width=1)
                canvas.create_text(x, TICK_Y, text=str(t), fill=TEXT_MUTED, font=("Segoe UI", 8))

    # ── Tabela de métricas ──────────────────────────────────────────────────────
    def _draw_metrics(self, metricas, tme, tmt):
        tk.Label(self.results_frame, text="Métricas por Processo",
                 bg=BG, fg=TEXT, font=("Segoe UI", 13, "bold"),
                 anchor="w").pack(anchor="w", pady=(0, 6))
        tk.Frame(self.results_frame, bg=GRAY, height=2).pack(fill="x", pady=(0, 10))

        card = tk.Frame(self.results_frame, bg=WHITE, relief="solid", bd=1)
        card.pack(fill="x", pady=(0, 20))

        cols = ["Processo", "Chegada", "Burst", "Conclusão", "Turnaround", "Espera"]

        hdr = tk.Frame(card, bg=GRAY)
        hdr.pack(fill="x")
        for col in cols:
            tk.Label(hdr, text=col, bg=GRAY, fg=WHITE, font=("Segoe UI", 10, "bold"),
                     anchor="center", pady=10, width=12).pack(side="left", expand=True, fill="x")

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
                    badge_frame.pack(side="left", expand=True, fill="x", pady=8, padx=4)
                    tk.Label(badge_frame, text=str(val), bg=gc_bg, fg=gc_fg, font=("Segoe UI", 10, "bold"),
                             padx=10, pady=2, relief="flat").pack()
                else:
                    tk.Label(row, text=str(val), bg=bg_c, fg=TEXT, font=("Segoe UI", 10),
                             anchor="center", width=12).pack(side="left", expand=True, fill="x", pady=8)

        summary = tk.Frame(self.results_frame, bg=BG)
        summary.pack(fill="x", pady=(4, 0))

        for label, val, desc in [
            ("Tempo Médio de Espera (TME)", f"{tme:.2f}", "Média do tempo em fila de prontos"),
            ("Tempo Médio de Turnaround (TMT)", f"{tmt:.2f}", "Média do tempo total de conclusão"),
        ]:
            c = tk.Frame(summary, bg=WHITE, relief="solid", bd=1)
            c.pack(side="left", expand=True, fill="x", padx=(0, 12) if label.startswith("TME") else 0, pady=4)
            tk.Label(c, text=label, bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold"), anchor="w").pack(anchor="w", padx=16, pady=(14, 0))
            tk.Label(c, text=val, bg=WHITE, fg=CYAN_DARK, font=("Segoe UI", 26, "bold"), anchor="w").pack(anchor="w", padx=16)
            tk.Label(c, text=desc, bg=WHITE, fg=TEXT_MUTED, font=("Segoe UI", 9), anchor="w").pack(anchor="w", padx=16, pady=(0, 14))

if __name__ == "__main__":
    app = App()
    app.mainloop()