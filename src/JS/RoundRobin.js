
const COLORS = ['gc-0','gc-1','gc-2','gc-3','gc-4','gc-5','gc-6','gc-7'];
const BADGE_BG  = ['#b2ebf2','#c8e6c9','#ffe0b2','#e1bee7','#fce4ec','#fff9c4','#b3e5fc','#dcedc8'];
const BADGE_FG  = ['#006064','#1b5e20','#bf360c','#4a148c','#880e4f','#f57f17','#01579b','#33691e'];

let counter = 0;

function addRow(arr='', bst='') {
  counter++;
  const pid = 'P' + counter;
  const tbody = document.getElementById('proc-body');
  const tr = document.createElement('tr');
  tr.dataset.pid = pid;
  tr.innerHTML = `
    <td>${pid}</td>
    <td><input type="number" class="arr-in" value="${arr}" min="0" placeholder="0"></td>
    <td><input type="number" class="bst-in" value="${bst}" min="1" placeholder="1"></td>
    <td>
      <button class="btn-del" onclick="delRow(this)" title="Remover">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/>
        </svg>
      </button>
    </td>`;
  tbody.appendChild(tr);
}

function delRow(btn) {
  btn.closest('tr').remove();
}

function getRows() {
  const rows = document.querySelectorAll('#proc-body tr');
  return Array.from(rows).map((tr, i) => ({
    pid: tr.dataset.pid,
    arrival: parseInt(tr.querySelector('.arr-in').value) || 0,
    burst: parseInt(tr.querySelector('.bst-in').value) || 1,
    colorIdx: i % COLORS.length
  }));
}

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
    t += ex; p.remaining -= ex;
    while (i < list.length && list[i].arrival <= t) {
      if (!inQ.has(list[i].pid)) { queue.push(list[i]); inQ.add(list[i].pid); }
      i++;
    }
    if (p.remaining > 0) queue.push(p);
    else { ct[p.pid] = t; done++; }
  }
  return { gantt, ct, total: t };
}

function runSim() {
  const procs = getRows();
  if (!procs.length) { alert('Adicione pelo menos um processo.'); return; }
  const quantum = parseInt(document.getElementById('quantum').value) || 2;
  const { gantt, ct, total } = roundRobin(procs, quantum);

  // GANTT
  const barsEl = document.getElementById('gantt-bars');
  const tlEl   = document.getElementById('gantt-timeline');
  barsEl.innerHTML = '';
  tlEl.innerHTML   = '';

  const totalW = Math.max(600, total * 52);
  const unitW  = totalW / total;

  gantt.forEach(g => {
    const w = Math.round((g.end - g.start) * unitW);
    const div = document.createElement('div');
    div.className = 'gantt-block ' + COLORS[g.colorIdx];
    div.style.width = w + 'px';
    div.style.minWidth = w + 'px';
    div.innerHTML = `<span class="g-pid">${g.pid}</span><span class="g-range">${g.start}–${g.end}</span>`;
    barsEl.appendChild(div);
  });

  // timeline ticks
  const ticks = new Set(gantt.flatMap(g => [g.start, g.end]));
  [...ticks].sort((a,b)=>a-b).forEach((tick, idx, arr) => {
    const span = document.createElement('div');
    span.className = 'gantt-tick';
    if (idx < arr.length - 1) {
      const nextTick = arr[idx + 1];
      const w = Math.round((nextTick - tick) * unitW);
      span.style.width = w + 'px';
      span.style.minWidth = w + 'px';
    }
    span.textContent = tick;
    tlEl.appendChild(span);
  });

  // METRICS TABLE
  const metrics = procs.map(p => ({
    pid: p.pid, arrival: p.arrival, burst: p.burst,
    ct: ct[p.pid],
    tat: ct[p.pid] - p.arrival,
    wt: ct[p.pid] - p.arrival - p.burst,
    colorIdx: p.colorIdx
  }));
  const mb = document.getElementById('metrics-body');
  mb.innerHTML = '';
  metrics.forEach(m => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="pid-badge" style="background:${BADGE_BG[m.colorIdx]};color:${BADGE_FG[m.colorIdx]}">${m.pid}</span></td>
      <td>${m.arrival}</td>
      <td>${m.burst}</td>
      <td>${m.ct}</td>
      <td>${m.tat}</td>
      <td>${m.wt}</td>`;
    mb.appendChild(tr);
  });

  const tme = metrics.reduce((s,m)=>s+m.wt, 0) / metrics.length;
  const tmt = metrics.reduce((s,m)=>s+m.tat, 0) / metrics.length;
  document.getElementById('tme-val').textContent = tme.toFixed(2);
  document.getElementById('tmt-val').textContent = tmt.toFixed(2);

  const res = document.getElementById('results');
  res.style.display = 'block';
  res.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Init with 3 example rows
addRow(0, 4);
addRow(1, 3);
addRow(2, 5);