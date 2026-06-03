---
id: wasserstein
nav: Wasserstein 距離
eyebrow: 5. Wasserstein Distance
title: Wasserstein 距離
---


最適輸送の最適値は，点の間の距離から測度（ヒストグラム）の間の距離を定める．本章では，地のコストが距離の \(p\) 乗であるとき，最適輸送が確率測度の空間上の距離——**Wasserstein 距離**——を与えることを示す．証明の核心は**貼り合わせ補題**（gluing lemma）による三角不等式であり，これが幾何的発展（測地線・曲率）の出発点となる．

## 地の距離と Wasserstein 距離


まず離散の設定を固定する．\(\mathbf{a}, \mathbf{b}, \mathbf{c}\) は同一の地の集合 \(\range{n}\) 上のヒストグラムであり，**確率単体**

\[
 \simplex_n
 \defeq
 \left\{
 \mathbf{a} \in \R_{\geq 0}^n
 \;\middle|\;
 \textstyle\sum_{i=1}^n a_i = 1
 \right\}
\]

に属するとする．

:::definition
### Def: 地の距離行列

行列 \(\distD \in \R_{\geq 0}^{n \times n}\) が\(\range{n}\) 上の**距離（地の距離行列）**であるとは，次を満たすことをいう．

\textrm{(i)} 対称性：\(\distD_{i,j} = \distD_{j,i}\)．
\textrm{(ii)} 非退化性：\(\distD_{i,j} = 0 \iff i = j\)．
\textrm{(iii)} 三角不等式：\(\distD_{i,k} \leq \distD_{i,j} + \distD_{j,k}\)（\(\forall\, i, j, k\)）．

これは距離空間の公理（[ref:Def: 距離空間|距離空間]）を有限集合 \(\range{n}\) に適用したものである．
:::


:::definition
### Def: 離散 Wasserstein 距離

地の距離行列 \(\distD\) と \(p \geq 1\) に対し，コスト行列を\(\mathbf{C} = \distD^p = (\distD_{i,j}^p)_{i,j}\) とする．\(\mathbf{a}, \mathbf{b} \in \simplex_n\) に対して**\(p\)-Wasserstein 距離**を

\[
 \WassD_p(\mathbf{a}, \mathbf{b})
 \defeq
 \MKD_{\distD^p}(\mathbf{a}, \mathbf{b})^{1/p}
 =
 \left(
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{P}}{\distD^p}
 \right)^{1/p}
\]

で定める（\(\WassD_p\) は \(\distD\) に依存する）．
:::


三角不等式の証明には，重み付き \(\ell^p\) ノルムの三角不等式——**Minkowski の不等式**——を用いる．

:::theorem
### Clm: Minkowski の不等式（重み付き）

\(p \geq 1\)，有限添字集合 \(I\)，非負の重み \((w_\iota)_{\iota \in I}\)，実数 \((u_\iota)_{\iota \in I}, (v_\iota)_{\iota \in I}\) に対して，

\[
 \left(
 \sum_{\iota \in I} w_\iota |u_\iota + v_\iota|^p
 \right)^{1/p}
 \leq
 \left(
 \sum_{\iota \in I} w_\iota |u_\iota|^p
 \right)^{1/p}
 +
 \left(
 \sum_{\iota \in I} w_\iota |v_\iota|^p
 \right)^{1/p}.
\]

:::details-embedded 証明
重み付き内積空間における \(L^p\) ノルム\(\norm{f}_{p,w} \defeq (\sum_\iota w_\iota |f_\iota|^p)^{1/p}\) の三角不等式にほかならない．これは古典的な Minkowski の不等式である（Hölder の不等式から従う標準的事実なので証明は省く）．
:::
:::


## \(\WassD_p\) が距離であること


:::theorem
### Thm: 離散 Wasserstein 距離の距離性

\(\distD\) を \(\range{n}\) 上の地の距離行列，\(p \geq 1\) とする．このとき \(\WassD_p\) は確率単体 \(\simplex_n\) 上の距離である．すなわち，任意の \(\mathbf{a}, \mathbf{b}, \mathbf{c} \in \simplex_n\) に対し

\textrm{(i)} 対称性：\(\WassD_p(\mathbf{a}, \mathbf{b}) = \WassD_p(\mathbf{b}, \mathbf{a})\)；
\textrm{(ii)} 非退化性：\(\WassD_p(\mathbf{a}, \mathbf{b}) \geq 0\) かつ\(\WassD_p(\mathbf{a}, \mathbf{b}) = 0 \iff \mathbf{a} = \mathbf{b}\)；
\textrm{(iii)} 三角不等式：\(\WassD_p(\mathbf{a}, \mathbf{c}) \leq \WassD_p(\mathbf{a}, \mathbf{b}) + \WassD_p(\mathbf{b}, \mathbf{c})\)．

:::details-embedded 証明
最適カップリングの存在は[ref:Clm: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在] による．

**(i) 対称性．**\(\distD^p\) は対称なので，転置 \(\mathbf{P} \mapsto \mathbf{P}^\top\) は\(\CouplingsD(\mathbf{a}, \mathbf{b})\) と \(\CouplingsD(\mathbf{b}, \mathbf{a})\) の間の全単射であり，\(\inner{\mathbf{P}^\top}{\distD^p} = \inner{\mathbf{P}}{\distD^p}\) で目的関数を保つ．ゆえに両者の最小値は等しい．

**(ii) 非退化性．**\(\distD^p \geq \mathbf{0}\) より \(\WassD_p \geq 0\)．\(\mathbf{a} = \mathbf{b}\) のとき，\(\mathbf{P}^\star = \diag(\mathbf{a})\) は\(\CouplingsD(\mathbf{a}, \mathbf{a})\) に属し（行和・列和とも \(\mathbf{a}\)），対角が \(0\) なので\(\inner{\diag(\mathbf{a})}{\distD^p} = \sum_i a_i \distD_{i,i}^p = 0\)，ゆえに \(\WassD_p(\mathbf{a}, \mathbf{a}) = 0\)．逆に \(\mathbf{a} \neq \mathbf{b}\) とする．任意の\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) が対角行列なら\(\mathbf{a} = \mathbf{P}\ones_n = \mathbf{P}^\top\ones_n = \mathbf{b}\) となり矛盾するので，ある \(i \neq j\) で \(P_{i,j} > 0\)．非退化性 (ii) より \(\distD_{i,j} > 0\) だから\(\inner{\mathbf{P}}{\distD^p} \geq P_{i,j}\distD_{i,j}^p > 0\)．最適 \(\mathbf{P}\) についてもこれが成り立つので\(\WassD_p(\mathbf{a}, \mathbf{b}) > 0\)．

**(iii) 三角不等式（貼り合わせ）．**\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\),\(\mathbf{Q} \in \CouplingsD(\mathbf{b}, \mathbf{c})\) を，それぞれ\((\mathbf{a},\mathbf{b})\), \((\mathbf{b},\mathbf{c})\) の最適カップリングとする．\(\mathbf{b}\) のゼロ成分を避けるため\(\tilde{b}_j \defeq b_j\)（\(b_j > 0\)），\(\tilde{b}_j \defeq 1\)（\(b_j = 0\)）とおき，**貼り合わせ**行列

\[
 \mathbf{S} \defeq \mathbf{P}\diag(1/\tilde{\mathbf{b}})\mathbf{Q},
 \qquad
 S_{i,k} = \sum_j \frac{P_{i,j} Q_{j,k}}{\tilde{b}_j}
\]

を定める．

まず \(\mathbf{S} \in \CouplingsD(\mathbf{a}, \mathbf{c})\) を示す．\(b_j = 0\) なら，列 \(j\) の和より \(\sum_i P_{i,j} = b_j = 0\) かつ行 \(j\) の和より \(\sum_k Q_{j,k} = b_j = 0\) なので，その \(j\) では \(P_{i,j} = Q_{j,k} = 0\)．したがって

\[
 \sum_k S_{i,k}
 = \sum_j \frac{P_{i,j}}{\tilde{b}_j}\sum_k Q_{j,k}
 = \sum_{j : b_j > 0} \frac{P_{i,j}}{b_j} \cdot b_j
 = \sum_j P_{i,j} = a_i,
\]

同様に \(\sum_i S_{i,k} = c_k\)．非負性も明らかなので\(\mathbf{S} \in \CouplingsD(\mathbf{a}, \mathbf{c})\)．

\(\mathbf{S}\) の劣最適性，\(\distD\) の三角不等式（および \(x \mapsto x^p\) の\([0,\infty)\) 上での単調性），重み\(w_{i,j,k} \defeq P_{i,j}Q_{j,k}/\tilde{b}_j \geq 0\) に対するMinkowski の不等式（[ref:Clm: Minkowski の不等式（重み付き）|Minkowski の不等式（重み付き）]）を順に用いると，

\[\begin{aligned}
 \WassD_p(\mathbf{a}, \mathbf{c})
 &\leq \inner{\mathbf{S}}{\distD^p}^{1/p}
 = \left(\sum_{i,j,k} \distD_{i,k}^p\, w_{i,j,k}\right)^{1/p} \\
 &\leq \left(\sum_{i,j,k}
 (\distD_{i,j} + \distD_{j,k})^p\, w_{i,j,k}\right)^{1/p} \\
 &\leq \left(\sum_{i,j,k} \distD_{i,j}^p\, w_{i,j,k}\right)^{1/p}
 + \left(\sum_{i,j,k} \distD_{j,k}^p\, w_{i,j,k}\right)^{1/p}.
\end{aligned}\]

第 1 項では \(\sum_k Q_{j,k} = b_j\) より

\[
 \sum_{i,j,k} \distD_{i,j}^p\, \frac{P_{i,j}Q_{j,k}}{\tilde{b}_j}
 = \sum_{i,j} \distD_{i,j}^p\, \frac{P_{i,j}}{\tilde{b}_j} b_j
 = \sum_{i,j} \distD_{i,j}^p\, P_{i,j}
 = \inner{\mathbf{P}}{\distD^p}
 = \WassD_p(\mathbf{a}, \mathbf{b})^p,
\]

第 2 項では \(\sum_i P_{i,j} = b_j\) より同様に\(\inner{\mathbf{Q}}{\distD^p} = \WassD_p(\mathbf{b}, \mathbf{c})^p\) を得る．（いずれも \(b_j = 0\) の項は \(P_{i,j} = Q_{j,k} = 0\) により寄与しない．）よって\(\WassD_p(\mathbf{a}, \mathbf{c}) \leq \WassD_p(\mathbf{a}, \mathbf{b}) + \WassD_p(\mathbf{b}, \mathbf{c})\)．
:::
:::


:::fact
### Rem: \(0 < p \leq 1\) の場合

\(0 < p \leq 1\) のときは \(\distD^p\) 自身が地の距離行列となり，\(\WassD_p(\mathbf{a}, \mathbf{b})^p\)（\(1/p\) 乗を外したもの）が\(\simplex_n\) 上の距離となる．以下では \(p \geq 1\) を仮定する．
:::


:::fact
### Rem: 本章のまとめと展望

地のコストが距離の \(p\) 乗のとき，最適輸送はヒストグラムの空間\(\simplex_n\) 上の距離 \(\WassD_p\) を定める（[ref:Thm: 離散 Wasserstein 距離の距離性|離散 Wasserstein 距離の距離性]）．証明の核心は，2 つの最適カップリングを貼り合わせて\(\mathbf{S} = \mathbf{P}\diag(1/\tilde{\mathbf{b}})\mathbf{Q}\) を作る構成にあった．

この距離の上で「測地線」や「曲率」といった幾何を論じるには，質量を中間点へ連続的に動かす必要があり，地の空間を\(\R^d\) のような連続空間にとらねばならない（有限ビン上では測地線が存在しない）．その連続版の道具立ては，必要となる幾何の章（Brenier 定理以降）で最小限に導入する．次章ではまず，非正則化 Kantorovich 問題の双対と \(c\)-変換を整備する．
:::
