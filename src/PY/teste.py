from collections import deque

def round_robin(processos, quantum):
    """
    Simulação do algoritmo de escalonamento Round Robin.

    Args:
        processos: lista de dicts com 'pid', 'arrival', 'burst'
        quantum:   fatia de tempo (time slice)

    Returns:
        dict com 'gantt', 'metricas', 'tme', 'tmt'
    """
    # Cria cópias para não alterar os dados originais
    procs = [
        {**p, 'remaining': p['burst'], 'completion': 0}
        for p in processos
    ]
    procs.sort(key=lambda p: p['arrival'])

    fila   = deque()
    gantt  = []          # lista de (pid, t_inicio, t_fim)
    in_fila = set()
    tempo  = 0
    feitos = 0
    i      = 0           # índice no vetor ordenado por arrival

    while feitos < len(procs):
        # Adiciona à fila processos que já chegaram
        while i < len(procs) and procs[i]['arrival'] <= tempo:
            if procs[i]['pid'] not in in_fila:
                fila.append(procs[i])
                in_fila.add(procs[i]['pid'])
            i += 1

        if not fila:
            # CPU ociosa: avança até o próximo processo
            tempo = procs[i]['arrival']
            continue

        proc = fila.popleft()
        exec_time = min(quantum, proc['remaining'])

        gantt.append((proc['pid'], tempo, tempo + exec_time))
        tempo += exec_time
        proc['remaining'] -= exec_time

        # Verifica novos processos que chegaram durante a execução
        while i < len(procs) and procs[i]['arrival'] <= tempo:
            if procs[i]['pid'] not in in_fila:
                fila.append(procs[i])
                in_fila.add(procs[i]['pid'])
            i += 1

        if proc['remaining'] > 0:
            fila.append(proc)          # volta para o fim da fila
        else:
            proc['completion'] = tempo  # registra conclusão
            feitos += 1

    # Calcula métricas
    metricas = []
    for p in procs:
        tat = p['completion'] - p['arrival']   # Turnaround
        wt  = tat - p['burst']                  # Waiting Time
        metricas.append({
            'pid':        p['pid'],
            'arrival':    p['arrival'],
            'burst':      p['burst'],
            'completion': p['completion'],
            'turnaround': tat,
            'waiting':    wt,
        })

    tme = sum(m['waiting']    for m in metricas) / len(metricas)
    tmt = sum(m['turnaround'] for m in metricas) / len(metricas)

    return {'gantt': gantt, 'metricas': metricas, 'tme': tme, 'tmt': tmt}


def imprimir_gantt(gantt):
    print("\nDiagrama de Gantt:")
    linha_pid  = ""
    linha_temp = "0"
    for pid, inicio, fim in gantt:
        duracao = fim - inicio
        linha_pid  += f"| {pid:^{duracao*2-1}} "
        linha_temp += f"{'':>{duracao*2}}{fim}"
    print(linha_pid + "|")
    print(linha_temp)


def imprimir_metricas(metricas, tme, tmt):
    header = f"{'PID':<6} {'Chegada':>8} {'Burst':>6} "             f"{'Conclusão':>10} {'Turnaround':>11} {'Espera':>7}"
    print("\nMétricas por processo:")
    print(header)
    print("-" * len(header))
    for m in metricas:
        print(f"{m['pid']:<6} {m['arrival']:>8} {m['burst']:>6} "
              f"{m['completion']:>10} {m['turnaround']:>11} {m['waiting']:>7}")
    print(f"\nTempo Médio de Espera (TME):      {tme:.2f}")
    print(f"Tempo Médio de Turnaround (TMT):   {tmt:.2f}")


# ── Exemplo de uso ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    processos = [
        {'pid': 'P1', 'arrival': 0, 'burst': 5},
        {'pid': 'P2', 'arrival': 1, 'burst': 3},
        {'pid': 'P3', 'arrival': 2, 'burst': 1},
        {'pid': 'P4', 'arrival': 3, 'burst': 2},
    ]
    quantum = 2

    resultado = round_robin(processos, quantum)
    imprimir_gantt(resultado['gantt'])
    imprimir_metricas(resultado['metricas'], resultado['tme'], resultado['tmt'])
