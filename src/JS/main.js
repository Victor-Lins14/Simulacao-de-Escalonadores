const COLORS = ['gc-0','gc-1','gc-2','gc-3','gc-4','gc-5','gc-6','gc-7'];
const BADGE_BG  = ['#b2ebf2','#c8e6c9','#ffe0b2','#e1bee7','#fce4ec','#fff9c4','#b3e5fc','#dcedc8'];
const BADGE_FG  = ['#006064','#1b5e20','#bf360c','#4a148c','#880e4f','#f57f17','#01579b','#33691e'];

// Ouvinte para ocultar/mostrar o Quantum de acordo com o Select
document.getElementById('algorithm').addEventListener('change', function() {
    const qWrapper = document.getElementById('quantum-wrapper');
    if (this.value === 'srtf') {
        qWrapper.style.display = 'none';
    } else {
        qWrapper.style.display = 'block';
    }
});

function addRow(arr='', bst='') {
  const tbody = document.getElementById('proc-body');
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td class="td-pid"></td>
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
  updateRows();
}

function delRow(btn) {
  const tbody = document.getElementById('proc-body');
  if (tbody.children.length <= 1) {
      alert("É necessário pelo menos 1 processo.");
      return;
  }
  btn.closest('tr').remove();
  updateRows(); 
}

function updateRows() {
    const rows = document.querySelectorAll('#proc-body tr');
    rows.forEach((tr, i) => {
        const newPid = 'P' + (i + 1);
        tr.dataset.pid = newPid;
        tr.querySelector('.td-pid').textContent = newPid;
    });
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

function runSim() {
  const procs = getRows();
  if (!procs.length) { alert('Adicione pelo menos um processo.'); return; }
  
  const algorithm = document.getElementById('algorithm').value;
  let result;

  if (algorithm === 'rr') {
      const quantum = parseInt(document.getElementById('quantum').value) || 2;
      result = roundRobin(procs, quantum);
  } else if (algorithm === 'srtf') {
      result = srtf(procs);
  }

  const { gantt, metrics, tme, tmt, total } = result;

  // GANTT
  const barsEl = document.getElementById('gantt-bars');
  const tlEl   = document.getElementById('gantt-timeline');
  barsEl.innerHTML = '';
  tlEl.innerHTML   = '';

  // Força uma unidade de tempo a ter no mínimo 40px para evitar esmagamento visual
  const UNIT = Math.max(40, 700 / (total > 0 ? total : 1));

  gantt.forEach(g => {
    const duration = g.end - g.start;
    const w = duration * UNIT;
    const div = document.createElement('div');
    div.className = 'gantt-block ' + COLORS[g.colorIdx];
    
    // Trava o tamanho nos 3 eixos para o CSS não desobedecer
    div.style.width = w + 'px';
    div.style.minWidth = w + 'px';
    div.style.maxWidth = w + 'px';
    
    div.innerHTML = `<span class="g-pid">${g.pid}</span><span class="g-range">${g.start}–${g.end}</span>`;
    barsEl.appendChild(div);
  });

  // Timeline ticks
  const ticks = new Set(gantt.flatMap(g => [g.start, g.end]));
  [...ticks].sort((a,b)=>a-b).forEach((tick, idx, arr) => {
    const span = document.createElement('div');
    span.className = 'gantt-tick';
    
    if (idx < arr.length - 1) {
      const nextTick = arr[idx + 1];
      const w = (nextTick - tick) * UNIT;
      span.style.width = w + 'px';
      span.style.minWidth = w + 'px';
      span.style.maxWidth = w + 'px';
    }
    span.textContent = tick;
    tlEl.appendChild(span);
  });

  // METRICS TABLE
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

  document.getElementById('tme-val').textContent = tme.toFixed(2);
  document.getElementById('tmt-val').textContent = tmt.toFixed(2);

  const res = document.getElementById('results');
  res.style.display = 'block';
  res.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Inicia com 3 processos padrão
addRow(0, 4);
addRow(1, 3);
addRow(2, 5);