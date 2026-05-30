const API = (location.hostname === 'localhost' || location.hostname === '127.0.0.1')
  ? 'http://localhost:8000' : location.origin;

const fi = document.getElementById('fi');
const btn = document.getElementById('btn');
const zone = document.getElementById('zone');
const fname = document.getElementById('fname');
const err = document.getElementById('err');
const prog = document.getElementById('prog');
const pfill = document.getElementById('pfill');
const plabel = document.getElementById('plabel');
const results = document.getElementById('results');

fi.addEventListener('change', () => { if (fi.files[0]) pick(fi.files[0]); });
zone.addEventListener('dragover', e => { e.preventDefault(); zone.style.background = '#f0f0f0'; });
zone.addEventListener('dragleave', () => { zone.style.background = ''; });
zone.addEventListener('drop', e => {
  e.preventDefault(); zone.style.background = '';
  if (e.dataTransfer.files[0]) { fi.files = e.dataTransfer.files; pick(e.dataTransfer.files[0]); }
});

function pick(f) { fname.textContent = f.name; btn.disabled = false; err.textContent = ''; }
function step(label, pct) { plabel.textContent = label; pfill.style.width = pct + '%'; }
function esc(s) { return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

async function go() {
  if (!fi.files[0]) return;
  err.textContent = '';
  results.classList.remove('on');
  prog.classList.add('on');
  btn.disabled = true;
  step('Загружаю...', 15);

  const fd = new FormData();
  fd.append('file', fi.files[0]);

  try {
    step('Транскрибирую...', 35);
    const r = await fetch(API + '/process', { method: 'POST', body: fd });
    step('Анализирую...', 75);
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Ошибка сервера');
    step('Готово', 100);

    document.getElementById('transcription').textContent = d.transcription || '—';
    document.getElementById('summary').textContent = d.summary || '—';

    const pEl = document.getElementById('participants');
    pEl.innerHTML = d.participants?.length
      ? d.participants.map(p => `<div class="row"><span class="meta">${esc(p.role)}</span><span>${esc(p.name)}</span></div>`).join('')
      : '<div class="empty">Не определены</div>';

    const tEl = document.getElementById('tasks');
    tEl.innerHTML = d.tasks?.length
      ? d.tasks.map(t => `<div class="row"><span>${esc(t.task)}</span><span class="arr">→</span><span class="meta">${esc(t.assignee || '—')}</span></div>`).join('')
      : '<div class="empty">Не найдены</div>';

    setTimeout(() => { prog.classList.remove('on'); results.classList.add('on'); }, 400);
  } catch(e) {
    prog.classList.remove('on');
    err.textContent = e.message || 'Сервер недоступен';
    btn.disabled = false;
  }
}