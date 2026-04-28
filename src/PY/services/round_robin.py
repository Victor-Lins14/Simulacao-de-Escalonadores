from collections import deque


def round_robin(processos, quantum):
    lista = [
        {**p, "remaining": p["burst"], "color_idx": p.get("color_idx", 0)}
        for p in processos
    ]
    lista.sort(key=lambda x: x["arrival"])

    fila, in_fila = deque(), set()
    gantt, ct = [], {}
    t, done, i = 0, 0, 0

    while done < len(lista):
        while i < len(lista) and lista[i]["arrival"] <= t:
            if lista[i]["pid"] not in in_fila:
                fila.append(lista[i])
                in_fila.add(lista[i]["pid"])
            i += 1

        if not fila:
            t = lista[i]["arrival"]
            continue

        p  = fila.popleft()
        ex = min(quantum, p["remaining"])
        gantt.append({"pid": p["pid"], "start": t, "end": t + ex,
                      "color_idx": p["color_idx"]})
        t += ex
        p["remaining"] -= ex

        while i < len(lista) and lista[i]["arrival"] <= t:
            if lista[i]["pid"] not in in_fila:
                fila.append(lista[i])
                in_fila.add(lista[i]["pid"])
            i += 1

        if p["remaining"] > 0:
            fila.append(p)
        else:
            ct[p["pid"]] = t
            done += 1

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
