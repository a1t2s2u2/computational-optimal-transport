# セミナー tex/site 二層化 設計書

`発表 2.pdf`（実際に発表した内容）を**正**とし、tex を「OT本編」と「前提知識（基礎）」の
二層に分離する。サイトは tex から生成され、本編チャプター + 付録（前提知識）として
発表と同じ粒度で読める形にする。

**「正とする」の意味＝本編の流れ・順序・粒度**を発表に合わせること。**内容は削らない**。
網羅度の方針（重要・不変）:

- **発表PDF** — 時間制約で前提を取捨選択（省略してよい唯一の成果物）。
- **site / tex（網羅版）** — 前提知識を**省略せず全網羅**。foundations 付録は独習できる完全版として通読可能に保つ。

つまり foundations は「削る」のではなく「別 tex へ移して全部残す」。本編は発表の粒度でクリーンに、
前提は付録で完全に——この二層が「網羅版」と「発表向け要点」を1ソースで両立させる。

## 背景（確定した分析）

現行 tex は既に7割方この二層構造を内包しているが、不統一だった。

| 章 | core | foundation | 実態 |
|---|---|---|---|
| ch01 準備 | 0 | 40 + 橋渡し8 | 丸ごと前提知識（位相・距離・測度・凸・コンパクト性）。OT固有ゼロ |
| ch02 OT基礎 | 11(定義) | 論証が前提依存 | 定義=core、存在/凸/コンパクト性の証明は ch01 を `\ref`。既に分離済み |
| ch03 エントロピー | 9 | 2 + 外部参照 | §3.1で前提吸収、§3.2-3.3はほぼ純 core |
| ch04 Sinkhorn | 6 | 6（インライン） | §4.2-4.3(Hilbert/Birkhoff)が本編に直挿し＝未分離 |

発表は前提を「色付きボックスで都度参照」しており、事実上もう二層。発表済み範囲は
ch01(基礎) + ch02 + ch03（Sinkhorn 手前 ε→0 まで。ch04 は「次回」）。

## 決定事項

1. **パッケージング**: 1つの `main.pdf`。本編の後に `\appendix` で foundations を綴じる。
   基礎は別 tex ファイル群だが、`\ref` は同一文書内で解決（クリック追従が効く）。
2. **サイト**: 本編チャプターをトップナビ、基礎は「付録：前提知識」ページ。
   本編からは既存の `[ref:ラベル]` 機構でサイドバーに前提をポップ（発表の貼り込み再現）。
3. **Sinkhorn(ch04)**: 本編章 `main/05_sinkhorn.tex` として整備し、
   インライン基礎(Hilbert/Birkhoff)は foundations へ分離。全章で方式を統一。

## 目標ファイル構成

```
seminar/tex/
  preamble.tex              共有（記号・ブロック環境・\blockmeta）
  main.tex                  \input main/* → \appendix → \input foundations/*
  main/                     【OT本編】発表2の流れ。foundations を \ref で引く
    01_assignment.tex         最適割当(OAP)            〔発表 u1-2〕
    02_monge.tex              Monge問題と困難           〔u4-5〕
    03_kantorovich.tex        Kantorovich・離散化・同値・存在/凸コンパクト/非一意 〔u6-9〕
    04_entropic.tex           エントロピー正則化・狭義凸・存在一意・KL/Gibbs・ε→0 〔u10-14〕
    05_sinkhorn.tex           Sinkhorn反復・線形収束（発表「次回」分）
  foundations/             【前提知識】OT非依存・自己完結・"参照される側"
    00_set_topology.tex       冪集合・位相・稠密・可分
    01_metric_compact.tex     距離/ノルム/開球/収束/完備/Polish/連続/コンパクト/BW・HB・Weierstrass・MVT
    02_measure.tex            σ代数/可測/ボレル/測度/確率測度/積分/単調収束/Dirac/押し出し/離散測度
    03_convex_linalg.tex      有限集合・最小元・置換・線形・ones・Frobenius・凸/狭義凸・最小点一意
    04_nonneg_matrix.tex      Hilbert射影計量・Birkhoff縮小（ch04 §4.2-4.3 から剥がす）
```

## ブロック移動表（**ラベルは一切変更しない**＝既存の `\ref`・proofgraph を壊さない）

### foundations/00_set_topology.tex  ← ch01 前半
- `def:sem-power-set` 冪集合
- `def:sem-topological-space` 位相空間 / `def:sem-dense` 稠密集合 / `def:sem-separable` 可分性〔blockmeta space=separable〕

### foundations/01_metric_compact.tex  ← ch01 距離空間節
- `def:sem-metric-space`〔space=metric〕/ `def:sem-normed-space`〔space=normed〕/ `def:sem-open-ball`
- `def:sem-convergence` / `def:sem-complete-metric`〔space=complete_metric〕/ `def:sem-polish`〔space=polish〕
- `def:sem-continuous` / `prop:sem-preimage-closed`
- `def:sem-bounded` / `def:sem-compact` / `clm:sem-bolzano-weierstrass` / `thm:sem-heine-borel`
- `thm:sem-weierstrass` / `prop:sem-finite-dim-linear-continuous` / `thm:sem-mvt`

### foundations/02_measure.tex  ← ch01 測度論節（丸ごと）
- `def:sem-sigma-algebra` / `def:sem-measurable-space` / `def:sem-measurable-map` / `def:sem-borel` / `def:sem-measurable-function`
- `def:sem-product-measurable` / `def:sem-projection` / `def:sem-measure` / `def:sem-probability-measure`
- `def:sem-indicator` / `def:sem-simple-function` / `def:sem-nonneg-integral` / `prop:sem-mct` / `prop:sem-measure-linearity`
- `def:sem-dirac` / `clm:sem-dirac-integral` / `def:sem-discrete-measure` / `clm:sem-discrete-measure-uniqueness`
- `def:sem-pushforward` / `prop:sem-dirac-pushforward`

### foundations/03_convex_linalg.tex  ← ch01 線形代数節
- `def:sem-finite` / `clm:sem-finite-min` / `def:sem-permutation`
- `def:sem-linear-function` / `def:sem-ones-vector` / `def:sem-frobenius-inner`
- `def:sem-convex` / `def:sem-convex-function` / `prop:sem-strict-convex-unique-min`

### foundations/04_nonneg_matrix.tex  ← ch04 §4.2-4.3（剥がし）
- `def:sem-hilbert-metric` / `clm:sem-hilbert-metric-properties`
- `clm:sem-weighted-average` / `clm:sem-projective-diameter` / `thm:sem-birkhoff` / `rem:sem-birkhoff-tightness`
- `clm:sem-division-isometry`（§4.4の補題だがHilbert計量の道具なのでここへ）

### main/01_assignment.tex  ← ch02 §最適割当
- `rem:sem-ch2-setup`（本編冒頭の「前提参照ノート」として再利用）
- `def:sem-assignment` / `ex:sem-assignment-cost-example` / `clm:sem-assignment-existence` / `clm:sem-uniqueness`

### main/02_monge.tex  ← ch02 §Monge
- `def:sem-monge` / `ex:sem-nonconvex` / `ex:sem-monge-noexist`

### main/03_kantorovich.tex  ← ch02 §Kantorovich
- `def:sem-kantorovich` / `rem:sem-marginal-pushforward` / `prop:sem-discrete-kantorovich` / `rem:sem-distinct-points`
- `ex:sem-factory-supermarket` / `clm:sem-discrete-kantorovich-existence` / `clm:sem-coupling-convex`
- `clm:sem-optimal-face` / `ex:sem-nonunique-example` / `rem:sem-lp-uniqueness` / `rem:sem-entropy-uniqueness-preview`

### main/04_entropic.tex  ← ch03（丸ごと）
- ch03 の全ブロックを移設（ラベル不変）。

### main/05_sinkhorn.tex  ← ch04 §4.1・§4.4 の core
- `prop:sem-matrix-scaling` / `alg:sem-sinkhorn` / `prop:sem-sinkhorn-welldefined` / `rem:sem-sinkhorn-kl-projection`
- `rem:sem-scaling-ambiguity` / `thm:sem-sinkhorn-linear-convergence` / `rem:sem-convergence-meaning`
- （Hilbert/Birkhoff は foundations/04 を `\ref`）

## ビルド／サイト／proofgraph の改修

- **tex2md.py**: `SEMINAR_DIR` の glob を `main/*.tex` + `foundations/*.tex` に拡張（ラベル写像は両方走査）。
  `CHAPTERS` を新ファイル集合に更新し、各章に `group: main|appendix` を frontmatter で付与。
- **build.mjs**: `group` を見て本編をトップナビ、foundations を「付録：前提知識」ナビに配置。
  ブロック横断の `[ref:]` 解決は既存機構のまま（`allBlocks` は全章集約）→ 前提がポップ対象になる。
- **proofgraph/extractor.py**: `SEMINAR_TEX/ch*.tex` の glob を `{main,foundations}/*.tex` に拡張。
  `\blockmeta space=` は foundations/00,01 に移るが内容不変。

## 移行フェーズ（各フェーズで `latexmk main` と `make site` が通ることを確認）

- **P1 Foundations 切り出し**: foundations/00-04 を作成、ch01 全体と ch04 §4.2-4.3 を**ラベル不変で**移設。
- **P2 Main 再編**: main/01-05 を作成、ch02 を3分割、ch03→04、ch04 core→05。発表粒度に整える。
- **P3 main.tex 組み替え**: `\input main/*` → `\appendix` → `\input foundations/*`。記号表は本編冒頭に維持。
- **P4 ビルド/サイト改修**: tex2md.py / build.mjs / proofgraph を上記のとおり改修し、サイト再生成。
- **P5 検証**: `main.pdf` の未解決参照(??)ゼロ、`make site` 成功、proofgraph 実行成功。
- **P6（別タスク）内容改善**: 構造確定後、各章を `発表 2.pdf` と突き合わせて本文を精緻化する。
  対象は**本編の流れ・順序・見せ方・粒度**と、発表で補った直感の取り込み。
  **前提知識は削らない**（網羅版の方針）。ch02 の性質系ブロックは順序・提示を整えるが定理は残す。
  構造移動とは分けて慎重に。

## 不変条件

- **網羅性を落とさない**: foundations は全て残す。site/tex から前提知識を省略しない（発表PDFのみ削減可）。
- **ラベルは一切リネームしない**（`\ref`・`\blockmeta uses=`・proofgraph・site の `[ref:]` を保つ）。
- 各フェーズ後に PDF とサイトが両方ビルド可能であること。
- ブランチは `feat/0607` を main から切って作業（CLAUDE.md ブランチ戦略）。
