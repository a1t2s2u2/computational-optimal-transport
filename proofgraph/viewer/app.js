'use strict';

const ENV_COLOR = {
  definition: '#2563eb', proposition: '#ea7317', theorem: '#dc2626',
  claim: '#16a34a', remark: '#ca8a04', example: '#6b7280',
};
const ENV_LABEL = {
  definition: 'Def', proposition: 'Prop', theorem: 'Thm',
  claim: 'Clm', remark: 'Rem', example: 'Ex',
};

let GRAPH = null;
let cy = null;
let NODE_BY_ID = {};
let activeRouteByNode = {};   // node id -> route name currently highlighted

// ---------------------------------------------------------------------------
// 読み込み
// ---------------------------------------------------------------------------
async function load() {
  let data;
  try {
    const res = await fetch('../out/graph.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    data = await res.json();
  } catch (e) {
    showError(
      'graph.json を読み込めませんでした（' + e.message + '）。\n\n' +
      'まず抽出器を実行し、ローカルサーバ経由で開いてください：\n\n' +
      '  python3 proofgraph/extractor.py\n' +
      '  cd proofgraph && python3 -m http.server 8000\n' +
      '  → http://localhost:8000/viewer/'
    );
    return;
  }
  GRAPH = data;
  GRAPH.nodes.forEach(n => { NODE_BY_ID[n.id] = n; });
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

// ---------------------------------------------------------------------------
// コントロール構築
// ---------------------------------------------------------------------------
function buildControls() {
  // 空間フィルタ
  const sf = document.getElementById('space-filter');
  Object.keys(GRAPH.spaces).forEach(key => {
    const o = document.createElement('option');
    o.value = key;
    o.textContent = `${GRAPH.spaces[key].label}（${key}）まで`;
    sf.appendChild(o);
  });
  sf.addEventListener('change', applyFilters);

  // env フィルタ
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

  // 章フィルタ
  const chapters = [...new Set(GRAPH.nodes.map(n => n.chapter).filter(Boolean))];
  const cf = document.getElementById('chapter-filters');
  chapters.forEach(ch => {
    const lab = document.createElement('label');
    lab.innerHTML = `<input type="checkbox" value="${cssEscape(ch)}" checked> ${stripMath(ch)}`;
    lab.querySelector('input').dataset.chapter = ch;
    lab.querySelector('input').addEventListener('change', applyFilters);
    cf.appendChild(lab);
  });

  document.getElementById('show-uses').addEventListener('change', applyFilters);
  document.getElementById('show-proof').addEventListener('change', applyFilters);
  document.getElementById('layout-select').addEventListener('change', runLayout);
  document.getElementById('fit-btn').addEventListener('click', () => cy.fit(null, 40));
}

// ---------------------------------------------------------------------------
// グラフ構築
// ---------------------------------------------------------------------------
function buildGraph() {
  const elements = [];
  GRAPH.nodes.forEach(n => {
    elements.push({ data: {
      id: n.id, label: `${ENV_LABEL[n.env]}. ${stripMath(n.title)}`,
      env: n.env, chapter: n.chapter, spaces: n.spaces,
    }});
  });
  GRAPH.edges.forEach((e, i) => {
    if (!NODE_BY_ID[e.to]) return;  // dangling は描かない
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
      { selector: 'node', style: {
        'background-color': ele => ENV_COLOR[ele.data('env')] || '#888',
        'label': 'data(label)', 'font-size': '9px', 'color': '#111',
        'text-wrap': 'wrap', 'text-max-width': '120px',
        'text-valign': 'bottom', 'text-margin-y': 3,
        'width': 16, 'height': 16, 'border-width': 0,
      }},
      { selector: 'node.dim', style: { 'opacity': 0.12 } },
      { selector: 'node.sel', style: {
        'border-width': 3, 'border-color': '#111827', 'width': 22, 'height': 22 }},
      { selector: 'node.hl', style: { 'border-width': 2, 'border-color': '#111827' }},
      { selector: 'node.support', style: {
        'border-width': 2, 'border-color': '#16a34a', 'opacity': 1 }},
      { selector: 'node.faded', style: { 'opacity': 0.08 }},
      { selector: 'edge.faded', style: { 'opacity': 0.03 }},
      { selector: 'edge', style: {
        'width': 1.2, 'line-color': '#b8b8c0', 'target-arrow-color': '#b8b8c0',
        'target-arrow-shape': 'triangle', 'arrow-scale': 0.7,
        'curve-style': 'bezier', 'opacity': 0.55,
      }},
      { selector: 'edge[kind = "proof"]', style: { 'line-style': 'dashed' }},
      { selector: 'edge.dim', style: { 'opacity': 0.04 }},
      { selector: 'edge.hl', style: {
        'line-color': '#111827', 'target-arrow-color': '#111827',
        'width': 2.4, 'opacity': 1 }},
      { selector: 'edge.route-on', style: {
        'line-color': '#dc2626', 'target-arrow-color': '#dc2626',
        'width': 2.6, 'opacity': 1 }},
    ],
  });

  cy.on('tap', 'node', evt => selectNode(evt.target.id()));
  cy.on('tap', evt => { if (evt.target === cy) clearSelection(); });

  runLayout();
  applyFilters();
}

function runLayout() {
  const name = document.getElementById('layout-select').value;
  const opts = { name, animate: false, fit: true, padding: 40 };
  if (name === 'dagre') { opts.rankDir = 'BT'; opts.nodeSep = 18; opts.rankSep = 55; }
  if (name === 'breadthfirst') { opts.directed = true; opts.spacingFactor = 1.1; }
  cy.layout(opts).run();
}

// ---------------------------------------------------------------------------
// フィルタ
// ---------------------------------------------------------------------------
function applyFilters() {
  const envOn = new Set([...document.querySelectorAll('#env-filters input:checked')].map(i => i.value));
  const chOn = new Set([...document.querySelectorAll('#chapter-filters input:checked')].map(i => i.dataset.chapter));
  const showUses = document.getElementById('show-uses').checked;
  const showProof = document.getElementById('show-proof').checked;
  const spaceKey = document.getElementById('space-filter').value;
  const provided = spaceKey ? new Set(GRAPH.spaces[spaceKey].closure) : null;

  cy.batch(() => {
    cy.nodes().forEach(n => {
      const d = NODE_BY_ID[n.id()];
      let visible = envOn.has(d.env) && chOn.has(d.chapter);
      // 空間フィルタ: 選んだ空間 X で成り立つ = node.spaces ⊆ closure(X)
      let holds = true;
      if (provided && d.spaces.length) {
        holds = d.spaces.every(s => provided.has(s));
      }
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
  });
}

// ---------------------------------------------------------------------------
// 選択 & 詳細
// ---------------------------------------------------------------------------
function selectNode(id) {
  clearSelection(false);
  const d = NODE_BY_ID[id];
  if (!d) return;
  cy.getElementById(id).addClass('sel');

  // 近傍ハイライト
  const node = cy.getElementById(id);
  node.outgoers('edge').addClass('hl');
  node.outgoers('node').addClass('hl');
  node.incomers('edge').addClass('hl');
  node.incomers('node').addClass('hl');

  renderDetail(d);
  const routes = routesOf(id);
  const defaultRoute = activeRouteByNode[id] || (routes[0] && routes[0].route);
  highlightRoute(d, defaultRoute);
}

function clearSelection(clearPanel = true) {
  cy.elements().removeClass('sel hl route-on support faded');
  if (clearPanel) {
    document.getElementById('detail-empty').hidden = false;
    document.getElementById('detail-body').hidden = true;
  }
}

function routesOf(id) {
  return GRAPH.routes.filter(r => r.node === id);
}

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
  document.getElementById('d-lean').innerHTML = d.lean
    ? `<span class="chip">Lean: ${d.lean}</span>` : '';

  // ルート
  const routes = routesOf(d.id);
  const rwrap = document.getElementById('d-routes-wrap');
  const rdiv = document.getElementById('d-routes');
  if (routes.length === 0) {
    rwrap.hidden = false;
    rdiv.innerHTML = '<span class="muted">証明ルートなし（定義・公理的ブロック）</span>';
  } else {
    rwrap.hidden = false;
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
        activeRouteByNode[d.id] = r.route;
        highlightRoute(d, r.route);
      });
      div.querySelector('[data-support]').addEventListener('click', () => {
        activeRouteByNode[d.id] = r.route;
        highlightSupport(d.id, r.route);
      });
      rdiv.appendChild(div);
    });
  }

  // 依存 / 被依存
  const allDeps = new Set();
  (d.uses || []).forEach(x => allDeps.add(x));
  routes.forEach(r => r.deps.forEach(x => allDeps.add(x)));
  // uses は edges から
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
window.__goto = id => { cy.getElementById(id) && cy.animate({ center: { eles: cy.getElementById(id) }, zoom: 1.2 }, { duration: 300 }); selectNode(id); };

// ルート強調: そのルートの proof エッジを赤く
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
  // ルートボタンの active 表示
  document.querySelectorAll('#d-routes .route').forEach(div => {
    const btn = div.querySelector('button');
    div.classList.toggle('active', btn && btn.dataset.route === routeName);
  });
}

// 支持集合: node を route で支える全ブロックの推移閉包を計算して強調する。
// model.py DependencyGraph.support_set と同じ意味論（downstream は最初のルート）。
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
    cy.nodes().forEach(n => {
      const s = inSet(n.id());
      n.toggleClass('support', s);
      n.toggleClass('faded', !s);
    });
    cy.edges().removeClass('route-on');
    cy.edges().forEach(e => {
      e.toggleClass('faded', !(inSet(e.source().id()) && inSet(e.target().id())));
    });
  });
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
function cssEscape(s) { return s.replace(/"/g, '&quot;'); }

load();
