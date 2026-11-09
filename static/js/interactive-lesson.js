/* =============================================================================
   Interaktiv dars: Python muharriri, natija oynasi, topshiriqlarni tekshirish,
   yordam (hint / qisman / to'liq yechim), avtosaqlash va vazifa ish maydoni.
   Kod brauzerda emas, serverdagi izolyatsiyalangan sandbox'da bajariladi.
   ============================================================================= */
(function () {
  'use strict';

  const cfgEl = document.getElementById('interactive-config');
  if (!cfgEl) return;
  const cfg = JSON.parse(cfgEl.textContent);
  const editors = {};        // key -> ace editor
  const saveTimers = {};

  // ---------------------------------------------------------------------------
  // Yordamchi funksiyalar
  // ---------------------------------------------------------------------------
  function getCookie(name) {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }
  const csrf = cfg.csrf || getCookie('csrftoken');

  function esc(text) {
    const d = document.createElement('div');
    d.textContent = text == null ? '' : String(text);
    return d.innerHTML;
  }

  function taskUrl(template, id) {
    return template.replace('/0/', '/' + id + '/');
  }

  async function postJSON(url, data) {
    const res = await fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
      body: JSON.stringify(data || {}),
    });
    let body = {};
    try { body = await res.json(); } catch (e) { body = { ok: false, error: "Serverdan noto'g'ri javob keldi." }; }
    return { status: res.status, body };
  }

  async function getJSON(url) {
    const res = await fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    let body = {};
    try { body = await res.json(); } catch (e) { body = { ok: false }; }
    return { status: res.status, body };
  }

  function setBusy(btn, busy, label) {
    if (!btn) return;
    if (busy) {
      btn.dataset.html = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i>' + (label || 'Kuting...');
    } else {
      btn.disabled = false;
      if (btn.dataset.html) btn.innerHTML = btn.dataset.html;
    }
  }

  function requireInteract() {
    if (cfg.canInteract) return true;
    if (!cfg.isAuthenticated && cfg.loginUrl) {
      window.location.href = cfg.loginUrl;
    } else {
      alert("Bu amal uchun kursga yozilishingiz kerak.");
    }
    return false;
  }

  // ---------------------------------------------------------------------------
  // Ace muharriri
  // ---------------------------------------------------------------------------
  function makeEditor(el, key, initial, opts) {
    if (!window.ace || !el) return null;
    const editor = ace.edit(el, Object.assign({
      mode: 'ace/mode/python',
      theme: 'ace/theme/one_dark',
      fontSize: 14,
      tabSize: 4,
      useSoftTabs: true,
      showPrintMargin: false,
      wrap: true,
      highlightActiveLine: true,
      scrollPastEnd: 0.2,
    }, opts || {}));
    const canSave = cfg.canInteract && cfg.urls && cfg.urls.draft;
    // Serverga hali yetib bormagan (sinxronlanmagan) lokal nusxa bo'lsa — u eng so'nggi holat
    const local = canSave ? readLocal(key) : null;
    const startValue = local && !local.synced ? local.code : (initial || '');
    editor.session.setValue(startValue);
    editor.renderer.setScrollMargin(6, 6);
    editors[key] = editor;
    if (canSave) {
      editor.session.on('change', () => { writeLocal(key, editor.getValue(), false); scheduleSave(key, el); });
      if (local && !local.synced) scheduleSave(key, el);  // serverga qayta yuborish
    }
    return editor;
  }

  // Lokal zaxira (localStorage): sahifa yopilishi/yangilanishi bilan yo'qolmasligi uchun sinxron yoziladi.
  // Saqlash ishonchli manbai — server; lokal nusxa faqat hali yuborilmagan o'zgarishlar uchun.
  function localKey(key) { return 'ilesson-draft:' + cfg.lessonId + ':' + key; }
  function readLocal(key) {
    try { const raw = localStorage.getItem(localKey(key)); return raw ? JSON.parse(raw) : null; } catch (e) { return null; }
  }
  function writeLocal(key, code, synced) {
    try { localStorage.setItem(localKey(key), JSON.stringify({ code, synced })); } catch (e) { /* xususiy rejim — server baribir saqlaydi */ }
  }

  async function saveNow(key, el, keepalive) {
    clearTimeout(saveTimers[key]);
    delete saveTimers[key];
    const editor = editors[key];
    if (!editor) return;
    const state = el ? findSaveState(el) : null;
    const code = editor.getValue();
    const payload = JSON.stringify({ lesson_id: cfg.lessonId, key, code });
    try {
      const res = await fetch(cfg.urls.draft, {
        method: 'POST', credentials: 'same-origin', keepalive: !!keepalive,
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
        body: payload,
      });
      if (res.status === 200 && editor.getValue() === code) writeLocal(key, code, true);
      if (state) state.textContent = res.status === 200 ? 'avtomatik saqlandi ✓' : 'saqlanmadi';
    } catch (e) {
      if (state) state.textContent = 'saqlanmadi';
    }
  }

  function scheduleSave(key, el) {
    clearTimeout(saveTimers[key]);
    const state = findSaveState(el);
    if (state) state.textContent = 'saqlanmoqda...';
    saveTimers[key] = setTimeout(() => saveNow(key, el, false), 1200);
  }

  // Sahifa yopilayotgan/yangilanayotgan bo'lsa, kutilayotgan saqlashlarni darhol yuborish
  function flushPendingSaves() {
    Object.keys(saveTimers).forEach((key) => saveNow(key, null, true));
  }
  window.addEventListener('pagehide', flushPendingSaves);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flushPendingSaves(); });

  function findSaveState(el) {
    const scope = el.closest('[data-task]') || el.closest('.playground-card') || document;
    return scope.querySelector('[data-save-state]');
  }

  function markErrorLine(editor, line, message) {
    if (!editor) return;
    const session = editor.session;
    (editor._errMarkers || []).forEach((id) => session.removeMarker(id));
    editor._errMarkers = [];
    session.clearAnnotations();
    if (!line) return;
    const Range = ace.require('ace/range').Range;
    editor._errMarkers.push(session.addMarker(new Range(line - 1, 0, line - 1, 1), 'ace_error-line', 'fullLine'));
    session.setAnnotations([{ row: line - 1, column: 0, text: message || 'Xato', type: 'error' }]);
  }

  // ---------------------------------------------------------------------------
  // Natija oynasi
  // ---------------------------------------------------------------------------
  function renderResult(box, result, editor) {
    if (!box) return;
    const ok = result.status === 'ok';
    const infra = ['unavailable', 'busy', 'invalid'].includes(result.status);
    let html = '<div class="flex items-center gap-2 mb-2 text-[11px] font-bold">';
    html += ok
      ? '<span class="px-2 py-0.5 rounded-md bg-emerald-500/15 text-emerald-400"><i class="fa-solid fa-circle-check mr-1"></i>' + esc(result.status_label) + '</span>'
      : '<span class="px-2 py-0.5 rounded-md ' + (infra ? 'bg-amber-500/15 text-amber-400' : 'bg-rose-500/15 text-rose-400') + '"><i class="fa-solid fa-circle-exclamation mr-1"></i>' + esc(result.status_label) + '</span>';
    if (result.elapsed_ms) html += '<span class="text-slate-500 font-mono">' + result.elapsed_ms + ' ms</span>';
    html += '</div>';

    if (result.stdout) {
      html += '<pre class="stdout-box font-mono text-[13px] text-slate-100 bg-black/30 rounded-lg p-2.5">' + esc(result.stdout) + '</pre>';
    } else if (ok) {
      html += '<p class="text-xs text-slate-500 font-mono">(Dastur ekranga hech narsa chiqarmadi)</p>';
    }
    if (!ok) {
      if (result.friendly_error) {
        html += '<div class="mt-2 rounded-lg border border-rose-500/30 bg-rose-500/10 p-2.5 text-[13px] text-rose-200 leading-relaxed"><i class="fa-solid fa-lightbulb text-amber-300 mr-1"></i>' + esc(result.friendly_error) + '</div>';
      }
      if (result.stderr) {
        html += '<details class="mt-2" ' + (result.friendly_error ? '' : 'open') + '><summary class="text-[11px] text-slate-400 cursor-pointer">Python xato xabari (traceback)</summary>' +
          '<pre class="mt-1 font-mono text-[12px] text-rose-300 bg-black/30 rounded-lg p-2.5">' + esc(result.stderr) + '</pre></details>';
      }
    }
    if (result.truncated) html += '<p class="mt-1 text-[11px] text-amber-400">Natija juda uzun bo\'lgani uchun qisqartirildi.</p>';
    box.innerHTML = html;
    if (editor) markErrorLine(editor, ok ? null : result.error_line, result.error && result.error.message);
  }

  function renderPending(box) {
    if (box) box.innerHTML = '<p class="text-xs text-slate-400 font-mono"><i class="fa-solid fa-spinner fa-spin mr-1"></i>Sandbox\'da bajarilmoqda...</p>';
  }

  function renderError(box, message) {
    if (box) box.innerHTML = '<div class="rounded-lg border border-amber-500/30 bg-amber-500/10 p-2.5 text-[13px] text-amber-200"><i class="fa-solid fa-triangle-exclamation mr-1"></i>' + esc(message) + '</div>';
  }

  async function runCode(code, stdin, extra) {
    const payload = Object.assign({ code, stdin: stdin || '' }, extra || {});
    return postJSON(cfg.urls.run, payload);
  }

  // ---------------------------------------------------------------------------
  // Statik kodni rangli ko'rsatish
  // ---------------------------------------------------------------------------
  function highlightStatic(root) {
    if (!window.ace) return;
    let highlighter;
    try { highlighter = ace.require('ace/ext/static_highlight'); } catch (e) { return; }
    const nodes = (root || document).querySelectorAll('pre[data-highlight]:not([data-hl-done]), .lesson-prose pre > code:not([data-hl-done])');
    nodes.forEach((node) => {
      node.setAttribute('data-hl-done', '1');
      const lang = (node.className || '').match(/language-(\w+)/);
      // Markdown ichidagi bloklardan faqat aniq ```python deb belgilanganlari bo'yaladi
      // (tilsiz bloklar — masalan, dastur natijasi — oddiy matn bo'lib qoladi)
      if (node.tagName === 'CODE' && !(lang && ['python', 'py'].includes(lang[1]))) return;
      const target = node.tagName === 'CODE' ? node.parentElement : node;
      const code = node.textContent;
      try {
        highlighter.render(code.replace(/\s+$/, ''), 'ace/mode/python', 'ace/theme/one_dark', 1, true, (hl) => {
          target.classList.add('static-code');
          target.innerHTML = hl.html;
          target.setAttribute('data-hl-done', '1');
          target.dataset.raw = code;
        });
      } catch (e) { /* rangsiz qoladi */ }
    });
  }

  // ---------------------------------------------------------------------------
  // Dars muharriri (playground)
  // ---------------------------------------------------------------------------
  const pgEl = document.getElementById('playground-editor');
  const pgOutput = document.getElementById('pg-output');
  const pgStdin = document.getElementById('pg-stdin');
  const panel = document.getElementById('playground-panel');
  let pg = null;
  if (pgEl) {
    const initial = (cfg.drafts && cfg.drafts.playground) || '# Bu yerda Python kodini yozing va «Ishga tushirish» tugmasini bosing\nprint("Salom, dunyo!")\n';
    pg = makeEditor(pgEl, 'playground', initial);
    if (pg) {
      pg.commands.addCommand({ name: 'run', bindKey: { win: 'Ctrl-Enter', mac: 'Command-Enter' }, exec: () => runPlayground() });
    }
  }

  async function runPlayground() {
    if (!pg || !requireInteract()) return;
    if (saveTimers.playground) saveNow('playground', pgEl, false);
    const btn = document.getElementById('pg-run');
    setBusy(btn, true, 'Bajarilmoqda');
    renderPending(pgOutput);
    try {
      const { status, body } = await runCode(pg.getValue(), pgStdin ? pgStdin.value : '', { lesson_id: cfg.lessonId });
      if (body.ok) renderResult(pgOutput, body.result, pg);
      else renderError(pgOutput, body.error || ('Xatolik (' + status + ')'));
    } catch (e) {
      renderError(pgOutput, "Serverga ulanib bo'lmadi. Internet aloqasini tekshiring.");
    } finally {
      setBusy(btn, false);
    }
  }

  function openPlayground() {
    if (panel && window.matchMedia('(max-width: 1023.98px)').matches) {
      panel.classList.add('is-open');
      setTimeout(() => pg && pg.resize(), 30);
    } else if (panel) {
      panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  const bind = (id, fn) => { const el = document.getElementById(id); if (el) el.addEventListener('click', fn); };
  bind('pg-run', runPlayground);
  bind('pg-rerun', runPlayground);
  bind('pg-clear', () => { if (pg) { pg.setValue('', -1); pg.focus(); } if (pgOutput) pgOutput.innerHTML = ''; markErrorLine(pg, null); });
  bind('playground-fab', openPlayground);
  bind('pg-close', () => panel && panel.classList.remove('is-open'));

  // Misollar: muharrirga yuklash / ishga tushirish
  document.querySelectorAll('[data-example]').forEach((card) => {
    const codeEl = card.querySelector('[data-example-code]');
    const getCode = () => (codeEl.dataset.raw != null ? codeEl.dataset.raw : codeEl.textContent);
    const load = card.querySelector('[data-example-load]');
    const run = card.querySelector('[data-example-run]');
    if (load) load.addEventListener('click', () => { if (pg) { pg.setValue(getCode(), 1); openPlayground(); pg.focus(); } });
    if (run) run.addEventListener('click', () => { if (pg) { pg.setValue(getCode(), 1); openPlayground(); runPlayground(); } });
  });

  // ---------------------------------------------------------------------------
  // Topshiriq vidjetlari
  // ---------------------------------------------------------------------------
  function collectAnswer(widget, kind, editor) {
    if (kind === 'single_choice' || kind === 'multiple_choice') {
      return { options: Array.from(widget.querySelectorAll('[data-options] input:checked')).map((i) => parseInt(i.value, 10)) };
    }
    if (kind === 'predict_output') {
      const t = widget.querySelector('[data-answer-text]');
      return { text: t ? t.value : '' };
    }
    if (kind === 'fill_blank') {
      const inputs = Array.from(widget.querySelectorAll('[data-blank]')).sort((a, b) => a.dataset.blank - b.dataset.blank);
      return { blanks: inputs.map((i) => i.value) };
    }
    return { code: editor ? editor.getValue() : '' };
  }

  function showFeedback(widget, body) {
    const fb = widget.querySelector('[data-feedback]');
    if (!fb) return;
    fb.classList.remove('hidden');
    const good = body.is_correct;
    let html = '<div class="rounded-xl border p-3 text-sm ' + (good
      ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-800 dark:text-emerald-300'
      : 'border-rose-500/40 bg-rose-500/10 text-rose-800 dark:text-rose-300') + '">';
    html += '<div class="font-extrabold"><i class="fa-solid ' + (good ? 'fa-circle-check' : 'fa-circle-xmark') + ' mr-1"></i>' + esc(body.message) + '</div>';
    html += '<div class="text-xs mt-1 opacity-80">Urinish #' + body.attempt_number + ' · ball: ' + body.score + ' / ' + body.max_score + '</div>';
    (body.option_feedback || []).forEach((f) => { html += '<div class="text-xs mt-1.5">• ' + esc(f.feedback) + '</div>'; });
    if (!good) {
      html += '<div class="text-xs mt-1.5 opacity-90">Maslahat tugmasidan foydalaning va qayta urinib ko\'ring.</div>';
    }
    if (good && body.explanation_html) {
      html += '<div class="lesson-prose text-[13px] mt-2 pt-2 border-t border-emerald-500/30">' + body.explanation_html + '</div>';
    }
    if (body.coins_awarded) {
      html += '<div class="text-xs mt-1.5 font-bold text-amber-600 dark:text-amber-400"><i class="fa-solid fa-coins mr-1"></i>+' + body.coins_awarded + ' tanga!</div>';
    }
    html += '</div>';
    fb.innerHTML = html;
    if (body.coins_awarded) {
      const c = document.getElementById('nav-user-coins');
      if (c && body.user_coins != null) c.textContent = body.user_coins;
      if (typeof window.celebrateCoins === 'function') window.celebrateCoins(body.coins_awarded);
    }
  }

  function showTests(widget, tests) {
    const ul = widget.querySelector('[data-tests]');
    if (!ul) return;
    if (!tests || !tests.length) { ul.classList.add('hidden'); ul.innerHTML = ''; return; }
    ul.classList.remove('hidden');
    ul.innerHTML = tests.map((t) =>
      '<li class="flex gap-2 text-[13px] ' + (t.passed ? 'text-emerald-700 dark:text-emerald-400' : 'text-rose-700 dark:text-rose-400') + '">' +
      '<i class="fa-solid ' + (t.passed ? 'fa-check' : 'fa-xmark') + ' mt-1 w-3"></i><span><span class="font-semibold">' + esc(t.description) + '</span>' +
      (t.message ? '<span class="block text-xs opacity-80">' + esc(t.message) + '</span>' : '') + '</span></li>'
    ).join('');
  }

  function updateRules(widget, rules, body) {
    const partial = widget.querySelector('[data-action="partial"]');
    if (partial && rules.partial) partial.disabled = false;
    const sol = widget.querySelector('[data-action="solution"]');
    if (sol) {
      if (rules.solution) {
        sol.disabled = false;
        const cnt = sol.querySelector('[data-unlock-count]');
        if (cnt) cnt.remove();
        sol.title = "Yechimni ko'rish";
      } else {
        const cnt = sol.querySelector('[data-unlock-count]');
        if (cnt) cnt.textContent = '(' + rules.attempts_needed + ')';
      }
    }
    const badge = widget.querySelector('[data-status-badge]');
    if (badge && body) {
      if (body.solved) {
        badge.className = 'ml-auto normal-case tracking-normal text-[11px] font-bold text-emerald-600 dark:text-emerald-400';
        badge.innerHTML = '<i class="fa-solid fa-circle-check"></i> Bajarilgan';
      } else {
        badge.textContent = body.attempts + ' ta urinish';
      }
    }
    const id = widget.dataset.taskId;
    const status = document.querySelector('[data-assignment-status="' + id + '"]');
    if (status && body) {
      status.innerHTML = body.solved
        ? '<span class="text-emerald-600 dark:text-emerald-400"><i class="fa-solid fa-circle-check mr-1"></i>Bajarilgan</span>'
        : '<span class="text-amber-600 dark:text-amber-400">' + body.attempts + ' ta urinish — hali yechilmagan</span>';
    }
  }

  function markOptions(widget, correctIds, selectedIds) {
    widget.querySelectorAll('[data-option-id]').forEach((label) => {
      const id = parseInt(label.dataset.optionId, 10);
      label.classList.remove('is-correct', 'is-wrong');
      if (correctIds && correctIds.includes(id)) label.classList.add('is-correct');
      else if (selectedIds && selectedIds.includes(id)) label.classList.add('is-wrong');
    });
  }

  function revealBox(title, inner, tone) {
    const tones = {
      amber: 'border-amber-500/40 bg-amber-500/10',
      sky: 'border-sky-500/40 bg-sky-500/10',
      slate: 'border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/60',
    };
    return '<div class="rounded-xl border p-3 ' + (tones[tone] || tones.slate) + '"><div class="text-[11px] font-black uppercase tracking-wider text-slate-500 mb-1.5">' + esc(title) + '</div>' + inner + '</div>';
  }

  function codeBlock(code, withLoad) {
    return '<pre class="static-code rounded-lg text-[13px]" data-highlight>' + esc(code) + '</pre>' +
      (withLoad ? '<button type="button" data-load-solution class="mt-2 text-xs font-bold text-blue-600 dark:text-blue-400 hover:underline"><i class="fa-solid fa-arrow-right-to-bracket mr-1"></i>Muharrirga yuklash</button>' : '');
  }

  function initTask(widget) {
    const id = widget.dataset.taskId;
    const kind = widget.dataset.kind;
    const key = 'task-' + id;
    const edEl = widget.querySelector('[data-editor]');
    const output = widget.querySelector('[data-output]');
    const reveal = widget.querySelector('[data-reveal]');
    let editor = null;
    let lastSelected = [];

    if (edEl) {
      const starter = (cfg.starters && cfg.starters[key]) || '';
      const draft = cfg.drafts && cfg.drafts[key];
      editor = makeEditor(edEl, key, draft != null ? draft : starter, widget.dataset.mode === 'workspace' ? {} : { minLines: 8, maxLines: 20 });
      if (editor) {
        editor.commands.addCommand({ name: 'run', bindKey: { win: 'Ctrl-Enter', mac: 'Command-Enter' }, exec: () => runTaskCode() });
      }
    }

    async function runTaskCode() {
      if (!editor || !requireInteract()) return;
      if (saveTimers[key]) saveNow(key, edEl, false);
      const btn = widget.querySelector('[data-action="run"]');
      setBusy(btn, true, 'Bajarilmoqda');
      renderPending(output);
      output.classList.add('rounded-xl', 'bg-slate-950', 'p-3');
      try {
        const { status, body } = await runCode(editor.getValue(), '', { task_id: parseInt(id, 10) });
        if (body.ok) renderResult(output, body.result, editor);
        else renderError(output, body.error || ('Xatolik (' + status + ')'));
      } catch (e) {
        renderError(output, "Serverga ulanib bo'lmadi.");
      } finally { setBusy(btn, false); }
    }

    async function check() {
      if (!requireInteract()) return;
      if (saveTimers[key]) saveNow(key, edEl, false);
      const btn = widget.querySelector('[data-action="check"]');
      const answer = collectAnswer(widget, kind, editor);
      lastSelected = answer.options || [];
      setBusy(btn, true, 'Tekshirilmoqda');
      try {
        const { status, body } = await postJSON(taskUrl(cfg.urls.check, id), answer);
        if (!body.ok) {
          const fb = widget.querySelector('[data-feedback]');
          fb.classList.remove('hidden');
          fb.innerHTML = '<div class="rounded-xl border border-amber-500/40 bg-amber-500/10 p-3 text-sm text-amber-800 dark:text-amber-300"><i class="fa-solid fa-circle-info mr-1"></i>' + esc(body.error || ('Xatolik (' + status + ')')) + '</div>';
          return;
        }
        showFeedback(widget, body);
        showTests(widget, body.tests);
        updateRules(widget, body.rules, body);
        if (body.run && output) {
          output.classList.add('rounded-xl', 'bg-slate-950', 'p-3');
          renderResult(output, body.run, editor);
        }
        if (kind === 'single_choice' || kind === 'multiple_choice') {
          markOptions(widget, body.is_correct ? lastSelected : null, body.is_correct ? null : lastSelected);
        }
        if (kind === 'fill_blank' && body.tests) {
          const inputs = widget.querySelectorAll('[data-blank]');
          if (body.tests.length === inputs.length) {
            inputs.forEach((inp, i) => { inp.classList.toggle('is-correct', body.tests[i].passed); inp.classList.toggle('is-wrong', !body.tests[i].passed); });
          }
        }
        highlightStatic(widget);
      } catch (e) {
        alert("Serverga ulanib bo'lmadi.");
      } finally { setBusy(btn, false); }
    }

    async function doReveal(what, btn) {
      if (!requireInteract()) return;
      setBusy(btn, true, 'Ochilmoqda');
      try {
        const { body } = await postJSON(taskUrl(cfg.urls.reveal, id), { what });
        if (!body.ok) {
          reveal.insertAdjacentHTML('afterbegin', revealBox('Hali mumkin emas', '<p class="text-sm">' + esc(body.error) + '</p>', 'slate'));
          return;
        }
        let html = '';
        if (what === 'hint') html = revealBox('Maslahat', '<p class="text-sm whitespace-pre-line">' + esc(body.hint) + '</p>', 'amber');
        if (what === 'partial') html = revealBox('Qisman yechim', codeBlock(body.partial, !!editor), 'sky');
        if (what === 'solution') {
          let inner = '';
          if (body.correct_options) markOptions(widget, body.correct_options, lastSelected);
          if (body.correct_answer != null) inner += '<div class="text-xs font-bold mb-1">To\'g\'ri natija:</div><pre class="rounded-lg bg-slate-950 text-emerald-300 font-mono text-[13px] p-2.5 whitespace-pre">' + esc(body.correct_answer) + '</pre>';
          if (body.correct_blanks) inner += '<div class="text-sm">To\'g\'ri javoblar: ' + body.correct_blanks.map((b) => '<code class="px-1.5 py-0.5 rounded bg-slate-200 dark:bg-slate-800 font-mono">' + esc(b) + '</code>').join(' , ') + '</div>';
          if (body.solution) inner += codeBlock(body.solution, !!editor);
          if (body.explanation_html) inner += '<div class="lesson-prose text-[13px] mt-2">' + body.explanation_html + '</div>';
          html = revealBox(editor ? "To'liq yechim" : 'Javob va tushuntirish', inner || '<p class="text-sm">—</p>', 'slate');
        }
        reveal.insertAdjacentHTML('afterbegin', html);
        btn.classList.add('ring-2', 'ring-offset-1', 'ring-blue-400/40');
        highlightStatic(reveal);
        reveal.querySelectorAll('[data-load-solution]').forEach((b) => {
          if (b.dataset.bound) return;
          b.dataset.bound = '1';
          b.addEventListener('click', () => {
            const pre = b.previousElementSibling;
            const code = pre.dataset.raw != null ? pre.dataset.raw : pre.textContent;
            if (editor) { editor.setValue(code, 1); editor.focus(); }
          });
        });
      } catch (e) {
        alert("Serverga ulanib bo'lmadi.");
      } finally { setBusy(btn, false); }
    }

    async function showHistory(btn) {
      const box = widget.querySelector('[data-history]');
      if (!box) return;
      if (!box.classList.contains('hidden')) { box.classList.add('hidden'); return; }
      if (!requireInteract()) return;
      setBusy(btn, true, 'Yuklanmoqda');
      try {
        const { body } = await getJSON(taskUrl(cfg.urls.attempts, id));
        box.classList.remove('hidden');
        if (!body.ok || !body.attempts.length) {
          box.innerHTML = '<p class="text-xs text-slate-500">Hali yechim yuborilmagan.</p>';
          return;
        }
        box.innerHTML = body.attempts.map((a, i) => {
          const when = new Date(a.submitted_at).toLocaleString('uz-UZ');
          return '<div class="rounded-xl border border-slate-200 dark:border-slate-800 p-2.5 text-xs">' +
            '<div class="flex flex-wrap items-center gap-2"><span class="font-bold">#' + a.number + '</span>' +
            '<span class="' + (a.is_correct ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400') + ' font-bold">' + (a.is_correct ? "To'g'ri" : "Noto'g'ri") + '</span>' +
            '<span class="text-slate-500">' + a.tests_passed + '/' + a.tests_total + ' test · ' + a.score + '/' + a.max_score + ' ball</span>' +
            '<span class="text-slate-400 ml-auto">' + esc(when) + '</span></div>' +
            (a.code ? '<button type="button" data-load-attempt="' + i + '" class="mt-1.5 text-blue-600 dark:text-blue-400 font-bold hover:underline">Shu kodni muharrirga yuklash</button>' : '') +
            '</div>';
        }).join('');
        box.querySelectorAll('[data-load-attempt]').forEach((b) => b.addEventListener('click', () => {
          const a = body.attempts[parseInt(b.dataset.loadAttempt, 10)];
          if (editor && a) { editor.setValue(a.code, 1); editor.focus(); }
        }));
      } finally { setBusy(btn, false); }
    }

    widget.addEventListener('click', (ev) => {
      const btn = ev.target.closest('[data-action]');
      if (!btn || !widget.contains(btn) || btn.closest('[data-task]') !== widget) return;
      const action = btn.dataset.action;
      if (action === 'check') check();
      else if (action === 'run') runTaskCode();
      else if (action === 'reset') {
        if (editor && confirm("Kodni boshlang'ich holatiga qaytarasizmi?")) {
          editor.setValue((cfg.starters && cfg.starters[key]) || '', 1);
          markErrorLine(editor, null);
          if (output) output.innerHTML = '';
        }
      } else if (action === 'from-playground') {
        if (editor && pg) { editor.setValue(pg.getValue(), 1); editor.focus(); }
      } else if (action === 'hint' || action === 'partial' || action === 'solution') doReveal(action, btn);
      else if (action === 'history') showHistory(btn);
    });

    widget._editor = editor;
  }

  document.querySelectorAll('[data-task]').forEach(initTask);
  highlightStatic(document);

  // ---------------------------------------------------------------------------
  // Vazifa ish maydoni (dars sahifasining ichida ochiladi)
  // ---------------------------------------------------------------------------
  function openWorkspace(id) {
    const ws = document.querySelector('[data-workspace="' + id + '"]');
    if (!ws) return;
    ws.classList.add('is-open');
    document.body.classList.add('workspace-open');
    const widget = ws.querySelector('[data-task]');
    setTimeout(() => { if (widget && widget._editor) { widget._editor.resize(); widget._editor.focus(); } }, 50);
    if (history.replaceState) history.replaceState(null, '', '#vazifa-' + id);
  }
  function closeWorkspaces() {
    document.querySelectorAll('[data-workspace].is-open').forEach((ws) => ws.classList.remove('is-open'));
    document.body.classList.remove('workspace-open');
    if (history.replaceState && location.hash.startsWith('#vazifa-')) history.replaceState(null, '', location.pathname + location.search);
  }
  document.querySelectorAll('[data-open-workspace]').forEach((b) => b.addEventListener('click', () => openWorkspace(b.dataset.openWorkspace)));
  document.querySelectorAll('[data-close-workspace]').forEach((b) => b.addEventListener('click', closeWorkspaces));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeWorkspaces();
      closeSyllabus();
      if (panel) panel.classList.remove('is-open');
    }
  });
  const hashMatch = location.hash.match(/^#vazifa-(\d+)$/);
  if (hashMatch) openWorkspace(hashMatch[1]);

  // ---------------------------------------------------------------------------
  // Mundarija
  // ---------------------------------------------------------------------------
  const drawer = document.getElementById('syllabus-drawer');
  function closeSyllabus() { if (drawer) drawer.classList.add('hidden'); }
  document.querySelectorAll('[data-open-syllabus]').forEach((b) => b.addEventListener('click', () => drawer && drawer.classList.remove('hidden')));
  document.querySelectorAll('[data-close-syllabus]').forEach((b) => b.addEventListener('click', closeSyllabus));

  // ---------------------------------------------------------------------------
  // Darsni tugatish (AJAX)
  // ---------------------------------------------------------------------------
  const completeForm = document.getElementById('lesson-complete-form');
  if (completeForm) {
    completeForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('lesson-complete-btn');
      setBusy(btn, true, 'Saqlanmoqda');
      try {
        const res = await fetch(completeForm.action, {
          method: 'POST',
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
          body: new FormData(completeForm),
        });
        const data = await res.json();
        if (!data.success) throw new Error();
        setBusy(btn, false);
        const done = data.is_completed;
        btn.className = 'px-4 py-2.5 rounded-xl text-sm font-extrabold ' + (done ? 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300' : 'bg-blue-600 hover:bg-blue-500 text-white');
        btn.innerHTML = done ? '<i class="fa-solid fa-rotate-left mr-1"></i>Tugallanmagan deb belgilash' : '<i class="fa-solid fa-check mr-1"></i>Darsni tugatdim';
        const chip = document.getElementById('lesson-status-chip');
        if (chip) {
          chip.className = 'px-2.5 py-1 rounded-lg font-bold ' + (done ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : 'bg-slate-100 dark:bg-slate-800 text-slate-500');
          chip.innerHTML = done ? '<i class="fa-solid fa-circle-check mr-1"></i>Dars tugallangan' : '<i class="fa-regular fa-circle mr-1"></i>Dars tugallanmagan';
        }
        const label = document.getElementById('course-progress-label');
        if (label) label.textContent = data.progress_percent;
      } catch (err) {
        setBusy(btn, false);
        completeForm.submit();
      }
    });
  }
})();
