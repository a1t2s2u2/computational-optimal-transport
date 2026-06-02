#!/usr/bin/env python3
"""graph.json から Lean4 のスケルトンを生成する。

2 つのファイルを生成する:

1. lean/Ot/Generated/Skeleton.lean  ── Mathlib 不要・即ビルド可能
   各ブロックを opaque な `Prop` として宣言し、その「証明済み性」を同名 `_pf`
   の項で表す。証明付きブロックは採択ルートの依存 `_pf` を `have` で参照しつつ
   `sorry` で閉じる。これにより `lake build` が
     - 依存先の存在（dangling なら未定義エラー）
     - 宣言順＝非循環性（循環なら前方参照エラー）
     - 未証明 obligation 数（`sorry` の数）
   を Lean の型検査として保証する。数学的内容ではなく「証明の骨格」を検証する層。

2. lean/Ot/Generated/MathlibCheck.lean ── `import Mathlib`
   \\blockmeta{lean=...} の対応先が Mathlib に実在するかを `#check` で検証する。
   Mathlib のキャッシュ取得後に `lake build` すると検査される。

使い方:
    python3 proofgraph/lean_gen.py        # 生成
    cd lean && lake build Ot              # スケルトンを型検査（Mathlib 不要）
"""

from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

from model import DependencyGraph, Node, Route, SpaceLattice  # noqa: E402

GRAPH_PATH = os.path.join(HERE, "out", "graph.json")
LEAN_ROOT = os.path.abspath(os.path.join(HERE, "..", "lean"))
SKELETON_PATH = os.path.join(LEAN_ROOT, "Ot", "Generated", "Skeleton.lean")
MATHLIB_CHECK_PATH = os.path.join(LEAN_ROOT, "Ot", "Generated", "MathlibCheck.lean")


def load_graph() -> tuple:
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    rbn: dict = {}
    for r in data.get("routes", []):
        rbn.setdefault(r["node"], []).append(Route(r["route"], list(r["deps"])))
    ubn: dict = {}
    for e in data.get("edges", []):
        if e.get("kind") == "uses":
            ubn.setdefault(e["from"], []).append(e["to"])
    nodes = [
        Node(
            id=n["id"], env=n["env"], title=n["title"],
            spaces=n.get("spaces", []), lean=n.get("lean", ""),
            has_proof=n.get("has_proof", False),
            uses=ubn.get(n["id"], []), routes=rbn.get(n["id"], []),
        )
        for n in data["nodes"]
    ]
    return data, DependencyGraph(nodes, SpaceLattice.load())


def ident(node_id: str) -> str:
    """ブロック id を Lean 識別子に変換。'thm:sem-foo-bar' -> 'thm_sem_foo_bar'。"""
    return re.sub(r"[^0-9A-Za-z]", "_", node_id)


def topo_order(graph: DependencyGraph) -> list:
    """grounding に使う依存（uses + 採択ルート）で位相ソートした id 列。

    循環があれば残余を末尾に付け、呼び出し側が検出できるようにする。
    """
    grounded = graph.grounded_set()
    # 各ノードの「証明に実際に使う依存」: uses + 採択（接地可能な最初の）ルート
    dep_of: dict = {}
    for nid, node in graph.nodes.items():
        deps = set(node.uses)
        if node.routes:
            chosen = next(
                (r for r in node.routes if all(d in grounded for d in r.deps)),
                node.routes[0],
            )
            deps.update(chosen.deps)
        dep_of[nid] = {d for d in deps if d in graph.nodes}

    order = []
    placed = set()
    # 反復的 Kahn 法
    changed = True
    while changed:
        changed = False
        for nid in graph.nodes:
            if nid in placed:
                continue
            if dep_of[nid] <= placed:
                order.append(nid)
                placed.add(nid)
                changed = True
    # 循環で残ったもの
    remaining = [nid for nid in graph.nodes if nid not in placed]
    return order, remaining, grounded, dep_of


def gen_skeleton(graph: DependencyGraph) -> tuple:
    order, remaining, grounded, dep_of = topo_order(graph)

    lines = [
        "/- 自動生成 by proofgraph/lean_gen.py — 手で編集しないこと。",
        "",
        "   各数学ブロックを opaque Prop として宣言し、依存構造を Lean の項として",
        "   組み上げる。`sorry` は未証明 obligation。`lake build` が非循環性・",
        "   依存存在・obligation 数を型検査として検証する。 -/",
        "",
        "namespace Ot.Generated",
        "",
        "-- 各ブロックの statement（内容は抽象化した Prop プレースホルダ）",
    ]
    for nid in graph.nodes:
        lines.append(f"opaque {ident(nid)} : Prop")
    lines.append("")
    lines.append("-- 各ブロックの『証明済み性』。foundational は axiom、証明付きは依存から導出。")

    n_axiom = 0
    n_sorry = 0
    for nid in order:
        node = graph.nodes[nid]
        name = ident(nid)
        if node.is_axiomatic and not node.uses:
            lines.append(f"axiom {name}_pf : {name}")
            n_axiom += 1
            continue
        # 採択ルートの依存（接地可能な最初のルート） + uses
        deps = sorted(dep_of[nid])
        comment = node.title.replace("\n", " ")
        lines.append(f"-- {comment}")
        if deps:
            lines.append(f"theorem {name}_pf : {name} := by")
            for d in deps:
                lines.append(f"  have _ := {ident(d)}_pf")
            lines.append("  sorry")
        else:
            lines.append(f"theorem {name}_pf : {name} := sorry")
        n_sorry += 1

    if remaining:
        lines.append("")
        lines.append("-- !! 循環のため接地できなかったブロック（要修正）:")
        for nid in remaining:
            lines.append(f"--   {nid}")

    lines.append("")
    lines.append("end Ot.Generated")
    lines.append("")
    return "\n".join(lines), {
        "n_axiom": n_axiom, "n_sorry": n_sorry,
        "n_cyclic": len(remaining), "cyclic": remaining,
    }


def gen_mathlib_check(data: dict) -> tuple:
    mapped = [(n["id"], n["lean"]) for n in data["nodes"]
              if n.get("lean") and _looks_mathlib(n["lean"])]
    lines = [
        "/- 自動生成 by proofgraph/lean_gen.py。",
        "   \\blockmeta{lean=...} の対応先が Mathlib に実在するかを #check で検証する。",
        "   Mathlib キャッシュ取得後に `lake build Ot.Generated.MathlibCheck` で確認。 -/",
        "import Mathlib",
        "",
        "namespace Ot.MathlibCheck",
        "",
    ]
    for nid, name in mapped:
        lines.append(f"-- {nid}")
        lines.append(f"#check @{name}")
    lines.append("")
    lines.append("end Ot.MathlibCheck")
    lines.append("")
    return "\n".join(lines), len(mapped)


def _looks_mathlib(name: str) -> bool:
    """Mathlib の宣言名らしい（大文字始まり等）。自前 'ot.foo' は除外。"""
    head = name.split(".")[0]
    return bool(head) and head[0].isupper()


def main() -> None:
    data, graph = load_graph()
    os.makedirs(os.path.dirname(SKELETON_PATH), exist_ok=True)

    skeleton, stats = gen_skeleton(graph)
    with open(SKELETON_PATH, "w", encoding="utf-8") as f:
        f.write(skeleton)

    check, n_mapped = gen_mathlib_check(data)
    with open(MATHLIB_CHECK_PATH, "w", encoding="utf-8") as f:
        f.write(check)

    print(f"Skeleton.lean   : axioms={stats['n_axiom']} "
          f"obligations(sorry)={stats['n_sorry']} cyclic={stats['n_cyclic']}")
    if stats["cyclic"]:
        print("  循環:", ", ".join(stats["cyclic"]))
    print(f"MathlibCheck.lean: {n_mapped} 個の lean= マッピングを #check")
    print(f"→ {SKELETON_PATH}")
    print(f"→ {MATHLIB_CHECK_PATH}")
    if stats["cyclic"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
