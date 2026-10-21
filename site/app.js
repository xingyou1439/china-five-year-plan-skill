'use strict';
(() => {
  const data = JSON.parse(document.querySelector('#guide-data').textContent);
  const cards = new Map(data.cards.map(card => [card.id, card]));
  function revealLibrary() {
    const hash = location.hash;
    if (!hash) return;
    const target = document.getElementById(hash.slice(1));
    const library = target && (target.matches('details') ? target : target.closest('details'));
    if (library) { library.open = true; target.scrollIntoView(); }
  }
  window.addEventListener('hashchange', revealLibrary);
  revealLibrary();
  const key = 'five-year-guide-plan-v1';
  let writable = true;
  let state = {selected: [], context: '', question: '', budget: '', stop: ''};
  try {
    const value = JSON.parse(localStorage.getItem(key) || 'null');
    if (value && typeof value === 'object') {
      state.selected = Array.isArray(value.selected) ? [...new Set(value.selected.filter(id => cards.has(id)))] : [];
      for (const field of ['context', 'question', 'budget', 'stop']) {
        state[field] = typeof value[field] === 'string' ? value[field].slice(0, 500) : '';
      }
    }
  } catch { writable = false; }
  let toastTimer;
  function toast(message) {
    const el = document.querySelector('#toast');
    el.textContent = message; el.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { el.hidden = true; }, 3200);
  }
  function persist() {
    try { localStorage.setItem(key, JSON.stringify(state)); }
    catch { writable = false; }
    const note = document.querySelector('#storage-note');
    if (note && !writable) note.textContent = '浏览器无法保存，当前内容仅留在本页。请及时下载验证清单。';
  }
  function sync() {
    document.querySelectorAll('[data-save]').forEach(button => {
      const selected = state.selected.includes(button.dataset.save);
      button.setAttribute('aria-pressed', String(selected));
      button.textContent = selected ? '已加入清单 ✓' : (button.classList.contains('bookmark') ? '加入清单 ＋' : '加入我的验证清单');
    });
    const list = document.querySelector('#selected-list');
    if (list) {
      list.replaceChildren();
      for (const id of state.selected) {
        const card = cards.get(id), li = document.createElement('li'), link = document.createElement('a'), remove = document.createElement('button');
        link.href = 'cards/' + card.slug + '.html'; link.textContent = id + ' / ' + card.short_title;
        remove.className = 'bookmark'; remove.textContent = '移除'; remove.dataset.save = id;
        remove.setAttribute('aria-label', '移除' + card.short_title);
        li.append(link, remove); list.append(li);
      }
      document.querySelector('#plan-empty').hidden = state.selected.length > 0;
    }
    persist();
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); toast('已复制'); }
    catch {
      const area = document.createElement('textarea'); area.value = text;
      area.style.position = 'fixed'; area.style.left = '-10000px'; document.body.append(area);
      area.select(); const ok = document.execCommand('copy'); area.remove();
      toast(ok ? '已复制' : '无法自动复制，请在页面中选择文字复制');
    }
  }
  document.addEventListener('click', event => {
    if (event.target.closest('a[href="#cases"]')) document.getElementById('cases').open = true;
    const button = event.target.closest('button'); if (!button) return;
    if (button.dataset.save) {
      const id = button.dataset.save; if (!cards.has(id)) return;
      state.selected = state.selected.includes(id) ? state.selected.filter(value => value !== id) : [...state.selected, id];
      sync();
    }
    if (button.dataset.filter) {
      const selected = button.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach(el => el.setAttribute('aria-pressed', String(el === button)));
      let count = 0;
      document.querySelectorAll('.teaser').forEach(el => {
        el.hidden = selected !== '全部' && !el.dataset.audience.split('|').includes(selected);
        if (!el.hidden) count++;
      });
      document.querySelector('#result-count').textContent = '显示' + count + '个案例' + (selected === '全部' ? '' : ' · ' + selected);
    }
    if (button.dataset.share) {
      const card = cards.get(button.dataset.share);
      copy(data.reader_url + 'cards/' + card.slug + '.html');
    }
    if (button.dataset.prompt) copy(document.querySelector('#prompt-' + button.dataset.prompt).textContent);
  });
  for (const field of ['context', 'question', 'budget', 'stop']) {
    const input = document.getElementById(field);
    if (input) { input.value = state[field]; input.addEventListener('input', () => { state[field] = input.value; persist(); }); }
  }
  const clear = document.querySelector('#clear-plan');
  if (clear) clear.addEventListener('click', () => {
    state = {selected: [], context: '', question: '', budget: '', stop: ''};
    for (const field of ['context', 'question', 'budget', 'stop']) document.getElementById(field).value = '';
    sync(); toast('本机记录已清空');
  });
  const exportButton = document.querySelector('#export-plan');
  if (exportButton) exportButton.addEventListener('click', () => {
    if (!state.selected.length) { toast('先选择至少一张决策卡'); return; }
    const lines = ['# 我的两周验证清单', '', '参考版本：v' + data.version + '；内容核验：' + data.reviewed, '', '城市与能力：' + state.context, '要查清的问题：' + state.question, '投入上限：' + state.budget, '我的停止条件：' + state.stop, ''];
    for (const id of state.selected) {
      const c = cards.get(id);
      lines.push('## ' + c.title, '', c.judgment, '', '付款方：' + c.payer, '', '证据缺口：' + c.gap, '', ...c.steps.map(step => '- [ ] ' + step), '', '继续条件：' + c.success, '', '停止条件：' + c.stop, '', '边界：' + c.boundary, '', '完整依据：' + data.reader_url + 'cards/' + c.slug + '.html', '');
    }
    const url = URL.createObjectURL(new Blob([lines.join('\n')], {type: 'text/markdown;charset=utf-8'}));
    const a = document.createElement('a'); a.href = url; a.download = '我的两周验证清单.md'; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  const contextInput = document.getElementById('ask-context');
  const questionInput = document.getElementById('ask-question');
  if (contextInput && questionInput) {
    let intent = 'understand';
    const modes = {
      understand: ['只想了解政策？直接填问题，不需要职业、城市和预算。', '请先用容易理解的话解释，给出实际读取的政策依据、适用范围，以及一个继续了解的方向。'],
      compare: ['写出正在犹豫的选择；还没有选项，也可以让助手先帮你缩小方向。', '请比较我的现实选项；若尚无选项，先根据我已说明的经验帮我缩小方向。先给简短判断、一两条政策依据、最大未知和今天的一步。'],
      act: ['说出已有方向和卡住的地方；需要时间或预算时，助手再补问。', '请从我已说明的方向出发，先给简短判断、政策依据、最该核实的一件事，以及今天能做的一步。说明找谁、问什么、什么结果会改变判断。']
    };
    function updatePrompt() {
      const context = contextInput.value.trim(), question = questionInput.value.trim() || '____';
      document.getElementById('prompt-start').textContent = '请使用 china-five-year-plan-skill。' + (context ? '我现在' + context + '。' : '') + '我最近想弄清楚' + question + '。\n' + modes[intent][1] + '\n只追问会改变答案的信息。如果该 Skill 尚未安装，请直接说明。';
      document.getElementById('intent-help').textContent = modes[intent][0];
    }
    document.querySelectorAll('[data-intent]').forEach(button => button.addEventListener('click', () => {
      if (!Object.hasOwn(modes, button.dataset.intent)) return;
      intent = button.dataset.intent;
      document.querySelectorAll('[data-intent]').forEach(el => el.setAttribute('aria-pressed', String(el === button)));
      updatePrompt();
    }));
    contextInput.addEventListener('input', updatePrompt);
    questionInput.addEventListener('input', updatePrompt);
    updatePrompt();
  }
  sync();
})();
