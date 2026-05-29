---
id: entropic
nav: エントロピー正則化
eyebrow: 3. Entropic Regularization
title: エントロピー正則化
---


離散 Kantorovich 問題の最適解は一般に一意でない
（[ref:Ex: 最適解の非一意性|最適解の非一意性]）．
本章では，目的関数に負エントロピー項を加えた
**エントロピー正則化問題**を導入する．
正則化された目的関数は狭義凸となるため，
任意の \(\varepsilon > 0\) に対して正則化問題の最適解は一意に定まる．
さらに \(\varepsilon \to 0\) の極限では，
非正則化問題の最適解の中で最大エントロピーのものが選ばれる．

以下，

\[
  \mathbf{a} \in \R_{>0}^{n},\qquad
  \mathbf{b} \in \R_{>0}^{m},\qquad
  \sum_{i=1}^{n} a_i = \sum_{j=1}^{m} b_j = 1,
\]

および \(\mathbf{C} \in \R_{\geq 0}^{n \times m}\) を固定する．
なお，正則化問題の一意性自体は \(\mathbf{a}, \mathbf{b}\) に
ゼロ成分を許しても成立する．
全成分正の仮定は正値性
（正則化解の正値性）に用いる．
離散カップリング集合 \(\CouplingsD(\mathbf{a}, \mathbf{b})\) は
[ref:Prop: 連続 Kantorovich 問題の離散化|連続 Kantorovich 問題の離散化] の通り

\[
  \CouplingsD(\mathbf{a}, \mathbf{b})
  =
  \left\{
    \mathbf{P} \in \R_{\geq 0}^{n \times m}
    \;\middle|\;
    \mathbf{P}\ones_m = \mathbf{a},\;
    \mathbf{P}^\top \ones_n = \mathbf{b}
  \right\}
\]

である．


## エントロピー正則化


:::definition
### Def: 離散エントロピー

非負行列 \(\mathbf{P} \in \R_{\geq 0}^{n \times m}\) に対して，
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
\(-\Hb\) の微分が

\[
  \frac{\partial(-\Hb)}{\partial P_{i,j}} = \log P_{i,j}
\]

と簡単になるからである．
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


:::fact
### Rem: 狭義凸化の仕組み

元の Kantorovich 問題の目的関数 \(\inner{\mathbf{C}}{\mathbf{P}}\) は
\(\mathbf{P}\) に関して線形（したがって凸だが狭義凸でない）であった．
エントロピー項 \(-\varepsilon\Hb(\mathbf{P})
= \varepsilon\sum_{i,j}P_{i,j}(\log P_{i,j}-1)\) を加えることで，
目的関数は狭義凸となる．
凸集合上の狭義凸関数の最小化問題では
最適解が存在すれば一意であるから，
一意性が構造的に保証される
（[ref:Prop: 狭義凸関数の最小点の一意性|狭義凸関数の最小点の一意性]）．
:::


:::proposition
### Prop: 正則化問題の解の存在と一意性

任意の \(\varepsilon > 0\) に対して，
正則化問題は一意な最適解
\(\mathbf{P}_\varepsilon \in \CouplingsD(\mathbf{a}, \mathbf{b})\) を持つ．

:::details-embedded 証明
**存在．**
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は空でないコンパクト集合である
（[ref:Clm: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在] の証明）．
関数 \(\varphi(x) \defeq x\log x - x\) は \([0,\infty)\) 上で連続であるから，
目的関数

\[
  F(\mathbf{P})
  \defeq
  \inner{\mathbf{C}}{\mathbf{P}} - \varepsilon \Hb(\mathbf{P})
  =
  \inner{\mathbf{C}}{\mathbf{P}}
  + \varepsilon \sum_{i,j} \varphi(P_{i,j})
\]

も連続である．
コンパクト集合上の連続関数は最小値を達成するから，
最適解が存在する．

**一意性．**
\(\varphi\) は \([0,\infty)\) 上で狭義凸であることを示す．
任意の \(x_1 \neq x_2 \in [0,\infty)\)，\(\lambda \in (0,1)\) に対し
\(x^* \defeq \lambda x_1+(1-\lambda)x_2\) とおく．
\(\varphi\) は \([0,\infty)\) 上で連続かつ \((0,\infty)\) 上で微分可能であるから，
平均値の定理より

\[\begin{aligned}
  \varphi(x_1)-\varphi(x^*) &= \varphi'(c_1)(x_1-x^*), \\
  \varphi(x_2)-\varphi(x^*) &= \varphi'(c_2)(x_2-x^*)
\end{aligned}\]

なる \(c_1\)（\(x_1\) と \(x^*\) の間），
\(c_2\)（\(x^*\) と \(x_2\) の間）が存在する．
\(\lambda\) 倍，\((1-\lambda)\) 倍してそれぞれ足すと，
\(x_1-x^* = (1-\lambda)(x_1-x_2)\)，
\(x_2-x^* = \lambda(x_2-x_1)\) であるから

\[
  \lambda\varphi(x_1)+(1-\lambda)\varphi(x_2)-\varphi(x^*)
  = \lambda(1-\lambda)(x_1-x_2)
    \bigl[\varphi'(c_1)-\varphi'(c_2)\bigr].
\]

\(c_1\) と \(c_2\) は \(x^*\) の反対側にあるので
\((x_1-x_2)\) と \((c_1-c_2)\) は同符号であり，
\(\varphi'(x)=\log x\) は狭義単調増加なので
\((c_1-c_2)\) と \((\varphi'(c_1)-\varphi'(c_2))\) も同符号である．
したがって
\((x_1-x_2)[\varphi'(c_1)-\varphi'(c_2)] > 0\) であり，
\(\lambda(1-\lambda) > 0\) と合わせて
\(\varphi(x^*) < \lambda\varphi(x_1)+(1-\lambda)\varphi(x_2)\)
を得る．
\(\mathbf{P} \neq \mathbf{Q}\) ならばある成分で
狭義凸性が効くので，\(\mathbf{P} \mapsto \sum_{i,j}\varphi(P_{i,j})\)
は \(\CouplingsD(\mathbf{a},\mathbf{b})\) 上で狭義凸である．
\(\inner{\mathbf{C}}{\mathbf{P}}\) は線形（したがって凸）であるから，
\(F = \inner{\mathbf{C}}{\mathbf{P}} + \varepsilon\sum_{i,j}\varphi(P_{i,j})\)
も狭義凸である．
狭義凸関数の最小点の一意性より最小点は一意．
:::
:::


:::proposition
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

この変化による目的関数の変化を評価する．
線形コストの変化は \(\theta\) に比例する．
\((i,j_1)\) 成分と \((i_1,j)\) 成分は正であるから，
これらの負エントロピー \(\varphi(x) = x\log x - x\) の変化は
\(\varphi'(x) = \log x\) が有限であることから \(O(\theta)\) である．
\((i_1,j_1)\) 成分は，正ならば同様に \(O(\theta)\) であり，
ゼロならば \(\varphi(\theta)-\varphi(0) = \theta\log\theta - \theta\)
が加わるが，これは目的関数をさらに減少させる方向に働く．
一方，\((i,j)\) 成分（もともとゼロ）の変化は

\[
  \varphi(\theta) - \varphi(0) = \theta\log\theta - \theta
\]

であり，\(\theta\) で割ると \(\log\theta-1 \to -\infty\)
（\(\theta \to 0^+\)）となる．
したがって十分小さい \(\theta>0\) では
この項が支配的となり，目的関数全体が減少する．
これは \(\mathbf{P}_\varepsilon\) の最適性に矛盾する．
よって全成分が正である．
:::
:::


:::fact
### Rem: \(\varepsilon\) の役割

\(\varepsilon\) は，元の線形計画と独立カップリングの間を補間する量である：

- \(\varepsilon \to 0\) のとき，\(\mathbf{P}_\varepsilon\) は
  非正則化問題 \(\MKD_{\mathbf{C}}\) の最適解のうち
  エントロピーが最大のものに収束する．
- \(\varepsilon \to +\infty\) のとき，\(\mathbf{P}_\varepsilon\) は
  積測度 \(\mathbf{a} \mathbf{b}^\top\) に収束する．
:::


## KL ダイバージェンスによる定式化


:::definition
### Def: 離散 KL ダイバージェンス

非負行列 \(\mathbf{P}, \mathbf{K} \in \R_{\geq 0}^{n \times m}\) に対して，
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
**Gibbs カーネル** \(\mathbf{K} \in \R_{>0}^{n \times m}\) を

\[
  K_{i,j} \defeq \exp\!\left(-\frac{C_{i,j}}{\varepsilon}\right)
\]

で定める．
:::


:::proposition
### Prop: 正則化 OT は KL 射影である

\(\mathbf{K} = \exp(-\mathbf{C}/\varepsilon)\) とすると，
正則化問題の最適解は

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


## 正則化パラメータの極限


非正則化 Kantorovich 問題が複数の最適解を持つとき，
エントロピー正則化はそのうちの一つ——
エントロピーが最大のもの——を自然に選び出す．


:::theorem
### Thm: \(\varepsilon \to 0\) による非正則化 OT への収束

\(\varepsilon_k > 0\)，\(\varepsilon_k \to 0\) とし，
\(\mathbf{P}_{\varepsilon_k}\) を正則化問題の一意解とする．
このとき，以下が成り立つ．

**(i)**
最適値は収束する：
\(\displaystyle
  \lim_{\varepsilon \to 0}
  \MKD_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
  =
  \MKD_{\mathbf{C}}(\mathbf{a},\mathbf{b}).
\)

**(ii)**
\(\mathbf{P}_{\varepsilon_k}\) の任意の極限点は
非正則化問題の最適解である．

**(iii)**
\(\{\mathbf{P}_\varepsilon\}_{\varepsilon > 0}\) 全体が，
非正則化最適解の中でエントロピー \(\Hb\) を最大化する
一意な解に収束する：

\[
  \mathbf{P}_\varepsilon
  \;\xrightarrow{\varepsilon \to 0}\;
  \argmax_{\mathbf{P} \in S^*} \Hb(\mathbf{P}).
\]

:::details-embedded 証明
非正則化問題の任意の最適解を \(\mathbf{P}^*\) とする．

**(i), (ii).**
\(\mathbf{P}_\varepsilon\) の最適性より

\[
  \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
  - \varepsilon\Hb(\mathbf{P}_\varepsilon)
  \leq
  \inner{\mathbf{C}}{\mathbf{P}^*}
  - \varepsilon\Hb(\mathbf{P}^*).
\]

一方，\(\mathbf{P}^*\) は非正則化問題の最適解なので
\(\inner{\mathbf{C}}{\mathbf{P}^*}
\leq \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}\) であり，

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
\(\inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
\to \inner{\mathbf{C}}{\mathbf{P}^*}
= \MKD_{\mathbf{C}}(\mathbf{a},\mathbf{b})\) であり，
\(\varepsilon\Hb(\mathbf{P}_\varepsilon) \to 0\) なので
\(\MKD_{\mathbf{C}}^\varepsilon \to \MKD_{\mathbf{C}}\) を得る．
コンパクト集合 \(\CouplingsD(\mathbf{a},\mathbf{b})\) 内の
任意の極限点は非正則化問題の最適値を達成するから，
最適解である．

**(iii).**
上の不等式から
\(\Hb(\mathbf{P}_\varepsilon) \geq \Hb(\mathbf{P}^*)\)
が任意の非正則化最適解 \(\mathbf{P}^*\) について成り立つ．
\(\Hb\) は連続であるから，任意の極限点 \(\mathbf{P}^0\) は
非正則化最適解の中で \(\Hb\) を最大化する．
最適解集合 \(S^*\) は凸であり（[ref:Clm: 最適解集合は凸かつコンパクト|最適解集合は凸かつコンパクト]），
\(-\Hb\) は狭義凸であるから，
狭義凸関数の最小点の一意性より
\(\Hb\) を最大化する \(S^*\) の元は一意である．
したがって \(\{\mathbf{P}_\varepsilon\}\) の任意の収束部分列は
同一の極限を持ち，コンパクト集合内の点列でこの性質を持つものは
全体として収束するから，
\(\mathbf{P}_\varepsilon\) は最大エントロピー最適解に収束する．
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
