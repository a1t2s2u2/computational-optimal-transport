#!/usr/bin/env python3
"""Stage 1: Extract structured mathematical blocks from LaTeX source files.

Imports tex2md.TexParser to reuse the existing parsing pipeline and outputs
one JSON record per named block environment (definition, theorem, etc.).
"""

import json
import os
import re
import sys

from tqdm import tqdm

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "seminar", "site", "scripts"))

import tex2md
from tex2md import (
    BLOCK_ENVS,
    TexParser,
    _join_multiline_inline_math,
    render_nodes,
    strip_comments,
)

SOURCE_FILES = [
    # Primary seminar content (Japanese, highest quality)
    ("seminar/tex/ch01_preliminaries.tex", "準備"),
    ("seminar/tex/ch02_ot_foundations.tex", "OT の基礎理論"),
    ("seminar/tex/ch03_algorithmic_foundations.tex", "アルゴリズムの基礎"),
    ("seminar/tex/ch04_entropic_regularization.tex", "エントロピー正則化"),
    ("seminar/tex/ch05_vae_geodesic.tex", "VAE と測地線"),
    # Cuturi-Peyré Japanese translation (supplementary)
    ("seminar/cuturi/translation/01_introduction.tex", "導入（翻訳）"),
    ("seminar/cuturi/translation/02_theoretical_foundations.tex", "理論的基礎（翻訳）"),
    ("seminar/cuturi/translation/03_algorithmic_foundations.tex", "アルゴリズム（翻訳）"),
    ("seminar/cuturi/translation/04_entropic_regularization.tex", "エントロピー正則化（翻訳）"),
]

OUTPUT_PATH = os.path.join(REPO_ROOT, "llm", "data", "raw", "blocks.jsonl")
# How many preceding text/math nodes to keep as context for each block.
CONTEXT_WINDOW = 4


def extract_raw_blocks(source_content: str) -> dict:
    """Return {(env_name, title): (body_raw, proof_raw)} by scanning raw TeX."""
    result = {}
    for m in re.finditer(r"\\begin\{(\w+)\}\{(.+?)\}\{(.+?)\}", source_content):
        env_name = m.group(1)
        title = m.group(2).strip()
        if env_name not in BLOCK_ENVS:
            continue
        start = m.end()
        end_m = re.search(
            rf"\\end\{{{re.escape(env_name)}\}}", source_content[start:]
        )
        if not end_m:
            continue
        body_raw = source_content[start : start + end_m.start()].strip()
        after_end = source_content[start + end_m.end() :]
        proof_m = re.match(
            r"\s*\\begin\{proof\}(.*?)\\end\{proof\}", after_end, re.DOTALL
        )
        proof_raw = proof_m.group(1).strip() if proof_m else None
        result[(env_name, title)] = (body_raw, proof_raw)
    return result


def process_file(tex_path: str, chapter: str) -> list[dict]:
    if not os.path.exists(tex_path):
        print(f"  SKIP (not found): {tex_path}")
        return []

    with open(tex_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    raw_map = extract_raw_blocks(raw_content)

    lines = [strip_comments(line) for line in raw_content.splitlines()]
    lines = _join_multiline_inline_math(lines)

    parser = TexParser(lines)
    nodes = parser.parse()

    blocks = []
    section = ""
    subsection = ""
    context_buf: list = []

    for node in nodes:
        kind = node[0]
        if kind == "section":
            section = node[1]
            subsection = ""
            context_buf.clear()
        elif kind == "subsection":
            subsection = node[1]
            context_buf.clear()
        elif kind in ("text", "display_math", "align"):
            context_buf.append(node)
            if len(context_buf) > CONTEXT_WINDOW:
                context_buf.pop(0)
        elif kind == "block":
            _, env_name, title, body_nodes, proof_nodes = node

            body_lines = render_nodes(body_nodes)
            body_md = "\n".join(body_lines).strip()

            proof_md = None
            if proof_nodes is not None:
                proof_lines = render_nodes(proof_nodes)
                proof_md = "\n".join(proof_lines).strip() or None

            ctx_lines = render_nodes(list(context_buf))
            context_before_md = "\n".join(ctx_lines).strip()

            raw_body, raw_proof = raw_map.get((env_name, title), ("", None))

            label_m = re.search(
                rf"\\begin\{{{re.escape(env_name)}\}}\{{{re.escape(title)}\}}\{{([^}}]+)\}}",
                raw_content,
            )
            label = label_m.group(1) if label_m else ""

            blocks.append(
                {
                    "source_file": os.path.relpath(tex_path, REPO_ROOT),
                    "chapter": chapter,
                    "section": section,
                    "subsection": subsection,
                    "env": env_name,
                    "title": title,
                    "label": label,
                    "body_md": body_md,
                    "proof_md": proof_md,
                    "body_raw": raw_body,
                    "proof_raw": raw_proof,
                    "context_before_md": context_before_md,
                }
            )
            context_buf.clear()

    return blocks


def main() -> None:
    # Populate label map so render_nodes can resolve \ref{} citations.
    tex2md.LABEL_MAP = tex2md.build_label_map()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    total = 0
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for rel_path, chapter in tqdm(SOURCE_FILES, desc="Extracting", unit="file"):
            tex_path = os.path.join(REPO_ROOT, rel_path)
            blocks = process_file(tex_path, chapter)
            for b in blocks:
                f.write(json.dumps(b, ensure_ascii=False) + "\n")
            tqdm.write(f"  {rel_path}: {len(blocks)} blocks")
            total += len(blocks)

    print(f"\nTotal: {total} blocks → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
