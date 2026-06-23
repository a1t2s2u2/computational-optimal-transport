## リポジトリ概要

最適輸送のセミナー資料（tex / site）と関連ツールを管理するリポジトリ。

- `seminar/` — Cuturi _Computational Optimal Transport_ に基づく資料（本編4章+付録3章）
- `ambrosio/` — Ambrosio _Lecture Notes on Optimal Transport Problems_ に基づく資料

## 参考文献

- [Computational Optimal Transport, G. Peyré & M. Cuturi](https://arxiv.org/abs/1803.00567) → `seminar/`
- Lecture Notes on Optimal Transport Problems, L. Ambrosio → `ambrosio/`

## セミナー方針

- 未定義の用語や概念は、必ず定義する
- 数学書の記述スタイルを参考に統一する

## tex コーディング規約

- 各参考文献の論文構成と記法に従うこと、ただし一部読み替えを含む
- コミット時 / PR時 には co-authored-by や ClaudeCode は記載しない

## ブランチ戦略

発表日 `feat/MMDD` ブランチを作成し、`main` にマージする運用とする。
適宜 `feat/MMDD` からブランチを切って、作業すること。
