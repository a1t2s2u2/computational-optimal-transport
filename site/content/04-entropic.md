---
id: entropic
nav: エントロピー正則化
eyebrow: 4. Entropic Regularization
title: エントロピー正則化と Sinkhorn アルゴリズム
---


離散 Kantorovich 問題は線形計画として解ける．
目的関数にエントロピー項を加えると，最適解は一意になり，
行列スケーリングによって計算できる．この行列スケーリング反復を
**Sinkhorn アルゴリズム**という．

以下，

\[
 \mathbf{a} \in \R_{++}^{n},\qquad
 \mathbf{b} \in \R_{++}^{m},\qquad
 \sum_{i=1}^{n} a_i = \sum_{j=1}^{m} b_j = 1,
\]

および \(\mathbf{C} \in \R_+^{n \times m}\) を固定する．
輸送多面体 \(\CouplingsD(\mathbf{a}, \mathbf{b})\) は
[ref:主張: 離散カップリングの行列表示|離散カップリングの行列表示] の通り

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
### 定義: 離散エントロピー

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
### 通常の Shannon エントロピーとの違い

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
### 定義: エントロピー正則化された離散最適輸送

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
### 命題: 正則化問題の解の存在と一意性

任意の \(\varepsilon > 0\) に対して，
[ref:定義: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] は一意な最適解
\(\mathbf{P}_\varepsilon \in \CouplingsD(\mathbf{a}, \mathbf{b})\) を持つ．

:::details-embedded 証明
輸送多面体 \(\CouplingsD(\mathbf{a}, \mathbf{b})\) は空でないコンパクト集合である
（[ref:主張: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在] の証明）．
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
### 命題: 正則化解の正値性

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
### \(\varepsilon\) の役割

\(\varepsilon\) は，元の線形計画と独立カップリングの間を補間する量である：

- \(\varepsilon\) が小さいほど，線形項 \(\inner{\mathbf{C}}{\mathbf{P}}\) が支配的になり，非正則化 OT に近づく．
- \(\varepsilon\) が大きいほど，エントロピー項が支配的になり， 質量を広く分散させるカップリングに近づく．

この意味で，エントロピー正則化は「疎な最適輸送計画」を
「拡散した輸送計画」に滑らかに変形する操作である．
:::


## KL 射影としての定式化


:::definition
### 定義: 離散 KL ダイバージェンス

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
### 定義: Gibbs カーネル

コスト行列 \(\mathbf{C}\) と \(\varepsilon > 0\) に対して，
**Gibbs カーネル** \(\mathbf{K} \in \R_{++}^{n \times m}\) を

\[
 K_{i,j} \defeq \exp\!\left(-\frac{C_{i,j}}{\varepsilon}\right)
\]

で定める．
:::


:::theorem
### 命題: 正則化 OT は KL 射影である

\(\mathbf{K} = \exp(-\mathbf{C}/\varepsilon)\) とすると，
[ref:定義: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] の最適解は

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


:::fact
KL 射影という見方では，

\[
 \text{Gibbs カーネル } \mathbf{K}
 \quad\longrightarrow\quad
 \text{周辺制約を満たす最近点 } \mathbf{P}_\varepsilon
\]

を KL ダイバージェンスで測っている．Sinkhorn アルゴリズムは，
行和制約と列和制約への KL 射影を交互に行う反復として理解できる．
:::


## Sinkhorn アルゴリズム


### 最適解のスケーリング形式


:::theorem
### 定理: スケーリング形式

[ref:定義: エントロピー正則化された離散最適輸送|エントロピー正則化された離散最適輸送] の最適解
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

とおく．[ref:命題: 正則化解の正値性|正則化解の正値性] より
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


:::fact
### スケーリングの非一意性

\(\lambda>0\) に対して
\((\mathbf{u},\mathbf{v})\) を
\((\lambda\mathbf{u},\lambda^{-1}\mathbf{v})\) に置き換えても
\(\diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\) は変わらない．
したがってスケーリングベクトル自体は一意でないが，
輸送計画 \(\mathbf{P}_\varepsilon\) は一意である．
:::


### 行列スケーリング反復


スケーリング形式を周辺条件に代入すると，

\[
 \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\ones_m = \mathbf{a},
 \qquad
 \diag(\mathbf{v})\mathbf{K}^\top\diag(\mathbf{u})\ones_n = \mathbf{b}
\]

である．成分ごとに書けば

\[
 \mathbf{u} \odot (\mathbf{K}\mathbf{v}) = \mathbf{a},
 \qquad
 \mathbf{v} \odot (\mathbf{K}^\top\mathbf{u}) = \mathbf{b}.
\]

したがって，一方を固定すれば他方は成分ごとの割り算で更新できる：

\[
 \mathbf{u} \leftarrow \mathbf{a} \oslash (\mathbf{K}\mathbf{v}),
 \qquad
 \mathbf{v} \leftarrow \mathbf{b} \oslash (\mathbf{K}^\top\mathbf{u}).
\]


:::theorem
### 定理: Sinkhorn 反復の収束

\(\mathbf{K} \in \R_{++}^{n \times m}\) かつ
\(\mathbf{a} \in \R_{++}^n\)，\(\mathbf{b} \in \R_{++}^m\) のとき，
 が生成する輸送計画

\[
 \mathbf{P}^{(\ell)}
 \defeq
 \diag(\mathbf{u}^{(\ell)})\mathbf{K}\diag(\mathbf{v}^{(\ell)})
\]

は，正則化問題の一意解 \(\mathbf{P}_\varepsilon\) に収束する．

:::details-embedded 証明
完全な証明には Hilbert 射影距離に関する Birkhoff の縮小定理を用いる．
この定理は正行列が正錐の射影距離に関して縮小写像を誘導することを述べる．
直感的には，各反復で行和制約と列和制約を交互に満たすように
正の行列 \(\mathbf{K}\) をスケールし，正の行列の錐の中でこの操作が縮小写像として働くため，
極限のスケーリング行列が一意に定まる．
:::
:::


:::fact
### 計算量と並列性

Sinkhorn の1反復は
\(\mathbf{K}\mathbf{v}\) と \(\mathbf{K}^\top\mathbf{u}\) の2つの行列ベクトル積であり，
計算量は \(O(nm)\) である．ネットワーク単体法と異なり，反復の中心は密な線形代数演算なので，
GPU やバッチ計算と相性がよい．
:::


## 対数領域 Sinkhorn


小さい \(\varepsilon\) では
\(K_{i,j}=\exp(-C_{i,j}/\varepsilon)\) が数値的に \(0\) に近くなり，
通常の Sinkhorn 反復は不安定になりやすい．そのため実装では，
スケーリングベクトルそのものではなく，双対ポテンシャル

\[
 f_i \defeq \varepsilon \log u_i,
 \qquad
 g_j \defeq \varepsilon \log v_j
\]

を更新する．

:::definition
### 定義: ソフト最小値

\(z_1,\ldots,z_m \in \R\) と \(\varepsilon>0\) に対し，
**ソフト最小値**を

\[
 \smin_\varepsilon(z_1,\ldots,z_m)
 \defeq
 -\varepsilon\log\left(\sum_{j=1}^{m} e^{-z_j/\varepsilon}\right)
\]

で定める．
:::


:::theorem
### 命題: 対数領域の更新式

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

と書ける．

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


## 正則化の正当性


エントロピー正則化の数学的な正当化は次の3点に集約される：

\[
 \text{一意な解}
 \quad+\quad
 \text{Sinkhorn による計算}
 \quad+\quad
 \varepsilon \to 0 \text{ で元問題に戻ること}.
\]


:::theorem
### 定理: \(\varepsilon \to 0\) による非正則化 OT への収束

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

輸送多面体はコンパクトであり，\(\Hb\) はその上で有界なので，
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


:::theorem
### 定理: \(\varepsilon \to +\infty\) による独立カップリングへの収束

\(\varepsilon \to +\infty\) のとき，
正則化問題の解は

\[
 \mathbf{P}_\varepsilon \to \mathbf{a}\mathbf{b}^\top
\]

に収束する．ここで
\((\mathbf{a}\mathbf{b}^\top)_{i,j}=a_i b_j\) は，
ソースとターゲットを独立に結合するカップリングである．

:::details-embedded 証明
\(\varepsilon\) で目的関数を割ると

\[
 \frac{1}{\varepsilon}\inner{\mathbf{C}}{\mathbf{P}}
 - \Hb(\mathbf{P})
\]

を最小化していることになる．\(\varepsilon \to +\infty\) では
第一項が消え，極限問題は

\[
 \max_{\mathbf{P} \in \CouplingsD(\mathbf{a},\mathbf{b})}
 \Hb(\mathbf{P})
\]

である．周辺分布を固定したとき，エントロピーを最大にする結合は
独立カップリング \(\mathbf{a}\mathbf{b}^\top\) である．したがって
\(\mathbf{P}_\varepsilon\) は \(\mathbf{a}\mathbf{b}^\top\) に収束する．
:::
:::


:::fact
以上により，エントロピー正則化は

\[
 \varepsilon \to 0
 \quad\Longrightarrow\quad
 \text{非正則化 OT},
 \qquad
 \varepsilon \to +\infty
 \quad\Longrightarrow\quad
 \text{独立カップリング}
\]

という2つの極限を持つ．実用上は，小さすぎる \(\varepsilon\) は数値不安定を招き，
大きすぎる \(\varepsilon\) は輸送構造をぼかしすぎる．
したがって \(\varepsilon\) は「計算安定性」と「非正則化 OT への近さ」の
トレードオフを制御するパラメータである．
:::
