(function () {
  const select = document.getElementById('query-select');
  const text = document.getElementById('query-text');
  const btn = document.getElementById('run-btn');
  const status = document.getElementById('status');
  const resultArea = document.getElementById('result-area');

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function cellHtml(binding) {
    if (!binding) return '';
    if (binding.type === 'uri') {
      const href = binding.value.startsWith(location.origin)
        ? binding.value.slice(location.origin.length)
        : binding.value;
      return '<a href="' + escapeHtml(href) + '">' + escapeHtml(binding.value) + '</a>';
    }
    return escapeHtml(binding.value);
  }

  function renderSelectResults(data) {
    const vars = data.head.vars || [];
    const rows = data.results.bindings;
    if (!rows.length) {
      resultArea.innerHTML = '<p>Không có kết quả.</p>';
      return;
    }
    let html = '<table><thead><tr>' + vars.map((v) => '<th>' + escapeHtml(v) + '</th>').join('') + '</tr></thead><tbody>';
    for (const row of rows) {
      html += '<tr>' + vars.map((v) => '<td>' + cellHtml(row[v]) + '</td>').join('') + '</tr>';
    }
    html += '</tbody></table>';
    resultArea.innerHTML = html;
  }

  function renderAskResult(data) {
    resultArea.innerHTML = '<p>Kết quả ASK: <strong>' + (data.boolean ? 'true' : 'false') + '</strong></p>';
  }

  function renderTurtle(text) {
    resultArea.innerHTML = '<pre class="iri">' + escapeHtml(text) + '</pre>';
  }

  async function runQuery() {
    const query = text.value.trim();
    if (!query) return;
    btn.disabled = true;
    status.textContent = 'Đang chạy...';
    resultArea.innerHTML = '';
    try {
      const res = await fetch('/sparql', {
        method: 'POST',
        headers: { 'Content-Type': 'application/sparql-query' },
        body: query,
      });
      const contentType = res.headers.get('content-type') || '';
      if (!res.ok) {
        const err = contentType.includes('json') ? (await res.json()).error : await res.text();
        resultArea.innerHTML = '<p class="error">' + escapeHtml(err || ('HTTP ' + res.status)) + '</p>';
        return;
      }
      if (contentType.includes('application/sparql-results+json')) {
        const data = await res.json();
        if ('boolean' in data) renderAskResult(data);
        else renderSelectResults(data);
      } else {
        renderTurtle(await res.text());
      }
      status.textContent = '';
    } catch (e) {
      resultArea.innerHTML = '<p class="error">' + escapeHtml(e.message) + '</p>';
    } finally {
      btn.disabled = false;
      status.textContent = '';
    }
  }

  async function init() {
    const queries = await (await fetch('/data/queries.json')).json();
    select.innerHTML = queries.map((q, i) => '<option value="' + i + '">' + escapeHtml(q.label) + '</option>').join('');
    function applySelection() {
      text.value = queries[select.value].query;
    }
    select.addEventListener('change', applySelection);
    applySelection();
    btn.addEventListener('click', runQuery);
  }

  init();
})();
