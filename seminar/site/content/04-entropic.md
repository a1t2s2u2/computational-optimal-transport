---
id: entropic
nav: エントロピー正則化
eyebrow: 4. Entropic Regularization
title: エントロピー正則化と Sinkhorn アルゴリズム
---


エントロピー正則化は，
最適輸送問題にエントロピー項を加えることで問題を狭義凸化する手法である．

以下，

\[
 \mathbf{a} \in \R_{++}^{n},\qquad
 \mathbf{b} \in \R_{++}^{m},\qquad
 \sum_{i=1}^{n} a_i = \sum_{j=1}^{m} b_j = 1,
\]

および \(\mathbf{C} \in \R_+^{n \times m}\) を固定する．
離散カップリング集合 \(\CouplingsD(\mathbf{a}, \mathbf{b})\) は
[ref:Prop: 連続 Kantorovich 問題の離散化|連続 Kantorovich 問題の離散化] の通り

\[
 \CouplingsD(\mathbf{a}, \mathbf{b})
 =
 \left\{
 \mathbf{P} \in \R_+^{n \times m}
 \;\middle|\;
 \mathbf{P}\ones_m = \mathbf{a},\;
 \mathbf{P}^\top \ones_n = \mathbf{b}
 \right\}
\]

である．

## エントロピー正則化


:::definition
### Def: 離散エントロピー

非負行列 \(\mathbf{P} \in \R_+^{n \times m}\) に対して，
**離散エントロピー**を

\[
 \Hb(\mathbf{P})
 \defeq
 - \sum_{i=1}^{n} \sum_{j=1}^{m}
 P_{i,j}\bigl(\log P_{i,j} - 1\bigr)
\]

で定める．ただし \(0\log 0 = 0\) と約束する．
:::


:::fact
### Rem: 通常の Shannon エントロピーとの違い

確率行列では \(\sum_{i,j}P_{i,j}=1\) なので，

\[
 \Hb(\mathbf{P})
 =
 -\sum_{i,j} P_{i,j}\log P_{i,j} + 1
\]

であり，通常の Shannon エントロピーとは定数 \(1\) だけ異なる．
この定数は最適化の解には影響しない．この形を使う理由は，
\(-\Hb\) の微分が簡単になるからである．積の微分則より

\[
 \frac{\partial(-\Hb)}{\partial P_{i,j}}
 = \frac{\partial}{\partial P_{i,j}}\bigl[P_{i,j}(\log P_{i,j} - 1)\bigr]
 = (\log P_{i,j} - 1) + P_{i,j} \cdot \frac{1}{P_{i,j}}
 = \log P_{i,j},
\]

定義中の \(-1\) と積の微分で生じる \(+1\) が打ち消し合い，\(\log P_{i,j}\) のみが残る．
:::


:::definition
### Def: エントロピー正則化された離散最適輸送

正則化パラメータ \(\varepsilon > 0\) に対して，
**エントロピー正則化された離散 Kantorovich 問題**を

\[
 \MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})
 \defeq
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \left\{
 \inner{\mathbf{C}}{\mathbf{P}}
 - \varepsilon \Hb(\mathbf{P})
 \right\}
\]

と定める．この問題の最適解を \(\mathbf{P}_\varepsilon\) と書く．
:::


:::theorem
### Prop: 正則化問題の解の存在と一意性

任意の \(\varepsilon > 0\) に対して，
[ref:Def: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] は一意な最適解
\(\mathbf{P}_\varepsilon \in \CouplingsD(\mathbf{a}, \mathbf{b})\) を持つ．

:::details-embedded 証明
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は空でないコンパクト集合である
（[ref:Clm: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在] の証明）．

**目的関数の連続性．**
\(g(x) \defeq x\log x - x\)（\(x > 0\)），\(g(0) \defeq 0\) とおく．
\(x > 0\) では \(g\) は連続．\(x = 0\) では \(x = e^{-t}\)（\(t \to +\infty\)）と置換すると

\[
 x\log x = -\frac{t}{e^t} \to 0,
\]

よって \(\lim_{x\to 0+} g(x) = 0 = g(0)\) であり \(g\) は \([0,\infty)\) 上で連続．
目的関数 \(\mathbf{P} \mapsto \inner{\mathbf{C}}{\mathbf{P}} + \varepsilon\sum_{i,j}g(P_{i,j})\)
は各成分の連続関数の和だから連続であり，コンパクト集合上の連続関数として最小値を達成する．

**目的関数の狭義凸性．**
\(x > 0\) において \(g''(x) = 1/x > 0\) だから \(g'\) は \((0,\infty)\) 上で狭義単調増加である．
任意の \(x_1 < x_2\) と \(\lambda \in (0,1)\) をとり \(x^* := \lambda x_1 + (1-\lambda)x_2\) とおく．
平均値定理（[ref:Thm: 平均値定理|平均値定理]）を \([x_1, x^*]\) と \([x^*, x_2]\) に適用すると
\(c_1 \in (x_1, x^*),\; c_2 \in (x^*, x_2)\) が存在して

\[\begin{aligned}
 \lambda g(x_1) + (1-\lambda)g(x_2) - g(x^*)
 &= \lambda\bigl[g(x_1)-g(x^*)\bigr] + (1-\lambda)\bigl[g(x_2)-g(x^*)\bigr] \\
 &= \lambda(1-\lambda)(x_2-x_1)\bigl[g'(c_2)-g'(c_1)\bigr] > 0.
\end{aligned}\]

ここで \(c_1 < c_2\) と \(g'\) の狭義単調増加性から \(g'(c_2) > g'(c_1)\)，
また \(\lambda(1-\lambda)(x_2-x_1) > 0\) だから不等式が成立する．
よって \(g\) は \((0,\infty)\) 上で狭義凸（[ref:Def: 凸関数と狭義凸関数|凸関数と狭義凸関数]）．
\(x = 0\) での連続性と合わせて \([0,\infty)\) 上でも狭義凸である．
各成分の狭義凸関数の和として，目的関数 \(\mathbf{P} \mapsto \inner{\mathbf{C}}{\mathbf{P}} + \varepsilon\sum_{i,j}g(P_{i,j})\) も \(\mathbf{P}\) について狭義凸である．

**最適解の一意性．**
目的関数が狭義凸であるとき，最適解は高々1つである．
実際，\(\mathbf{P}_1 \neq \mathbf{P}_2\) がともに最適解であるとすると，
中点 \(\mathbf{P}^* = (\mathbf{P}_1 + \mathbf{P}_2)/2\) も \(\CouplingsD(\mathbf{a},\mathbf{b})\) に属し（凸集合），
狭義凸性から

\[
 f(\mathbf{P}^*) < \tfrac{1}{2}f(\mathbf{P}_1) + \tfrac{1}{2}f(\mathbf{P}_2) = f(\mathbf{P}_1)
\]

となり，\(\mathbf{P}_1\) が最適解であることに矛盾する．よって最適解は一意である．
:::
:::


:::theorem
### Prop: 正則化解の正値性

正則化問題の一意解 \(\mathbf{P}_\varepsilon\) は

\[
 (P_\varepsilon)_{i,j} > 0
 \qquad(\forall\, i \in \range{n},\, j \in \range{m})
\]

を満たす．

:::details-embedded 証明
背理法で示す．ある \((i,j)\) で
\((P_\varepsilon)_{i,j}=0\) とする．
\(a_i>0\) なので同じ行に \((P_\varepsilon)_{i,j_1}>0\) となる
\(j_1\) が存在する．また \(b_j>0\) なので同じ列に
\((P_\varepsilon)_{i_1,j}>0\) となる \(i_1\) が存在する．
小さい \(\theta>0\) に対し，4成分だけを

\[
 P_{i,j} \leftarrow P_{i,j}+\theta,\quad
 P_{i,j_1} \leftarrow P_{i,j_1}-\theta,\quad
 P_{i_1,j} \leftarrow P_{i_1,j}-\theta,\quad
 P_{i_1,j_1} \leftarrow P_{i_1,j_1}+\theta
\]

と変化させる．\(\theta\) を
\((P_\varepsilon)_{i,j_1}\) と \((P_\varepsilon)_{i_1,j}\) より小さく取れば，
非負性と周辺条件は保たれる．

この変化による線形コストの変化は \(\theta\) に比例する．
一方，エントロピー項のうち \(0\) だった成分に対応する負エントロピー
\(x\log x-x\) の変化は

\[
 \theta\log\theta - \theta
\]

であり，これを \(\theta\) で割ると \(\log\theta-1 \to -\infty\)
となる．したがって十分小さい \(\theta>0\) では，
全体の目的関数
\(\inner{\mathbf{C}}{\mathbf{P}}-\varepsilon\Hb(\mathbf{P})\)
は小さくなる．これは \(\mathbf{P}_\varepsilon\) の最適性に矛盾する．
よって全成分が正である．
:::
:::


:::fact
### Rem: \(\varepsilon\) の役割

\(\varepsilon\) は，元の線形計画と独立カップリングの間を補間する量である：

- \(\varepsilon \to 0\) のとき，\(\mathbf{P}_\varepsilon\) は 非正則化問題 \(\MKD_{\mathbf{C}}\) の最適解のうち エントロピーが最大のものに収束する （[ref:Thm: \(\varepsilon \to 0\) による非正則化 OT への収束|\(\varepsilon \to 0\) による非正則化 OT への収束]）．
- \(\varepsilon \to +\infty\) のとき，\(\mathbf{P}_\varepsilon\) は 積測度 \(\mathbf{a} \mathbf{b}^\top\) に収束する （[ref:Rem: \(\varepsilon \to +\infty\) による独立カップリングへの収束|\(\varepsilon \to +\infty\) による独立カップリングへの収束]）．
:::


### KL ダイバージェンスによる定式化


:::definition
### Def: 離散 KL ダイバージェンス

非負行列 \(\mathbf{P}, \mathbf{K} \in \R_+^{n \times m}\) に対して，
**KL ダイバージェンス**を

\[
 \KLD(\mathbf{P} \| \mathbf{K})
 \defeq
 \sum_{i,j}
 \left(
 P_{i,j}\log\frac{P_{i,j}}{K_{i,j}}
 - P_{i,j} + K_{i,j}
 \right)
\]

で定める．ただし \(0\log 0 = 0\) と約束し，
\(P_{i,j} > 0\) かつ \(K_{i,j}=0\) となる成分がある場合は
\(\KLD(\mathbf{P}\|\mathbf{K}) = +\infty\) とする．
:::


:::definition
### Def: Gibbs カーネル

コスト行列 \(\mathbf{C}\) と \(\varepsilon > 0\) に対して，
**Gibbs カーネル** \(\mathbf{K} \in \R_{++}^{n \times m}\) を

\[
 K_{i,j} \defeq \exp\!\left(-\frac{C_{i,j}}{\varepsilon}\right)
\]

で定める．
:::


:::theorem
### Prop: 正則化 OT は KL 射影である

\(\mathbf{K} = \exp(-\mathbf{C}/\varepsilon)\) とすると，
[ref:Def: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] の最適解は

\[
 \mathbf{P}_\varepsilon
 =
 \argmin_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \KLD(\mathbf{P}\|\mathbf{K})
\]

と書ける．

:::details-embedded 証明
\(\log K_{i,j} = -C_{i,j}/\varepsilon\) より

\[\begin{aligned}
 \varepsilon \KLD(\mathbf{P}\|\mathbf{K})
 &=
 \varepsilon\sum_{i,j}
 \left(
 P_{i,j}\log P_{i,j}
 - P_{i,j}\log K_{i,j}
 - P_{i,j}
 + K_{i,j}
 \right) \\
 &=
 \sum_{i,j} C_{i,j}P_{i,j}
 + \varepsilon\sum_{i,j} P_{i,j}(\log P_{i,j}-1)
 + \varepsilon\sum_{i,j} K_{i,j} \\
 &=
 \inner{\mathbf{C}}{\mathbf{P}} - \varepsilon \Hb(\mathbf{P})
 + \varepsilon\sum_{i,j} K_{i,j}.
\end{aligned}\]

最後の項は \(\mathbf{P}\) に依存しない定数なので，
両者の最小化問題は同じ最適解を持つ．
:::
:::


### 正則化パラメータの極限


:::theorem
### Thm: \(\varepsilon \to 0\) による非正則化 OT への収束

\(\varepsilon_k > 0\)，\(\varepsilon_k \to 0\) とし，
\(\mathbf{P}_{\varepsilon_k}\) を正則化問題の一意解とする．
もし部分列 \(\mathbf{P}_{\varepsilon_{k_\ell}}\) が
\(\mathbf{P}^0\) に収束するならば，
\(\mathbf{P}^0\) は非正則化問題

\[
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}}
\]

の最適解である．また最適値は

\[
 \lim_{\varepsilon \to 0}
 \MKD_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
 =
 \MKD_{\mathbf{C}}(\mathbf{a},\mathbf{b})
\]

を満たす．さらに，非正則化問題の最適解が複数ある場合，
\(\mathbf{P}_\varepsilon\) はその中でエントロピー \(\Hb\) が最大のものに収束する．

:::details-embedded 証明
非正則化問題の任意の最適解を \(\mathbf{P}^*\) とする．
\(\mathbf{P}_\varepsilon\) の最適性より

\[
 \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
 - \varepsilon\Hb(\mathbf{P}_\varepsilon)
 \leq
 \inner{\mathbf{C}}{\mathbf{P}^*}
 - \varepsilon\Hb(\mathbf{P}^*).
\]

一方，\(\mathbf{P}^*\) は非正則化問題の最適解なので

\[
 0
 \leq
 \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
 - \inner{\mathbf{C}}{\mathbf{P}^*}
 \leq
 \varepsilon\bigl(\Hb(\mathbf{P}_\varepsilon)-\Hb(\mathbf{P}^*)\bigr).
\]

\(\CouplingsD(\mathbf{a}, \mathbf{b})\) はコンパクトであり，\(\Hb\) はその上で有界なので，
右辺は \(\varepsilon \to 0\) で \(0\) に収束する．
したがって
\(\inner{\mathbf{C}}{\mathbf{P}_\varepsilon} \to \inner{\mathbf{C}}{\mathbf{P}^*}\) である．また
\(\varepsilon\Hb(\mathbf{P}_\varepsilon) \to 0\) なので，
\(\MKD_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b}) \to \MKD_{\mathbf{C}}(\mathbf{a},\mathbf{b})\) である．
任意の極限点 \(\mathbf{P}^0\) は非正則化問題の最適値を達成する．
さらに上の不等式から

\[
 \Hb(\mathbf{P}_\varepsilon) \geq \Hb(\mathbf{P}^*)
\]

が任意の非正則化最適解 \(\mathbf{P}^*\) について成り立つ．
\(\Hb\) は連続なので，任意の極限点 \(\mathbf{P}^0\) は
非正則化最適解の中で \(\Hb\) を最大化する．
非正則化最適解集合は凸であり，\(-\Hb\) は狭義凸であるから，
\(\Hb\) を最大化する非正則化最適解は一意である．したがって
\(\mathbf{P}_\varepsilon\) 全体がその最大エントロピー最適解に収束する．
:::
:::


:::fact
### Rem: \(\varepsilon \to +\infty\) による独立カップリングへの収束

\(\varepsilon \to +\infty\) のとき
\(\mathbf{P}_\varepsilon \to \mathbf{a}\mathbf{b}^\top\) が成り立つ．
\(\varepsilon\) で目的関数を割ると
\(\varepsilon^{-1}\inner{\mathbf{C}}{\mathbf{P}} - \Hb(\mathbf{P})\)
の最小化であり，\(\varepsilon \to +\infty\) では
エントロピー最大化
\(\max_{\mathbf{P} \in \CouplingsD} \Hb(\mathbf{P})\)
に帰着する．周辺分布を固定したエントロピー最大化の解は
独立カップリング \(\mathbf{a}\mathbf{b}^\top\) である．
:::
