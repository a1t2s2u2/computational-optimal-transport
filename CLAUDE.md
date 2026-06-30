## リポジトリ概要

最適輸送のセミナー資料（tex / site）と関連ツールを管理するリポジトリ。

- `seminar/cuturi/` — Peyré–Cuturi _Computational Optimal Transport_ に基づく資料（本編4章+付録3章）
- `seminar/wasserstein/` — Wasserstein 距離の理論と性質（複数文献を横断的に参照）

## 参考文献

### `seminar/cuturi/`

- [Computational Optimal Transport, G. Peyré & M. Cuturi](https://arxiv.org/abs/1803.00567)

### `seminar/wasserstein/`

複数の文献を横断的に参照し、現代的な記法で再構成する。

- [A class of Wasserstein metrics for probability distributions, C. R. Givens & R. M. Shortt (1984)](https://doi.org/10.1307/mmj/1029003026) — 骨格となる定義・命題の出典
- [Optimal Transport: Old and New, C. Villani (2009)](https://doi.org/10.1007/978-3-540-71050-9) — 現代的記法・証明の補完
- [確率測度の空間における最適輸送問題, 桑江 (2024)](https://www.math.chuo-u.ac.jp/ENCwMATH/EwM63resume.pdf) — 日本語の解説、定義の補完

記法は Villani / Peyré–Cuturi に準拠し、Givens–Shortt 原論文の記号は読み替え表で対応する。
文献間で定義が異なる場合は、最も一般的な定義を採用し、差異を注意として記載する。

## セミナー方針

- 未定義の用語や概念は、必ず定義する
- 数学書の記述スタイルを参考に統一する

## tex コーディング規約

- 記法は現代的な標準（Villani / Peyré–Cuturi）に従う
- 複数文献から定義・命題を引く場合、出典を明示する
- コミット時 / PR時 には co-authored-by や ClaudeCode は記載しない

## ブランチ戦略

発表日 `feat/MMDD` ブランチを作成し、`main` にマージする運用とする。
適宜 `feat/MMDD` からブランチを切って、作業すること。
