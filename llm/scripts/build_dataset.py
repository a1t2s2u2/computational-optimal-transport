#!/usr/bin/env python3
"""Build training dataset purely from LaTeX source — no external API required.

Three complementary formats for mathematical mastery:

  A — CPT (Continued Pre-Training)
      Raw LaTeX text chunks.  Loss computed on ALL tokens.
      Teaches: notation, vocabulary, structure, inter-theorem prose.
      Format: {"text": "...raw LaTeX chunk..."}

  B — Proof completion
      Given a theorem/proposition statement, generate its proof.
      Teaches: deductive reasoning within the seminar's notation.
      Format: {"messages": [system, user=theorem, assistant=proof]}

  C — Block continuation
      Given the raw LaTeX of block N, generate block N+1.
      Teaches: how mathematical exposition is structured and flows.
      Format: {"messages": [system, user=block_N_latex, assistant=block_{N+1}_latex]}

Validation split: ch05 (VAE と測地線) held out entirely; 10% of ch04 sampled.

Usage:
    python llm/scripts/build_dataset.py [--seed 42]
"""

import argparse
import os
import re
import json
import random
import sys

from tqdm import tqdm

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "seminar", "site", "scripts"))

from tex2md import strip_comments, _join_multiline_inline_math

BLOCKS_PATH = os.path.join(REPO_ROOT, "llm", "data", "raw", "blocks.jsonl")
TRAIN_PATH  = os.path.join(REPO_ROOT, "llm", "data", "train.jsonl")
VALID_PATH  = os.path.join(REPO_ROOT, "llm", "data", "valid.jsonl")

# ──────────────────────────────────────────────
# Format A — CPT source files
# ──────────────────────────────────────────────

CPT_FILES = [
    "seminar/tex/ch01_preliminaries.tex",
    "seminar/tex/ch02_ot_foundations.tex",
    "seminar/tex/ch03_algorithmic_foundations.tex",
    "seminar/tex/ch04_entropic_regularization.tex",
    "seminar/tex/ch05_vae_geodesic.tex",
    "seminar/cuturi/translation/01_introduction.tex",
    "seminar/cuturi/translation/02_theoretical_foundations.tex",
    "seminar/cuturi/translation/03_algorithmic_foundations.tex",
    "seminar/cuturi/translation/04_entropic_regularization.tex",
]

# Lines starting with these are preamble / structure directives, not math content.
_SKIP_STARTS = (
    "\\usepackage", "\\documentclass", "\\input{", "\\begin{document}",
    "\\end{document}", "\\maketitle", "\\tableofcontents", "\\bibliography",
    "\\bibliographystyle", "\\newcommand", "\\renewcommand", "\\DeclareMathOperator",
    "\\setlength", "\\geometry", "\\pagestyle", "\\hypersetup",
)

CPT_CHUNK_CHARS = 1400   # target characters per CPT chunk (~500 tokens)
CPT_MIN_CHARS   = 200    # discard chunks shorter than this

# ──────────────────────────────────────────────
# Format B — Proof completion
# ──────────────────────────────────────────────

ENV_JP = {
    "definition":  "定義",
    "theorem":     "定理",
    "proposition": "命題",
    "claim":       "主張",
    "remark":      "注意",
    "example":     "例",
}

SYSTEM_CPT = (
    "あなたは計算的最適輸送の数学者です。"
    "与えられた LaTeX テキストの続きを，同じ文体・記法で記述してください。"
)

SYSTEM_PROOF = (
    "あなたは計算的最適輸送の専門数学者です。"
    "セミナーの LaTeX マクロ（\\MKD, \\CouplingsD, \\Couplings, \\Hb, \\KLD, "
    "\\inner, \\defeq, \\X, \\Y 等）を用いて与えられた定理・命題を厳密に証明してください。"
    "インライン数式は $...$，ディスプレイ数式は \\[...\\] で記述してください。"
)

PROOF_MIN_CHARS = 80  # discard proofs shorter than this

# ──────────────────────────────────────────────
# Format C — Block continuation
# ──────────────────────────────────────────────

SYSTEM_CONTINUATION = (
    "あなたは計算的最適輸送のセミナーノートを LaTeX 形式で執筆する数学者です。"
    "前のブロックに続く定義・定理・命題・注意を，tcolorbox 環境形式"
    "（\\begin{definition}{タイトル}{ラベル}...\\end{definition} 等）で記述してください。"
)

# ──────────────────────────────────────────────
# Validation split
# ──────────────────────────────────────────────

VALID_CH_FULL   = "ch05_vae_geodesic"   # entire chapter as validation
VALID_CH_SAMPLE = "ch04_entropic"        # 10% of this chapter
VALID_SAMPLE_RATE = 0.10

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def has_unclosed_dollars(text: str) -> bool:
    count = sum(
        1 for i, c in enumerate(text)
        if c == "$" and (i == 0 or text[i - 1] != "\\")
    )
    return count % 2 != 0


def is_valid_source(source_label: str, valid_ch04_labels: set) -> bool:
    if VALID_CH_FULL in source_label:
        return True
    if VALID_CH_SAMPLE in source_label and source_label in valid_ch04_labels:
        return True
    return False


# ──────────────────────────────────────────────
# Format A: CPT chunks
# ──────────────────────────────────────────────

def build_cpt_chunks(tex_path: str) -> list[dict]:
    with open(tex_path, "r", encoding="utf-8") as f:
        raw = f.read()

    lines = [strip_comments(line) for line in raw.splitlines()]
    lines = _join_multiline_inline_math(lines)

    # Drop preamble / structural directives
    filtered = []
    for line in lines:
        s = line.strip()
        if any(s.startswith(p) for p in _SKIP_STARTS):
            continue
        filtered.append(line)

    text = "\n".join(filtered)

    # Split at paragraph boundaries
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    # Accumulate paragraphs into chunks, then split each chunk into
    # context (user) / continuation (assistant) at the midpoint paragraph.
    chunks = []
    buf: list[str] = []
    buf_len = 0

    def _emit(buf: list[str]) -> None:
        if not buf:
            return
        full = "\n\n".join(buf)
        if len(full) < CPT_MIN_CHARS:
            return
        # Split roughly at 60% into context and continuation.
        mid = max(1, round(len(buf) * 0.6))
        context      = "\n\n".join(buf[:mid])
        continuation = "\n\n".join(buf[mid:])
        if not continuation.strip():
            continuation = context[-200:]  # fallback: last 200 chars as target
            context      = context[:-200]
        chunks.append({
            "_src": tex_path,
            "_format": "cpt",
            "messages": [
                {"role": "system",    "content": SYSTEM_CPT},
                {"role": "user",      "content": context},
                {"role": "assistant", "content": continuation},
            ],
        })

    for para in paragraphs:
        if buf_len + len(para) > CPT_CHUNK_CHARS and buf:
            _emit(buf)
            buf = []
            buf_len = 0
        buf.append(para)
        buf_len += len(para)

    _emit(buf)
    return chunks


# ──────────────────────────────────────────────
# Format B: Proof completion
# ──────────────────────────────────────────────

def build_proof_pairs(blocks: list[dict]) -> list[dict]:
    pairs = []
    for b in tqdm(blocks, desc="Proof pairs", unit="block", leave=False):
        if b["env"] not in ("theorem", "proposition", "claim"):
            continue
        proof = b.get("proof_raw", "")
        body  = b.get("body_raw", "")
        if not proof or len(proof) < PROOF_MIN_CHARS:
            continue
        if has_unclosed_dollars(proof):
            continue

        env_jp = ENV_JP.get(b["env"], b["env"])
        user_content = (
            f"**{env_jp}**（{b['chapter']} / {b.get('section', '')}）\n\n"
            f"「{b['title']}」\n\n"
            f"{body}\n\n"
            f"この{env_jp}を証明してください。"
        )
        pairs.append({
            "_src": b["source_file"],
            "_format": "proof_completion",
            "messages": [
                {"role": "system",    "content": SYSTEM_PROOF},
                {"role": "user",      "content": user_content},
                {"role": "assistant", "content": proof},
            ],
        })
    return pairs


# ──────────────────────────────────────────────
# Format C: Block continuation
# ──────────────────────────────────────────────

def build_continuation_pairs(blocks: list[dict]) -> list[dict]:
    pairs = []
    for i in tqdm(range(len(blocks) - 1), desc="Continuation pairs", unit="pair", leave=False):
        a, b = blocks[i], blocks[i + 1]
        if a["chapter"] != b["chapter"]:
            continue
        if not a.get("body_raw") or not b.get("body_raw"):
            continue

        def _block_tex(bl: dict) -> str:
            env, title, label = bl["env"], bl["title"], bl.get("label", "")
            tex = (
                f"\\begin{{{env}}}{{{title}}}{{{label}}}\n"
                f"{bl['body_raw']}\n"
                f"\\end{{{env}}}"
            )
            if bl.get("proof_raw"):
                tex += f"\n\\begin{{proof}}\n{bl['proof_raw']}\n\\end{{proof}}"
            return tex

        prev_tex = _block_tex(a)
        next_tex = _block_tex(b)
        env_jp   = ENV_JP.get(b["env"], b["env"])

        user_content = (
            f"以下の LaTeX ブロックの後に続く{env_jp}「{b['title']}」を書いてください。\n\n"
            f"```latex\n{prev_tex}\n```"
        )
        pairs.append({
            "_src": b["source_file"],
            "_format": "block_continuation",
            "messages": [
                {"role": "system",    "content": SYSTEM_CONTINUATION},
                {"role": "user",      "content": user_content},
                {"role": "assistant", "content": f"```latex\n{next_tex}\n```"},
            ],
        })
    return pairs


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

def main(seed: int = 42) -> None:
    rng = random.Random(seed)

    # ── Stage 1 output ──────────────────────────
    with open(BLOCKS_PATH, "r", encoding="utf-8") as f:
        blocks = [json.loads(line) for line in f]
    print(f"Loaded {len(blocks)} blocks")

    # ── Format A: CPT ───────────────────────────
    cpt_records: list[dict] = []
    for rel_path in tqdm(CPT_FILES, desc="CPT chunks", unit="file"):
        tex_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.exists(tex_path):
            tqdm.write(f"  skip (not found): {rel_path}")
            continue
        chunks = build_cpt_chunks(tex_path)
        cpt_records.extend(chunks)
        tqdm.write(f"  {rel_path}: {len(chunks)} chunks")
    print(f"Format A (CPT): {len(cpt_records)} chunks total")

    # ── Format B: Proof completion ───────────────
    proof_records = build_proof_pairs(blocks)
    print(f"Format B (proof completion): {len(proof_records)} pairs")

    # ── Format C: Block continuation ────────────
    cont_records = build_continuation_pairs(blocks)
    print(f"Format C (block continuation): {len(cont_records)} pairs")

    # ── Determine validation labels ─────────────
    # ch04 labels for 10% sampling
    ch04_src_keys = {
        r["_src"] for r in (proof_records + cont_records)
        if VALID_CH_SAMPLE in r.get("_src", "")
    }
    n_valid_ch04 = max(1, round(len(ch04_src_keys) * VALID_SAMPLE_RATE))
    valid_ch04_src = set(rng.sample(sorted(ch04_src_keys), n_valid_ch04))

    def _is_valid(rec: dict) -> bool:
        src = rec.get("_src", "")
        if VALID_CH_FULL in src:
            return True
        if VALID_CH_SAMPLE in src and src in valid_ch04_src:
            return True
        return False

    # ── Split and write ──────────────────────────
    all_sft = proof_records + cont_records
    rng.shuffle(all_sft)

    train_lines: list[str] = []
    valid_lines: list[str] = []

    # All records now use {"messages": [...]} format for mlx-lm compatibility.
    for rec in cpt_records:
        out = {"messages": rec["messages"]}
        if _is_valid(rec):
            valid_lines.append(json.dumps(out, ensure_ascii=False))
        else:
            train_lines.append(json.dumps(out, ensure_ascii=False))

    for rec in all_sft:
        out = {"messages": rec["messages"]}
        if _is_valid(rec):
            valid_lines.append(json.dumps(out, ensure_ascii=False))
        else:
            train_lines.append(json.dumps(out, ensure_ascii=False))

    # Shuffle training set
    rng.shuffle(train_lines)

    os.makedirs(os.path.dirname(TRAIN_PATH), exist_ok=True)
    with open(TRAIN_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(train_lines) + "\n")
    with open(VALID_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_lines) + "\n")

    # ── Summary ─────────────────────────────────
    n_cpt   = sum(1 for r in cpt_records   if not _is_valid(r))
    n_proof = sum(1 for r in proof_records if not _is_valid(r))
    n_cont  = sum(1 for r in cont_records  if not _is_valid(r))

    print(f"\n{'─'*40}")
    print(f"Train: {len(train_lines):>4}  (CPT {n_cpt}, proof {n_proof}, continuation {n_cont})")
    print(f"Valid: {len(valid_lines):>4}")
    print(f"→ {TRAIN_PATH}")
    print(f"→ {VALID_PATH}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    main(seed=args.seed)
