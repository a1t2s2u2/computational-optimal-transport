import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(__dirname, "..");
const contentDir = path.join(siteRoot, "content");

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

const allBlocks = [];
const usedBlockIds = new Set();
let currentChapterId = null;

function makeBlockId(type, rawName) {
  const prefixMap = { definition: "def", theorem: "thm", remark: "rem", example: "ex" };
  const prefix = prefixMap[type] || type;
  const slug = rawName
    .replace(/\\\(([^)]*)\\\)/g, (_, tex) =>
      tex.replace(/\\[a-zA-Z]+/g, "").replace(/[{}^_]/g, "").trim()
    )
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9぀-ゟ゠-ヿ一-鿿-]/g, "")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
  let id = `${prefix}-${slug || "unnamed"}`;
  if (usedBlockIds.has(id)) {
    let n = 2;
    while (usedBlockIds.has(`${id}-${n}`)) n += 1;
    id = `${id}-${n}`;
  }
  usedBlockIds.add(id);
  return id;
}

function parseFrontmatter(source, filePath) {
  const src = source.replaceAll("\r\n", "\n");
  if (!src.startsWith("---\n")) {
    throw new Error(`${filePath}: frontmatter is required`);
  }

  const end = src.indexOf("\n---\n", 4);
  if (end === -1) {
    throw new Error(`${filePath}: frontmatter is not closed`);
  }

  const raw = src.slice(4, end);
  const body = src.slice(end + 5);
  const data = {};
  for (const line of raw.split("\n")) {
    if (!line.trim()) continue;
    const index = line.indexOf(":");
    if (index === -1) {
      throw new Error(`${filePath}: invalid frontmatter line "${line}"`);
    }
    const key = line.slice(0, index).trim();
    const value = line.slice(index + 1).trim();
    data[key] = value;
  }
  return { data, body };
}

function renderInline(source) {
  const mathSpans = [];
  const shielded = source.replace(/\\\([^]*?\\\)/g, (m) => {
    mathSpans.push(m);
    return `\x00MATH${mathSpans.length - 1}\x00`;
  });

  let result = escapeHtml(shielded)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(
      /\[term:([^|\]]+)\|([a-z0-9-]+)\]/g,
      (_match, label, term) => `<button type="button" class="term" data-term="${term}">${label}</button>`
    )
    .replace(
      /\[ref:([^|\]]+?)(?:\|([^\]]+))?\]/g,
      (_match, first, second) => {
        const refName = second || first;
        const typeMatch = /^(Def|Clm|Thm|Prop|Rem|Ex):\s*(.+)$/.exec(first);
        const display = typeMatch ? typeMatch[1] : first;
        return `<button type="button" class="ref" data-ref="${refName}" title="${escapeHtml(first)}">${escapeHtml(display)}</button>`;
      }
    );

  return result.replace(/\x00MATH(\d+)\x00/g, (_, i) =>
    escapeHtml(mathSpans[parseInt(i)])
  );
}

function transportDiagramStyle() {
  return `
<style>
.tp-fig{position:relative;width:100%;max-width:460px;height:200px;margin:12px auto}
.tp-fig .node{position:absolute;width:76px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;border:1.5px solid}
.tp-fig .node--f{background:#dbeafe;border-color:#3b82f6}
.tp-fig .node--s{background:#ffedd5;border-color:#f97316}
.tp-fig .lbl{position:absolute;font-size:13px;white-space:nowrap}
.tp-fig .edge-lbl{position:absolute;font-size:12px;background:rgba(255,255,255,.85);padding:0 3px;white-space:nowrap}
.tp-fig svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
</style>`;
}

function transportCostDiagram() {
  return `
${transportDiagramStyle()}
<figure aria-label="輸送コストのネットワーク" style="margin:1em 0">
  <div class="tp-fig">
    <svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="ac" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto"><polygon points="0,0 7,2.5 0,5" fill="#555"/></marker></defs>
      <line x1="152" y1="50" x2="295" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#ac)"/>
      <line x1="152" y1="62" x2="295" y2="155" stroke="#555" stroke-width="1.5" marker-end="url(#ac)"/>
      <line x1="152" y1="155" x2="295" y2="62" stroke="#555" stroke-width="1.5" marker-end="url(#ac)"/>
      <line x1="152" y1="165" x2="295" y2="165" stroke="#555" stroke-width="1.5" marker-end="url(#ac)"/>
    </svg>
    <span class="lbl" style="left:90px;top:2px;font-weight:bold">工場</span>
    <span class="lbl" style="left:310px;top:2px;font-weight:bold">スーパー</span>
    <div class="node node--f" style="left:75px;top:30px">\\(x_1\\)</div>
    <div class="node node--f" style="left:75px;top:145px">\\(x_2\\)</div>
    <div class="node node--s" style="left:296px;top:30px">\\(y_1\\)</div>
    <div class="node node--s" style="left:296px;top:145px">\\(y_2\\)</div>
    <span class="lbl" style="right:395px;top:38px">\\(a_1\\!=\\!\\tfrac{2}{3}\\)</span>
    <span class="lbl" style="right:395px;top:153px">\\(a_2\\!=\\!\\tfrac{1}{3}\\)</span>
    <span class="lbl" style="left:380px;top:38px">\\(b_1\\!=\\!\\tfrac{1}{3}\\)</span>
    <span class="lbl" style="left:380px;top:153px">\\(b_2\\!=\\!\\tfrac{2}{3}\\)</span>
    <span class="edge-lbl" style="left:192px;top:28px;color:#333">\\(C_{1,1}\\!=\\!1\\)</span>
    <span class="edge-lbl" style="left:170px;top:98px;color:#333">\\(C_{1,2}\\!=\\!2\\)</span>
    <span class="edge-lbl" style="left:230px;top:88px;color:#333">\\(C_{2,1}\\!=\\!3\\)</span>
    <span class="edge-lbl" style="left:192px;top:170px;color:#333">\\(C_{2,2}\\!=\\!1\\)</span>
  </div>
  <figcaption style="text-align:center;font-size:0.9em;color:#666;margin-top:4px">
    輸送コストのネットワーク．各辺の数値は単位量あたりの輸送コスト \\(C_{i,j}\\) を表す．
  </figcaption>
</figure>`;
}

function transportOptimalDiagram() {
  return `
<figure aria-label="最適輸送計画" style="margin:1em 0">
  <div class="tp-fig">
    <svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="ao" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto"><polygon points="0,0 7,2.5 0,5" fill="#3b82f6"/></marker>
        <marker id="ag" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto"><polygon points="0,0 7,2.5 0,5" fill="#bbb"/></marker>
      </defs>
      <line x1="152" y1="50" x2="295" y2="50" stroke="#3b82f6" stroke-width="3" marker-end="url(#ao)"/>
      <line x1="152" y1="62" x2="295" y2="155" stroke="#3b82f6" stroke-width="3" marker-end="url(#ao)"/>
      <line x1="152" y1="155" x2="295" y2="62" stroke="#bbb" stroke-width="1" stroke-dasharray="6,4" marker-end="url(#ag)"/>
      <line x1="152" y1="165" x2="295" y2="165" stroke="#3b82f6" stroke-width="3" marker-end="url(#ao)"/>
    </svg>
    <span class="lbl" style="left:90px;top:2px;font-weight:bold">工場</span>
    <span class="lbl" style="left:310px;top:2px;font-weight:bold">スーパー</span>
    <div class="node node--f" style="left:75px;top:30px">\\(x_1\\)</div>
    <div class="node node--f" style="left:75px;top:145px">\\(x_2\\)</div>
    <div class="node node--s" style="left:296px;top:30px">\\(y_1\\)</div>
    <div class="node node--s" style="left:296px;top:145px">\\(y_2\\)</div>
    <span class="lbl" style="right:395px;top:38px">\\(a_1\\!=\\!\\tfrac{2}{3}\\)</span>
    <span class="lbl" style="right:395px;top:153px">\\(a_2\\!=\\!\\tfrac{1}{3}\\)</span>
    <span class="lbl" style="left:380px;top:38px">\\(b_1\\!=\\!\\tfrac{1}{3}\\)</span>
    <span class="lbl" style="left:380px;top:153px">\\(b_2\\!=\\!\\tfrac{2}{3}\\)</span>
    <span class="edge-lbl" style="left:175px;top:28px;color:#1e40af">\\(P_{1,1}^\\star\\!=\\!\\tfrac{1}{3}\\) <span style="font-size:11px;color:#666">\\((C\\!=\\!1)\\)</span></span>
    <span class="edge-lbl" style="left:153px;top:98px;color:#1e40af">\\(P_{1,2}^\\star\\!=\\!\\tfrac{1}{3}\\) <span style="font-size:11px;color:#666">\\((C\\!=\\!2)\\)</span></span>
    <span class="edge-lbl" style="left:218px;top:88px;color:#999">\\(P_{2,1}^\\star\\!=\\!0\\) <span style="font-size:11px;color:#888">\\((C\\!=\\!3)\\)</span></span>
    <span class="edge-lbl" style="left:175px;top:170px;color:#1e40af">\\(P_{2,2}^\\star\\!=\\!\\tfrac{1}{3}\\) <span style="font-size:11px;color:#666">\\((C\\!=\\!1)\\)</span></span>
  </div>
  <figcaption style="text-align:center;font-size:0.9em;color:#666;margin-top:4px">
    最適輸送計画 \\(\\mathbf{P}^\\star\\)．安価な経路 \\(x_1 \\to y_1\\)（コスト 1）と
    \\(x_2 \\to y_2\\)（コスト 1）を最大限利用し，残りを \\(x_1 \\to y_2\\)（コスト 2）で補う．
    高コストの \\(x_2 \\to y_1\\)（コスト 3）は使われない．
  </figcaption>
</figure>`;
}

function sinkhornDemo() {
  return `
<div class="demo" aria-label="Sinkhorn デモ">
  <div class="demo-head">
    <h3>\\(\\varepsilon\\) と輸送計画</h3>
    <label>
      <span>\\(\\varepsilon\\)</span>
      <input id="epsilon-slider" type="range" min="0.08" max="2.4" step="0.02" value="0.48" />
      <output id="epsilon-value">0.48</output>
    </label>
  </div>
  <div class="matrix-layout">
    <div>
      <h4>Cost \\(\\mathbf{C}\\)</h4>
      <div id="cost-matrix" class="matrix-grid"></div>
    </div>
    <div>
      <h4>Plan \\(\\mathbf{P}_{\\varepsilon}\\)</h4>
      <div id="plan-matrix" class="matrix-grid"></div>
    </div>
  </div>
</div>`;
}

function renderMarkdown(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const html = [];
  const stack = [];
  let paragraph = [];
  let listType = null;
  let currentBlock = null;

  const closeList = () => {
    if (!listType) return;
    html.push(`</${listType}>`);
    listType = null;
  };

  const flushParagraph = () => {
    if (paragraph.length === 0) return;
    html.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
    paragraph = [];
  };

  const openList = (type) => {
    if (listType === type) return;
    closeList();
    html.push(`<${type}>`);
    listType = type;
  };

  const closeContainer = () => {
    flushParagraph();
    closeList();
    const closing = stack.pop();
    if (!closing) {
      throw new Error("container close marker without an open container");
    }
    if (currentBlock && stack.length === currentBlock.depth) {
      if (currentBlock.name) {
        const contentHtml = html.slice(currentBlock.divIndex + 1).join("\n");
        allBlocks.push({
          id: currentBlock.id,
          name: currentBlock.name,
          type: currentBlock.type,
          title: currentBlock.fullTitle,
          chapter: currentChapterId,
          html: contentHtml
        });
      }
      currentBlock = null;
    }
    html.push(closing);
  };

  const openContainer = (spec) => {
    flushParagraph();
    closeList();

    if (spec === "grid two") {
      html.push('<div class="grid two">');
      stack.push("</div>");
      return;
    }
    if (spec === "compare") {
      html.push('<div class="compare">');
      stack.push("</div>");
      return;
    }
    if (spec === "column") {
      html.push("<div>");
      stack.push("</div>");
      return;
    }
    if (spec === "definition") {
      currentBlock = { type: "definition", divIndex: html.length, depth: stack.length };
      html.push('<div class="block block--def">');
      stack.push("</div>");
      return;
    }
    if (spec === "theorem") {
      currentBlock = { type: "theorem", divIndex: html.length, depth: stack.length };
      html.push('<div class="block block--thm">');
      stack.push("</div>");
      return;
    }
    if (spec === "algorithm") {
      currentBlock = { type: "algorithm", divIndex: html.length, depth: stack.length };
      html.push('<div class="block block--algo">');
      stack.push("</div>");
      return;
    }
    if (spec === "fact") {
      currentBlock = { type: "remark", divIndex: html.length, depth: stack.length };
      html.push('<aside class="margin-note">');
      stack.push("</aside>");
      return;
    }
    if (spec === "fact accent") {
      currentBlock = { type: "example", divIndex: html.length, depth: stack.length };
      html.push('<div class="example-band"><article class="example-band__inner">');
      stack.push("</article></div>");
      return;
    }
    if (spec.startsWith("details-embedded ")) {
      const title = spec.slice("details-embedded ".length);
      html.push(`<details class="proof"><summary>${renderInline(title)}</summary>`);
      stack.push("</details>");
      return;
    }
    if (spec.startsWith("details ")) {
      const title = spec.slice("details ".length);
      html.push(`<details class="fold"><summary>${renderInline(title)}</summary>`);
      stack.push("</details>");
      return;
    }
    if (spec === "demo sinkhorn") {
      html.push('<div class="demo-breakout">');
      html.push(sinkhornDemo());
      html.push('</div>');
      return;
    }
    if (spec === "demo transport-cost") {
      html.push(transportCostDiagram());
      return;
    }
    if (spec === "demo transport-optimal") {
      html.push(transportOptimalDiagram());
      return;
    }

    throw new Error(`unknown container "${spec}"`);
  };

  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    const trimmed = raw.trim();

    if (trimmed === "") {
      flushParagraph();
      closeList();
      continue;
    }

    if (trimmed.startsWith("```")) {
      flushParagraph();
      closeList();
      const language = trimmed.slice(3).trim();
      const code = [];
      i += 1;
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        code.push(lines[i]);
        i += 1;
      }
      if (i >= lines.length) {
        throw new Error("unclosed code fence (```) at EOF");
      }
      if (language === "mermaid") {
        html.push(`<div class="map-wrap"><pre class="mermaid">${escapeHtml(code.join("\n"))}</pre></div>`);
      } else {
        html.push(`<pre class="code-block"><code>${escapeHtml(code.join("\n"))}</code></pre>`);
      }
      continue;
    }

    if (trimmed === ":::") {
      closeContainer();
      continue;
    }

    if (trimmed.startsWith(":::")) {
      openContainer(trimmed.slice(3).trim());
      continue;
    }

    if (trimmed.startsWith("\\[")) {
      flushParagraph();
      closeList();
      const math = [trimmed];
      if (!trimmed.endsWith("\\]")) {
        i += 1;
        while (i < lines.length) {
          math.push(lines[i]);
          if (lines[i].trim().endsWith("\\]")) break;
          i += 1;
        }
      }
      html.push(`<div class="math-block">${escapeHtml(math.join("\n"))}</div>`);
      continue;
    }

    const heading = /^(#{2,4})\s+(.+)$/.exec(trimmed);
    if (heading) {
      flushParagraph();
      closeList();
      const level = heading[1].length;
      if (currentBlock && level === 3 && !currentBlock.name) {
        const rawTitle = heading[2];
        const nameMatch = /^(?:Def|Clm|Thm|Prop|Rem|Ex):\s*(.+)$/.exec(rawTitle);
        const name = nameMatch ? nameMatch[1].trim() : rawTitle.trim();
        const id = makeBlockId(currentBlock.type, name);
        currentBlock.name = name;
        currentBlock.id = id;
        currentBlock.fullTitle = rawTitle;
        const original = html[currentBlock.divIndex];
        html[currentBlock.divIndex] = original.replace(/>/, ` id="${escapeHtml(id)}">`);
      }
      if (level === 2) {
        const slug = heading[2].trim().toLowerCase()
          .replace(/\\\([^)]*\\\)/g, "")
          .replace(/\s+/g, "-")
          .replace(/[^a-z0-9ぁ-ゟ゠-ヿ一-鿿-]/g, "")
          .replace(/-+/g, "-")
          .replace(/^-|-$/g, "");
        html.push(`<h2 id="sec-${slug}">${renderInline(heading[2])}</h2>`);
      } else {
        html.push(`<h${level}>${renderInline(heading[2])}</h${level}>`);
      }
      continue;
    }

    const ordered = /^\d+\.\s+(.+)$/.exec(trimmed);
    if (ordered) {
      flushParagraph();
      openList("ol");
      html.push(`<li>${renderInline(ordered[1])}</li>`);
      continue;
    }

    const unordered = /^[-*]\s+(.+)$/.exec(trimmed);
    if (unordered) {
      flushParagraph();
      openList("ul");
      html.push(`<li>${renderInline(unordered[1])}</li>`);
      continue;
    }

    paragraph.push(trimmed);
  }

  flushParagraph();
  closeList();
  if (stack.length > 0) {
    throw new Error(`${stack.length} unclosed container(s) (:::) at EOF`);
  }

  return html.join("\n");
}

/* ==========================================================================
   Templates — multi-page output
   ========================================================================== */

function mathJaxScript() {
  return `<script>
      window.MathJax = {
        tex: {
          inlineMath: [["\\\\(", "\\\\)"]],
          displayMath: [["\\\\[", "\\\\]"]],
          macros: {
            R: "\\\\mathbb{R}",
            N: "\\\\mathbb{N}",
            E: "\\\\mathbb{E}",
            Z: "\\\\mathbb{Z}",
            Q: "\\\\mathbb{Q}",
            X: "\\\\mathcal{X}",
            Y: "\\\\mathcal{Y}",
            Mm: "\\\\mathcal{M}",
            Bb: "\\\\mathcal{B}",
            Cc: "\\\\mathcal{C}",
            Pp: "\\\\mathcal{P}",
            Couplings: "\\\\mathcal{U}",
            CouplingsD: "\\\\Pi",
            MK: "\\\\mathcal{L}",
            MKD: "\\\\mathrm{L}",
            Potentials: "\\\\mathcal{R}",
            PotentialsD: "\\\\mathbf{R}",
            Hb: "\\\\mathrm{H}",
            KLD: "\\\\mathrm{KL}",
            ones: "\\\\mathbf{1}",
            Identity: "\\\\mathbf{I}",
            simplex: "\\\\Sigma",
            diag: "\\\\operatorname{diag}",
            tr: "\\\\operatorname{tr}",
            Perm: "\\\\operatorname{Perm}",
            rank: "\\\\operatorname{rank}",
            supp: "\\\\operatorname{supp}",
            smin: "\\\\operatorname{smin}",
            Id: "\\\\operatorname{Id}",
            argmin: "\\\\operatorname*{arg\\\\,min}",
            argmax: "\\\\operatorname*{arg\\\\,max}",
            pushforward: "{_\\\\sharp}",
            d: "\\\\mathrm{d}",
            abs: ["\\\\lvert #1\\\\rvert", 1],
            norm: ["\\\\lVert #1\\\\rVert", 1],
            inner: ["\\\\langle #1,\\\\,#2\\\\rangle", 2],
            defeq: "\\\\overset{\\\\mathrm{def}}{=}",
            range: ["{\\\\lbrack\\\\!\\\\lbrack}#1{\\\\rbrack\\\\!\\\\rbrack}", 1],
            dist: "d",
            distD: "\\\\mathbf{D}",
            Wass: "\\\\mathcal{W}",
            WassD: "\\\\mathrm{W}"
          }
        },
        svg: { fontCache: "global" }
      };
    </script>`;
}

function siteHeader(sections, currentId) {
  const links = sections
    .map((s, i) => {
      const cls = s.data.id === currentId ? " is-current" : "";
      return `          <a href="${escapeHtml(s.data.id)}.html" class="site-header__link${cls}"><span class="site-header__num">${i + 1}</span>${escapeHtml(s.data.nav ?? s.data.title)}</a>`;
    })
    .join("\n");

  return `<header class="site-header">
      <div class="site-header__inner">
        <a href="index.html" class="site-header__home">
          <span class="site-header__logo">OT</span>
          <span class="site-header__name">計算最適輸送</span>
        </a>
        <nav class="site-header__nav">
${links}
        </nav>
      </div>
    </header>`;
}

function chapterTemplate(section, sections, index, chapterFilesMap) {
  const chapterNum = String(index + 1).padStart(2, "0");
  const eyebrow = section.data.eyebrow
    ? `<p class="chapter-hero__eyebrow">${escapeHtml(section.data.eyebrow)}</p>`
    : "";

  let pagerPrev = "<span></span>";
  let pagerNext = "<span></span>";
  if (index > 0) {
    const p = sections[index - 1];
    pagerPrev = `<a class="chapter-pager__link chapter-pager__prev" href="${escapeHtml(p.data.id)}.html">
          <span class="chapter-pager__dir">&larr; 前の章</span>
          <strong>${escapeHtml(p.data.title)}</strong>
        </a>`;
  }
  if (index < sections.length - 1) {
    const n = sections[index + 1];
    pagerNext = `<a class="chapter-pager__link chapter-pager__next" href="${escapeHtml(n.data.id)}.html">
          <span class="chapter-pager__dir">次の章 &rarr;</span>
          <strong>${escapeHtml(n.data.title)}</strong>
        </a>`;
  }

  const blocksJson = JSON.stringify(allBlocks).replace(/<\//g, "<\\/");
  const filesJson = JSON.stringify(chapterFilesMap);

  return `<!doctype html>
<!-- Generated by build.mjs — edit site/content/*.md instead -->
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(section.data.title)} — 計算最適輸送</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./styles.css" />
    ${mathJaxScript()}
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
      window.__blocks = ${blocksJson};
      window.__chapterFiles = ${filesJson};
      window.__currentChapter = "${escapeHtml(section.data.id)}";
    </script>
    <script defer src="./app.js"></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true">
      <div class="reading-progress__fill"></div>
    </div>

    ${siteHeader(sections, section.data.id)}

    <div class="page-layout">
      <nav class="chapter-toc" aria-label="目次"></nav>

      <main class="content">
        <div class="chapter-hero">
          <span class="chapter-hero__num" aria-hidden="true">${chapterNum}</span>
          <div class="chapter-hero__text">
            ${eyebrow}
            <h1 class="chapter-hero__title">${escapeHtml(section.data.title)}</h1>
          </div>
        </div>

        <article class="prose" id="${escapeHtml(section.data.id)}">
          ${section.html}
        </article>

        <nav class="chapter-pager">
          ${pagerPrev}
          ${pagerNext}
        </nav>
      </main>

      <aside class="ref-sidebar" aria-label="参照">
        <div class="ref-sidebar__header">
          <span class="ref-sidebar__label">参照</span>
        </div>
        <div class="ref-sidebar__body">
          <p class="ref-sidebar__empty">参照リンクをクリックすると<br>ここに定義や定理が表示されます</p>
        </div>
      </aside>
    </div>

    <dialog class="ref-sheet" id="ref-sheet">
      <div class="ref-sheet__content"></div>
      <button class="ref-sheet__close" type="button" aria-label="閉じる">&times;</button>
    </dialog>
  </body>
</html>
`;
}

function landingTemplate(sections) {
  const cards = sections
    .map((s, i) => {
      const num = String(i + 1).padStart(2, "0");
      const eyebrow = s.data.eyebrow
        ? `\n          <span class="toc-card__eyebrow">${escapeHtml(s.data.eyebrow)}</span>`
        : "";
      return `        <a href="${escapeHtml(s.data.id)}.html" class="toc-card">
          <span class="toc-card__num">${num}</span>${eyebrow}
          <h2 class="toc-card__title">${escapeHtml(s.data.title)}</h2>
        </a>`;
    })
    .join("\n");

  return `<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>計算最適輸送セミナー</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="landing">
      <div class="landing__hero">
        <h1 class="landing__title">
          計算最適輸送
          <span>セミナー資料</span>
        </h1>
        <p class="landing__sub">Computational Optimal Transport</p>
      </div>
      <nav class="landing__toc">
${cards}
      </nav>
      <footer class="landing__footer">
        <p>Based on <em>Computational Optimal Transport</em> by G. Peyr&eacute; &amp; M. Cuturi</p>
      </footer>
    </main>
  </body>
</html>
`;
}

/* ==========================================================================
   Build
   ========================================================================== */

const sections = readdirSync(contentDir)
  .filter((file) => file.endsWith(".md"))
  .sort()
  .map((file) => {
    const fullPath = path.join(contentDir, file);
    const source = readFileSync(fullPath, "utf8");
    const parsed = parseFrontmatter(source, fullPath);
    currentChapterId = parsed.data.id || null;
    return {
      file,
      data: parsed.data,
      html: renderMarkdown(parsed.body)
    };
  });

for (const section of sections) {
  for (const key of ["id", "title", "nav"]) {
    if (!section.data[key]) {
      throw new Error(`${section.file}: missing frontmatter key "${key}"`);
    }
  }
}

const chapterFiles = {};
sections.forEach((s) => {
  chapterFiles[s.data.id] = `${s.data.id}.html`;
});

writeFileSync(path.join(siteRoot, "index.html"), landingTemplate(sections), "utf8");
sections.forEach((section, i) => {
  const filename = `${section.data.id}.html`;
  writeFileSync(path.join(siteRoot, filename), chapterTemplate(section, sections, i, chapterFiles), "utf8");
});

console.log(`Built ${sections.length + 1} HTML files (landing + ${sections.length} chapters).`);
