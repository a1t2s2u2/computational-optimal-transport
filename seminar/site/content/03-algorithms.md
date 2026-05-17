---
id: algorithms
nav: アルゴリズムの基礎
eyebrow: 3. Algorithms
title: アルゴリズムの基礎
---


## 線形計画としての定式化


離散 Kantorovich 問題

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 \defeq \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}}
\]

は線形計画である．
\(\mathbf{P}\) と \(\mathbf{C}\) をそれぞれベクトル化した
\(\mathbf{p}, \mathbf{c} \in \R^{nm}\)，
周辺条件をまとめた制約行列 \(\mathbf{A} \in \R^{(n+m) \times nm}\) を用いると，
標準形

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \min_{\substack{\mathbf{p} \in \R_+^{nm} \\
 \mathbf{A}\mathbf{p} = [\mathbf{a}^\top, \mathbf{b}^\top]^\top}}
 \mathbf{c}^\top \mathbf{p}
\]

と表される．\(nm\) 個の変数と \(n + m\) 本の等式制約を持つ有限次元の線形計画であり，
**ネットワーク単体法**（network simplex）をはじめとする
LP アルゴリズムで厳密に解ける．


## エントロピー正則化への動機付け


ネットワーク単体法は厳密解を与えるが，
大規模応用の観点では根本的な制約をもつ：


- **計算量**：\(O(nm)\) 個の変数に対する反復・データ構造管理は， \(n, m\) が \(10^5\) オーダーになると現実的でない． GPU 並列化にも本質的に向かない（離散探索的）．
- **微分不可能性**：最適値 \(\MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\) は \(\mathbf{a}, \mathbf{b}\) について区分線形にしかならず， 自動微分による勾配最適化に組み込みにくい．


これらの困難は，目的関数にエントロピー項を加えて
正則化することで大きく緩和される．
正則化された問題は **Sinkhorn アルゴリズム**で効率的に解け，
計算は GPU 並列に適し，最適値は周辺分布に関して微分可能となる．
