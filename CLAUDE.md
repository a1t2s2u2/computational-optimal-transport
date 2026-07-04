## リポジトリ概要

最適輸送のセミナー資料（tex / site）と関連ツールを管理するリポジトリ。

- `seminar/cuturi/` — Peyré–Cuturi _Computational Optimal Transport_ に基づく資料（詳細は `seminar/cuturi/CLAUDE.md`）
- `seminar/wasserstein/` — Wasserstein 距離の理論と性質（詳細は `seminar/wasserstein/CLAUDE.md`）

## セミナー方針（共通）

- 未定義の用語や概念は、必ず定義する
- 数学書の記述スタイルを参考に統一する

## tex コーディング規約（共通）

- 記法は現代的な標準（Villani / Peyré–Cuturi）に従う
- 複数文献から定義・命題を引く場合、出典を明示する
- コミット時 / PR時 には co-authored-by や ClaudeCode は記載しない

## ブランチ戦略

発表日 `feat/MMDD` ブランチを作成し、`main` にマージする運用とする。
適宜 `feat/MMDD` からブランチを切って、作業すること。
