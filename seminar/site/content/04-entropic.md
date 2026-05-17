---
id: entropic
nav: エントロピー正則化
eyebrow: 4. Entropic Regularization
title: エントロピー正則化と Sinkhorn アルゴリズム
---


エントロピー正則化は，
最適輸送問題にエントロピー項を加えることで問題を狭義凸化し，
行列スケーリングの反復（Sinkhorn アルゴリズム）で効率的に解を得る手法である．

以下，

\[
 \mathbf{a} \in \R_{++}^{n},\qquad
 \mathbf{b} \in \R_{++}^{m},\qquad
 \sum_{i=1}^{n} a_i = \sum_{j=1}^{m} b_j = 1,
\]

および \(\mathbf{C} \in \R_+^{n \times m}\) を固定する．
離散カップリング集合 \(\CouplingsD(\mathbf{a}, \mathbf{b})\) は
 の通り

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


:::theorem
### Prop: 正則化問題の解の存在と一意性

任意の \(\varepsilon > 0\) に対して，
[ref:Def: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] は一意な最適解
\(\mathbf{P}_\varepsilon \in \CouplingsD(\mathbf{a}, \mathbf{b})\) を持つ．

:::details-embedded 証明
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は空でないコンパクト集合である
（[ref:Clm: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在] の証明）．
関数 \(x \mapsto x\log x - x\) は \([0,\infty)\) 上で連続かつ狭義凸である．
したがって

\[
 \mathbf{P}
 \mapsto
 \inner{\mathbf{C}}{\mathbf{P}} - \varepsilon \Hb(\mathbf{P})
 =
 \inner{\mathbf{C}}{\mathbf{P}}
 + \varepsilon \sum_{i,j} P_{i,j}(\log P_{i,j}-1)
\]

は連続かつ凸である．コンパクト集合上の連続関数なので最小値を達成する．
\(x\log x-x\) の狭義凸性により，異なる2つの最適解があれば
その中点で目的関数がより小さくなるため矛盾する．
よって最適解は一意である．
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


## Sinkhorn アルゴリズム


### 最適解の構造


:::theorem
### Thm: スケーリング形式

[ref:Def: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] の最適解
\(\mathbf{P}_\varepsilon\) は，ある正ベクトル
\(\mathbf{u} \in \R_{++}^{n}\)，\(\mathbf{v} \in \R_{++}^{m}\) により

\[
 \mathbf{P}_\varepsilon
 =
 \diag(\mathbf{u})\,\mathbf{K}\,\diag(\mathbf{v})
\]

と表される．すなわち

\[
 (P_\varepsilon)_{i,j} = u_i K_{i,j} v_j.
\]

:::details-embedded 証明
ラグランジュ関数を

\[
 \mathcal{L}(\mathbf{P},\mathbf{f},\mathbf{g})
 =
 \inner{\mathbf{C}}{\mathbf{P}} - \varepsilon\Hb(\mathbf{P})
 - \inner{\mathbf{f}}{\mathbf{P}\ones_m - \mathbf{a}}
 - \inner{\mathbf{g}}{\mathbf{P}^\top\ones_n - \mathbf{b}}
\]

とおく．[ref:Prop: 正則化解の正値性|正則化解の正値性] より
最適解では \(P_{i,j}>0\) であり，その点での一階条件は

\[
 \frac{\partial \mathcal{L}}{\partial P_{i,j}}
 =
 C_{i,j} + \varepsilon\log P_{i,j} - f_i - g_j
 = 0
\]

である．したがって

\[
 P_{i,j}
 =
 \exp\!\left(\frac{f_i}{\varepsilon}\right)
 \exp\!\left(-\frac{C_{i,j}}{\varepsilon}\right)
 \exp\!\left(\frac{g_j}{\varepsilon}\right).
\]

\(u_i \defeq \exp(f_i/\varepsilon)\)，
\(v_j \defeq \exp(g_j/\varepsilon)\) とおけば，
\(P_{i,j}=u_iK_{i,j}v_j\) を得る．
:::
:::


### Sinkhorn の反復


スケーリング形式を周辺条件に代入すると，

\[
 \mathbf{u} \odot (\mathbf{K}\mathbf{v}) = \mathbf{a},
 \qquad
 \mathbf{v} \odot (\mathbf{K}^\top\mathbf{u}) = \mathbf{b}
\]

が得られる（\(\odot\) はアダマール積）．
Sinkhorn アルゴリズムは，この2つの条件を交互に満たすよう
\(\mathbf{u}\) と \(\mathbf{v}\) を更新する．


各反復は行列ベクトル積 \(\mathbf{K}\mathbf{v}\) および \(\mathbf{K}^\top \mathbf{u}\) を
計算するだけであり，計算量は \(O(nm)\) である．

:::fact
### Rem: Bregman 射影としての解釈

Sinkhorn の各ステップは，KL ダイバージェンスに関する交互射影と解釈できる：

\[\begin{aligned}
 \mathbf{P}^{(\ell+1/2)}
 &= \argmin_{\mathbf{P}\ones_m = \mathbf{a}} \KLD(\mathbf{P} \| \mathbf{P}^{(\ell)}),
 \\
 \mathbf{P}^{(\ell+1)}
 &= \argmin_{\mathbf{P}^\top \ones_n = \mathbf{b}}
 \KLD(\mathbf{P} \| \mathbf{P}^{(\ell+1/2)}).
\end{aligned}\]

行制約と列制約への KL 射影を交互に行うことに対応する．
:::


:::fact
### Rem: GPU 並列化

複数の入力対 \((\mathbf{a}_1, \mathbf{b}_1), \ldots, (\mathbf{a}_N, \mathbf{b}_N)\) に対して
同一コスト行列 \(\mathbf{C}\) のもとでの計算は，
行列 \(\mathbf{A} = [\mathbf{a}_1, \ldots, \mathbf{a}_N]\)，
\(\mathbf{B} = [\mathbf{b}_1, \ldots, \mathbf{b}_N]\) を用いて

\[
 \mathbf{U}^{(\ell+1)} = \mathbf{A} \oslash (\mathbf{K} \mathbf{V}^{(\ell)}), \qquad
 \mathbf{V}^{(\ell+1)} = \mathbf{B} \oslash (\mathbf{K}^\top \mathbf{U}^{(\ell+1)})
\]

と行列--行列積でバッチ化でき，GPU 上で効率的に実行できる．
:::


## 収束性


Sinkhorn アルゴリズムの収束は Hilbert 射影距離を用いて解析される．

:::definition
### Def: Hilbert 射影距離

正ベクトル \(\mathbf{u}, \mathbf{u}' \in \R_{++}^n\) に対して，
**Hilbert 射影距離**を

\[
 d_{\mathrm{H}}(\mathbf{u}, \mathbf{u}')
 \defeq \log \max_{i,j} \frac{u_i \, u'_j}{u_j \, u'_i}
\]

で定義する．\(d_{\mathrm{H}}(\mathbf{u}, \mathbf{u}') = 0\) は
\(\mathbf{u}\) と \(\mathbf{u}'\) が定数倍の関係にあることと同値であり，
射影空間 \(\R_{++}^n / {\sim}\) 上の距離となる．
:::


:::theorem
### Thm: Birkhoff の縮小定理

正行列 \(\mathbf{K} \in \R_{++}^{n \times m}\) に対して，
任意の \(\mathbf{v}, \mathbf{v}' \in \R_{++}^m\) について

\[
 d_{\mathrm{H}}(\mathbf{K}\mathbf{v},\, \mathbf{K}\mathbf{v}')
 \leq \lambda(\mathbf{K}) \, d_{\mathrm{H}}(\mathbf{v},\, \mathbf{v}')
\]

が成り立つ．ここで **Birkhoff 縮小率**
\(\lambda(\mathbf{K}) \in [0, 1)\) は

\[
 \lambda(\mathbf{K})
 = \frac{\sqrt{\eta(\mathbf{K})} - 1}{\sqrt{\eta(\mathbf{K})} + 1},
 \qquad
 \eta(\mathbf{K})
 = \max_{i,j,k,\ell}
 \frac{K_{i,k} \, K_{j,\ell}}{K_{j,k} \, K_{i,\ell}}
\]

で定義される．Gibbs カーネル \(K_{i,j} = e^{-C_{i,j}/\varepsilon}\) に対しては
\(\eta(\mathbf{K}) = e^{2\norm{\mathbf{C}}_\infty / \varepsilon}\) であり，
\(\varepsilon\) が大きいほど \(\lambda(\mathbf{K})\) は小さくなる（収束が速い）．
:::


:::theorem
### Prop: Sinkhorn の線形収束

アルゴリズム のスケーリングベクトルは，
Hilbert 距離の意味で最適スケーリング \((\mathbf{u}^*, \mathbf{v}^*)\) に線形収束する：

\[
 d_{\mathrm{H}}(\mathbf{u}^{(\ell)}, \mathbf{u}^*)
 = O(\lambda(\mathbf{K})^{2\ell}).
\]

停止条件としては，周辺分布の制約違反
\(\norm{\mathbf{P}^{(\ell)} \ones_m - \mathbf{a}}_1\) の監視が実用的である．
:::


## 数値安定性と対数領域計算


\(\varepsilon\) が小さいとき，Gibbs カーネルの成分 \(K_{i,j} = e^{-C_{i,j}/\varepsilon}\) は
機械精度のアンダーフローを起こしうる．
この問題は，**対数領域**（log-domain）で計算を行うことで回避できる．

### 正則化問題の双対


:::theorem
### Prop: エントロピー正則化の双対問題

エントロピー正則化された最適輸送の双対問題は

\[
 \MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})
 = \max_{\mathbf{f} \in \R^n,\, \mathbf{g} \in \R^m}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 - \varepsilon \sum_{i,j} e^{(f_i + g_j - C_{i,j})/\varepsilon}
\]

で与えられる．ここで \((\mathbf{f}, \mathbf{g})\) とスケーリング変数の関係は
\(u_i = e^{f_i/\varepsilon}\)，\(v_j = e^{g_j/\varepsilon}\) である．

:::details-embedded 証明
[ref:Thm: スケーリング形式|スケーリング形式] の証明における
ラグランジュ関数に最適解 \(P_{i,j} = u_i K_{i,j} v_j\) を代入する．
\(P_{i,j} = e^{(f_i + g_j - C_{i,j})/\varepsilon}\) なので

\[\begin{aligned}
 \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
 - \varepsilon\Hb(\mathbf{P}_\varepsilon)
 &= \sum_{i,j} P_{i,j}(C_{i,j} + \varepsilon\log P_{i,j} - \varepsilon) \\
 &= \sum_{i,j} P_{i,j}(f_i + g_j - \varepsilon) \\
 &= \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 - \varepsilon \sum_{i,j} P_{i,j}.
\end{aligned}\]

\(\sum_{i,j} P_{i,j} = \sum_{i,j} e^{(f_i + g_j - C_{i,j})/\varepsilon}\)
を代入すれば結論を得る．
:::
:::


### 対数領域 Sinkhorn


双対変数 \(f_i = \varepsilon \log u_i\)，\(g_j = \varepsilon \log v_j\) を
直接更新すれば，Gibbs カーネルの成分を陽に計算する必要がない．

:::theorem
### Prop: 対数領域の更新式

Sinkhorn の更新は，双対ポテンシャル \((\mathbf{f},\mathbf{g})\) に対して

\[
 f_i
 \leftarrow
 \varepsilon\log a_i
 +
 \smin_\varepsilon
 \bigl(C_{i,1}-g_1,\ldots,C_{i,m}-g_m\bigr),
\]


\[
 g_j
 \leftarrow
 \varepsilon\log b_j
 +
 \smin_\varepsilon
 \bigl(C_{1,j}-f_1,\ldots,C_{n,j}-f_n\bigr)
\]

と書ける．ここで \(\smin_\varepsilon\) は
[ref:Def: ソフト最小値|ソフト最小値] のソフト最小値である．

:::details-embedded 証明
\(\mathbf{u} = \mathbf{a}\oslash(\mathbf{K}\mathbf{v})\) の第 \(i\) 成分は

\[
 u_i
 =
 \frac{a_i}{\sum_j \exp(-C_{i,j}/\varepsilon)\exp(g_j/\varepsilon)}.
\]

両辺の対数を取り \(\varepsilon\) を掛けると

\[
 f_i
 =
 \varepsilon\log a_i
 -
 \varepsilon\log
 \sum_j \exp\!\left(-\frac{C_{i,j}-g_j}{\varepsilon}\right)
 =
 \varepsilon\log a_i
 +
 \smin_\varepsilon(C_{i,1}-g_1,\ldots,C_{i,m}-g_m).
\]

\(\mathbf{v}\) の更新も同様である．
:::
:::


### ソフト最小値と log-sum-exp


:::definition
### Def: ソフト最小値

\(z_1,\ldots,z_m \in \R\) と \(\varepsilon>0\) に対し，
**ソフト最小値**を

\[
 \smin_\varepsilon(z_1,\ldots,z_m)
 \defeq
 -\varepsilon\log\left(\sum_{j=1}^{m} e^{-z_j/\varepsilon}\right)
\]

で定める．\(\varepsilon \to 0\) のとき
\(\smin_\varepsilon \mathbf{z} \to \min_j z_j\) となる．
:::


:::fact
### Rem: log-sum-exp の安定化

\(\smin_\varepsilon\) の計算では，指数関数のオーバーフローを避けるために
**log-sum-exp トリック**を用いる：

\[
 \smin_\varepsilon \mathbf{z}
 = \underline{z} - \varepsilon \log \sum_j e^{-(z_j - \underline{z})/\varepsilon},
 \qquad \underline{z} = \min_j z_j.
\]

指数関数の引数が非正となるため，オーバーフローが回避される．
:::


## 正則化された輸送コストの近似


\(\MKD_{\mathbf{C}}^\varepsilon\) は正則化によりバイアスを含む．
双対変数から非正則化コスト \(\MKD_{\mathbf{C}}\) の近似が得られる．

:::theorem
### Prop: 双対変数からの下界

エントロピー正則化問題の最適双対変数 \((\mathbf{f}^*, \mathbf{g}^*)\) は
非正則化問題の双対実行可能集合 \(\PotentialsD(\mathbf{C})\) に属し，

\[
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 \leq \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
\]

が成り立つ．

:::details-embedded 証明
一階条件 \(f_i^* + g_j^* - C_{i,j} = \varepsilon \log P_{i,j}^*\) において
\(P_{i,j}^* > 0\)（[ref:Prop: 正則化解の正値性|正則化解の正値性]）であるから
\(\log P_{i,j}^*\) は有限であり，特に \(f_i^* + g_j^* \leq C_{i,j}\) が
任意の \((i,j)\) で成り立つ．
したがって \((\mathbf{f}^*, \mathbf{g}^*) \in \PotentialsD(\mathbf{C})\) であり，
非正則化問題の弱双対性から下界が従う．
:::
:::


これを利用して，2種類の **Sinkhorn ダイバージェンス**を定義する：

\[\begin{aligned}
 \mathrm{S}_{\mathbf{C}}^{\varepsilon,\,\mathrm{dual}}(\mathbf{a}, \mathbf{b})
 &\defeq \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 &&(\text{下界}),
 \\
 \mathrm{S}_{\mathbf{C}}^{\varepsilon,\,\mathrm{primal}}(\mathbf{a}, \mathbf{b})
 &\defeq \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
 &&(\text{上界}).
\end{aligned}\]

両者の差は
\(\mathrm{S}^{\varepsilon,\,\mathrm{primal}} - \mathrm{S}^{\varepsilon,\,\mathrm{dual}} = \varepsilon(\Hb(\mathbf{P}_\varepsilon) + 1)\)
であり，\(\varepsilon \to 0\) で消失する．

:::fact
### Rem: \((\mathbf{a}, \mathbf{b})\) に関する凸性

\(\MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})\) は \((\mathbf{a}, \mathbf{b})\) に関して
凸であり，\(\varepsilon > 0\) のとき微分可能で
\(\nabla_{\mathbf{a}} \MKD_{\mathbf{C}}^\varepsilon = \mathbf{f}^*\)，
\(\nabla_{\mathbf{b}} \MKD_{\mathbf{C}}^\varepsilon = \mathbf{g}^*\)
が成り立つ．この性質は Wasserstein 重心の計算などで重要である．
:::
