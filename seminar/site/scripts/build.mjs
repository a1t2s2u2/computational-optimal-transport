// セミナー資料サイトのビルド：seminar/tex/*.tex を直接 dist/*.html へ変換する。
//
// 旧構成は tex2md.mjs（tex→md）と build.mjs（md→html）の 2 段で、中間の
// content/*.md をディスク経由で受け渡していた。本スクリプトは両者を統合し、
// tex→md はメモリ上で行って中間ファイルを介さず html を生成する。
// tex が唯一の source of truth。

import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(__dirname, "..");
const distDir = path.join(siteRoot, "dist");
const REPO_ROOT = path.resolve(__dirname, "..", "..", "..");
const SEMINAR_DIR = path.join(REPO_ROOT, "seminar", "tex");

/* ==========================================================================
   TeX → markdown（メモリ上の中間表現）
   ========================================================================== */

// 本編(main/) と 付録(foundations/) の全 tex を出現順に返す。
// ラベル写像・章写像の走査対象（preamble.tex / main.tex は含めない）。
function allChapterTex() {
  const paths = [];
  for (const sub of ["main", "foundations"]) {
    const dir = path.join(SEMINAR_DIR, sub);
    if (!existsSync(dir)) continue;
    for (const name of readdirSync(dir)) {
      if (name.endsWith(".tex")) paths.push(path.join(dir, name));
    }
  }
  paths.sort();
  return paths;
}

// 変換対象の章。本編(main/) と 付録:前提知識(foundations/) を tex から生成する。
// group=main は本編、group=appendix は付録ナビに振り分けられる。
// 参照（\ref）解決は buildLabelMap()／buildChapterMap() が main/ と foundations/ の
// 全 tex を走査するため、付録のラベルも本編からタイトル表示・参照できる。
const CHAPTERS = [
  // ---- 本編（OT）：発表2の流れ ----
  ["main/01_assignment.tex", "01-assignment.md", {
    id: "assignment", group: "main",
    nav: "最適割当", eyebrow: "1. Assignment",
    title: "最適割当問題",
  }],
  ["main/02_monge.tex", "02-monge.md", {
    id: "monge", group: "main",
    nav: "Monge", eyebrow: "2. Monge",
    title: "Monge 問題",
  }],
  ["main/03_kantorovich.tex", "03-kantorovich.md", {
    id: "kantorovich", group: "main",
    nav: "Kantorovich", eyebrow: "3. Kantorovich",
    title: "Kantorovich 問題",
  }],
  ["main/04_entropic.tex", "04-entropic.md", {
    id: "entropic", group: "main",
    nav: "エントロピー", eyebrow: "4. Entropic Regularization",
    title: "エントロピー正則化",
  }],
  ["main/05_sinkhorn.tex", "05-sinkhorn.md", {
    id: "sinkhorn", group: "main",
    nav: "Sinkhorn", eyebrow: "5. Sinkhorn",
    title: "Sinkhorn アルゴリズムと収束",
  }],
  // ---- 付録：前提知識（OT非依存・網羅版） ----
  ["foundations/00_set_topology.tex", "A0-set-topology.md", {
    id: "found-set-topology", group: "appendix",
    nav: "集合と位相", eyebrow: "付録 A. Set & Topology",
    title: "集合と位相",
  }],
  ["foundations/01_metric_compact.tex", "A1-metric.md", {
    id: "found-metric", group: "appendix",
    nav: "距離・コンパクト", eyebrow: "付録 B. Metric & Compactness",
    title: "距離空間・連続・コンパクト性",
  }],
  ["foundations/02_measure.tex", "A2-measure.md", {
    id: "found-measure", group: "appendix",
    nav: "測度論", eyebrow: "付録 C. Measure Theory",
    title: "測度論",
  }],
  ["foundations/03_convex_linalg.tex", "A3-convex.md", {
    id: "found-convex", group: "appendix",
    nav: "凸・線形代数", eyebrow: "付録 D. Convexity & Linear Algebra",
    title: "凸性と線形代数",
  }],
  ["foundations/04_nonneg_matrix.tex", "A4-nonneg-matrix.md", {
    id: "found-nonneg-matrix", group: "appendix",
    nav: "非負行列", eyebrow: "付録 E. Nonnegative Matrices",
    title: "非負行列と Hilbert 射影計量",
  }],
];

// Named block environments and their markdown mappings.
// env_name -> [container_class, heading_prefix]
const BLOCK_ENVS = {
  definition: ["definition", "Def"],
  claim: ["theorem", "Clm"],
  theorem: ["theorem", "Thm"],
  proposition: ["theorem", "Prop"],
  remark: ["fact", "Rem"],
  example: ["fact accent", "Ex"],
  algorithm: ["definition", ""],
};

const LABEL_PREFIX_MAP = {
  def: "Def",
  clm: "Clm",
  thm: "Thm",
  prop: "Prop",
  rem: "Rem",
  ex: "Ex",
};

const JP_TO_ABBREV = {
  "定義": "Def", "主張": "Clm", "命題": "Prop",
  "定理": "Thm", "例": "Ex", "注意": "Rem", "Claim": "Clm",
};

const ENV_TO_PREFIX = {
  definition: "def",
  claim: "clm",
  theorem: "thm",
  proposition: "prop",
  remark: "rem",
  example: "ex",
};

let LABEL_MAP = {};
let CHAPTER_MAP = {};

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Remove TeX line comments (% ...), preserving escaped \%.
function stripComments(line) {
  const result = [];
  for (let i = 0; i < line.length; i++) {
    if (line[i] === "%" && (i === 0 || line[i - 1] !== "\\")) break;
    result.push(line[i]);
  }
  return result.join("").replace(/\s+$/, "");
}

// Convert $...$ to \(...\), but leave $$...$$ alone (shouldn't appear).
function convertInlineMath(text) {
  const parts = [];
  let inMath = false;
  for (let i = 0; i < text.length; i++) {
    if (text[i] === "$" && (i === 0 || text[i - 1] !== "\\")) {
      if (inMath) {
        parts.push("\\)");
        inMath = false;
      } else {
        parts.push("\\(");
        inMath = true;
      }
    } else {
      parts.push(text[i]);
    }
  }
  // If we ended with an unclosed math, revert (multi-line $ shouldn't happen
  // after line-joining, but be safe)
  if (inMath) return text;
  return parts.join("");
}

// Convert \textbf{X} -> **X**, \textit{X} -> *X*.
// Handles one level of nested braces (e.g. \textbf{...\mathbf{P}...}).
function convertTextCommands(text) {
  const nested = "(?:[^{}]|\\{[^{}]*\\})*";
  text = text.replace(new RegExp(`\\\\textbf\\{(${nested})\\}`, "g"), "**$1**");
  text = text.replace(new RegExp(`\\\\textit\\{(${nested})\\}`, "g"), "*$1*");
  return text;
}

// Remove \label{...} commands.
function stripLabel(text) {
  return text.replace(/\\label\{[^}]*\}/g, "");
}

// Remove \ref{...} commands and clean up surrounding artifacts.
function stripRef(text) {
  text = text.replace(/第~?\\ref\{[^}]*\}~?章/g, "");
  text = text.replace(/§~?\\ref\{[^}]*\}/g, "");
  text = text.replace(/~?\\ref\{[^}]*\}/g, "");
  text = text.replace(/  +/g, " ");
  text = text.replace(/（\s*）/g, "");
  text = text.replace(/\(\s*\)/g, "");
  return text;
}

// Extract a brace-balanced {…} argument starting at *start*.
// Returns [content, endIndex] or null if *start* is not '{'.
function extractBraceArg(text, start) {
  if (start >= text.length || text[start] !== "{") return null;
  let depth = 0;
  for (let i = start; i < text.length; i++) {
    if (text[i] === "{") depth += 1;
    else if (text[i] === "}") {
      depth -= 1;
      if (depth === 0) return [text.slice(start + 1, i), i + 1];
    }
  }
  return null;
}

// Scan every TeX chapter file and build a map: 'prefix:label' -> title.
function buildLabelMap() {
  const labelMap = {};
  for (const texPath of allChapterTex()) {
    if (!existsSync(texPath)) continue;
    const content = readFileSync(texPath, "utf-8");
    for (const m of content.matchAll(/\\begin\{(\w+)\}/g)) {
      const envName = m[1];
      if (!(envName in ENV_TO_PREFIX)) continue;
      let pos = m.index + m[0].length;
      const titleResult = extractBraceArg(content, pos);
      if (titleResult === null) continue;
      const title = titleResult[0];
      pos = titleResult[1];
      const labelResult = extractBraceArg(content, pos);
      if (labelResult === null) continue;
      const label = labelResult[0];
      const prefix = ENV_TO_PREFIX[envName];
      labelMap[`${prefix}:${label}`] = title;
    }
  }
  return labelMap;
}

// \texorpdfstring{A}{B} -> A など、章タイトル中の表示用整形を除く。
function cleanChapterTitle(title) {
  const nested = "(?:[^{}]|\\{[^{}]*\\})*";
  title = title.replace(
    new RegExp(`\\\\texorpdfstring\\{(${nested})\\}\\{${nested}\\}`, "g"),
    "$1",
  );
  return title.trim();
}

// Scan every TeX chapter file for \chapter{TITLE}\label{ch:...} pairs.
function buildChapterMap() {
  const chapterMap = {};
  for (const texPath of allChapterTex()) {
    const content = readFileSync(texPath, "utf-8");
    for (const m of content.matchAll(/\\chapter\{/g)) {
      const res = extractBraceArg(content, m.index + m[0].length - 1);
      if (res === null) continue;
      const [title, pos] = res;
      const labelM = content.slice(pos, pos + 200).match(/^\s*\\label\{(ch:[^}]*)\}/);
      if (!labelM) continue;
      chapterMap[labelM[1]] = cleanChapterTitle(title);
    }
  }
  return chapterMap;
}

// Convert \ref{...} to clickable [ref:display|name] links.
function convertRefs(text) {
  text = text.replace(/第~?\\ref\{(ch:[^}]*)\}~?章/g, (_, label) => {
    const title = CHAPTER_MAP[label];
    return title ? `「${title}」の章` : "本章";
  });
  text = text.replace(/§~?\\ref\{sec:[^}]*\}/g, "本節");
  text = text.replace(/Algorithm~?\\ref\{alg:[^}]*\}/g, "アルゴリズム");

  text = text.replace(
    /(定義|主張|命題|定理|例|注意|Claim|正則化問題)~?\\ref\{([^}]+)\}/g,
    (_, g1, label) => {
      const title = LABEL_MAP[label];
      if (!title) return "";
      const prefix = label.includes(":") ? label.split(":")[0] : "";
      const abbrev = LABEL_PREFIX_MAP[prefix] || (JP_TO_ABBREV[g1] ?? g1);
      return `[ref:${abbrev}: ${title}|${title}]`;
    },
  );

  text = text.replace(/~?\\ref\{([^}]+)\}/g, (_, label) => {
    const title = LABEL_MAP[label];
    if (!title) return "";
    const prefix = label.includes(":") ? label.split(":")[0] : "";
    const typeName = LABEL_PREFIX_MAP[prefix] || "";
    const display = typeName ? `${typeName}: ${title}` : title;
    return `[ref:${display}|${title}]`;
  });

  text = text.replace(/  +/g, " ");
  text = text.replace(/（\s*）/g, "");
  text = text.replace(/\(\s*\)/g, "");
  return text;
}

// Convert non-breaking space ~ to regular space.
function convertTilde(text) {
  return text.replaceAll("~", " ");
}

// Convert \paragraph{Title.} to **Title.** on its own line.
function convertParagraph(text) {
  return text.replace(/\\paragraph\{([^}]*)\}/g, "\n**$1**\n");
}

// \texorpdfstring{A}{B} -> A（見出し・本文中に現れる表示用整形を除く）。
function convertTexorpdfstring(text) {
  const nested = "(?:[^{}]|\\{[^{}]*\\})*";
  return text.replace(
    new RegExp(`\\\\texorpdfstring\\{(${nested})\\}\\{${nested}\\}`, "g"),
    "$1",
  );
}

// Apply all inline-level conversions to a line of text.
function applyInlineConversions(text, convertReferences = true) {
  // \blockmeta{...} is proofgraph metadata: invisible in the PDF, and likewise
  // must not leak into the site markdown.
  text = text.replace(/\\blockmeta\{[^}]*\}/g, "");
  text = stripLabel(text);
  if (convertReferences && Object.keys(LABEL_MAP).length > 0) {
    text = convertRefs(text);
  } else {
    text = stripRef(text);
  }
  text = convertTilde(text);
  text = convertTextCommands(text);
  text = convertParagraph(text);
  text = convertTexorpdfstring(text);
  text = convertInlineMath(text);
  return text;
}

class TexParser {
  constructor(lines) {
    this.lines = lines;
    this.pos = 0;
  }

  atEnd() {
    return this.pos >= this.lines.length;
  }

  peek() {
    if (this.atEnd()) return "";
    return this.lines[this.pos];
  }

  advance() {
    const line = this.lines[this.pos];
    this.pos += 1;
    return line;
  }

  parse() {
    const nodes = [];
    this.parseBody(nodes, null);
    return nodes;
  }

  parseBody(nodes, stopEnv) {
    while (!this.atEnd()) {
      const line = this.peek();
      const stripped = line.trim();

      // Check for end of enclosing environment
      if (stopEnv && stripped === `\\end{${stopEnv}}`) {
        this.advance();
        return;
      }

      // Skip blank lines (emit paragraph break)
      if (!stripped) {
        this.advance();
        while (!this.atEnd() && !this.peek().trim()) this.advance();
        nodes.push(["blank"]);
        continue;
      }

      // \demohint{NAME}  →  emit a demo block marker for the site
      const mDemo = stripped.match(/^\\demohint\{([^}]+)\}/);
      if (mDemo) {
        this.advance();
        nodes.push(["demo", mDemo[1]]);
        continue;
      }

      // Skip \chapter
      if (stripped.startsWith("\\chapter{")) {
        this.advance();
        if (!this.atEnd() && this.peek().trim().startsWith("\\label{")) {
          this.advance();
        }
        continue;
      }

      // Section headings
      let m = stripped.match(/^\\section\{(.+)\}/);
      if (m) {
        this.advance();
        if (!this.atEnd() && this.peek().trim().startsWith("\\label{")) {
          this.advance();
        }
        nodes.push(["section", m[1]]);
        continue;
      }

      m = stripped.match(/^\\subsection\{(.+)\}/);
      if (m) {
        this.advance();
        if (!this.atEnd() && this.peek().trim().startsWith("\\label{")) {
          this.advance();
        }
        nodes.push(["subsection", m[1]]);
        continue;
      }

      m = stripped.match(/^\\subsubsection\{(.+)\}/);
      if (m) {
        this.advance();
        if (!this.atEnd() && this.peek().trim().startsWith("\\label{")) {
          this.advance();
        }
        nodes.push(["subsubsection", m[1]]);
        continue;
      }

      // Skip figure environments (including those with optional args)
      if (/^\\begin\{figure\}/.test(stripped)) {
        this.skipEnvironment("figure");
        continue;
      }

      // Skip standalone tikzpicture (not inside figure)
      if (/^\\begin\{tikzpicture\}/.test(stripped)) {
        this.skipEnvironment("tikzpicture");
        continue;
      }

      // Skip standalone center that contains tikzpicture or tabular
      if (stripped === "\\begin{center}") {
        this.skipEnvironment("center");
        continue;
      }

      // Algorithm environments -> rendered as a block.
      // \begin{algorithm}{label} ... \end{algorithm}（引数はラベル）。
      const mAlg = stripped.match(/^\\begin\{algorithm\}\{(.+?)\}/);
      if (mAlg) {
        this.advance();
        const raw = [];
        while (!this.atEnd() && this.peek().trim() !== "\\end{algorithm}") {
          raw.push(this.advance());
        }
        if (!this.atEnd()) this.advance(); // consume \end{algorithm}
        // 行末の '\\'（改行）を空行＝段落区切りに変換し、各ステップを
        // 別行で描画する（生の <br> は escape されるため使えない）。
        const processed = [];
        for (const ln of raw) {
          const s = ln.replace(/\s+$/, "");
          if (s.endsWith("\\\\")) {
            processed.push(s.slice(0, -2).replace(/\s+$/, ""));
            processed.push("");
          } else {
            processed.push(ln);
          }
        }
        const blockNodes = new TexParser(processed).parse();
        nodes.push(["block", "algorithm", "アルゴリズム", blockNodes, null]);
        continue;
      }

      // Named block environments: definition, claim, theorem, etc.
      m = stripped.match(/^\\begin\{(\w+)\}\{(.+?)\}\{(.+?)\}/);
      if (m && m[1] in BLOCK_ENVS) {
        const envName = m[1];
        const title = m[2];
        // label = m[3]  -- not used in output
        this.advance();
        const blockNodes = [];
        this.parseBody(blockNodes, envName);
        // Check if next thing is a proof that belongs to this block
        const proofNodes = this.tryParseProof();
        nodes.push(["block", envName, title, blockNodes, proofNodes]);
        continue;
      }

      // memo* environment -> fact block
      if (stripped === "\\begin{memo*}") {
        this.advance();
        const blockNodes = [];
        this.parseBody(blockNodes, "memo*");
        nodes.push(["memo", blockNodes]);
        continue;
      }

      // Standalone proof (not following a block -- rare but possible).
      // Optional argument \begin{proof}[...] も受け付ける。
      if (/^\\begin\{proof\}/.test(stripped)) {
        this.advance();
        const proofNodes = [];
        this.parseBody(proofNodes, "proof");
        nodes.push(["standalone_proof", proofNodes]);
        continue;
      }

      // Display math: \[ ... \]
      if (stripped.startsWith("\\[")) {
        const mathLines = this.collectDisplayMath();
        nodes.push(["display_math", mathLines]);
        continue;
      }

      // align* environment
      if (stripped.startsWith("\\begin{align*}")) {
        const mathLines = this.collectEnvironment("align*");
        nodes.push(["align", mathLines]);
        continue;
      }

      // enumerate
      if (stripped === "\\begin{enumerate}") {
        this.advance();
        const items = this.collectListItems("enumerate");
        nodes.push(["enumerate", items]);
        continue;
      }

      // itemize
      if (stripped === "\\begin{itemize}") {
        this.advance();
        const items = this.collectListItems("itemize");
        nodes.push(["itemize", items]);
        continue;
      }

      // Skip vertical spacing commands
      if (/^\\(medskip|bigskip|smallskip|vspace\*?\{[^}]*\})\s*$/.test(stripped)) {
        this.advance();
        continue;
      }

      // Regular text line
      this.advance();
      nodes.push(["text", line]);
    }
  }

  // Skip past \end{envName}, handling nesting.
  skipEnvironment(envName) {
    const esc = escapeRegExp(envName);
    const beginRe = new RegExp(`^\\\\begin\\{${esc}\\}`);
    const endRe = new RegExp(`^\\\\end\\{${esc}\\}`);
    let depth = 1;
    this.advance(); // consume \begin line
    while (!this.atEnd()) {
      const line = this.peek().trim();
      if (beginRe.test(line)) depth += 1;
      if (line === `\\end{${envName}}` || endRe.test(line)) {
        depth -= 1;
        if (depth === 0) {
          this.advance();
          // Also skip \caption and \label lines that follow
          while (!this.atEnd()) {
            const nxt = this.peek().trim();
            if (nxt.startsWith("\\caption{") || nxt.startsWith("\\label{")) {
              this.advance();
            } else {
              break;
            }
          }
          return;
        }
      }
      this.advance();
    }
  }

  // If the next non-blank content is \begin{proof}, parse it.
  tryParseProof() {
    const savedPos = this.pos;
    while (!this.atEnd() && !this.peek().trim()) this.pos += 1;
    if (!this.atEnd() && /^\\begin\{proof\}/.test(this.peek().trim())) {
      this.advance();
      const proofNodes = [];
      this.parseBody(proofNodes, "proof");
      return proofNodes;
    }
    this.pos = savedPos;
    return null;
  }

  // Collect lines of display math from \[ to \].
  collectDisplayMath() {
    const lines = [];
    const firstLine = this.advance().trim();
    if (firstLine.includes("\\]")) {
      const content = firstLine.replaceAll("\\[", "").replaceAll("\\]", "").trim();
      return [content];
    }
    const contentAfter = firstLine.replaceAll("\\[", "").trim();
    if (contentAfter) lines.push(contentAfter);
    while (!this.atEnd()) {
      const line = this.advance();
      if (line.includes("\\]")) {
        const contentBefore = line.replaceAll("\\]", "").trim();
        if (contentBefore) lines.push(contentBefore);
        break;
      }
      lines.push(line.replace(/\s+$/, ""));
    }
    return lines;
  }

  // Collect all lines inside \begin{envName}...\end{envName}.
  collectEnvironment(envName) {
    const lines = [];
    const firstLine = this.advance().trim();
    const esc = escapeRegExp(envName);
    const after = firstLine.replace(new RegExp(`\\\\begin\\{${esc}\\}`), "").trim();
    if (after) lines.push(after);
    const endTag = `\\end{${envName}}`;
    while (!this.atEnd()) {
      const line = this.advance();
      if (line.includes(endTag)) {
        const before = line.replaceAll(endTag, "").trim();
        if (before) lines.push(before);
        break;
      }
      lines.push(line.replace(/\s+$/, ""));
    }
    return lines;
  }

  // Collect list items until \end{envName}. Returns list of [label, nodeList].
  collectListItems(envName) {
    const items = [];
    let currentLabel = null;
    let currentNodes = null;

    const flushItem = () => {
      if (currentNodes !== null) {
        items.push([currentLabel, currentNodes]);
      }
      currentLabel = null;
      currentNodes = null;
    };

    while (!this.atEnd()) {
      const stripped = this.peek().trim();
      if (stripped === `\\end{${envName}}`) {
        this.advance();
        flushItem();
        break;
      }

      const m = stripped.match(/^\\item(?:\[([^\]]*)\])?\s*([\s\S]*)/);
      if (m && stripped.startsWith("\\item")) {
        flushItem();
        currentLabel = m[1] !== undefined ? m[1] : null;
        const rest = m[2].trim();
        currentNodes = [];
        if (rest) currentNodes.push(["text", rest]);
        this.advance();
      } else {
        if (currentNodes === null) currentNodes = [];
        this.parseItemContent(currentNodes, envName);
      }
    }

    return items;
  }

  // Parse a single piece of content within a list item.
  parseItemContent(nodes, listEnvName) {
    const stripped = this.peek().trim();

    if (!stripped) {
      this.advance();
      nodes.push(["blank"]);
      return;
    }

    if (stripped.startsWith("\\[")) {
      const mathLines = this.collectDisplayMath();
      nodes.push(["display_math", mathLines]);
      return;
    }

    if (stripped === "\\begin{align*}") {
      const mathLines = this.collectEnvironment("align*");
      nodes.push(["align", mathLines]);
      return;
    }

    if (stripped === "\\begin{enumerate}") {
      this.advance();
      const items = this.collectListItems("enumerate");
      nodes.push(["enumerate", items]);
      return;
    }

    if (stripped === "\\begin{itemize}") {
      this.advance();
      const items = this.collectListItems("itemize");
      nodes.push(["itemize", items]);
      return;
    }

    // \begin{cases|pmatrix|bmatrix} falls through to text

    nodes.push(["text", this.advance()]);
  }
}

// Render a list item preserving content order (text, math, text, ...).
function renderListItem(output, prefix, itemNodes) {
  let firstText = true;
  const textBuf = [];

  const flushText = () => {
    if (textBuf.length === 0) return;
    let text = textBuf.filter((t) => t).join("");
    text = applyInlineConversions(text);
    if (text) {
      if (firstText) {
        output.push(`${prefix}${text}`);
        firstText = false;
      } else {
        output.push(text);
      }
    }
    textBuf.length = 0;
  };

  for (const n of itemNodes) {
    if (n[0] === "text") {
      textBuf.push(n[1].trim());
    } else if (n[0] === "blank") {
      continue;
    } else {
      flushText();
      const blockLines = renderNodes([n]);
      for (const bl of blockLines) output.push(bl);
    }
  }

  flushText();
  if (firstText) output.push(prefix.replace(/\s+$/, ""));
}

// Render parsed nodes into markdown lines.
function renderNodes(nodes) {
  const output = [];
  let textBuf = [];

  const flushText = () => {
    // 段落内で連続するテキスト行を 1 行に連結する。renderMarkdown は段落を
    // スペースで連結するため、ここで連結しておかないと行折り返し位置に
    // 日本語の余計な空白が入る。CJK 想定で空文字連結。
    if (textBuf.length > 0) {
      output.push(textBuf.join(""));
      textBuf = [];
    }
  };

  for (const node of nodes) {
    const kind = node[0];

    if (kind !== "text") flushText();

    if (kind === "blank") {
      output.push("");
      continue;
    }

    if (kind === "section") {
      const title = applyInlineConversions(node[1]);
      output.push(`## ${title}`);
      output.push("");
      continue;
    }

    if (kind === "subsection") {
      const title = applyInlineConversions(node[1]);
      output.push(`### ${title}`);
      output.push("");
      continue;
    }

    if (kind === "subsubsection") {
      const title = applyInlineConversions(node[1]);
      output.push(`**${title}**`);
      output.push("");
      continue;
    }

    if (kind === "demo") {
      output.push(`:::demo ${node[1]}`);
      output.push("");
      continue;
    }

    if (kind === "block") {
      const [, envName, title, bodyNodes, proofNodes] = node;
      const [containerClass, prefix] = BLOCK_ENVS[envName];
      output.push(`:::${containerClass}`);
      let heading;
      if (prefix) {
        heading = `### ${prefix}: ${applyInlineConversions(title)}`;
      } else {
        heading = `### ${applyInlineConversions(title)}`;
      }
      output.push(heading);
      const bodyLines = renderNodes(bodyNodes);
      const bodyText = bodyLines.join("\n").trim();
      if (bodyText) {
        output.push("");
        output.push(bodyText);
      }
      if (proofNodes !== null && proofNodes !== undefined) {
        output.push("");
        output.push(":::details-embedded 証明");
        const proofLines = renderNodes(proofNodes);
        const proofText = proofLines.join("\n").trim();
        if (proofText) output.push(proofText);
        output.push(":::");
      }
      output.push(":::");
      output.push("");
      continue;
    }

    if (kind === "memo") {
      const bodyNodes = node[1];
      output.push(":::fact");
      const bodyLines = renderNodes(bodyNodes);
      const bodyText = bodyLines.join("\n").trim();
      if (bodyText) output.push(bodyText);
      output.push(":::");
      output.push("");
      continue;
    }

    if (kind === "standalone_proof") {
      const proofNodes = node[1];
      output.push(":::details-embedded 証明");
      const proofLines = renderNodes(proofNodes);
      const proofText = proofLines.join("\n").trim();
      if (proofText) output.push(proofText);
      output.push(":::");
      output.push("");
      continue;
    }

    if (kind === "display_math") {
      const mathLines = node[1];
      output.push("");
      output.push("\\[");
      for (const ml of mathLines) {
        output.push(applyInlineConversions(ml, false));
      }
      output.push("\\]");
      output.push("");
      continue;
    }

    if (kind === "align") {
      const mathLines = node[1];
      output.push("");
      output.push("\\[\\begin{aligned}");
      for (const ml of mathLines) {
        output.push(applyInlineConversions(ml, false));
      }
      output.push("\\end{aligned}\\]");
      output.push("");
      continue;
    }

    if (kind === "enumerate") {
      const items = node[1];
      output.push("");
      let idx = 1;
      for (const [label, itemNodes] of items) {
        const prefix = label ? `${label} ` : `${idx}. `;
        renderListItem(output, prefix, itemNodes);
        idx += 1;
      }
      output.push("");
      continue;
    }

    if (kind === "itemize") {
      const items = node[1];
      output.push("");
      for (const [label, itemNodes] of items) {
        const prefix = label ? `${label} ` : "- ";
        renderListItem(output, prefix, itemNodes);
      }
      output.push("");
      continue;
    }

    if (kind === "text") {
      const text = node[1].trim();
      if (text) textBuf.push(applyInlineConversions(text));
      continue;
    }
  }

  flushText();
  return output;
}

// Post-process the rendered markdown: collapse blank lines, trim.
function cleanOutput(text) {
  const lines = text.split("\n").map((line) => line.replace(/\s+$/, ""));
  const cleaned = [];
  let blankCount = 0;
  for (const line of lines) {
    if (line === "") {
      blankCount += 1;
      if (blankCount <= 2) cleaned.push(line);
    } else {
      blankCount = 0;
      cleaned.push(line);
    }
  }
  const result = cleaned.join("\n").trim();
  return result + "\n";
}

// Count unescaped $ signs in a line (not inside \[ \] blocks).
function countUnescapedDollars(line) {
  let count = 0;
  for (let i = 0; i < line.length; i++) {
    if (line[i] === "$" && (i === 0 || line[i - 1] !== "\\")) count += 1;
  }
  return count;
}

// Join lines where $ inline math spans multiple lines.
function joinMultilineInlineMath(lines) {
  const result = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const stripped = line.trim();
    if (stripped.startsWith("\\[") || stripped.startsWith("\\begin{")) {
      result.push(line);
      i += 1;
      continue;
    }
    let nDollars = countUnescapedDollars(line);
    if (nDollars % 2 === 1) {
      let joined = line;
      i += 1;
      while (i < lines.length) {
        joined = joined.replace(/\s+$/, "") + " " + lines[i].trim();
        nDollars += countUnescapedDollars(lines[i]);
        i += 1;
        if (nDollars % 2 === 0) break;
      }
      result.push(joined);
    } else {
      result.push(line);
      i += 1;
    }
  }
  return result;
}

// 1 章ぶんの tex を読み、frontmatter 付きの markdown 文字列を返す（中間
// ファイルは作らない）。tex が無ければ null。
function chapterToMarkdown(texFilename, frontmatter) {
  const texPath = path.join(SEMINAR_DIR, texFilename);
  if (!existsSync(texPath)) {
    console.log(`  SKIP (not found): ${texFilename}`);
    return null;
  }

  const rawContent = readFileSync(texPath, "utf-8");
  const rawLines = rawContent.split("\n");
  // readlines() 相当：ファイル末尾の改行による空要素を落とす。
  if (rawLines.length > 0 && rawLines[rawLines.length - 1] === "") {
    rawLines.pop();
  }

  let lines = rawLines.map((line) => stripComments(line.replace(/\n$/, "")));
  lines = joinMultilineInlineMath(lines);

  const nodes = new TexParser(lines).parse();
  const body = renderNodes(nodes).join("\n");

  let fm = "---\n";
  fm += `id: ${frontmatter.id}\n`;
  fm += `group: ${frontmatter.group ?? "main"}\n`;
  fm += `nav: ${frontmatter.nav}\n`;
  fm += `eyebrow: ${frontmatter.eyebrow}\n`;
  fm += `title: ${frontmatter.title}\n`;
  fm += "---\n\n";

  return cleanOutput(fm + body);
}

/* ==========================================================================
   markdown（中間表現）→ html
   ========================================================================== */

// 各ページの dist 相対出力パス（本編→ main/、付録→ appendix/）。
function outPathOf(section) {
  const sub = section.data.group === "appendix" ? "appendix" : "main";
  return `${sub}/${section.data.id}.html`;
}

// from ページ（dist 相対）から to リソース（dist 相対）への相対 URL を返す。
function relUrl(fromOutPath, toOutPath) {
  const rel = path.posix.relative(path.posix.dirname(fromOutPath), toOutPath);
  return rel || ".";
}

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
  const prefixMap = { definition: "def", theorem: "thm", proposition: "prop", remark: "rem", example: "ex" };
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
    if (spec === "proposition") {
      currentBlock = { type: "proposition", divIndex: html.length, depth: stack.length };
      html.push('<div class="block block--prop">');
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
      } else if (language === "rawhtml") {
        html.push(code.join("\n"));
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
            WassD: "\\\\mathrm{W}",
            Lcal: "\\\\mathcal{L}",
            Hm: "\\\\mathrm{H}",
            Tan: "\\\\mathrm{Tan}",
            Ric: "\\\\operatorname{Ric}",
            CD: "\\\\mathrm{CD}",
            diverg: "\\\\nabla\\\\!\\\\cdot\\\\!",
            dHil: "d_{\\\\mathcal{H}}"
          }
        },
        svg: { fontCache: "global" }
      };
    </script>`;
}

function siteHeader(sections, currentSection) {
  const curOut = outPathOf(currentSection);
  const mainSecs = sections.filter((s) => s.data.group !== "appendix");
  const appendixSecs = sections.filter((s) => s.data.group === "appendix");

  const renderLink = (s, label) => {
    const cls = s.data.id === currentSection.data.id ? " is-current" : "";
    const href = relUrl(curOut, outPathOf(s));
    return `          <a href="${escapeHtml(href)}" class="site-header__link${cls}"><span class="site-header__num">${label}</span>${escapeHtml(s.data.nav ?? s.data.title)}</a>`;
  };

  const mainLinks = mainSecs.map((s, i) => renderLink(s, i + 1)).join("\n");
  const appendixLinks = appendixSecs
    .map((s, i) => renderLink(s, String.fromCharCode(65 + i)))
    .join("\n");

  const appendixNav = appendixSecs.length
    ? `\n          <span class="site-header__group-label">付録</span>\n${appendixLinks}`
    : "";

  return `<header class="site-header">
      <div class="site-header__inner">
        <a href="${escapeHtml(relUrl(curOut, "index.html"))}" class="site-header__home">
          <span class="site-header__logo">OT</span>
          <span class="site-header__name">計算最適輸送</span>
        </a>
        <nav class="site-header__nav">
${mainLinks}${appendixNav}
        </nav>
      </div>
    </header>`;
}

function chapterTemplate(section, sections, index) {
  const curOut = outPathOf(section);
  // 参照ジャンプ用に「現在ページからの相対 URL」で章ファイル表を作る（app.js が使用）。
  const chapterFilesMap = {};
  sections.forEach((s) => {
    chapterFilesMap[s.data.id] = relUrl(curOut, outPathOf(s));
  });
  const chapterNum = String(index + 1).padStart(2, "0");
  const eyebrow = section.data.eyebrow
    ? `<p class="chapter-hero__eyebrow">${escapeHtml(section.data.eyebrow)}</p>`
    : "";

  let pagerPrev = "<span></span>";
  let pagerNext = "<span></span>";
  if (index > 0) {
    const p = sections[index - 1];
    pagerPrev = `<a class="chapter-pager__link chapter-pager__prev" href="${escapeHtml(relUrl(curOut, outPathOf(p)))}">
          <span class="chapter-pager__dir">&larr; 前の章</span>
          <strong>${escapeHtml(p.data.title)}</strong>
        </a>`;
  }
  if (index < sections.length - 1) {
    const n = sections[index + 1];
    pagerNext = `<a class="chapter-pager__link chapter-pager__next" href="${escapeHtml(relUrl(curOut, outPathOf(n)))}">
          <span class="chapter-pager__dir">次の章 &rarr;</span>
          <strong>${escapeHtml(n.data.title)}</strong>
        </a>`;
  }

  const blocksJson = JSON.stringify(allBlocks).replace(/<\//g, "<\\/");
  const filesJson = JSON.stringify(chapterFilesMap);

  return `<!doctype html>
<!-- Generated by build.mjs — edit seminar/tex/*.tex instead -->
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(section.data.title)} — 計算最適輸送</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="${relUrl(curOut, "styles.css")}" />
    ${mathJaxScript()}
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
      window.__blocks = ${blocksJson};
      window.__chapterFiles = ${filesJson};
      window.__currentChapter = "${escapeHtml(section.data.id)}";
    </script>
    <script defer src="${relUrl(curOut, "app.js")}"></script>
  </head>
  <body>
    <div class="reading-progress" aria-hidden="true">
      <div class="reading-progress__fill"></div>
    </div>

    ${siteHeader(sections, section)}

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
  const renderCards = (secs) =>
    secs
      .map((s, i) => {
        const num =
          s.data.group === "appendix"
            ? String.fromCharCode(65 + i)
            : String(i + 1).padStart(2, "0");
        const eyebrow = s.data.eyebrow
          ? `\n          <span class="toc-card__eyebrow">${escapeHtml(s.data.eyebrow)}</span>`
          : "";
        return `        <a href="${escapeHtml(outPathOf(s))}" class="toc-card">
          <span class="toc-card__num">${num}</span>${eyebrow}
          <h2 class="toc-card__title">${escapeHtml(s.data.title)}</h2>
        </a>`;
      })
      .join("\n");

  const mainSecs = sections.filter((s) => s.data.group !== "appendix");
  const appendixSecs = sections.filter((s) => s.data.group === "appendix");

  const appendixBlock = appendixSecs.length
    ? `
      <div class="landing__group">
        <h2 class="landing__group-title">付録：前提知識</h2>
        <p class="landing__group-sub">発表では省略した数学的前提を網羅した完全版．本編から参照される．</p>
      </div>
      <nav class="landing__toc">
${renderCards(appendixSecs)}
      </nav>`
    : "";

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
${renderCards(mainSecs)}
      </nav>${appendixBlock}
      <footer class="landing__footer">
        <p>Based on <em>Computational Optimal Transport</em> by G. Peyr&eacute; &amp; M. Cuturi</p>
      </footer>
    </main>
  </body>
</html>
`;
}

/* ==========================================================================
   Build：tex → (in-memory markdown) → dist/*.html
   ========================================================================== */

LABEL_MAP = buildLabelMap();
CHAPTER_MAP = buildChapterMap();

const sections = CHAPTERS
  .map(([texFile, mdFile, fm]) => ({ mdFile, md: chapterToMarkdown(texFile, fm) }))
  .filter((s) => s.md !== null)
  .map(({ mdFile, md }) => {
    const parsed = parseFrontmatter(md, mdFile);
    currentChapterId = parsed.data.id || null;
    return {
      file: mdFile,
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

mkdirSync(path.join(distDir, "main"), { recursive: true });
mkdirSync(path.join(distDir, "appendix"), { recursive: true });

writeFileSync(path.join(distDir, "index.html"), landingTemplate(sections), "utf8");
sections.forEach((section, i) => {
  writeFileSync(path.join(distDir, outPathOf(section)), chapterTemplate(section, sections, i), "utf8");
});

// html から相対参照される静的アセットを dist へコピーする。
for (const asset of ["styles.css", "app.js"]) {
  copyFileSync(path.join(siteRoot, asset), path.join(distDir, asset));
}

const nMain = sections.filter((s) => s.data.group !== "appendix").length;
console.log(
  `Built dist/ : index.html + main/(${nMain}) + appendix/(${sections.length - nMain}).`
);
