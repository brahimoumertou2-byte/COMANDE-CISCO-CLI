const API_BASE = 'http://127.0.0.1:8000';
let selectedCategory = '';
let selectedCommand = null;

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      if (body.detail) detail = body.detail;
    } catch (_) {}
    throw new Error(detail);
  }
  return response.json();
}

function setApiStatus(connected, message = '') {
  $('apiStatus').textContent = connected ? `API: connected${message ? ` — ${message}` : ''}` : 'API: disconnected';
}

async function checkApi() {
  try {
    await api('/health');
    setApiStatus(true);
  } catch (error) {
    setApiStatus(false);
    console.error(error);
  }
}

function renderCategories(categories) {
  const box = $('categoryList');
  box.innerHTML = '';
  categories.forEach((category) => {
    const button = document.createElement('button');
    button.className = 'category-btn';
    button.textContent = category;
    button.dataset.category = category;
    button.addEventListener('click', () => {
      selectedCategory = category;

  // Clear search when selecting a category
      $('searchInput').value = '';

  // Update active category
      document.querySelectorAll('.category-btn').forEach((b) => {
        b.classList.remove('active');
  });

      
      button.classList.add('active');

  // Load commands for selected category
      loadCommands();
});
    box.appendChild(button);
  });
}

function renderCommands(commands) {
  const box = $('commandList');
  box.innerHTML = '';
  if (!commands.length) {
    box.innerHTML = '<p>No commands found.</p>';
    return;
  }
  commands.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'command-card';
    card.innerHTML = `<div class="cmd"></div><div class="meta"></div>`;
    card.querySelector('.cmd').textContent = item.command;
    card.querySelector('.meta').textContent = `${item.category} · ${item.device} · ${item.mode}`;
    card.addEventListener('click', () => showDetails(item));
    box.appendChild(card);
  });
}

async function loadCategories() {
  const data = await api('/api/categories');
  renderCategories(data.categories || []);
}

async function loadCommands() {
  const query = $('searchInput').value.trim();

  try {
    let commands;

    // Category has priority when a category is selected
    if (selectedCategory) {
      commands = await api(
        `/api/commands?category=${encodeURIComponent(selectedCategory)}`
      );
    } else if (query) {
      commands = await api(
        `/api/search?q=${encodeURIComponent(query)}`
      );
    } else {
      commands = await api('/api/commands');
    }

    renderCommands(commands);
    setApiStatus(true);

  } catch (error) {
    setApiStatus(false);
    $('commandList').innerHTML = `<p>${escapeHtml(error.message)}</p>`;
  }
}

function showDetails(item) {
  selectedCommand = item;
  $('detailPanel').hidden = false;
  $('detailTitle').textContent = item.command;
  $('detailMeta').textContent = `${item.category} · ${item.device} · ${item.mode}`;
  $('detailCommand').textContent = item.command;
  $('detailDescription').textContent = item.description;
  $('detailSyntax').textContent = item.syntax;
  $('detailExample').textContent = item.example;
  $('detailPlatform').textContent = item.platform;
  $('detailPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function generateCommands() {
  const payload = {
    technology: $('tech').value,
    process_id: Number($('processId').value) || 1,
    network: $('network').value.trim() || null,
    area: Number($('area').value) || 0,
    destination: $('destination').value.trim() || null,
    mask: $('mask').value.trim() || null,
    next_hop: $('nextHop').value.trim() || null,
    router_id: $('routerId').value.trim() || null
  };
  try {
    const result = await api('/api/generator', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    $('generatorOutput').classList.remove('empty');
    $('generatorOutput').textContent = result.commands.join('\n');
    $('generatorNotes').textContent = (result.notes || []).join(' ');
    setApiStatus(true);
  } catch (error) {
    $('generatorOutput').textContent = `Error: ${error.message}`;
  }
}

async function troubleshoot() {
  const output = $('troubleshootInput').value.trim();
  if (!output) return;
  try {
    const result = await api('/api/troubleshooting', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ output, context: $('troubleshootContext').value.trim() || null })
    });
    $('troubleshootOutput').innerHTML = '';
    result.findings.forEach((finding) => {
      const node = document.createElement('div');
      node.className = 'finding';
      node.innerHTML = `<strong>${escapeHtml(finding.level)}</strong><strong>${escapeHtml(finding.title)}</strong><div>${escapeHtml(finding.detail)}</div>`;
      $('troubleshootOutput').appendChild(node);
    });
    setApiStatus(true);
  } catch (error) {
    $('troubleshootOutput').textContent = `Error: ${error.message}`;
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[char]));
}

$('searchInput').addEventListener(
  'input',
  debounce(() => {
    selectedCategory = '';

    document.querySelectorAll('.category-btn').forEach((b) => {
      b.classList.remove('active');
    });

    const allButton = document.querySelector('.category-btn[data-category=""]');
    if (allButton) {
      allButton.classList.add('active');
    }

    loadCommands();
  }, 200)
);$('generateBtn').addEventListener('click', generateCommands);
$('troubleshootBtn').addEventListener('click', troubleshoot);
$('copyDetail').addEventListener('click', async () => {
  if (!selectedCommand) return;
  await navigator.clipboard.writeText(selectedCommand.command);
  $('copyDetail').textContent = 'Copied';
  setTimeout(() => $('copyDetail').textContent = 'Copy', 1000);
});

document.querySelector('[data-category=""]').addEventListener('click', () => {
  selectedCategory = '';
  document.querySelectorAll('.category-btn').forEach((b) => b.classList.remove('active'));
  document.querySelector('[data-category=""]').classList.add('active');
  loadCommands();
});

function debounce(fn, wait) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), wait);
  };
}

Promise.all([checkApi(), loadCategories(), loadCommands()]).catch(console.error);
setInterval(checkApi, 30000);
