/* =========================================================================
   You shouldn't need to edit this file — edit data.js instead.
   ========================================================================= */

document.addEventListener('DOMContentLoaded', () => {
  renderProfile();
  renderTerminal();
  renderFilters();
  renderCards(PROJECTS);
  wireNav();
  wireModal();
  document.getElementById('footerYear').textContent = new Date().getFullYear();
});

/* ---------------- profile / about / contact ---------------- */
function renderProfile() {
  const p = PROFILE;
  setText('navName', slug(p.name));
  setText('heroName', p.name);
  setText('heroRole', p.role);
  setText('aboutBody', p.about);
  setText('aboutLocation', p.location);
  setText('aboutFocus', p.focus);
  setText('aboutExperience', p.experience);
  setText('footerName', p.name);

  const skillsEl = document.getElementById('skillsList');
  skillsEl.innerHTML = p.skills.map(s => `<span class="skill-pill">${escapeHTML(s)}</span>`).join('');

  const linksEl = document.getElementById('contactLinks');
  linksEl.innerHTML = p.links.map(l => `<a href="${escapeAttr(l.url)}" target="_blank" rel="noopener">${escapeHTML(l.label)}</a>`).join('');
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

/* ---------------- hero terminal typing effect ---------------- */
function renderTerminal() {
  const body = document.getElementById('terminalBody');
  const lines = [
    { prompt: '$ whoami', out: PROFILE.name.toLowerCase().replace(/\s+/g, '-') },
    { prompt: '$ cat role.txt', out: PROFILE.role },
    { prompt: '$ ls projects/', out: PROJECTS.map(p => p.id).join('  ') },
    { prompt: '$ echo $STATUS', out: 'available_for_work=true' }
  ];

  body.innerHTML = '';
  let li = 0;

  function typeLine() {
    if (li >= lines.length) {
      const cursorLine = document.createElement('div');
      cursorLine.className = 'term-line';
      cursorLine.innerHTML = `<span class="term-prompt">$</span> <span class="term-cursor"></span>`;
      body.appendChild(cursorLine);
      return;
    }
    const { prompt, out } = lines[li];
    const promptEl = document.createElement('div');
    promptEl.className = 'term-line';
    body.appendChild(promptEl);

    let i = 0;
    const speed = 22;
    const timer = setInterval(() => {
      promptEl.innerHTML = `<span class="term-prompt">${escapeHTML(prompt.slice(0, i + 1))}</span>`;
      i++;
      if (i >= prompt.length) {
        clearInterval(timer);
        const outEl = document.createElement('div');
        outEl.className = 'term-line term-out';
        outEl.textContent = out;
        body.appendChild(outEl);
        li++;
        setTimeout(typeLine, 260);
      }
    }, speed);
  }

  typeLine();
}

/* ---------------- project cards + filters ---------------- */
function allTechs() {
  const set = new Set();
  PROJECTS.forEach(p => p.tech.forEach(t => set.add(t)));
  return Array.from(set).sort();
}

function renderFilters() {
  const row = document.getElementById('filterRow');
  const techs = allTechs();
  row.innerHTML = `<button class="chip active" data-tech="all">all</button>` +
    techs.map(t => `<button class="chip" data-tech="${escapeAttr(t)}">${escapeHTML(t)}</button>`).join('');

  row.addEventListener('click', (e) => {
    const btn = e.target.closest('.chip');
    if (!btn) return;
    row.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const tech = btn.dataset.tech;
    const filtered = tech === 'all' ? PROJECTS : PROJECTS.filter(p => p.tech.includes(tech));
    renderCards(filtered);
  });
}

function renderCards(list) {
  const grid = document.getElementById('cardsGrid');
  if (!list.length) {
    grid.innerHTML = `<p class="empty-note">No projects match that filter yet.</p>`;
    return;
  }
  grid.innerHTML = list.map((p, idx) => `
    <article class="card" data-id="${escapeAttr(p.id)}" tabindex="0" role="button" aria-label="Open ${escapeAttr(p.title)} case study">
      <span class="card-index">${String(idx + 1).padStart(2, '0')} /</span>
      <h3 class="card-title">${escapeHTML(p.title)}</h3>
      <p class="card-desc">${escapeHTML(p.description)}</p>
      <div class="card-tech">
        ${p.tech.slice(0, 4).map(t => `<span class="tag">${escapeHTML(t)}</span>`).join('')}
      </div>
      <span class="card-open">open case study →</span>
    </article>
  `).join('');

  grid.querySelectorAll('.card').forEach(card => {
    const open = () => openModal(card.dataset.id);
    card.addEventListener('click', open);
    card.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
  });
}

/* ---------------- modal / case study ---------------- */
function wireModal() {
  const overlay = document.getElementById('modalOverlay');
  document.getElementById('modalClose').addEventListener('click', closeModal);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  document.getElementById('modalTabs').addEventListener('click', (e) => {
    const btn = e.target.closest('.tab-btn');
    if (!btn) return;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
}

function openModal(id) {
  const p = PROJECTS.find(x => x.id === id);
  if (!p) return;

  setText('modalEyebrow', '// case study');
  setText('modalTitle', p.title);
  setText('modalTagline', p.description);

  const linksEl = document.getElementById('modalLinks');
  linksEl.innerHTML = (p.links || []).map(l => `<a href="${escapeAttr(l.url)}" target="_blank" rel="noopener">${escapeHTML(l.label)} ↗</a>`).join('');

  document.getElementById('tab-readme').innerHTML = p.readme
    ? `<div class="readme">${renderMarkdown(p.readme)}</div>`
    : `<p class="empty-note">No README added for this project yet — add one in data.js.</p>`;

  const media = [];
  (p.videos || []).forEach(src => {
    if (isYouTube(src)) {
      media.push(`<iframe width="100%" height="220" src="${escapeAttr(toYouTubeEmbed(src))}" style="border:0;border-radius:4px;" allowfullscreen></iframe>`);
    } else {
      media.push(`<video src="${escapeAttr(src)}" controls></video>`);
    }
  });
  (p.images || []).forEach(src => {
    media.push(`<img src="${escapeAttr(src)}" alt="${escapeAttr(p.title)} screenshot" loading="lazy">`);
  });
  document.getElementById('tab-media').innerHTML = media.length
    ? `<div class="media-grid">${media.join('')}</div>`
    : `<p class="empty-note">No screenshots or videos added yet — drop files in assets/images or assets/videos and reference them in data.js.</p>`;

  document.getElementById('tab-stack').innerHTML = `<div class="stack-grid">${p.tech.map(t => `<span class="tag">${escapeHTML(t)}</span>`).join('')}</div>`;

  document.querySelectorAll('.tab-btn').forEach((b, i) => b.classList.toggle('active', i === 0));
  document.querySelectorAll('.tab-panel').forEach((el, i) => el.classList.toggle('active', i === 0));

  document.getElementById('modalOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modalOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

/* ---------------- nav ---------------- */
function wireNav() {
  const toggle = document.getElementById('navToggle');
  const links = document.querySelector('.nav-links');
  toggle.addEventListener('click', () => links.classList.toggle('open'));
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => links.classList.remove('open')));
}

/* ---------------- tiny markdown renderer (headings, bold, italic, code, lists, links) ---------------- */
function renderMarkdown(src) {
  let text = src.trim();

  // fenced code blocks first (protect from other rules)
  const blocks = [];
  text = text.replace(/```([\s\S]*?)```/g, (_, code) => {
    blocks.push(`<pre><code>${escapeHTML(code.trim())}</code></pre>`);
    return `\u0000BLOCK${blocks.length - 1}\u0000`;
  });

  const lines = text.split('\n');
  let html = '';
  let inList = false;

  for (let raw of lines) {
    const line = raw.trim();

    if (line.startsWith('\u0000BLOCK')) {
      if (inList) { html += '</ul>'; inList = false; }
      html += line.replace(/\u0000BLOCK(\d+)\u0000/, (_, i) => blocks[Number(i)]);
      continue;
    }

    if (!line) { if (inList) { html += '</ul>'; inList = false; } continue; }

    const h3 = line.match(/^###\s+(.*)/);
    const h2 = line.match(/^##\s+(.*)/);
    const h1 = line.match(/^#\s+(.*)/);
    const li = line.match(/^[-*]\s+(.*)/);

    if (h3) { if (inList) { html += '</ul>'; inList = false; } html += `<h3>${inline(h3[1])}</h3>`; continue; }
    if (h2) { if (inList) { html += '</ul>'; inList = false; } html += `<h2>${inline(h2[1])}</h2>`; continue; }
    if (h1) { if (inList) { html += '</ul>'; inList = false; } html += `<h1>${inline(h1[1])}</h1>`; continue; }
    if (li) {
      if (!inList) { html += '<ul>'; inList = true; }
      html += `<li>${inline(li[1])}</li>`;
      continue;
    }

    if (inList) { html += '</ul>'; inList = false; }
    html += `<p>${inline(line)}</p>`;
  }
  if (inList) html += '</ul>';
  return html;
}

function inline(str) {
  let s = escapeHTML(str);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  return s;
}

/* ---------------- helpers ---------------- */
function slug(str) { return str.toLowerCase().trim().replace(/\s+/g, '-'); }

function isYouTube(url) { return /youtube\.com|youtu\.be/.test(url); }

function toYouTubeEmbed(url) {
  const idMatch = url.match(/(?:v=|youtu\.be\/)([\w-]+)/);
  const id = idMatch ? idMatch[1] : '';
  return `https://www.youtube.com/embed/${id}`;
}

function escapeHTML(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}
function escapeAttr(str) { return escapeHTML(str).replace(/"/g, '&quot;'); }

