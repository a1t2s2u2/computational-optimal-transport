## リポジトリ概要
最適輸送のセミナー資料（tex / site）と関連ツールを管理するリポジトリ。

- `seminar/` — Cuturi *Computational Optimal Transport* に基づく資料（本編4章+付録3章）
- `ambrosio/` — Ambrosio *Lecture Notes on Optimal Transport Problems* に基づく資料

## 参考文献
- [Computational Optimal Transport, G. Peyré & M. Cuturi](https://arxiv.org/abs/1803.00567) → `seminar/`
- Lecture Notes on Optimal Transport Problems, L. Ambrosio → `ambrosio/`

## セミナー方針
- 未定義の用語や概念は、必ず定義する
- 数学書の記述スタイルを参考に統一する
- Ambrosio の記法に準拠する（$X \subset \mathbb{R}^n$ コンパクト凸、$\mu, \nu$ で測度、$\psi$ で輸送写像、$\gamma$ で輸送計画）。ただし Ambrosio 原文の $f_0, f_1$ は $\mu, \nu$ に読み替える

## tex コーディング規約
- 各参考文献の論文構成と記法に従うこと
- コミット時 / PR時 には co-authored-by や ClaudeCode は記載しない

## ブランチ戦略
発表日 `feat/MMDD` ブランチを作成し、`main` にマージする運用とする。
適宜 `feat/MMDD` からブランチを切って、作業すること。
