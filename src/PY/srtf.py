def srtf(processos):
    lista = [
        {**p, "remaining": p["burst"], "color_idx": p.get("color_idx", 0)}
        for p in processos
    ]
    
    t = 0
    done = 0
    n = len(lista)
    gantt = []
    ct = {}
    
    current_pid = None
    block_start = 0
    current_color = 0
    
    while done < n:
        # Encontra todos os processos que já chegaram e ainda precisam executar
        available = [p for p in lista if p["arrival"] <= t and p["remaining"] > 0]
        
        if not available:
            if current_pid is not None:
                gantt.append({"pid": current_pid, "start": block_start, "end": t, "color_idx": current_color})
                current_pid = None
            
            # Pula o tempo para a próxima chegada
            t = min([p["arrival"] for p in lista if p["remaining"] > 0])
            continue
        
        # Pega o processo com menor tempo restante
        available.sort(key=lambda x: (x["remaining"], x["arrival"]))
        shortest = available[0]
        
        # Se houve troca de contexto, registra o bloco anterior no Gantt
        if shortest["pid"] != current_pid:
            if current_pid is not None:
                gantt.append({"pid": current_pid, "start": block_start, "end": t, "color_idx": current_color})
            current_pid = shortest["pid"]
            block_start = t
            current_color = shortest["color_idx"]
            
        # Executa por 1 unidade de tempo (preempção)
        shortest["remaining"] -= 1
        t += 1
        
        # Se finalizou
        if shortest["remaining"] == 0:
            gantt.append({"pid": current_pid, "start": block_start, "end": t, "color_idx": current_color})
            ct[shortest["pid"]] = t
            current_pid = None
            done += 1

    # Calcula as métricas exigidas
    metricas = []
    for p in processos:
        tat = ct[p["pid"]] - p["arrival"]
        wt  = tat - p["burst"]
        metricas.append({
            "pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"],
            "ct": ct[p["pid"]], "tat": tat, "wt": wt,
            "color_idx": p.get("color_idx", 0),
        })

    tme = sum(m["wt"]  for m in metricas) / len(metricas) if metricas else 0
    tmt = sum(m["tat"] for m in metricas) / len(metricas) if metricas else 0
    
    return gantt, metricas, tme, tmt