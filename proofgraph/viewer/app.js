'use strict';

const ENV_COLOR = {
  definition: '#2563eb', proposition: '#ea7317', theorem: '#dc2626',
  claim: '#16a34a', remark: '#ca8a04', example: '#6b7280',
};
const ENV_LABEL = {
  definition: 'Def', proposition: 'Prop', theorem: 'Thm',
  claim: 'Clm', remark: 'Rem', example: 'Ex',
};
// 章コンテナの淡色タイル（出現順に循環割当）
const CHAP_TINT = ['#dbeafe', '#dcfce7', '#fef3c7', '#fae8ff',
                   '#ffedd5', '#cffafe', '#fee2e2', '#ede9fe', '#f1f5f9', '#fce7f3'];
const LABEL_ZOOM = 0.95;   // このズーム以上で全ラベルを自動表示

let GRAPH = null;
let cy = null;
let NODE_BY_ID = {};
let CHAP_ORDER = [];                 // 章ラベルの出現順
let UP = {}, DOWN = {};              // 隣接（描画される辺ベース）up=依存先, down=被依存
let activeRouteByNode = {};
let focusSet = null;                 // null=全体表示。Set のときフォーカス中
let selectedId = null;

// ---------------------------------------------------------------------------
// 読み込み
// ---------------------------------------------------------------------------
// ?data=... で読み込むグラフを差し替え可能（既定はセミナー抽出結果）。
// 例: viewer/?data=sample.graph.json はデモ用の小さなサンプルを開く。
const DATA_SRC = new URLSearchParams(location.search).get('data') || '../out/graph.json';

async function load() {
  let data;
  try {
    const res = await fetch(DATA_SRC, { cache: 'no-store' });
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    data = await res.json();
  } catch (e) {
    showError(
      `データ（${DATA_SRC}）を読み込めませんでした（` + e.message + '）。\n\n' +
      'まず抽出してローカルサーバ経由で開いてください：\n\n' +
      '  cd proofgraph && uv run pg.py        # 抽出 → 検証 → サーバ起動\n' +
      '  → http://localhost:8000/viewer/\n\n' +
      'サンプル（抽出不要）を見るには:\n' +
      '  → http://localhost:8000/viewer/?data=sample.graph.json'
    );
    return;
  }
  GRAPH = data;
  GRAPH.nodes.forEach(n => { NODE_BY_ID[n.id] = n; });
  CHAP_ORDER = [...new Set(GRAPH.nodes.map(n => n.chapter).filter(Boolean))];
  buildAdjacency();
  buildControls();
  buildGraph();
  document.getElementById('stats').textContent =
    `${data.stats.n_nodes} blocks · ${data.stats.n_edges} edges · ` +
    `${data.stats.n_annotated_space} space-tagged`;
}

function showError(msg) {
  const el = document.getElementById('error');
  el.hidden = false;
  el.textContent = msg;
}

// 描画される辺（dangling 除去後）から隣接リストを作る
function buildAdjacency() {
  GRAPH.nodes.forEach(n => { UP[n.id] = new Set(); DOWN[n.id] = new Set(); });
  GRAPH.edges.forEach(e => {
    if (!NODE_BY_ID[e.to] || !NODE_BY_ID[e.from]) return;
    UP[e.from].add(e.to);     // from は to を使う → to は依存先
    DOWN[e.to].add(e.from);   // to は from に使われる → from は被依存
  });
}

function chapTint(ch) {
  const i = CHAP_ORDER.indexOf(ch);
  return CHAP_TINT[(i < 0 ? 0 : i) % CHAP_TINT.length];
}
function chapId(ch) { return 'chap::' + ch; }

// ---------------------------------------------------------------------------
// コントロール構築
// ---------------------------------------------------------------------------
function buildControls() {
  const sf = document.getElementById('space-filter');
  Object.keys(GRAPH.spaces).forEach(key => {
    const o = document.createElement('option');
    o.value = key;
    o.textContent = `${GRAPH.spaces[key].label}（${key}）まで`;
    sf.appendChild(o);
  });
  sf.addEventListener('change', applyFilters);

  const ef = document.getElementById('env-filters');
  Object.keys(ENV_LABEL).forEach(env => {
    if (!GRAPH.nodes.some(n => n.env === env)) return;
    const lab = document.createElement('label');
    lab.innerHTML =
      `<input type="checkbox" value="${env}" checked> ` +
      `<span style="color:${ENV_COLOR[env]};font-weight:700">${ENV_LABEL[env]}</span>`;
    lab.querySelector('input').addEventListener('change', applyFilters);
    ef.appendChild(lab);
  });

  const cf = document.getElementById('chapter-filters');
  CHAP_ORDER.forEach(ch => {
    const lab = document.createElement('label');
    lab.innerHTML =
      `<input type="checkbox" checked> ` +
      `<span class="chap-swatch" style="background:${chapTint(ch)}"></span>${stripMath(ch)}`;
    lab.querySelector('input').dataset.chapter = ch;
    lab.querySelector('input').addEventListener('change', applyFilters);
    cf.appendChild(lab);
  });

  // 現在のデータセットのリンクを active 表示
  const isSample = /sample\.graph\.json/.test(DATA_SRC);
  document.querySelectorAll('.dataset a').forEach(a => {
    const sample = a.getAttribute('href').includes('data=');
    a.classList.toggle('active', sample === isSample);
  });

  document.getElementById('show-uses').addEventListener('change', applyFilters);
  document.getElementById('show-proof').addEventListener('change', applyFilters);
  document.getElementById('group-chapter').addEventListener('change', rebuild);
  document.getElementById('label-mode').addEventListener('change', refreshLabels);
  document.getElementById('focus-scope').addEventListener('change', () => {
    if (selectedId) applyFocus(selectedId); else clearFocus();
  });
  document.getElementById('layout-select').addEventListener('change', () => runLayout(true));
  document.getElementById('fit-btn').addEventListener('click', clearFocus);
}

// ---------------------------------------------------------------------------
// グラフ構築
// ---------------------------------------------------------------------------
function grouped() { return document.getElementById('group-chapter').checked; }

function buildGraph() {
  const elements = [];
  if (grouped()) {
    CHAP_ORDER.forEach(ch => {
      elements.push({ data: {
        id: chapId(ch), label: stripMath(ch), isParent: true, tint: chapTint(ch),
      }, classes: 'chapter' });
    });
  }
  GRAPH.nodes.forEach(n => {
    elements.push({ data: {
      id: n.id, label: `${ENV_LABEL[n.env]}. ${stripMath(n.title)}`,
      env: n.env, chapter: n.chapter, spaces: n.spaces,
      parent: grouped() && n.chapter ? chapId(n.chapter) : undefined,
    }, classes: 'leaf' });
  });
  GRAPH.edges.forEach((e, i) => {
    if (!NODE_BY_ID[e.to]) return;
    elements.push({ data: {
      id: 'e' + i, source: e.from, target: e.to,
      kind: e.kind, route: e.route || '',
    }});
  });

  cy = cytoscape({
    container: document.getElementById('cy'),
    elements,
    wheelSensitivity: 0.2,
    style: [
      { selector: 'node.leaf', style: {
        'background-color': ele => ENV_COLOR[ele.data('env')] || '#888',
        'label': 'data(label)', 'font-size': '10px', 'color': '#0f172a',
        'text-wrap': 'wrap', 'text-max-width': '130px',
        'text-valign': 'bottom', 'text-margin-y': 4,
        'text-background-color': '#ffffff', 'text-background-opacity': 0.82,
        'text-background-padding': '2px', 'text-background-shape': 'roundrectangle',
        'text-opacity': 0,                       // 既定は非表示（refreshLabels で制御）
        'width': 22, 'height': 22, 'border-width': 0,
        'transition-property': 'opacity, text-opacity', 'transition-duration': '120ms',
      }},
      { selector: 'node.leaf.lbl', style: { 'text-opacity': 1 }},
      // 章コンテナ
      { selector: 'node.chapter', style: {
        'background-color': 'data(tint)', 'background-opacity': 0.45,
        'border-width': 1, 'border-color': '#cbd5e1', 'border-style': 'dashed',
        'shape': 'roundrectangle', 'padding': '22px',
        'label': 'data(label)', 'text-valign': 'top', 'text-halign': 'center',
        'font-size': '13px', 'font-weight': 'bold', 'color': '#475569',
        'text-margin-y': 2, 'text-opacity': 1,
      }},
      { selector: 'node.chapter.collapsed-empty', style: { 'display': 'none' }},
      { selector: 'node.leaf.dim', style: { 'opacity': 0.12 }},
      { selector: 'node.leaf.sel', style: {
        'border-width': 4, 'border-color': '#0f172a', 'width': 28, 'height': 28 }},
      { selector: 'node.leaf.hl', style: { 'border-width': 3, 'border-color': '#0f172a' }},
      { selector: 'node.leaf.support', style: {
        'border-width': 3, 'border-color': '#16a34a', 'opacity': 1 }},
      { selector: 'node.leaf.faded', style: { 'opacity': 0.06 }},
      { selector: 'edge.faded', style: { 'opacity': 0.025 }},
      { selector: 'edge', style: {
        'width': 1.2, 'line-color': '#c4c4cc', 'target-arrow-color': '#c4c4cc',
        'target-arrow-shape': 'triangle', 'arrow-scale': 0.8,
        'curve-style': 'bezier', 'opacity': 0.4,
      }},
      { selector: 'edge[kind = "proof"]', style: { 'line-style': 'dashed' }},
      { selector: 'edge.dim', style: { 'opacity': 0.03 }},
      // フォーカス時の方向別の色: 依存先＝青、被依存＝紫
      { selector: 'edge.up', style: {
        'line-color': '#2563eb', 'target-arrow-color': '#2563eb', 'width': 2.4, 'opacity': 0.95 }},
      { selector: 'edge.down', style: {
        'line-color': '#7c3aed', 'target-arrow-color': '#7c3aed', 'width': 2.4, 'opacity': 0.95 }},
      { selector: 'edge.hl', style: {
        'line-color': '#0f172a', 'target-arrow-color': '#0f172a', 'width': 2.6, 'opacity': 1 }},
      { selector: 'edge.route-on', style: {
        'line-color': '#dc2626', 'target-arrow-color': '#dc2626', 'width': 2.8, 'opacity': 1 }},
    ],
  });

  cy.on('tap', 'node.leaf', evt => selectNode(evt.target.id()));
  cy.on('tap', evt => { if (evt.target === cy) clearSelection(); });
  cy.on('mouseover', 'node.leaf', evt => { evt.target.addClass('hov'); refreshLabels(); });
  cy.on('mouseout', 'node.leaf', evt => { evt.target.removeClass('hov'); refreshLabels(); });
  let zt = null;
  cy.on('zoom', () => { if (zt) return; zt = requestAnimationFrame(() => { zt = null; refreshLabels(); }); });

  runLayout();
  applyFilters();
}

// グループ化トグル時に作り直す
function rebuild() {
  const z = cy ? cy.zoom() : null;
  if (cy) cy.destroy();
  selectedId = null; focusSet = null;
  document.getElementById('detail-empty').hidden = false;
  document.getElementById('detail-body').hidden = true;
  buildGraph();
}

function runLayout(refit) {
  const name = document.getElementById('layout-select').value;
  const eles = focusSet ? cy.elements(':visible') : cy.elements();
  const opts = { name, animate: false, fit: true, padding: 36 };
  if (name === 'dagre') {
    opts.rankDir = 'BT'; opts.nodeSep = 26; opts.rankSep = 70;
    opts.spacingFactor = 1.0;
  }
  if (name === 'breadthfirst') { opts.directed = true; opts.spacingFactor = 1.2; }
  if (name === 'cose') { opts.idealEdgeLength = 90; opts.nodeRepulsion = 12000; }
  eles.layout(opts).run();
  refreshLabels();
}

// ---------------------------------------------------------------------------
// ラベルの出し分け（俯瞰では消し、ズーム / hover / 選択 / フォーカスで出す）
// ---------------------------------------------------------------------------
function refreshLabels() {
  if (!cy) return;
  const mode = document.getElementById('label-mode').value;  // auto | always
  const z = cy.zoom();
  const focusing = !!focusSet;
  cy.batch(() => {
    cy.nodes('.leaf').forEach(n => {
      if (n.style('display') === 'none') { n.removeClass('lbl'); return; }
      const show = mode === 'always' || focusing || z >= LABEL_ZOOM
        || n.hasClass('sel') || n.hasClass('hl') || n.hasClass('hov');
      n.toggleClass('lbl', show);
    });
  });
}

// ---------------------------------------------------------------------------
// フィルタ（env / 章 / 辺 / 空間）＋ フォーカス制限
// ---------------------------------------------------------------------------
function applyFilters() {
  const envOn = new Set([...document.querySelectorAll('#env-filters input:checked')].map(i => i.value));
  const chOn = new Set([...document.querySelectorAll('#chapter-filters input:checked')].map(i => i.dataset.chapter));
  const showUses = document.getElementById('show-uses').checked;
  const showProof = document.getElementById('show-proof').checked;
  const spaceKey = document.getElementById('space-filter').value;
  const provided = spaceKey ? new Set(GRAPH.spaces[spaceKey].closure) : null;

  cy.batch(() => {
    cy.nodes('.leaf').forEach(n => {
      const d = NODE_BY_ID[n.id()];
      let visible = envOn.has(d.env) && chOn.has(d.chapter);
      if (focusSet && !focusSet.has(n.id())) visible = false;
      let holds = true;
      if (provided && d.spaces.length) holds = d.spaces.every(s => provided.has(s));
      n.style('display', visible ? 'element' : 'none');
      n.toggleClass('dim', visible && provided && !holds);
    });
    cy.edges().forEach(e => {
      const okKind = (e.data('kind') === 'uses' && showUses) ||
                     (e.data('kind') === 'proof' && showProof);
      const ends = e.source().style('display') === 'element' &&
                   e.target().style('display') === 'element';
      e.style('display', (okKind && ends) ? 'element' : 'none');
    });
    // 空の章コンテナは隠す
    cy.nodes('.chapter').forEach(p => {
      const anyVisible = p.children().some(c => c.style('display') === 'element');
      p.style('display', anyVisible ? 'element' : 'none');
    });
  });
  refreshLabels();
}

// ---------------------------------------------------------------------------
// フォーカス：選択ノードの依存近傍だけに絞る
// ---------------------------------------------------------------------------
function closure(id, adj, transitive) {
  const out = new Set();
  const stack = [...adj[id]];
  while (stack.length) {
    const x = stack.pop();
    if (out.has(x)) continue;
    out.add(x);
    if (transitive) adj[x].forEach(y => stack.push(y));
  }
  return out;
}

function applyFocus(id) {
  const scope = document.getElementById('focus-scope').value;  // off | direct | transitive
  if (scope === 'off') { clearFocus(); return; }
  const trans = scope === 'transitive';
  const up = closure(id, UP, trans);
  const down = closure(id, DOWN, trans);
  focusSet = new Set([id, ...up, ...down]);
  applyFilters();
  // 方向で辺を色分け（依存先＝青 up、被依存＝紫 down）
  cy.batch(() => {
    cy.edges().removeClass('up down');
    cy.edges(':visible').forEach(e => {
      const s = e.source().id(), t = e.target().id();
      if (focusSet.has(s) && focusSet.has(t)) {
        // s が t を使う。t が id 側（上流）なら up、s が id 側（下流）なら down
        if (up.has(t) || t === id) e.addClass('up');
        else if (down.has(s) || s === id) e.addClass('down');
      }
    });
  });
  runLayout(true);
  const n = NODE_BY_ID[id];
  document.getElementById('stats').textContent =
    `フォーカス: ${ENV_LABEL[n.env]}. ${stripMath(n.title)} — 依存 ${up.size} / 被依存 ${down.size}` +
    `（${trans ? '推移閉包' : '直接'}）`;
}

function clearFocus() {
  if (!cy) return;
  if (focusSet) {
    focusSet = null;
    cy.edges().removeClass('up down');
    applyFilters();
    runLayout(true);
  } else {
    cy.fit(null, 36);
  }
  document.getElementById('stats').textContent =
    `${GRAPH.stats.n_nodes} blocks · ${GRAPH.stats.n_edges} edges · ` +
    `${GRAPH.stats.n_annotated_space} space-tagged`;
}

// ---------------------------------------------------------------------------
// 選択 & 詳細
// ---------------------------------------------------------------------------
function selectNode(id) {
  clearSelection(false);
  const d = NODE_BY_ID[id];
  if (!d) return;
  selectedId = id;
  const node = cy.getElementById(id);
  node.addClass('sel');
  node.outgoers('edge').addClass('hl');
  node.outgoers('node').addClass('hl');
  node.incomers('edge').addClass('hl');
  node.incomers('node').addClass('hl');

  renderDetail(d);
  const routes = routesOf(id);
  const defaultRoute = activeRouteByNode[id] || (routes[0] && routes[0].route);
  highlightRoute(d, defaultRoute);

  if (document.getElementById('focus-scope').value !== 'off') applyFocus(id);
  refreshLabels();
}

function clearSelection(clearPanel = true) {
  selectedId = null;
  cy.elements().removeClass('sel hl route-on support faded');
  if (clearPanel) {
    document.getElementById('detail-empty').hidden = false;
    document.getElementById('detail-body').hidden = true;
  }
  refreshLabels();
}

function routesOf(id) { return GRAPH.routes.filter(r => r.node === id); }

function renderDetail(d) {
  document.getElementById('detail-empty').hidden = true;
  const body = document.getElementById('detail-body');
  body.hidden = false;

  const envEl = document.getElementById('d-env');
  envEl.className = 'badge ' + d.env;
  envEl.textContent = ENV_LABEL[d.env];

  document.getElementById('d-title').innerHTML = d.title;
  const loc = [d.chapter, d.section, d.subsection].filter(Boolean).map(stripMath).join(' › ');
  document.getElementById('d-loc').textContent = loc + '  ·  ' + d.id;

  document.getElementById('d-spaces').innerHTML = d.spaces.length
    ? d.spaces.map(s => `<span class="chip">${GRAPH.spaces[s] ? GRAPH.spaces[s].label : s}</span>`).join('')
    : '<span class="muted">空間タグなし</span>';

  // フォーカスボタン
  const fwrap = document.getElementById('d-focus');
  fwrap.innerHTML =
    `<button id="d-focus-direct">前後に絞る（直接）</button>` +
    `<button id="d-focus-trans">前後に絞る（推移）</button>`;
  document.getElementById('d-focus-direct').onclick = () => {
    document.getElementById('focus-scope').value = 'direct'; applyFocus(d.id);
  };
  document.getElementById('d-focus-trans').onclick = () => {
    document.getElementById('focus-scope').value = 'transitive'; applyFocus(d.id);
  };

  const routes = routesOf(d.id);
  const rwrap = document.getElementById('d-routes-wrap');
  const rdiv = document.getElementById('d-routes');
  rwrap.hidden = false;
  if (routes.length === 0) {
    rdiv.innerHTML = '<span class="muted">証明ルートなし（定義・公理的ブロック）</span>';
  } else {
    rdiv.innerHTML = '';
    routes.forEach(r => {
      const div = document.createElement('div');
      div.className = 'route';
      const name = r.route === '_auto' ? '自動抽出' : `ルート ${r.route}`;
      const deps = r.deps.length
        ? '<ul>' + r.deps.map(depLi).join('') + '</ul>'
        : '<span class="muted">（外部依存のみ／依存なし）</span>';
      div.innerHTML =
        `<div class="route-head">${name} ` +
        `<button data-route="${r.route}">辺を強調</button> ` +
        `<button data-support="${r.route}">支持集合</button></div>${deps}`;
      div.querySelector('[data-route]').addEventListener('click', () => {
        activeRouteByNode[d.id] = r.route; highlightRoute(d, r.route);
      });
      div.querySelector('[data-support]').addEventListener('click', () => {
        activeRouteByNode[d.id] = r.route; highlightSupport(d.id, r.route);
      });
      rdiv.appendChild(div);
    });
  }

  const allDeps = new Set();
  (d.uses || []).forEach(x => allDeps.add(x));
  routes.forEach(r => r.deps.forEach(x => allDeps.add(x)));
  GRAPH.edges.filter(e => e.from === d.id && e.kind === 'uses').forEach(e => allDeps.add(e.to));
  document.getElementById('d-deps').innerHTML =
    [...allDeps].map(depLi).join('') || '<li class="muted" style="cursor:default">なし</li>';

  const rdeps = GRAPH.edges.filter(e => e.to === d.id).map(e => e.from);
  document.getElementById('d-rdeps').innerHTML =
    [...new Set(rdeps)].map(depLi).join('') || '<li class="muted" style="cursor:default">なし</li>';

  if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([body]);
}

function depLi(id) {
  const t = NODE_BY_ID[id];
  if (!t) return `<li class="missing">${id}（未定義）</li>`;
  return `<li data-goto="${id}" onclick="window.__goto('${id}')">${ENV_LABEL[t.env]}. ${stripMath(t.title)}</li>`;
}
window.__goto = id => {
  if (!cy.getElementById(id).nonempty()) return;
  if (focusSet && !focusSet.has(id)) clearFocus();
  cy.animate({ center: { eles: cy.getElementById(id) }, zoom: 1.3 }, { duration: 300 });
  selectNode(id);
};

function highlightRoute(d, routeName) {
  cy.edges().removeClass('route-on');
  if (!routeName) return;
  const deps = (routesOf(d.id).find(r => r.route === routeName) || {}).deps || [];
  cy.edges().forEach(e => {
    if (e.data('kind') === 'proof' && e.source().id() === d.id &&
        e.data('route') === routeName && deps.includes(e.target().id())) {
      e.addClass('route-on');
    }
  });
  document.querySelectorAll('#d-routes .route').forEach(div => {
    const btn = div.querySelector('button');
    div.classList.toggle('active', btn && btn.dataset.route === routeName);
  });
}

function depsFor(id, route) {
  const n = NODE_BY_ID[id];
  if (!n) return [];
  const deps = new Set();
  GRAPH.edges.filter(e => e.from === id && e.kind === 'uses').forEach(e => deps.add(e.to));
  const routes = routesOf(id);
  if (routes.length) {
    let chosen = route != null ? routes.find(r => r.route === route) : null;
    if (!chosen) chosen = routes[0];
    chosen.deps.forEach(x => deps.add(x));
  }
  return [...deps];
}

function computeSupport(id, route) {
  const support = new Set();
  const stack = depsFor(id, route);
  while (stack.length) {
    const nid = stack.pop();
    if (support.has(nid) || !NODE_BY_ID[nid]) continue;
    support.add(nid);
    depsFor(nid, null).forEach(x => stack.push(x));
  }
  support.delete(id);
  return support;
}

function highlightSupport(id, route) {
  const support = computeSupport(id, route);
  const inSet = nid => nid === id || support.has(nid);
  cy.batch(() => {
    cy.nodes('.leaf').forEach(n => {
      const s = inSet(n.id());
      n.toggleClass('support', s);
      n.toggleClass('faded', !s);
    });
    cy.edges().removeClass('route-on');
    cy.edges().forEach(e => {
      e.toggleClass('faded', !(inSet(e.source().id()) && inSet(e.target().id())));
    });
  });
  refreshLabels();
  const label = route === '_auto' ? '自動ルート' : `ルート ${route}`;
  document.getElementById('stats').textContent =
    `支持集合（${stripMath(NODE_BY_ID[id].title)} / ${label}）: ${support.size} ブロック`;
}

// ---------------------------------------------------------------------------
// ユーティリティ
// ---------------------------------------------------------------------------
function stripMath(s) {
  if (!s) return '';
  return s.replace(/\$([^$]*)\$/g, '$1')
          .replace(/\\[a-zA-Z]+/g, '').replace(/[{}]/g, '').trim();
}

load();
