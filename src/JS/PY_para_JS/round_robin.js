function roundRobin(procs, quantum) {
  const list = procs.map(p => ({...p, remaining: p.burst})).sort((a,b) => a.arrival - b.arrival);
  const queue = [], inQ = new Set();
  const gantt = [], ct = {};
  let t = 0, done = 0, i = 0;

  while (done < list.length) {
    while (i < list.length && list[i].arrival <= t) {
      if (!inQ.has(list[i].pid)) { queue.push(list[i]); inQ.add(list[i].pid); }
      i++;
    }
    if (!queue.length) { t = list[i].arrival; continue; }
    
    const p = queue.shift();
    const ex = Math.min(quantum, p.remaining);
    
    gantt.push({pid: p.pid, start: t, end: t + ex, colorIdx: p.colorIdx});
    t += ex; 
    p.remaining -= ex;
    
    while (i < list.length && list[i].arrival <= t) {
      if (!inQ.has(list[i].pid)) { queue.push(list[i]); inQ.add(list[i].pid); }
      i++;
    }
    
    if (p.remaining > 0) queue.push(p);
    else { ct[p.pid] = t; done++; }
  }

  const metrics = procs.map(p => {
    const tat = ct[p.pid] - p.arrival;
    const wt = tat - p.burst;
    return {
      pid: p.pid, arrival: p.arrival, burst: p.burst,
      ct: ct[p.pid], tat: tat, wt: wt,
      colorIdx: p.colorIdx
    };
  });

  const tme = metrics.reduce((s,m) => s + m.wt, 0) / metrics.length || 0;
  const tmt = metrics.reduce((s,m) => s + m.tat, 0) / metrics.length || 0;

  return { gantt, metrics, tme, tmt, total: t };
}