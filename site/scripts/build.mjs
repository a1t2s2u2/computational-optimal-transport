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
  return escapeHtml(source)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(
      /\[term:([^|\]]+)\|([a-z0-9-]+)\]/g,
      (_match, label, term) => `<button type="button" class="term" data-term="${term}">${label}</button>`
    )
    .replace(
      /\[ref:([^|\]]+?)(?:\|([^\]]+))?\]/g,
      (_match, first, second) => {
        const display = first;
        const refName = second || first;
        return `<button type="button" class="ref" data-ref="${refName}">${display}</button>`;
      }
    );
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
      html.push('<div class="block definition">');
      stack.push("</div>");
      return;
    }
    if (spec === "theorem") {
      currentBlock = { type: "theorem", divIndex: html.length, depth: stack.length };
      html.push('<div class="block theorem">');
      stack.push("</div>");
      return;
    }
    if (spec === "algorithm") {
      html.push('<div class="algorithm">');
      stack.push("</div>");
      return;
    }
    if (spec === "fact") {
      currentBlock = { type: "remark", divIndex: html.length, depth: stack.length };
      html.push('<article class="fact">');
      stack.push("</article>");
      return;
    }
    if (spec === "fact accent") {
      currentBlock = { type: "example", divIndex: html.length, depth: stack.length };
      html.push('<article class="fact accent">');
      stack.push("</article>");
      return;
    }
    if (spec.startsWith("details-embedded ")) {
      const title = spec.slice("details-embedded ".length);
      html.push(`<details class="fold embedded"><summary>${renderInline(title)}</summary>`);
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
      html.push(sinkhornDemo());
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

    if (trimmed === "\\[") {
      flushParagraph();
      closeList();
      const math = [trimmed];
      i += 1;
      while (i < lines.length) {
        math.push(lines[i]);
        if (lines[i].trim() === "\\]") break;
        i += 1;
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
        const nameMatch = /^(?:定義|命題|定理|補題|主張|例):\s*(.+)$/.exec(rawTitle);
        const name = nameMatch ? nameMatch[1].trim() : rawTitle.trim();
        const id = makeBlockId(currentBlock.type, name);
        currentBlock.name = name;
        currentBlock.id = id;
        currentBlock.fullTitle = rawTitle;
        const original = html[currentBlock.divIndex];
        html[currentBlock.divIndex] = original.replace(/>/, ` id="${escapeHtml(id)}">`);
      }
      html.push(`<h${level}>${renderInline(heading[2])}</h${level}>`);
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

function renderHeading(section, isFirst) {
  const title = escapeHtml(section.data.title);
  const level = isFirst ? "h1" : "h2";
  if (section.data.term) {
    return `<${level}><button type="button" class="term heading-term" data-term="${escapeHtml(section.data.term)}">${title}</button></${level}>`;
  }
  return `<${level}>${title}</${level}>`;
}

function renderSection(section, index) {
  const eyebrow = section.data.eyebrow
    ? `<p class="eyebrow">${escapeHtml(section.data.eyebrow)}</p>`
    : "";
  const lead = section.data.lead ? `<p class="lead">${renderInline(section.data.lead)}</p>` : "";
  const parts = [
    `<section id="${escapeHtml(section.data.id)}" class="chapter">`,
    eyebrow,
    renderHeading(section, index === 0),
    lead,
    section.html,
    "</section>"
  ].filter(Boolean);
  return parts.join("\n");
}

function pageTemplate(sections) {
  const nav = sections
    .map((section) => `<a href="#${escapeHtml(section.data.id)}">${escapeHtml(section.data.nav ?? section.data.title)}</a>`)
    .join("\n          ");
  const renderedSections = sections.map(renderSection).join("\n");

  return `<!doctype html>
<!-- Generated by site/scripts/build.mjs. Edit site/content/*.md instead. -->
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>計算最適輸送セミナー</title>
    <link rel="stylesheet" href="./styles.css" />
    <script>
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
            CouplingsD: "\\\\mathbf{U}",
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
            oslash: "\\\\oslash",
            range: ["\\\\llbracket #1\\\\rrbracket", 1],
            dist: "d",
            distD: "\\\\mathbf{D}",
            Wass: "\\\\mathcal{W}",
            WassD: "\\\\mathrm{W}"
          }
        },
        svg: { fontCache: "global" }
      };
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>window.__blocks = ${JSON.stringify(allBlocks).replace(/<\//g, "<\\/")};</script>
    <script defer src="./app.js"></script>
  </head>
  <body>
    <div class="site-shell">
      <aside class="sidebar" aria-label="章ナビゲーション">
        <div class="brand">
          <span class="brand-mark">OT</span>
          <div>
            <strong>計算最適輸送</strong>
            <span>Cuturi / Peyre ルート</span>
          </div>
        </div>
        <nav class="chapter-nav">
          ${nav}
        </nav>
      </aside>

      <main class="content">
        ${renderedSections}
      </main>

      <aside class="inspector" aria-label="用語と対応表">
        <section class="panel glossary-panel">
          <h2>用語</h2>
          <div id="glossary-box">
            <h3>Polish 空間</h3>
            <p>完備かつ可分な距離空間。測度論的 OT の標準的な基礎空間。</p>
          </div>
        </section>

        <section class="panel">
          <h2>有限と無限</h2>
          <table class="mini-table">
            <tbody>
              <tr>
                <th>測度</th>
                <td>\\(\\alpha=\\sum_i a_i\\delta_{x_i}\\)</td>
              </tr>
              <tr>
                <th>結合</th>
                <td>\\(\\pi=\\sum_{i,j}P_{ij}\\delta_{(x_i,y_j)}\\)</td>
              </tr>
              <tr>
                <th>コスト</th>
                <td>\\(C_{ij}=c(x_i,y_j)\\)</td>
              </tr>
              <tr>
                <th>極限</th>
                <td>\\(\\varepsilon\\to0\\) で非正則化 OT</td>
              </tr>
            </tbody>
          </table>
        </section>
      </aside>
    </div>
  </body>
</html>
`;
}

const sections = readdirSync(contentDir)
  .filter((file) => file.endsWith(".md"))
  .sort()
  .map((file) => {
    const fullPath = path.join(contentDir, file);
    const source = readFileSync(fullPath, "utf8");
    const parsed = parseFrontmatter(source, fullPath);
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

writeFileSync(path.join(siteRoot, "index.html"), pageTemplate(sections), "utf8");
console.log(`Built site/index.html from ${sections.length} markdown files.`);
