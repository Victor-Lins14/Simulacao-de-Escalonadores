# Simulacao-de-Escalonadores


src/PY/
├── main.py                        ← 3-line entry point
├── models/
│   ├── process.py                 ← dataclasses: Process, GanttBlock, ProcessMetrics, SimulationResult
│   └── schedulers/
│       ├── base_scheduler.py      ← IScheduler (ABC / interface)
│       ├── round_robin_scheduler.py
│       ├── srtf_scheduler.py
│       └── registry.py            ← scheduler factory + discovery
├── views/
│   ├── theme.py                   ← color constants (single source of truth)
│   ├── main_window.py             ← root window; exposes clean interface to controller
│   └── components/
│       ├── header.py
│       ├── config_panel.py
│       ├── process_table.py
│       ├── action_buttons.py
│       └── results_panel.py       ← Gantt + metrics rendering
└── controllers/
    └── simulation_controller.py   ← wires view events → model
