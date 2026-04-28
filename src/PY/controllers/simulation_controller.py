from services.round_robin import round_robin
from services.srtf import srtf

ALGORITHMS = {
    "Round Robin": "rr",
    "SRTF (Shortest Remaining Time First)": "srtf",
}


def parse_processes(rows):
    processes = []
    for i, row in enumerate(rows):
        try:
            arr = int(row["arr_var"].get())
            bst = int(row["bst_var"].get())
            if arr < 0 or bst < 1:
                raise ValueError
        except ValueError:
            raise ValueError(
                f"{row['pid']}: valores inválidos.\nChegada ≥ 0 e Burst ≥ 1."
            )
        processes.append({
            "pid": row["pid"],
            "arrival": arr,
            "burst": bst,
            "color_idx": i,
        })
    return processes


def run_simulation(processes, algorithm, quantum=None):
    if algorithm == "Round Robin":
        if quantum is None or quantum < 1:
            raise ValueError("Quantum deve ser um inteiro ≥ 1.")
        return round_robin(processes, quantum)
    if algorithm == "SRTF (Shortest Remaining Time First)":
        return srtf(processes)
    raise ValueError(f"Algoritmo desconhecido: {algorithm}")
