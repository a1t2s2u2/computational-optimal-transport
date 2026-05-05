/**
 * md2tex.mjs — site/content/*.md → seminar-compatible .tex
 *
 * Usage:
 *   node site/scripts/md2tex.mjs              # 全ファイルを site/tex-out/ に出力
 *   node site/scripts/md2tex.mjs 05-entropic  # 指定ファイルのみ
 *   node site/scripts/md2tex.mjs --stdout     # 標準出力に出力（デバッグ用）
 */

import { readdirSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(__dirname, "..");
const contentDir = path.join(siteRoot, "content");
const outDir = path.join(siteRoot, "tex-out");

// ---------------------------------------------------------------------------
// Frontmatter parser (same as build.mjs)
// ---------------------------------------------------------------------------

function parseFrontmatter(source, filePath) {
  if (!source.startsWith("---\n")) {
    throw new Error(`${filePath}: frontmatter is required`);
  }
  const end = source.indexOf("\n---\n", 4);
  if (end === -1) {
    throw new Error(`${filePath}: frontmatter is not closed`);
  }
  const raw = source.slice(4, end);
  const body = source.slice(end + 5);
  const data = {};
  for (const line of raw.split("\n")) {
    if (!line.trim()) continue;
    const index = line.indexOf(":");
    if (index === -1) continue;
    data[line.slice(0, index).trim()] = line.slice(index + 1).trim();
  }
  return { data, body };
}

// ---------------------------------------------------------------------------
// Math normalisation: \(...\) → $...$  (display math \[...\] stays)
// ---------------------------------------------------------------------------

function normalizeMath(line) {
  return line.replace(/\\\((.+?)\\\)/g, "$$$1$$");
}

// ---------------------------------------------------------------------------
// Term references: [term:Label|key] → \textbf{Label}
// ---------------------------------------------------------------------------

function normalizeTerms(line) {
  return line.replace(/\[term:([^|\]]+)\|[a-z0-9-]+\]/g, "\\textbf{$1}");
}

// ---------------------------------------------------------------------------
// Label generation from Japanese title
// ---------------------------------------------------------------------------

let labelCounter = 0;
function makeLabel(prefix, title) {
  labelCounter++;
  const slug = title
    .replace(/[\\${}]/g, "")
    .replace(/\s+/g, "-")
    .slice(0, 30)
    .replace(/-+$/, "");
  return `site-${prefix}-${labelCounter}`;
}

// ---------------------------------------------------------------------------
// Block type detection from heading inside a container
// ---------------------------------------------------------------------------

function parseBlockHeading(lines, startIdx) {
  for (let i = startIdx; i < lines.length && i < startIdx + 3; i++) {
    const m = lines[i].match(/^###\s+(.+)$/);
    if (m) return { headingIdx: i, heading: m[1] };
  }
  return null;
}

function classifyHeading(heading) {
  if (heading.startsWith("定義:") || heading.startsWith("定義: ")) {
    return { env: "definition", title: heading.replace(/^定義:\s*/, "") };
  }
  if (heading.startsWith("定理:") || heading.startsWith("定理: ")) {
    return { env: "theorem", title: heading.replace(/^定理:\s*/, "") };
  }
  if (heading.startsWith("命題:") || heading.startsWith("命題: ")) {
    return { env: "proposition", title: heading.replace(/^命題:\s*/, "") };
  }
  if (heading.startsWith("主張:") || heading.startsWith("主張: ")) {
    return { env: "claim", title: heading.replace(/^主張:\s*/, "") };
  }
  return { env: null, title: heading };
}

// ---------------------------------------------------------------------------
// Main converter
// ---------------------------------------------------------------------------

function convertFile(filePath) {
  const source = readFileSync(filePath, "utf8");
  const { data, body } = parseFrontmatter(source, filePath);

  const lines = body.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;

  // Chapter/section header from frontmatter
  out.push(`%% ============================================================`);
  out.push(`%% ${data.title} (from ${path.basename(filePath)})`);
  out.push(`%% ============================================================`);
  out.push(``);

  function processLine(line) {
    return normalizeTerms(normalizeMath(line));
  }

  function collectUntilClose(depth = 1) {
    const content = [];
    let d = depth;
    while (i < lines.length) {
      const l = lines[i];
      const trimmed = l.trim();
      if (trimmed === ":::") {
        d--;
        if (d === 0) { i++; return content; }
        content.push(l);
        i++;
      } else if (trimmed.startsWith(":::")) {
        d++;
        content.push(l);
        i++;
      } else {
        content.push(l);
        i++;
      }
    }
    return content;
  }

  function convertBlock(containerType, contentLines) {
    // Find heading
    let headingInfo = null;
    let bodyStart = 0;
    for (let k = 0; k < contentLines.length && k < 4; k++) {
      const m = contentLines[k].match(/^###\s+(.+)$/);
      if (m) {
        headingInfo = m[1];
        bodyStart = k + 1;
        break;
      }
    }

    // Skip blank lines after heading
    while (bodyStart < contentLines.length && contentLines[bodyStart].trim() === "") {
      bodyStart++;
    }

    const bodyLines = contentLines.slice(bodyStart);

    if (containerType === "definition" || containerType === "theorem" || containerType === "algorithm") {
      let env = containerType;
      let title = headingInfo || "";

      if (headingInfo) {
        const classified = classifyHeading(headingInfo);
        if (classified.env) env = classified.env;
        title = classified.title;
      }

      if (env === "algorithm") {
        const label = makeLabel("alg", title);
        out.push(`\\begin{algorithm}{${label}}`);
        convertBodyLines(bodyLines);
        out.push(`\\end{algorithm}`);
      } else {
        const label = makeLabel(env.slice(0, 3), title);
        out.push(`\\begin{${env}}{${processLine(title)}}{${label}}`);
        convertBodyLines(bodyLines);
        out.push(`\\end{${env}}`);
      }
    } else if (containerType.startsWith("details-embedded ")) {
      const title = containerType.slice("details-embedded ".length);
      out.push(`\\begin{proof}[${processLine(title)}]`);
      convertBodyLines(bodyLines.length > 0 ? bodyLines : contentLines);
      out.push(`\\end{proof}`);
    } else if (containerType.startsWith("details ")) {
      const title = containerType.slice("details ".length);
      out.push(`\\begin{remark}{${processLine(title)}}{${makeLabel("rem", title)}}`);
      convertBodyLines(bodyLines.length > 0 ? bodyLines : contentLines);
      out.push(`\\end{remark}`);
    } else if (containerType === "compare") {
      out.push(`% --- compare block (manual formatting needed) ---`);
      convertBodyLines(contentLines);
    } else if (containerType === "column") {
      convertBodyLines(contentLines);
    } else if (containerType === "fact" || containerType === "fact accent") {
      convertBodyLines(contentLines);
    } else if (containerType === "grid two") {
      convertBodyLines(contentLines);
    } else if (containerType.startsWith("demo ")) {
      out.push(`% [interactive demo: ${containerType.slice(5)}]`);
    }
  }

  function convertBodyLines(bodyLines) {
    let j = 0;
    while (j < bodyLines.length) {
      const line = bodyLines[j];
      const trimmed = line.trim();

      if (trimmed === "") {
        out.push("");
        j++;
        continue;
      }

      // Nested container
      if (trimmed.startsWith(":::") && trimmed !== ":::") {
        const nestedType = trimmed.slice(3).trim();
        j++;
        const nestedContent = [];
        let depth = 1;
        while (j < bodyLines.length) {
          const l = bodyLines[j].trim();
          if (l === ":::") {
            depth--;
            if (depth === 0) { j++; break; }
            nestedContent.push(bodyLines[j]);
            j++;
          } else if (l.startsWith(":::")) {
            depth++;
            nestedContent.push(bodyLines[j]);
            j++;
          } else {
            nestedContent.push(bodyLines[j]);
            j++;
          }
        }
        convertBlock(nestedType, nestedContent);
        continue;
      }

      if (trimmed === ":::") {
        j++;
        continue;
      }

      // Display math
      if (trimmed === "\\[") {
        out.push("  \\[");
        j++;
        while (j < bodyLines.length) {
          out.push(`  ${bodyLines[j]}`);
          if (bodyLines[j].trim() === "\\]") { j++; break; }
          j++;
        }
        continue;
      }

      // Heading → section/subsection
      const h2 = trimmed.match(/^##\s+(.+)$/);
      if (h2) {
        out.push(`\\section{${processLine(h2[1])}}`);
        j++;
        continue;
      }
      const h3 = trimmed.match(/^###\s+(.+)$/);
      if (h3) {
        out.push(`\\subsection{${processLine(h3[1])}}`);
        j++;
        continue;
      }
      const h4 = trimmed.match(/^####\s+(.+)$/);
      if (h4) {
        out.push(`\\subsubsection{${processLine(h4[1])}}`);
        j++;
        continue;
      }

      // Ordered list
      const ol = trimmed.match(/^\d+\.\s+(.+)$/);
      if (ol) {
        out.push("\\begin{enumerate}");
        while (j < bodyLines.length) {
          const olm = bodyLines[j].trim().match(/^\d+\.\s+(.+)$/);
          if (!olm) break;
          out.push(`  \\item ${processLine(olm[1])}`);
          j++;
        }
        out.push("\\end{enumerate}");
        continue;
      }

      // Unordered list
      const ul = trimmed.match(/^[-*]\s+(.+)$/);
      if (ul) {
        out.push("\\begin{itemize}");
        while (j < bodyLines.length) {
          const ulm = bodyLines[j].trim().match(/^[-*]\s+(.+)$/);
          if (!ulm) break;
          out.push(`  \\item ${processLine(ulm[1])}`);
          j++;
        }
        out.push("\\end{itemize}");
        continue;
      }

      // Mermaid code block (skip)
      if (trimmed.startsWith("```mermaid")) {
        out.push(`% [mermaid diagram omitted]`);
        j++;
        while (j < bodyLines.length && !bodyLines[j].trim().startsWith("```")) j++;
        j++;
        continue;
      }

      // Other code block
      if (trimmed.startsWith("```")) {
        j++;
        out.push("\\begin{verbatim}");
        while (j < bodyLines.length && !bodyLines[j].trim().startsWith("```")) {
          out.push(bodyLines[j]);
          j++;
        }
        out.push("\\end{verbatim}");
        j++;
        continue;
      }

      // Regular paragraph line
      out.push(processLine(trimmed));
      j++;
    }
  }

  // Main loop
  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (trimmed === "") { out.push(""); i++; continue; }

    // Container open
    if (trimmed.startsWith(":::") && trimmed !== ":::") {
      const containerType = trimmed.slice(3).trim();
      i++;
      const content = collectUntilClose(1);
      convertBlock(containerType, content);
      continue;
    }

    if (trimmed === ":::") { i++; continue; }

    // Display math at top level
    if (trimmed === "\\[") {
      out.push("\\[");
      i++;
      while (i < lines.length) {
        out.push(lines[i]);
        if (lines[i].trim() === "\\]") { i++; break; }
        i++;
      }
      continue;
    }

    // Heading
    const h2 = trimmed.match(/^##\s+(.+)$/);
    if (h2) { out.push(`\\section{${processLine(h2[1])}}`); i++; continue; }
    const h3 = trimmed.match(/^###\s+(.+)$/);
    if (h3) { out.push(`\\subsection{${processLine(h3[1])}}`); i++; continue; }

    // Mermaid
    if (trimmed.startsWith("```mermaid")) {
      out.push(`% [mermaid diagram omitted]`);
      i++;
      while (i < lines.length && !lines[i].trim().startsWith("```")) i++;
      i++;
      continue;
    }

    // Code block
    if (trimmed.startsWith("```")) {
      i++;
      out.push("\\begin{verbatim}");
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        out.push(lines[i]);
        i++;
      }
      out.push("\\end{verbatim}");
      i++;
      continue;
    }

    // Regular text
    out.push(processLine(trimmed));
    i++;
  }

  return out.join("\n") + "\n";
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);
const toStdout = args.includes("--stdout");
const filter = args.find((a) => !a.startsWith("--"));

const files = readdirSync(contentDir)
  .filter((f) => f.endsWith(".md"))
  .filter((f) => !filter || f.includes(filter))
  .sort();

if (files.length === 0) {
  console.error(`No matching files found${filter ? ` for "${filter}"` : ""}`);
  process.exit(1);
}

if (!toStdout) {
  mkdirSync(outDir, { recursive: true });
}

for (const file of files) {
  labelCounter = 0;
  const fullPath = path.join(contentDir, file);
  const tex = convertFile(fullPath);

  if (toStdout) {
    console.log(`%% === ${file} ===`);
    console.log(tex);
  } else {
    const outFile = path.join(outDir, file.replace(/\.md$/, ".tex"));
    writeFileSync(outFile, tex, "utf8");
  }
}

if (!toStdout) {
  console.log(`Converted ${files.length} files → ${outDir}/`);
}
