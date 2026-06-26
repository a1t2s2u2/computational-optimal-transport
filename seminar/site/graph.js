'use strict';

const ENV_COLOR = {};
const ENV_LABEL = {};
const TINT = ['#dbeafe', '#dcfce7', '#fef3c7', '#fae8ff',
              '#ffedd5', '#cffafe', '#fee2e2', '#ede9fe', '#f1f5f9', '#fce7f3'];

let cy = null;
let GRAPH = null;
let NODE_BY_ID = {};
let selectedId = null;
let UP = {}, DOWN = {};

function readCssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function initColors() {
  ENV_COLOR.definition = readCssVar('--teal') || '#0d9488';
  ENV_COLOR.theorem = readCssVar('--indigo') || '#4338ca';
  ENV_COLOR.proposition = readCssVar('--orange') || '#ea580c';
  ENV_COLOR.algorithm = readCssVar('--amber') || '#d97706';
  ENV_COLOR.remark = readCssVar('--muted') || '#78716c';
  ENV_COLOR.example = readCssVar('--wine') || '#be123c';

  ENV_LABEL.definition = 'Def';
  ENV_LABEL.theorem = 'Thm';
  ENV_LABEL.proposition = 'Prop';
  ENV_LABEL.algorithm = 'Algo';
  ENV_LABEL.remark = 'Rem';
  ENV_LABEL.example = 'Ex';
}

async function load() {
  initColors();
  let data;
  try {
    const res = await fetch('graph-data.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText);
    data = await res.json();
  } catch (e) {
    document.getElementById('graph-detail').innerHTML =
      `<p class="graph-detail__empty">データを読み込めません: ${e.message}</p>`;
    return;
  }
  GRAPH = data;
  GRAPH.nodes.forEach(n => { NODE_BY_ID[n.id] = n; });
  buildAdjacency();
  buildChapterFilter();
  buildGraph();
}

function buildAdjacency() {
  GRAPH.nodes.forEach(n => { UP[n.id] = new Set(); DOWN[n.id] = new Set(); });
  GRAPH.edges.forEach(e => {
    if (!NODE_BY_ID[e.to] || !NODE_BY_ID[e.from]) return;
    UP[e.from].add(e.to);
    DOWN[e.to].add(e.from);
  });
}

function buildChapterFilter() {
  const chapters = [...new Set(GRAPH.nodes.map(n => n.chapter))];
  const sel = document.getElementById('chapter-filter');
  chapters.forEach(ch => {
    const opt = document.createElement('option');
    opt.value = ch;
    opt.textContent = ch;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', applyFilters);
  document.getElementById('type-filter').addEventListener('change', applyFilters);
  document.getElementById('hide-isolated').addEventListener('change', applyFilters);
  document.getElementById('fit-btn').addEventListener('click', () => {
    clearSelection();
    cy.elements().removeClass('dimmed');
    cy.fit(undefined, 40);
  });
}

function nodeLabel(n) {
  const prefix = ENV_LABEL[n.type] || n.type;
  const title = n.name || n.title || '';
  const short = title.length > 24 ? title.slice(0, 22) + '…' : title;
  return `${prefix}. ${short}`;
}

function buildGraph() {
  const elements = [];
  const chapters = [...new Set(GRAPH.nodes.map(n => n.chapter))];
  const connected = new Set();
  GRAPH.edges.forEach(e => { connected.add(e.from); connected.add(e.to); });

  GRAPH.nodes.forEach(n => {
    const isIsolated = !connected.has(n.id);
    const chIdx = chapters.indexOf(n.chapter);
    elements.push({
      data: {
        id: n.id,
        label: nodeLabel(n),
        env: n.type,
        chapter: n.chapter,
        chapterTint: TINT[chIdx % TINT.length],
        isolated: isIsolated,
      },
      classes: isIsolated ? 'leaf isolated' : 'leaf'
    });
  });

  GRAPH.edges.forEach((e, i) => {
    if (!NODE_BY_ID[e.to] || !NODE_BY_ID[e.from]) return;
    elements.push({
      data: { id: 'e' + i, source: e.from, target: e.to }
    });
  });

  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const bgColor = readCssVar('--bg') || (isDark ? '#0c0e14' : '#faf9f7');
  const lineColor = readCssVar('--line') || (isDark ? '#2a2f3a' : '#e7e5e4');
  const inkColor = readCssVar('--ink') || (isDark ? '#e4e6ea' : '#1c1917');
  const mutedColor = readCssVar('--muted') || '#78716c';

  cy = cytoscape({
    container: document.getElementById('cy'),
    elements,
    wheelSensitivity: 0.3,
    minZoom: 0.15,
    maxZoom: 3,
    style: [
      {
        selector: 'node.leaf',
        style: {
          'shape': 'round-rectangle',
          'width': 'label',
          'height': 'label',
          'padding': '12px',
          'background-color': function(ele) {
            return ENV_COLOR[ele.data('env')] || '#666';
          },
          'background-opacity': 0.12,
          'border-width': 2,
          'border-color': function(ele) {
            return ENV_COLOR[ele.data('env')] || '#666';
          },
          'label': 'data(label)',
          'font-family': '"Noto Sans JP", system-ui, sans-serif',
          'font-size': 13,
          'font-weight': 600,
          'color': inkColor,
          'text-valign': 'center',
          'text-halign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': 160,
          'transition-property': 'opacity, border-width',
          'transition-duration': 200,
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 1.5,
          'line-color': lineColor,
          'target-arrow-color': lineColor,
          'target-arrow-shape': 'triangle',
          'arrow-scale': 0.8,
          'curve-style': 'bezier',
          'opacity': 0.5,
          'transition-property': 'opacity, line-color',
          'transition-duration': 200,
        }
      },
      {
        selector: '.dimmed',
        style: {
          'opacity': 0.08,
        }
      },
      {
        selector: '.highlighted',
        style: {
          'opacity': 1,
          'border-width': 3,
          'z-index': 10,
        }
      },
      {
        selector: 'edge.highlighted',
        style: {
          'opacity': 1,
          'width': 2.5,
          'line-color': function(ele) {
            const src = NODE_BY_ID[ele.data('source')];
            return src ? (ENV_COLOR[src.type] || '#666') : '#666';
          },
          'target-arrow-color': function(ele) {
            const src = NODE_BY_ID[ele.data('source')];
            return src ? (ENV_COLOR[src.type] || '#666') : '#666';
          },
        }
      },
      {
        selector: 'node.selected-node',
        style: {
          'border-width': 4,
          'border-color': readCssVar('--teal') || '#0d9488',
          'background-opacity': 0.25,
          'z-index': 20,
        }
      },
      {
        selector: 'node.isolated',
        style: {
          'opacity': 0.4,
          'border-style': 'dashed',
          'border-width': 1.5,
        }
      }
    ],
    layout: {
      name: 'dagre',
      rankDir: 'TB',
      nodeSep: 35,
      rankSep: 55,
      edgeSep: 15,
      padding: 40,
    },
  });

  cy.on('tap', 'node.leaf', (evt) => {
    selectNode(evt.target.id());
  });

  cy.on('tap', (evt) => {
    if (evt.target === cy) clearSelection();
  });
}

function selectNode(id) {
  const node = NODE_BY_ID[id];
  if (!node) return;
  selectedId = id;

  cy.elements().removeClass('highlighted selected-node dimmed');

  const cyNode = cy.getElementById(id);
  const neighborhood = cyNode.neighborhood().add(cyNode);

  cy.elements().not(neighborhood).addClass('dimmed');
  neighborhood.addClass('highlighted');
  cyNode.addClass('selected-node');

  showDetail(node);
}

function clearSelection() {
  selectedId = null;
  cy.elements().removeClass('highlighted selected-node dimmed');
  document.getElementById('graph-detail').innerHTML =
    '<p class="graph-detail__empty">ノードをクリックすると<br>詳細が表示されます</p>';
}

function showDetail(node) {
  const detail = document.getElementById('graph-detail');
  const typeLabels = {
    definition: '定義', theorem: '定理', proposition: '命題',
    remark: '注意', example: '例', algorithm: '算法'
  };
  const typeColor = ENV_COLOR[node.type] || 'var(--muted)';
  const chapterFiles = window.__chapterFiles || {};
  const href = chapterFiles[node.chapter]
    ? `${chapterFiles[node.chapter]}#${node.id}`
    : '#';

  const upList = [...(UP[node.id] || [])].map(id => NODE_BY_ID[id]).filter(Boolean);
  const downList = [...(DOWN[node.id] || [])].map(id => NODE_BY_ID[id]).filter(Boolean);
  const neighborsHtml = [];
  if (upList.length > 0) {
    neighborsHtml.push(`<strong>参照先:</strong> ${upList.map(n => n.name || n.title).join(', ')}`);
  }
  if (downList.length > 0) {
    neighborsHtml.push(`<strong>参照元:</strong> ${downList.map(n => n.name || n.title).join(', ')}`);
  }

  detail.innerHTML = `
    <div class="graph-detail__card">
      <div class="graph-detail__type" style="color:${typeColor}">${typeLabels[node.type] || node.type}</div>
      <div class="graph-detail__content">${node.html}</div>
      <a class="graph-detail__link" href="${href}">本文で見る &rarr;</a>
      ${neighborsHtml.length > 0 ? `<div class="graph-detail__neighbors">${neighborsHtml.join('<br>')}</div>` : ''}
    </div>`;

  if (window.MathJax?.typesetPromise) {
    MathJax.typesetPromise([detail]);
  }
}

function applyFilters() {
  const chapter = document.getElementById('chapter-filter').value;
  const type = document.getElementById('type-filter').value;
  const hideIsolated = document.getElementById('hide-isolated').checked;

  cy.nodes('.leaf').forEach(node => {
    const matchChapter = chapter === 'all' || node.data('chapter') === chapter;
    const matchType = type === 'all' || node.data('env') === type;
    const matchIsolated = !hideIsolated || !node.data('isolated');
    node.style('display', (matchChapter && matchType && matchIsolated) ? 'element' : 'none');
  });

  cy.edges().forEach(edge => {
    const src = cy.getElementById(edge.data('source'));
    const tgt = cy.getElementById(edge.data('target'));
    edge.style('display', (src.style('display') !== 'none' && tgt.style('display') !== 'none') ? 'element' : 'none');
  });

  cy.fit(cy.elements().filter(e => e.style('display') !== 'none'), 40);
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') clearSelection();
});

window.addEventListener('DOMContentLoaded', load);
