#!/usr/bin/env python3
"""tex の数学ブロックを走査して依存グラフ (graph.json) を生成する。

既存の tex2md パーサ基盤（seminar/site/scripts/tex2md.py）を再利用する:
  - BLOCK_ENVS / ENV_TO_PREFIX : ブロック環境とラベル接頭辞
  - strip_comments             : 行コメント除去（コメントアウトされた \\ref を数えない）
  - _extract_brace_arg         : 入れ子の波括弧に対応した引数抽出
  - build_label_map / build_chapter_map : ラベル→タイトル, 章ラベル→章題

ブロックごとに以下を抽出する:
  - env / title / label / 章・節・小節
  - body 内の \\ref（statement 依存）と proof 内の \\ref（証明依存）を分離
  - \\blockmeta{...}（space=, uses=, route.X=, lean=）

出力 proofgraph/out/graph.json:
  {nodes, edges, routes, spaces(lattice), stats}
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "seminar", "site", "scripts"))

import tex2md  # noqa: E402
from tex2md import (  # noqa: E402
    BLOCK_ENVS,
    ENV_TO_PREFIX,
    _extract_brace_arg,
    strip_comments,
)

from model import Node, Route, SpaceLattice  # noqa: E402

SEMINAR_TEX = os.path.join(REPO_ROOT, "seminar", "tex")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "out", "graph.json")

# uses/routes の依存として採用する参照接頭辞（ブロックを指すもののみ）。
# ch:/sec:/alg:/eq:/fig: などは依存グラフのノードではないので除外する。
BLOCK_PREFIXES = set(ENV_TO_PREFIX.values())  # {def, clm, thm, prop, rem, ex}

_REF_RE = re.compile(r"\\ref\{([^}]+)\}")
_BLOCKMETA_RE = re.compile(r"\\blockmeta\b")


# ---------------------------------------------------------------------------
# 低レベル走査ヘルパ
# ---------------------------------------------------------------------------

def _strip_all_comments(content: str) -> str:
    return "\n".join(strip_comments(line) for line in content.splitlines())


def _find_matching_end(content: str, env: str, start: int) -> int | None:
    r"""start 以降で env の対応する \end{env} の開始位置を返す（入れ子対応）。"""
    begin = re.compile(r"\\begin\{" + re.escape(env) + r"\}")
    end = re.compile(r"\\end\{" + re.escape(env) + r"\}")
    depth = 1
    i = start
    while i < len(content):
        bm = begin.search(content, i)
        em = end.search(content, i)
        if em is None:
            return None
        if bm is not None and bm.start() < em.start():
            depth += 1
            i = bm.end()
        else:
            depth -= 1
            if depth == 0:
                return em.start()
            i = em.end()
    return None


def _section_index(content: str) -> list:
    """(pos, level, title) のリスト。level は section/subsection/subsubsection。"""
    idx = []
    for m in re.finditer(r"\\(section|subsection|subsubsection)\{", content):
        res = _extract_brace_arg(content, m.end() - 1)
        if res is None:
            continue
        title, _ = res
        idx.append((m.start(), m.group(1), title.strip()))
    return idx


def _context_at(section_idx: list, pos: int) -> tuple:
    section = subsection = ""
    for p, level, title in section_idx:
        if p >= pos:
            break
        if level == "section":
            section, subsection = title, ""
        elif level == "subsection":
            subsection = title
    return section, subsection


def _chapter_title(content: str) -> str:
    m = re.search(r"\\chapter\{", content)
    if not m:
        return ""
    res = _extract_brace_arg(content, m.end() - 1)
    return tex2md._clean_chapter_title(res[0]) if res else ""


def _extract_blockmeta(body: str) -> tuple:
    r"""body から \blockmeta{...} を取り出し、(meta_dict, body_without_meta) を返す。"""
    m = _BLOCKMETA_RE.search(body)
    if not m:
        return {}, body
    brace = body.find("{", m.start())
    if brace == -1:
        return {}, body
    res = _extract_brace_arg(body, brace)  # (arg, pos_after_closing_brace)
    if res is None:
        return {}, body
    arg, end = res
    cleaned = body[: m.start()] + body[end:]   # \blockmeta{...} 全体を除去
    return _parse_meta(arg), cleaned


def _parse_meta(arg: str) -> dict:
    """'space=polish; uses=a,b; route.A=c; lean=x' -> dict。

    値はカンマ区切りでリスト化（lean は文字列のまま）。route.* は別キーで保持。
    """
    meta: dict = {}
    for part in arg.split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, val = part.partition("=")
        key = key.strip()
        val = val.strip()
        if key == "lean":
            meta["lean"] = val
        else:
            items = [v.strip() for v in val.split(",") if v.strip()]
            meta[key] = items
    return meta


def _refs_in(text: str) -> list:
    """text 中の \\ref のうちブロックを指すものを順序を保ってユニーク抽出。"""
    out = []
    seen = set()
    for m in _REF_RE.finditer(text):
        ref = m.group(1).strip()
        prefix = ref.split(":")[0] if ":" in ref else ""
        if prefix not in BLOCK_PREFIXES:
            continue
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


# ---------------------------------------------------------------------------
# ブロック抽出
# ---------------------------------------------------------------------------

def _parse_proofs_after(content: str, pos: int) -> list:
    r"""pos 直後に連続する \begin{proof}[opt]...\end{proof} の本文リストを返す。"""
    proofs = []
    while True:
        m = re.match(r"\s*\\begin\{proof\}(\[[^\]]*\])?", content[pos:])
        if not m:
            break
        body_start = pos + m.end()
        end = _find_matching_end(content, "proof", body_start)
        if end is None:
            break
        proofs.append(content[body_start:end])
        pos = end + len("\\end{proof}")
    return proofs


def extract_file(tex_path: str) -> list:
    with open(tex_path, "r", encoding="utf-8") as f:
        raw = f.read()
    content = _strip_all_comments(raw)
    section_idx = _section_index(content)
    chapter = _chapter_title(content)
    rel = os.path.relpath(tex_path, REPO_ROOT)

    nodes = []
    for m in re.finditer(r"\\begin\{(\w+)\}", content):
        env = m.group(1)
        if env not in BLOCK_ENVS:
            continue
        title_res = _extract_brace_arg(content, m.end())
        if title_res is None:
            continue
        title, after_title = title_res
        label_res = _extract_brace_arg(content, after_title)
        if label_res is None:
            continue
        label, body_start = label_res

        body_end = _find_matching_end(content, env, body_start)
        if body_end is None:
            continue
        body = content[body_start:body_end]
        after = body_end + len(f"\\end{{{env}}}")
        proofs = _parse_proofs_after(content, after)

        meta, body_no_meta = _extract_blockmeta(body)
        section, subsection = _context_at(section_idx, m.start())

        node = _build_node(
            env=env, title=title.strip(), label=label.strip(),
            chapter=chapter, section=section, subsection=subsection,
            source_file=rel, body=body_no_meta, proofs=proofs, meta=meta,
        )
        nodes.append(node)
    return nodes


def _build_node(env, title, label, chapter, section, subsection,
                source_file, body, proofs, meta) -> Node:
    node_id = f"{ENV_TO_PREFIX[env]}:{label}"

    # statement 依存: meta.uses があれば優先、無ければ body の \ref から自動補完
    body_refs = [r for r in _refs_in(body) if r != node_id]
    uses = meta.get("uses") if "uses" in meta else body_refs
    uses = [u for u in dict.fromkeys(uses) if u != node_id]

    # 証明ルート: meta.route.* があれば採用、無ければ proof 本文の \ref から _auto ルート
    routes = []
    route_keys = sorted(k for k in meta if k.startswith("route."))
    if route_keys:
        for k in route_keys:
            deps = [d for d in dict.fromkeys(meta[k]) if d != node_id]
            routes.append(Route(name=k.split(".", 1)[1], deps=deps))
    elif proofs:
        proof_refs = []
        for p in proofs:
            proof_refs.extend(_refs_in(p))
        deps = [d for d in dict.fromkeys(proof_refs) if d != node_id]
        routes.append(Route(name="_auto", deps=deps))

    spaces = meta.get("space", []) or meta.get("spaces", [])

    return Node(
        id=node_id, env=env, title=title,
        chapter=chapter, section=section, subsection=subsection,
        source_file=source_file, spaces=spaces, uses=uses, routes=routes,
        lean=meta.get("lean", ""), has_proof=bool(proofs),
    )


# ---------------------------------------------------------------------------
# グラフ組み立て & 出力
# ---------------------------------------------------------------------------

def build_graph(nodes: list, lattice: SpaceLattice) -> dict:
    node_json = []
    edges = []
    routes_json = []
    for n in nodes:
        node_json.append({
            "id": n.id, "env": n.env, "title": n.title,
            "chapter": n.chapter, "section": n.section, "subsection": n.subsection,
            "source_file": n.source_file, "spaces": n.spaces, "lean": n.lean,
            "has_proof": n.has_proof, "is_axiomatic": n.is_axiomatic,
        })
        for u in n.uses:
            edges.append({"from": n.id, "to": u, "kind": "uses"})
        for r in n.routes:
            routes_json.append({"node": n.id, "route": r.name, "deps": r.deps})
            for d in r.deps:
                edges.append({"from": n.id, "to": d, "kind": "proof", "route": r.name})
    return {
        "nodes": node_json,
        "edges": edges,
        "routes": routes_json,
        "spaces": lattice.lattice_json(),
        "stats": {
            "n_nodes": len(node_json),
            "n_edges": len(edges),
            "n_annotated_space": sum(1 for n in nodes if n.spaces),
            "n_lean_mapped": sum(1 for n in nodes if n.lean),
        },
    }


def collect_nodes() -> list:
    nodes = []
    for path in sorted(glob.glob(os.path.join(SEMINAR_TEX, "ch*.tex"))):
        nodes.extend(extract_file(path))
    return nodes


def main() -> None:
    # tex2md の \ref 解決用ラベル辞書（タイトル表示に使う場合に備えて）
    tex2md.LABEL_MAP = tex2md.build_label_map()
    tex2md.CHAPTER_MAP = tex2md.build_chapter_map()

    lattice = SpaceLattice.load()
    nodes = collect_nodes()

    # id 重複チェック（同一ラベルが二度定義されていないか）
    seen: dict = {}
    for n in nodes:
        if n.id in seen:
            print(f"  WARN: 重複ラベル {n.id} ({seen[n.id]} と {n.source_file})")
        seen[n.id] = n.source_file

    graph = build_graph(nodes, lattice)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    s = graph["stats"]
    print(f"nodes={s['n_nodes']} edges={s['n_edges']} "
          f"space-annotated={s['n_annotated_space']} lean-mapped={s['n_lean_mapped']}")
    print(f"→ {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
