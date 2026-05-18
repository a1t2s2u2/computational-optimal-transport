#!/usr/bin/env python3
"""Convert TeX seminar chapter files into site content markdown files."""

import glob
import os
import re

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SEMINAR_DIR = os.path.join(REPO_ROOT, "seminar", "tex")
CONTENT_DIR = os.path.join(REPO_ROOT, "seminar", "site", "content")

CHAPTERS = [
    ("ch01_preliminaries.tex", "01-preliminaries.md", {
        "id": "preliminaries",
        "nav": "準備",
        "eyebrow": "1. Foundations",
        "title": "準備",
    }),
    ("ch02_ot_foundations.tex", "02-ot-foundations.md", {
        "id": "ot-foundations",
        "nav": "Monge と Kantorovich",
        "eyebrow": "2. OT Foundations",
        "title": "Optimal Transport の基礎理論",
    }),
    ("ch03_algorithmic_foundations.tex", "03-algorithms.md", {
        "id": "algorithms",
        "nav": "アルゴリズムの基礎",
        "eyebrow": "3. Algorithms",
        "title": "アルゴリズムの基礎",
    }),
    ("ch04_entropic_regularization.tex", "04-entropic.md", {
        "id": "entropic",
        "nav": "エントロピー正則化",
        "eyebrow": "4. Entropic Regularization",
        "title": "エントロピー正則化と Sinkhorn アルゴリズム",
    }),
    # ch05 は vae-geodesic.html で独立レンダリングするため変換対象外
]

# Named block environments and their markdown mappings.
# (env_name, container_class, heading_prefix)
BLOCK_ENVS = {
    "definition": ("definition", "Def"),
    "claim":      ("theorem",    "Clm"),
    "theorem":    ("theorem",    "Thm"),
    "proposition":("theorem",    "Prop"),
    "remark":     ("fact",       "Rem"),
    "example":    ("fact accent","Ex"),
}

LABEL_PREFIX_MAP = {
    "def": "Def",
    "clm": "Clm",
    "thm": "Thm",
    "prop": "Prop",
    "rem": "Rem",
    "ex": "Ex",
}

_JP_TO_ABBREV = {
    "定義": "Def", "主張": "Clm", "命題": "Prop",
    "定理": "Thm", "例": "Ex", "注意": "Rem", "Claim": "Clm",
}

ENV_TO_PREFIX = {
    "definition": "def",
    "claim": "clm",
    "theorem": "thm",
    "proposition": "prop",
    "remark": "rem",
    "example": "ex",
}

LABEL_MAP = {}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def strip_comments(line: str) -> str:
    """Remove TeX line comments (% ...), preserving escaped \\%."""
    result = []
    i = 0
    while i < len(line):
        if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        result.append(line[i])
        i += 1
    return "".join(result).rstrip()


def convert_inline_math(text: str) -> str:
    r"""Convert $...$ to \(...\), but leave $$...$$ alone (shouldn't appear)."""
    # We need to be careful not to match \$ or $$ .
    # Strategy: find $ that is not preceded by \ and not followed by $,
    # then pair them up.
    parts = []
    i = 0
    in_math = False
    while i < len(text):
        if text[i] == "$" and (i == 0 or text[i - 1] != "\\"):
            if in_math:
                parts.append("\\)")
                in_math = False
            else:
                parts.append("\\(")
                in_math = True
            i += 1
        else:
            parts.append(text[i])
            i += 1
    # If we ended with an unclosed math, revert (multi-line $ shouldn't happen
    # after line-joining, but be safe)
    if in_math:
        return text
    return "".join(parts)


def convert_text_commands(text: str) -> str:
    r"""Convert \textbf{X} -> **X**, \textit{X} -> *X*.
    Handles one level of nested braces (e.g. \textbf{...\mathbf{P}...})."""
    nested = r"(?:[^{}]|\{[^{}]*\})*"
    text = re.sub(rf"\\textbf\{{({nested})\}}", r"**\1**", text)
    text = re.sub(rf"\\textit\{{({nested})\}}", r"*\1*", text)
    return text


def strip_label(text: str) -> str:
    r"""Remove \label{...} commands."""
    return re.sub(r"\\label\{[^}]*\}", "", text)


def strip_ref(text: str) -> str:
    r"""Remove \ref{...} commands and clean up surrounding artifacts."""
    # 第~\ref{ch:...}~章 → (remove, chapters have no numbers on site)
    text = re.sub(r"第~?\\ref\{[^}]*\}~?章", "", text)
    # §\ref{sec:...} → (remove)
    text = re.sub(r"§~?\\ref\{[^}]*\}", "", text)
    # General \ref with optional preceding ~
    text = re.sub(r"~?\\ref\{[^}]*\}", "", text)
    # Clean up double spaces
    text = re.sub(r"  +", " ", text)
    # Remove empty parenthetical refs: （ ） or (  )
    text = re.sub(r"（\s*）", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    return text


def _extract_brace_arg(text: str, start: int) -> tuple[str, int] | None:
    """Extract a brace-balanced {…} argument starting at *start*.
    Returns (content, end_index) or None if *start* is not '{'."""
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    return None


def build_label_map():
    """Scan all TeX chapter files and build a map: 'prefix:label' -> title."""
    label_map = {}
    for tex_file, _, _ in CHAPTERS:
        tex_path = os.path.join(SEMINAR_DIR, tex_file)
        if not os.path.exists(tex_path):
            continue
        with open(tex_path, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r"\\begin\{(\w+)\}", content):
            env_name = m.group(1)
            if env_name not in ENV_TO_PREFIX:
                continue
            pos = m.end()
            title_result = _extract_brace_arg(content, pos)
            if title_result is None:
                continue
            title, pos = title_result
            label_result = _extract_brace_arg(content, pos)
            if label_result is None:
                continue
            label, _ = label_result
            prefix = ENV_TO_PREFIX[env_name]
            label_map[f"{prefix}:{label}"] = title
    return label_map


def convert_refs(text: str) -> str:
    r"""Convert \ref{...} to clickable [ref:display|name] links."""
    text = re.sub(r"第~?\\ref\{ch:[^}]*\}~?章", "本章", text)
    text = re.sub(r"§~?\\ref\{sec:[^}]*\}", "本節", text)
    text = re.sub(r"Algorithm~?\\ref\{alg:[^}]*\}", "アルゴリズム", text)

    def _replace_typed(m):
        label = m.group(2)
        title = LABEL_MAP.get(label)
        if not title:
            return ""
        prefix = label.split(":")[0] if ":" in label else ""
        abbrev = LABEL_PREFIX_MAP.get(prefix) or _JP_TO_ABBREV.get(m.group(1), m.group(1))
        return f"[ref:{abbrev}: {title}|{title}]"

    text = re.sub(
        r"(定義|主張|命題|定理|例|注意|Claim|正則化問題)~?\\ref\{([^}]+)\}",
        lambda m: _replace_typed(m),
        text,
    )

    def _replace_bare(m):
        label = m.group(1)
        title = LABEL_MAP.get(label)
        if not title:
            return ""
        prefix = label.split(":")[0] if ":" in label else ""
        type_name = LABEL_PREFIX_MAP.get(prefix, "")
        display = f"{type_name}: {title}" if type_name else title
        return f"[ref:{display}|{title}]"

    text = re.sub(r"~?\\ref\{([^}]+)\}", _replace_bare, text)

    text = re.sub(r"  +", " ", text)
    text = re.sub(r"（\s*）", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    return text


def convert_tilde(text: str) -> str:
    """Convert non-breaking space ~ to regular space."""
    return text.replace("~", " ")


def convert_paragraph(text: str) -> str:
    r"""Convert \paragraph{Title.} to **Title.** on its own line."""
    return re.sub(r"\\paragraph\{([^}]*)\}", r"\n**\1**\n", text)


def apply_inline_conversions(text: str, convert_references: bool = True) -> str:
    """Apply all inline-level conversions to a line of text."""
    text = strip_label(text)
    if convert_references and LABEL_MAP:
        text = convert_refs(text)
    else:
        text = strip_ref(text)
    text = convert_tilde(text)
    text = convert_text_commands(text)
    text = convert_paragraph(text)
    text = convert_inline_math(text)
    return text


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


class TexParser:
    """Parse a TeX chapter file into a list of content nodes."""

    def __init__(self, lines):
        self.lines = lines
        self.pos = 0

    def at_end(self):
        return self.pos >= len(self.lines)

    def peek(self):
        if self.at_end():
            return ""
        return self.lines[self.pos]

    def advance(self):
        line = self.lines[self.pos]
        self.pos += 1
        return line

    def parse(self):
        """Return a list of content nodes."""
        nodes = []
        self._parse_body(nodes, stop_env=None)
        return nodes

    def _parse_body(self, nodes, stop_env):
        """Parse body content, appending nodes, until \\end{stop_env} or EOF."""
        while not self.at_end():
            line = self.peek()
            stripped = line.strip()

            # Check for end of enclosing environment
            if stop_env and stripped == f"\\end{{{stop_env}}}":
                self.advance()
                return

            # Skip blank lines (emit paragraph break)
            if not stripped:
                self.advance()
                # Collapse multiple blank lines
                while not self.at_end() and not self.peek().strip():
                    self.advance()
                nodes.append(("blank",))
                continue

            # \demohint{NAME}  →  emit a demo block marker for the site
            m_demo = re.match(r"\\demohint\{([^}]+)\}", stripped)
            if m_demo:
                self.advance()
                nodes.append(("demo", m_demo.group(1)))
                continue

            # Skip \chapter
            if stripped.startswith("\\chapter{"):
                self.advance()
                # Also skip label if next line
                if not self.at_end() and self.peek().strip().startswith("\\label{"):
                    self.advance()
                continue

            # Section headings
            m = re.match(r"\\section\{(.+)\}", stripped)
            if m:
                self.advance()
                # Skip label on next line if present
                if not self.at_end() and self.peek().strip().startswith("\\label{"):
                    self.advance()
                nodes.append(("section", m.group(1)))
                continue

            m = re.match(r"\\subsection\{(.+)\}", stripped)
            if m:
                self.advance()
                if not self.at_end() and self.peek().strip().startswith("\\label{"):
                    self.advance()
                nodes.append(("subsection", m.group(1)))
                continue

            m = re.match(r"\\subsubsection\{(.+)\}", stripped)
            if m:
                self.advance()
                if not self.at_end() and self.peek().strip().startswith("\\label{"):
                    self.advance()
                nodes.append(("subsubsection", m.group(1)))
                continue

            # Skip figure environments (including those with optional args)
            if re.match(r"\\begin\{figure\}", stripped):
                self._skip_environment("figure")
                continue

            # Skip standalone tikzpicture (not inside figure)
            if re.match(r"\\begin\{tikzpicture\}", stripped):
                self._skip_environment("tikzpicture")
                continue

            # Skip standalone center that contains tikzpicture or tabular
            if stripped == "\\begin{center}":
                self._skip_environment("center")
                continue

            # Skip algorithm environments
            if re.match(r"\\begin\{algorithm\}", stripped):
                self._skip_environment("algorithm")
                continue

            # Named block environments: definition, claim, theorem, etc.
            m = re.match(r"\\begin\{(\w+)\}\{(.+?)\}\{(.+?)\}", stripped)
            if m and m.group(1) in BLOCK_ENVS:
                env_name = m.group(1)
                title = m.group(2)
                # label = m.group(3)  -- not used in output
                self.advance()
                block_nodes = []
                self._parse_body(block_nodes, stop_env=env_name)
                # Check if next thing is a proof that belongs to this block
                proof_nodes = self._try_parse_proof()
                nodes.append(("block", env_name, title, block_nodes, proof_nodes))
                continue

            # memo* environment -> fact block
            if stripped == "\\begin{memo*}":
                self.advance()
                block_nodes = []
                self._parse_body(block_nodes, stop_env="memo*")
                nodes.append(("memo", block_nodes))
                continue

            # Standalone proof (not following a block -- rare but possible)
            if stripped == "\\begin{proof}":
                self.advance()
                proof_nodes = []
                self._parse_body(proof_nodes, stop_env="proof")
                nodes.append(("standalone_proof", proof_nodes))
                continue

            # Display math: \[ ... \]
            if stripped.startswith("\\["):
                math_lines = self._collect_display_math()
                nodes.append(("display_math", math_lines))
                continue

            # align* environment
            if stripped.startswith("\\begin{align*}"):
                math_lines = self._collect_environment("align*")
                nodes.append(("align", math_lines))
                continue

            # enumerate
            if stripped == "\\begin{enumerate}":
                self.advance()
                items = self._collect_list_items("enumerate")
                nodes.append(("enumerate", items))
                continue

            # itemize
            if stripped == "\\begin{itemize}":
                self.advance()
                items = self._collect_list_items("itemize")
                nodes.append(("itemize", items))
                continue

            # Skip vertical spacing commands
            if re.match(r"\\(medskip|bigskip|smallskip|vspace\*?\{[^}]*\})\s*$", stripped):
                self.advance()
                continue

            # Regular text line
            self.advance()
            nodes.append(("text", line))

        # If we reach here and stop_env was set, the environment was never closed.
        # This shouldn't happen in well-formed TeX.

    def _skip_environment(self, env_name):
        """Skip past \\end{env_name}, handling nesting."""
        depth = 1
        self.advance()  # consume \begin line
        while not self.at_end():
            line = self.peek().strip()
            if re.match(rf"\\begin\{{{env_name}\}}", line):
                depth += 1
            if line == f"\\end{{{env_name}}}" or re.match(rf"\\end\{{{env_name}\}}", line):
                depth -= 1
                if depth == 0:
                    self.advance()
                    # Also skip \caption and \label lines that follow
                    while not self.at_end():
                        nxt = self.peek().strip()
                        if nxt.startswith("\\caption{") or nxt.startswith("\\label{"):
                            self.advance()
                        else:
                            break
                    return
            self.advance()

    def _try_parse_proof(self):
        """If the next non-blank content is \\begin{proof}, parse it."""
        saved_pos = self.pos
        # Skip blank lines
        while not self.at_end() and not self.peek().strip():
            self.pos += 1
        if not self.at_end() and self.peek().strip() == "\\begin{proof}":
            self.advance()
            proof_nodes = []
            self._parse_body(proof_nodes, stop_env="proof")
            return proof_nodes
        # Not a proof -- restore position
        self.pos = saved_pos
        return None

    def _collect_display_math(self):
        """Collect lines of display math from \\[ to \\]."""
        lines = []
        first_line = self.advance().strip()
        # Check if \[ and \] are on the same line
        if "\\]" in first_line:
            content = first_line.replace("\\[", "").replace("\\]", "").strip()
            return [content]
        # \[ is on its own line (or has content after it)
        content_after = first_line.replace("\\[", "").strip()
        if content_after:
            lines.append(content_after)
        while not self.at_end():
            line = self.advance()
            if "\\]" in line:
                content_before = line.replace("\\]", "").strip()
                if content_before:
                    lines.append(content_before)
                break
            lines.append(line.rstrip())
        return lines

    def _collect_environment(self, env_name):
        """Collect all lines inside \\begin{env_name}...\\end{env_name}."""
        lines = []
        first_line = self.advance().strip()
        # Content after \begin{env_name} on same line
        # Use re.escape for env_name since it may contain * (e.g., align*)
        esc = re.escape(env_name)
        after = re.sub(rf"\\begin\{{{esc}\}}", "", first_line).strip()
        if after:
            lines.append(after)
        end_tag = f"\\end{{{env_name}}}"
        while not self.at_end():
            line = self.advance()
            if end_tag in line:
                before = line.replace(end_tag, "").strip()
                if before:
                    lines.append(before)
                break
            lines.append(line.rstrip())
        return lines

    def _collect_list_items(self, env_name):
        """Collect list items until \\end{env_name}. Returns list of (label, node_list)."""
        items = []
        current_label = None
        current_nodes = None

        def flush_item():
            nonlocal current_label, current_nodes
            if current_nodes is not None:
                items.append((current_label, current_nodes))
            current_label = None
            current_nodes = None

        while not self.at_end():
            stripped = self.peek().strip()
            if stripped == f"\\end{{{env_name}}}":
                self.advance()
                flush_item()
                break

            m = re.match(r"\\item(?:\[([^\]]*)\])?\s*(.*)", stripped)
            if m:
                flush_item()
                current_label = m.group(1)
                rest = m.group(2).strip()
                current_nodes = []
                if rest:
                    current_nodes.append(("text", rest))
                self.advance()
            else:
                if current_nodes is None:
                    current_nodes = []
                self._parse_item_content(current_nodes, env_name)

        return items

    def _parse_item_content(self, nodes, list_env_name):
        """Parse a single piece of content within a list item."""
        stripped = self.peek().strip()

        if not stripped:
            self.advance()
            nodes.append(("blank",))
            return

        if stripped.startswith("\\["):
            math_lines = self._collect_display_math()
            nodes.append(("display_math", math_lines))
            return

        if stripped == "\\begin{align*}":
            math_lines = self._collect_environment("align*")
            nodes.append(("align", math_lines))
            return

        if stripped == "\\begin{enumerate}":
            self.advance()
            items = self._collect_list_items("enumerate")
            nodes.append(("enumerate", items))
            return

        if stripped == "\\begin{itemize}":
            self.advance()
            items = self._collect_list_items("itemize")
            nodes.append(("itemize", items))
            return

        if re.match(r"\\begin\{(cases|pmatrix|bmatrix)", stripped):
            pass  # fall through to text

        nodes.append(("text", self.advance()))


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _render_list_item(output, prefix, item_nodes):
    """Render a list item preserving content order (text, math, text, ...)."""
    first_text = True
    text_buf = []

    def flush_text():
        nonlocal first_text
        if not text_buf:
            return
        text = " ".join(t for t in text_buf if t)
        text = apply_inline_conversions(text)
        if text:
            if first_text:
                output.append(f"{prefix}{text}")
                first_text = False
            else:
                output.append(text)
        text_buf.clear()

    for n in item_nodes:
        if n[0] == "text":
            text_buf.append(n[1].strip())
        elif n[0] == "blank":
            continue
        else:
            flush_text()
            block_lines = render_nodes([n])
            for bl in block_lines:
                output.append(bl)

    flush_text()
    if first_text:
        output.append(prefix.rstrip())


def render_nodes(nodes, indent=0):
    """Render parsed nodes into markdown lines."""
    output = []

    for node in nodes:
        kind = node[0]

        if kind == "blank":
            output.append("")
            continue

        if kind == "section":
            title = apply_inline_conversions(node[1])
            output.append(f"## {title}")
            output.append("")
            continue

        if kind == "subsection":
            title = apply_inline_conversions(node[1])
            output.append(f"### {title}")
            output.append("")
            continue

        if kind == "subsubsection":
            title = apply_inline_conversions(node[1])
            output.append(f"**{title}**")
            output.append("")
            continue

        if kind == "demo":
            output.append(f":::demo {node[1]}")
            output.append("")
            continue

        if kind == "block":
            _, env_name, title, body_nodes, proof_nodes = node
            container_class, prefix = BLOCK_ENVS[env_name]
            output.append(f":::{container_class}")
            if prefix:
                heading = f"### {prefix}: {apply_inline_conversions(title)}"
            else:
                heading = f"### {apply_inline_conversions(title)}"
            output.append(heading)
            # Render body
            body_lines = render_nodes(body_nodes)
            body_text = "\n".join(body_lines).strip()
            if body_text:
                output.append("")
                output.append(body_text)
            # Render proof if present (nested inside the block)
            if proof_nodes is not None:
                output.append("")
                output.append(":::details-embedded 証明")
                proof_lines = render_nodes(proof_nodes)
                proof_text = "\n".join(proof_lines).strip()
                if proof_text:
                    output.append(proof_text)
                output.append(":::")
            output.append(":::")
            output.append("")
            continue

        if kind == "memo":
            body_nodes = node[1]
            output.append(":::fact")
            body_lines = render_nodes(body_nodes)
            body_text = "\n".join(body_lines).strip()
            if body_text:
                output.append(body_text)
            output.append(":::")
            output.append("")
            continue

        if kind == "standalone_proof":
            proof_nodes = node[1]
            output.append(":::details-embedded 証明")
            proof_lines = render_nodes(proof_nodes)
            proof_text = "\n".join(proof_lines).strip()
            if proof_text:
                output.append(proof_text)
            output.append(":::")
            output.append("")
            continue

        if kind == "display_math":
            math_lines = node[1]
            output.append("")
            output.append("\\[")
            for ml in math_lines:
                output.append(apply_inline_conversions(ml, convert_references=False))
            output.append("\\]")
            output.append("")
            continue

        if kind == "align":
            math_lines = node[1]
            output.append("")
            output.append("\\[\\begin{aligned}")
            for ml in math_lines:
                output.append(apply_inline_conversions(ml, convert_references=False))
            output.append("\\end{aligned}\\]")
            output.append("")
            continue

        if kind == "enumerate":
            items = node[1]
            output.append("")
            for idx, (label, item_nodes) in enumerate(items, 1):
                prefix = f"{label} " if label else f"{idx}. "
                _render_list_item(output, prefix, item_nodes)
            output.append("")
            continue

        if kind == "itemize":
            items = node[1]
            output.append("")
            for label, item_nodes in items:
                prefix = f"{label} " if label else "- "
                _render_list_item(output, prefix, item_nodes)
            output.append("")
            continue

        if kind == "text":
            text = node[1]
            # Strip leading TeX indentation (typically 2-space indent inside envs)
            text = text.strip()
            if not text:
                continue
            text = apply_inline_conversions(text)
            output.append(text)
            continue

    return output


def clean_output(text: str) -> str:
    """Post-process the rendered markdown: collapse blank lines, trim."""
    # Remove trailing whitespace on each line
    lines = [line.rstrip() for line in text.split("\n")]
    # Collapse 3+ consecutive blank lines into 2
    cleaned = []
    blank_count = 0
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned.append(line)
        else:
            blank_count = 0
            cleaned.append(line)
    # Strip leading/trailing blank lines
    result = "\n".join(cleaned).strip()
    # Ensure file ends with newline
    return result + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _count_unescaped_dollars(line):
    """Count unescaped $ signs in a line (not inside \\[ \\] blocks)."""
    count = 0
    for i, ch in enumerate(line):
        if ch == "$" and (i == 0 or line[i - 1] != "\\"):
            count += 1
    return count


def _join_multiline_inline_math(lines):
    """Join lines where $ inline math spans multiple lines."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Don't join inside display math or environments
        if stripped.startswith("\\[") or stripped.startswith("\\begin{"):
            result.append(line)
            i += 1
            continue
        n_dollars = _count_unescaped_dollars(line)
        if n_dollars % 2 == 1:
            # Odd number of $ -- join with next line(s)
            joined = line
            i += 1
            while i < len(lines):
                joined = joined.rstrip() + " " + lines[i].strip()
                n_dollars += _count_unescaped_dollars(lines[i])
                i += 1
                if n_dollars % 2 == 0:
                    break
            result.append(joined)
        else:
            result.append(line)
            i += 1
    return result


def process_chapter(tex_filename, md_filename, frontmatter):
    """Process one chapter: read TeX, parse, render, write markdown."""
    tex_path = os.path.join(SEMINAR_DIR, tex_filename)
    md_path = os.path.join(CONTENT_DIR, md_filename)

    if not os.path.exists(tex_path):
        print(f"  SKIP (not found): {tex_filename}")
        return None

    with open(tex_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Strip comments from each line
    lines = [strip_comments(line.rstrip("\n")) for line in raw_lines]

    # Join multi-line inline math: if a line has an odd number of
    # unescaped $, the inline math spans to the next line(s).
    lines = _join_multiline_inline_math(lines)

    # Parse
    parser = TexParser(lines)
    nodes = parser.parse()

    # Render
    md_lines = render_nodes(nodes)
    body = "\n".join(md_lines)

    # Build frontmatter
    fm = "---\n"
    fm += f"id: {frontmatter['id']}\n"
    fm += f"nav: {frontmatter['nav']}\n"
    fm += f"eyebrow: {frontmatter['eyebrow']}\n"
    fm += f"title: {frontmatter['title']}\n"
    fm += "---\n\n"

    full = fm + body
    full = clean_output(full)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(full)

    # Count blocks
    block_count = sum(1 for n in nodes if n[0] == "block")
    return block_count


def main():
    global LABEL_MAP
    LABEL_MAP = build_label_map()
    print(f"Built label map with {len(LABEL_MAP)} entries")

    # Clean existing markdown files
    existing = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    for f in existing:
        os.remove(f)
    print(f"Cleaned {len(existing)} existing markdown file(s) from {CONTENT_DIR}")
    print()

    total_blocks = 0
    for tex_file, md_file, fm in CHAPTERS:
        print(f"Converting {tex_file} -> {md_file}")
        count = process_chapter(tex_file, md_file, fm)
        if count is not None:
            total_blocks += count
            print(f"  {count} block(s) written")
        print()

    print(f"Done. Generated {len(CHAPTERS)} file(s), {total_blocks} total block(s).")
    generated = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")))
    for f in generated:
        print(f"  {os.path.basename(f)}")


if __name__ == "__main__":
    main()
