function srtf(procs) {
  const list = procs.map(p => ({...p, remaining: p.burst})).sort((a, b) => a.arrival - b.arrival);
  let t = 0, done = 0;
  const n = list.length;
  const gantt = [];
  const ct = {};

  let current_pid = null;
  let block_start = 0;
  let current_color = 0;

  while (done < n) {
      const available = list.filter(p => p.arrival <= t && p.remaining > 0);

      if (available.length === 0) {
          if (current_pid !== null) {
              gantt.push({pid: current_pid, start: block_start, end: t, colorIdx: current_color});
              current_pid = null;
          }
          const future = list.filter(p => p.remaining > 0);
          t = Math.min(...future.map(p => p.arrival));
          continue;
      }

      available.sort((a, b) => {
          if (a.remaining === b.remaining) return a.arrival - b.arrival;
          return a.remaining - b.remaining;
      });
      const shortest = available[0];

      if (shortest.pid !== current_pid) {
          if (current_pid !== null) {
              gantt.push({pid: current_pid, start: block_start, end: t, colorIdx: current_color});
          }
          current_pid = shortest.pid;
          block_start = t;
          current_color = shortest.colorIdx;
      }

      shortest.remaining -= 1;
      t += 1;

      if (shortest.remaining === 0) {
          gantt.push({pid: current_pid, start: block_start, end: t, colorIdx: current_color});
          ct[shortest.pid] = t;
          current_pid = null;
          done += 1;
      }
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

  const tme = metrics.reduce((s, m) => s + m.wt, 0) / metrics.length || 0;
  const tmt = metrics.reduce((s, m) => s + m.tat, 0) / metrics.length || 0;

  return { gantt, metrics, tme, tmt, total: t };
}