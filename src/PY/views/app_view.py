import tkinter as tk
from tkinter import ttk, messagebox

from views.theme import (
    CYAN, CYAN_DARK, WHITE, BG, ROW_ALT, TEXT, TEXT_MUTED, BORDER, RED, GRAY,
    GANTT_COLORS,
)
from views.gantt_view import draw_gantt
from views.metrics_view import draw_metrics
from controllers.simulation_controller import parse_processes, run_simulation


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

        tk.Label(hdr, text="⚙", bg=GRAY, fg=WHITE,
                 font=("Segoe UI Emoji", 20)).pack(side="left", padx=(18, 8), pady=10)
        tk.Label(hdr, text="Simulador de Escalonamento de CPU",
                 bg=GRAY, fg=WHITE,
                 font=("Segoe UI", 14, "bold")).pack(side="left", pady=10)

    # ── Body ───────────────────────────────────────────────────────────────────

    def _build_body(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(canvas, bg=BG)
        sf_id = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(sf_id, width=e.width))
        self.scroll_frame.bind("<Configure>",
                               lambda e: canvas.configure(
                                   scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(
                            int(-1 * (e.delta / 120)), "units"))

        self._build_config(self.scroll_frame)
        self._build_table(self.scroll_frame)
        self._build_buttons(self.scroll_frame)
        self._build_results(self.scroll_frame)

    # ── Config ─────────────────────────────────────────────────────────────────

    def _build_config(self, parent):
        frm = tk.Frame(parent, bg=BG)
        frm.pack(fill="x", padx=28, pady=(24, 0))

        left = tk.Frame(frm, bg=BG)
        left.pack(side="left", fill="x", expand=True, padx=(0, 16))
        tk.Label(left, text="Algoritmo de Escalonamento", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")

        self.alg_var = tk.StringVar(value="Round Robin")
        cb = ttk.Combobox(left, textvariable=self.alg_var,
                          values=["Round Robin",
                                  "SRTF (Shortest Remaining Time First)"],
                          state="readonly", font=("Segoe UI", 11))
        cb.pack(fill="x", pady=(4, 0), ipady=4)
        cb.bind("<<ComboboxSelected>>", self._on_alg_change)

        self.quantum_frame = tk.Frame(frm, bg=BG, width=200)
        self.quantum_frame.pack(side="right", fill="y")
        self.quantum_frame.pack_propagate(False)
        tk.Label(self.quantum_frame, text="Quantum", bg=BG, fg=TEXT_MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.quantum_var = tk.StringVar(value="2")
        tk.Entry(self.quantum_frame, textvariable=self.quantum_var,
                 font=("Segoe UI", 11), justify="left",
                 relief="solid", bd=1).pack(fill="x", pady=(4, 0), ipady=4)

    def _on_alg_change(self, _event=None):
        if self.alg_var.get() == "SRTF (Shortest Remaining Time First)":
            self.quantum_frame.pack_forget()
        else:
            self.quantum_frame.pack(side="right", fill="y")

    # ── Process table ──────────────────────────────────────────────────────────

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
        idx    = len(self.process_rows)
        pid    = f"P{idx + 1}"
        bg_col = WHITE if idx % 2 == 0 else ROW_ALT

        row_frame = tk.Frame(self.rows_frame, bg=bg_col)
        row_frame.pack(fill="x")
        sep = tk.Frame(self.rows_frame, bg=BORDER, height=1)
        sep.pack(fill="x")

        lbl_pid = tk.Label(row_frame, text=pid, bg=bg_col, fg=TEXT,
                           font=("Segoe UI", 11, "bold"),
                           width=12, anchor="center")
        lbl_pid.pack(side="left", pady=8)

        arr_var = tk.StringVar(value=str(arrival))
        tk.Entry(row_frame, textvariable=arr_var, font=("Segoe UI", 11),
                 justify="center", relief="solid", bd=1,
                 width=18).pack(side="left", expand=True, fill="x",
                                padx=12, pady=8)

        bst_var = tk.StringVar(value=str(burst))
        tk.Entry(row_frame, textvariable=bst_var, font=("Segoe UI", 11),
                 justify="center", relief="solid", bd=1,
                 width=18).pack(side="left", expand=True, fill="x",
                                padx=12, pady=8)

        btn = tk.Button(row_frame, text="🗑", bg=bg_col, fg=RED,
                        font=("Segoe UI Emoji", 13), relief="flat",
                        cursor="hand2", width=3)
        btn.pack(side="left", padx=4)

        data = {
            "pid": pid, "arr_var": arr_var, "bst_var": bst_var,
            "row_frame": row_frame, "sep": sep,
            "lbl_pid": lbl_pid, "btn": btn,
        }
        btn.config(command=lambda d=data: self._del_row(d))

        self.process_rows.append(data)
        self._refresh_rows()

    def _del_row(self, data):
        if len(self.process_rows) <= 1:
            messagebox.showwarning("Aviso", "É necessário pelo menos 1 processo.")
            return
        data["row_frame"].destroy()
        data["sep"].destroy()
        self.process_rows.remove(data)
        self._refresh_rows()

    def _refresh_rows(self):
        for i, row in enumerate(self.process_rows):
            new_pid  = f"P{i + 1}"
            bg_color = WHITE if i % 2 == 0 else ROW_ALT
            row["pid"] = new_pid
            row["lbl_pid"].config(text=new_pid, bg=bg_color)
            row["row_frame"].config(bg=bg_color)
            row["btn"].config(bg=bg_color)

    def _add_default_rows(self):
        self._add_row(0, 4)
        self._add_row(1, 3)
        self._add_row(2, 5)

    # ── Buttons ────────────────────────────────────────────────────────────────

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

        for btn, normal, hover in [(btn_add, CYAN, "#60d3e8"),
                                   (btn_run, GRAY, "#424242")]:
            btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, n=normal: b.config(bg=n))

    # ── Results area ───────────────────────────────────────────────────────────

    def _build_results(self, parent):
        self.results_frame = tk.Frame(parent, bg=BG)
        self.results_frame.pack(fill="x", padx=28, pady=(24, 32))

    # ── Run ────────────────────────────────────────────────────────────────────

    def _run(self):
        try:
            processes = parse_processes(self.process_rows)
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return

        algorithm = self.alg_var.get()
        quantum   = None

        if algorithm == "Round Robin":
            try:
                quantum = int(self.quantum_var.get())
                if quantum < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Quantum deve ser um inteiro ≥ 1.")
                return

        try:
            gantt, metricas, tme, tmt = run_simulation(processes, algorithm, quantum)
        except ValueError as exc:
            messagebox.showerror("Erro", str(exc))
            return

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        draw_gantt(self.results_frame, gantt)
        draw_metrics(self.results_frame, metricas, tme, tmt)
