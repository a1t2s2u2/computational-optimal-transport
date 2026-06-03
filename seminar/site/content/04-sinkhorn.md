---
id: sinkhorn
nav: Sinkhorn 双対
eyebrow: 4. Sinkhorn
title: 正則化問題の双対と Sinkhorn アルゴリズム
---


前章で，エントロピー正則化された離散 Kantorovich 問題\(\MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})\) が一意な最適解 \(\mathbf{P}_\varepsilon\) を持つことを見た．本章ではまず，その解が**全成分正**（＝輸送多面体の内点）であることを示し，この**狭義凸性**と**内点性**を活用して，最適解が \(n+m\) 個の変数で表せること——すなわち \(nm\) 変数の問題が本質的に双対的であること——を示す．この構造から，行列ベクトル積のみで最適解を反復計算する**Sinkhorn アルゴリズム**が自然に導かれる．これは計算最適輸送の中核をなすアルゴリズムである．

本章を通じて，\(\mathbf{a} \in \R_{>0}^n\)，\(\mathbf{b} \in \R_{>0}^m\) はすべての成分が正なヒストグラム（\(\sum_i a_i = \sum_j b_j = 1\)）とする．

## 正則化問題の双対とスケーリング形式


まず，最適解が輸送多面体の内点（全成分が正）であることを確認する．これは以降の一次条件・スケーリング形式の前提となる．

:::theorem
### Prop: 正則化解の正値性

\(\MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})\) の一意解 \(\mathbf{P}_\varepsilon\) は

\[
 (P_\varepsilon)_{i,j} > 0
 \qquad(\forall\, i \in \range{n},\, j \in \range{m})
\]

を満たす．

:::details-embedded 証明
背理法で示す．ある \((i,j)\) で\((P_\varepsilon)_{i,j}=0\) とする．\(a_i>0\) なので同じ行に \((P_\varepsilon)_{i,j_1}>0\) となる\(j_1\) が存在する．また \(b_j>0\) なので同じ列に\((P_\varepsilon)_{i_1,j}>0\) となる \(i_1\) が存在する．小さい \(\theta>0\) に対し，4成分だけを

\[
 P_{i,j} \leftarrow P_{i,j}+\theta,\quad
 P_{i,j_1} \leftarrow P_{i,j_1}-\theta,\quad
 P_{i_1,j} \leftarrow P_{i_1,j}-\theta,\quad
 P_{i_1,j_1} \leftarrow P_{i_1,j_1}+\theta
\]

と変化させる．\(\theta\) を\((P_\varepsilon)_{i,j_1}\) と \((P_\varepsilon)_{i_1,j}\) より小さく取れば，非負性と周辺条件は保たれる．

この変化による目的関数の変化を評価する．線形コストの変化は \(\theta\) に比例する．\((i,j_1)\) 成分と \((i_1,j)\) 成分は正であるから，これらの負エントロピー \(\varphi(x) = x\log x - x\) の変化は\(\varphi'(x) = \log x\) が有限であることから \(O(\theta)\) である．\((i_1,j_1)\) 成分は，正ならば同様に \(O(\theta)\) であり，ゼロならば \(\varphi(\theta)-\varphi(0) = \theta\log\theta - \theta\)が加わるが，これは目的関数をさらに減少させる方向に働く．一方，\((i,j)\) 成分（もともとゼロ）の変化は

\[
 \varphi(\theta) - \varphi(0) = \theta\log\theta - \theta
\]

であり，\(\theta\) で割ると \(\log\theta-1 \to -\infty\)（\(\theta \to 0^+\)）となる．したがって十分小さい \(\theta>0\) ではこの項が支配的となり，目的関数全体が減少する．これは \(\mathbf{P}_\varepsilon\) の最適性に矛盾する．よって全成分が正である．
:::
:::


最適解の構造を取り出す鍵は，正則化問題を Gibbs カーネル \(\mathbf{K}\) のKL 射影（[ref:Prop: 正則化 OT は KL 射影である|正則化 OT は KL 射影である]）とみなし，KL ダイバージェンスの勾配と，周辺制約が定める**アフィン部分空間**の幾何を組み合わせることである．

:::definition
### Def: 周辺制約の方向空間

周辺分布を変えない摂動全体

\[
 \mathcal{T}
 \defeq
 \left\{
 \mathbf{Q} \in \R^{n \times m}
 \;\middle|\;
 \mathbf{Q}\ones_m = \mathbf{0},\;
 \mathbf{Q}^\top \ones_n = \mathbf{0}
 \right\}
\]

を**方向空間**とよぶ．すなわち \(\mathbf{Q} \in \mathcal{T}\) はすべての行和・列和が \(0\) の行列である．
:::


\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) かつ\(\mathbf{Q} \in \mathcal{T}\) ならば \(\mathbf{P} + t\mathbf{Q}\) も（非負性が保たれる限り）周辺制約を満たす．したがって \(\mathcal{T}\) は実行可能集合\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の「動ける方向」を表す．

:::theorem
### Prop: 方向空間の直交補空間

フロベニウス内積に関する \(\mathcal{T}\) の直交補空間は，**ランク 1 の和**の形をした行列全体に一致する：

\[
 \mathcal{T}^\perp
 =
 \left\{
 \mathbf{M} \in \R^{n \times m}
 \;\middle|\;
 \exists\, \mathbf{f} \in \R^n,\, \mathbf{g} \in \R^m
 \text{ s.t. } M_{i,j} = f_i + g_j
 \right\}.
\]

:::details-embedded 証明
\(\mathcal{S} \defeq \{\mathbf{M} : M_{i,j} = f_i + g_j\}\) とおく．

**\(\mathcal{S} \subseteq \mathcal{T}^\perp\)．**\(M_{i,j} = f_i + g_j\) かつ \(\mathbf{Q} \in \mathcal{T}\) ならば

\[
 \inner{\mathbf{M}}{\mathbf{Q}}
 = \sum_{i,j}(f_i + g_j) Q_{i,j}
 = \sum_i f_i \underbrace{\sum_j Q_{i,j}}_{=0}
 + \sum_j g_j \underbrace{\sum_i Q_{i,j}}_{=0}
 = 0.
\]


**\(\mathcal{T}^\perp \subseteq \mathcal{S}\)．**\(\mathbf{M} \in \mathcal{T}^\perp\) とする．任意の添字 \(i, i_1, j, j_1\) に対して，4 成分のみを変化させる行列

\[
 \mathbf{Q}
 = \mathbf{E}_{i,j} - \mathbf{E}_{i,j_1}
 - \mathbf{E}_{i_1,j} + \mathbf{E}_{i_1,j_1}
\]

（\(\mathbf{E}_{k,\ell}\) は \((k,\ell)\) 成分のみ \(1\) の行列）は行和・列和がすべて \(0\) なので \(\mathbf{Q} \in \mathcal{T}\) である．よって \(\inner{\mathbf{M}}{\mathbf{Q}} = 0\)，すなわち

\[
 M_{i,j} - M_{i,j_1} - M_{i_1,j} + M_{i_1,j_1} = 0
 \tag{\(\ast\)}
\]

が任意の \(i, i_1, j, j_1\) で成り立つ．そこで基準の添字 \(i_1 = 1\), \(j_1 = 1\) を固定し，

\[
 f_i \defeq M_{i,1} - M_{1,1}, \qquad
 g_j \defeq M_{1,j}
\]

とおくと，\((\ast)\) より\(M_{i,j} = M_{i,1} + M_{1,j} - M_{1,1} = f_i + g_j\) を得る．したがって \(\mathbf{M} \in \mathcal{S}\)．
:::
:::


:::theorem
### Prop: スケーリング形式

\(\MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})\) の一意解 \(\mathbf{P}_\varepsilon\) は，ある正ベクトル\(\mathbf{u} \in \R_{>0}^n\)，\(\mathbf{v} \in \R_{>0}^m\) を用いて

\[
 (P_\varepsilon)_{i,j} = u_i\, K_{i,j}\, v_j
 \qquad (\forall\, i, j)
\]

と表される．ただし \(\mathbf{K} = \exp(-\mathbf{C}/\varepsilon)\) はGibbs カーネル（[ref:Def: Gibbs カーネル|Gibbs カーネル]）である．行列形式では

\[
 \mathbf{P}_\varepsilon = \diag(\mathbf{u})\, \mathbf{K}\, \diag(\mathbf{v})
\]

と書ける．

:::details-embedded 証明
[ref:Prop: 正則化 OT は KL 射影である|正則化 OT は KL 射影である] より，\(\mathbf{P}_\varepsilon\) はGibbs カーネル \(\mathbf{K}\) の \(\CouplingsD(\mathbf{a}, \mathbf{b})\) への KL 射影

\[
 \mathbf{P}_\varepsilon
 = \argmin_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \KLD(\mathbf{P} \| \mathbf{K})
\]

である．実行可能集合はアフィン集合\(\mathcal{A} \defeq \{\mathbf{P} : \mathbf{P}\ones_m = \mathbf{a},\, \mathbf{P}^\top \ones_n = \mathbf{b}\}\) と非負象限の共通部分だが，\(\mathbf{P}_\varepsilon\) は**内点**，すなわち全成分が正である（[ref:Prop: 正則化解の正値性|正則化解の正値性]）から，非負制約は不活性であり，\(\mathbf{P}_\varepsilon\) は \(\mathcal{A}\) 上で\(\KLD(\cdot \| \mathbf{K})\) を最小化する点とみなせる．

**一次の最適性条件．**任意の \(\mathbf{Q} \in \mathcal{T}\) をとる．\(\mathbf{P}_\varepsilon\) の成分はすべて正なので，十分小さい \(|t|\) に対して\(\mathbf{P}_\varepsilon + t\mathbf{Q} \in \mathcal{A}\) かつ全成分が正であり，実行可能である．\(t \mapsto \KLD(\mathbf{P}_\varepsilon + t\mathbf{Q} \| \mathbf{K})\) は\(t = 0\) で最小値をとるから，

\[
 0 = \left.\frac{\d}{\d t}\right|_{t=0}
 \KLD(\mathbf{P}_\varepsilon + t\mathbf{Q} \| \mathbf{K})
 = \inner{\nabla \KLD(\mathbf{P}_\varepsilon \| \mathbf{K})}{\mathbf{Q}}.
\]

これが任意の \(\mathbf{Q} \in \mathcal{T}\) で成り立つので\(\nabla \KLD(\mathbf{P}_\varepsilon \| \mathbf{K}) \in \mathcal{T}^\perp\)．

**勾配の計算とスケーリング形式．**\(\KLD(\mathbf{P} \| \mathbf{K}) = \sum_{i,j}\bigl(P_{i,j}\log\tfrac{P_{i,j}}{K_{i,j}} - P_{i,j} + K_{i,j}\bigr)\)（[ref:Def: 離散 KL ダイバージェンス|離散 KL ダイバージェンス]）の各成分を \(P_{i,j}\) で微分すると，\(\frac{\partial}{\partial P_{i,j}} \bigl(P_{i,j}\log\tfrac{P_{i,j}}{K_{i,j}} - P_{i,j}\bigr) = \log\tfrac{P_{i,j}}{K_{i,j}} + 1 - 1\) より

\[
 \frac{\partial \KLD(\cdot \| \mathbf{K})}{\partial P_{i,j}}(\mathbf{P}_\varepsilon)
 = \log\frac{(P_\varepsilon)_{i,j}}{K_{i,j}}.
\]

[ref:Prop: 方向空間の直交補空間|方向空間の直交補空間] より，この勾配が \(\mathcal{T}^\perp\) に属することは，ある \(\mathbf{f} \in \R^n\), \(\mathbf{g} \in \R^m\) が存在して

\[
 \log\frac{(P_\varepsilon)_{i,j}}{K_{i,j}} = \frac{f_i + g_j}{\varepsilon}
 \qquad(\forall\, i, j)
\]

となることと同値である（ランク 1 の和の各因子を \(\varepsilon\) 倍して\(\mathbf{f}, \mathbf{g}\) と命名した；これが双対変数となることは備考[ref:Rem: 双対変数とスケーリング変数|双対変数とスケーリング変数] で述べる）．両辺を \((P_\varepsilon)_{i,j}\) について解くと，\(K_{i,j} = e^{-C_{i,j}/\varepsilon}\) より

\[
 (P_\varepsilon)_{i,j}
 = K_{i,j}\, e^{(f_i + g_j)/\varepsilon}
 = \underbrace{e^{f_i/\varepsilon}}_{u_i}
 \underbrace{e^{-C_{i,j}/\varepsilon}}_{K_{i,j}}
 \underbrace{e^{g_j/\varepsilon}}_{v_j}.
\]

\(u_i, v_j > 0\) であり，所望の形を得る．
:::
:::


:::fact
### Rem: 双対変数とスケーリング変数

上の証明に現れた \(\mathbf{f}, \mathbf{g}\) は，周辺制約に対する Lagrange 乗数（**双対変数**）であり，スケーリング変数とは

\[
 u_i = e^{f_i/\varepsilon}, \qquad v_j = e^{g_j/\varepsilon}
\]

で対応する．\(nm\) 個の変数 \(\mathbf{P}\) を持つ問題が，\(n + m\) 個の双対変数 \((\mathbf{f}, \mathbf{g})\) に「縮約」される点が要諦である．この双対変数による定式化は \S で詳しく扱う．
:::


## 行列スケーリングと Sinkhorn の反復


スケーリング形式 \(\mathbf{P}_\varepsilon = \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\) を周辺制約に代入すると，未知ベクトル \((\mathbf{u}, \mathbf{v})\) に対する非線形方程式系が得られる．

:::theorem
### Prop: 行列スケーリング方程式

\(\mathbf{P} = \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\) が\(\CouplingsD(\mathbf{a}, \mathbf{b})\) に属することは，

\[
 \mathbf{u} \odot (\mathbf{K}\mathbf{v}) = \mathbf{a}
 \qquad\text{かつ}\qquad
 \mathbf{v} \odot (\mathbf{K}^\top \mathbf{u}) = \mathbf{b}
\]

と同値である．ただし \(\odot\) は成分ごとの積（アダマール積）である．

:::details-embedded 証明
\(\mathbf{P} = \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\) の\((i,j)\) 成分は \(u_i K_{i,j} v_j\) である．行和は

\[
 (\mathbf{P}\ones_m)_i
 = \sum_j u_i K_{i,j} v_j
 = u_i \sum_j K_{i,j} v_j
 = u_i (\mathbf{K}\mathbf{v})_i
 = \bigl(\mathbf{u} \odot (\mathbf{K}\mathbf{v})\bigr)_i.
\]

これが \(a_i\) に等しいことが第一の制約 \(\mathbf{P}\ones_m = \mathbf{a}\) である．列和についても同様に\((\mathbf{P}^\top \ones_n)_j = v_j (\mathbf{K}^\top \mathbf{u})_j = (\mathbf{v} \odot (\mathbf{K}^\top \mathbf{u}))_j = b_j\)を得る．
:::
:::


この方程式系を直接解くのは難しいが，**交互に**片方ずつ満たすよう更新すれば反復解法が得られる．\(\mathbf{v}\) を固定して第一式を \(\mathbf{u}\) について解けば\(\mathbf{u} = \mathbf{a} \oslash (\mathbf{K}\mathbf{v})\)，\(\mathbf{u}\) を固定して第二式を \(\mathbf{v}\) について解けば\(\mathbf{v} = \mathbf{b} \oslash (\mathbf{K}^\top \mathbf{u})\)となる（\(\oslash\) は成分ごとの除算）．これを交互に繰り返すのが Sinkhorn アルゴリズムである．


:::theorem
### Prop: 反復の整合性と計算量

\(\mathbf{K} \in \R_{>0}^{n \times m}\)，\(\mathbf{a}, \mathbf{b} \in \R_{>0}\) のとき，アルゴリズム の各更新は**0 除算なく定義され**，常に正ベクトルを生成する．各反復の計算量は，行列ベクトル積 \(\mathbf{K}\mathbf{v}\),\(\mathbf{K}^\top \mathbf{u}\) が支配的で \(O(nm)\) である．

:::details-embedded 証明
\(\mathbf{v} > \mathbf{0}\) かつ \(\mathbf{K} > \mathbf{0}\) ならば\(\mathbf{K}\mathbf{v} > \mathbf{0}\)（各成分が正の和）であり，\(\mathbf{a} > \mathbf{0}\) との成分ごとの除算\(\mathbf{a} \oslash (\mathbf{K}\mathbf{v})\) は well-defined かつ正である．\(\mathbf{v}\) の更新も同様．初期値 \(\mathbf{v} = \ones_m > \mathbf{0}\) から帰納的に正値性が保たれる．計算量は \(\mathbf{K}\mathbf{v}\) が \(O(nm)\)，成分ごとの演算が \(O(n) + O(m)\) なので，反復あたり \(O(nm)\)．
:::
:::


:::fact
### Rem: スケーリング変数の定数倍の自由度

方程式系[ref:Prop: 行列スケーリング方程式|行列スケーリング方程式] は，\(\lambda > 0\) に対して\((\mathbf{u}, \mathbf{v}) \mapsto (\lambda\mathbf{u}, \lambda^{-1}\mathbf{v})\)という変換で不変である（\(u_i K_{i,j} v_j = (\lambda u_i) K_{i,j} (\lambda^{-1} v_j)\)）．したがって \((\mathbf{u}, \mathbf{v})\) は定数倍の自由度を除いてのみ定まる．一方，積 \(\mathbf{P} = \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\) は一意である（[ref:Prop: 正則化解の存在と一意性|正則化解の存在と一意性]）．この自由度は，\S で収束を**射影空間**上で論じる動機となる．
:::


## 平滑化された無制約双対


備考[ref:Rem: 双対変数とスケーリング変数|双対変数とスケーリング変数] で触れた双対変数\((\mathbf{f}, \mathbf{g})\) は，実は**無制約な凹最大化問題**の変数として特徴づけられる．これが Sinkhorn の別の——そしてより最適化に即した——解釈を与える．

:::theorem
### Prop: エントロピー正則化の双対問題

エントロピー正則化問題は，次の無制約な凹最大化問題と同じ最適値を持つ：

\[
 \MKD_{\mathbf{C}}^\varepsilon(\mathbf{a}, \mathbf{b})
 = \max_{\mathbf{f} \in \R^n,\, \mathbf{g} \in \R^m}
 E(\mathbf{f}, \mathbf{g}),
 \qquad
 E(\mathbf{f}, \mathbf{g})
 \defeq
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 - \varepsilon \sum_{i,j} e^{(f_i + g_j - C_{i,j})/\varepsilon}.
\]

最大化は，スケーリング形式の双対変数\(f_i^* = \varepsilon \log u_i\), \(g_j^* = \varepsilon \log v_j\)で達成される．

:::details-embedded 証明
正則化問題の Lagrange 関数を，周辺制約のみ緩和して

\[
 \mathcal{L}(\mathbf{P}, \mathbf{f}, \mathbf{g})
 = \inner{\mathbf{C}}{\mathbf{P}}
 + \varepsilon \sum_{i,j}\varphi(P_{i,j})
 - \inner{\mathbf{f}}{\mathbf{P}\ones_m - \mathbf{a}}
 - \inner{\mathbf{g}}{\mathbf{P}^\top \ones_n - \mathbf{b}}
\]

とおく（\(\varphi(x) = x\log x - x\)）．整理すると

\[
 \mathcal{L}(\mathbf{P}, \mathbf{f}, \mathbf{g})
 = \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 + \sum_{i,j}\Bigl[
 (C_{i,j} - f_i - g_j) P_{i,j} + \varepsilon\varphi(P_{i,j})
 \Bigr].
\]


**双対関数の計算．**双対関数 \(E(\mathbf{f}, \mathbf{g}) \defeq \min_{\mathbf{P} \geq \mathbf{0}} \mathcal{L}(\mathbf{P}, \mathbf{f}, \mathbf{g})\) を求める．和は各成分について独立なので，各 \((i,j)\) で\(h(p) \defeq (C_{i,j} - f_i - g_j) p + \varepsilon(p\log p - p)\)を \(p \geq 0\) 上で最小化すればよい．\(h''(p) = \varepsilon/p > 0\) より \(h\) は狭義凸で，\(h'(p) = (C_{i,j} - f_i - g_j) + \varepsilon\log p = 0\) から最小点 \(p^* = e^{(f_i + g_j - C_{i,j})/\varepsilon}\) を得る．このとき \(\varepsilon\log p^* = f_i + g_j - C_{i,j}\) を使うと

\[
 h(p^*)
 = (C_{i,j} - f_i - g_j)p^* + p^*(f_i + g_j - C_{i,j}) - \varepsilon p^*
 = -\varepsilon p^*.
\]

したがって

\[
 E(\mathbf{f}, \mathbf{g})
 = \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 - \varepsilon \sum_{i,j} e^{(f_i + g_j - C_{i,j})/\varepsilon}
\]

となり，主張の目的関数を得る．

**弱双対性．**\(\mathbf{P}_\varepsilon\) は周辺制約を満たすので，任意の \((\mathbf{f}, \mathbf{g})\) に対して\(\mathcal{L}(\mathbf{P}_\varepsilon, \mathbf{f}, \mathbf{g}) = F(\mathbf{P}_\varepsilon) = \MKD_{\mathbf{C}}^\varepsilon\)（乗数項が消える）．ゆえに

\[
 E(\mathbf{f}, \mathbf{g})
 = \min_{\mathbf{P} \geq \mathbf{0}}
 \mathcal{L}(\mathbf{P}, \mathbf{f}, \mathbf{g})
 \leq \mathcal{L}(\mathbf{P}_\varepsilon, \mathbf{f}, \mathbf{g})
 = \MKD_{\mathbf{C}}^\varepsilon.
\]


**強双対性（最適性の達成）．**[ref:Prop: スケーリング形式|スケーリング形式] の双対変数\(f_i^* = \varepsilon\log u_i\), \(g_j^* = \varepsilon\log v_j\) をとると，\(e^{(f_i^* + g_j^* - C_{i,j})/\varepsilon} = u_i K_{i,j} v_j = (P_\varepsilon)_{i,j}\) であり，\(\sum_{i,j}(P_\varepsilon)_{i,j} = 1\) なので第 3 項は\(-\varepsilon\sum_{i,j}(P_\varepsilon)_{i,j} = -\varepsilon\)．さらに周辺制約より

\[
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 = \sum_{i,j}(f_i^* + g_j^*)(P_\varepsilon)_{i,j}
 = \sum_{i,j}(P_\varepsilon)_{i,j}
 \bigl(C_{i,j} + \varepsilon\log(P_\varepsilon)_{i,j}\bigr).
\]

ここで \(\sum (P_\varepsilon)\log(P_\varepsilon) = 1 - \Hb(\mathbf{P}_\varepsilon)\)（\(\Hb(\mathbf{P}) = -\sum P\log P + 1\)，備考[ref:Rem: 通常の Shannon エントロピーとの違い|通常の Shannon エントロピーとの違い]）を用いると

\[
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 = \inner{\mathbf{C}}{\mathbf{P}_\varepsilon}
 + \varepsilon\bigl(1 - \Hb(\mathbf{P}_\varepsilon)\bigr)
 = \MKD_{\mathbf{C}}^\varepsilon + \varepsilon.
\]

ゆえに\(E(\mathbf{f}^*, \mathbf{g}^*) = (\MKD_{\mathbf{C}}^\varepsilon + \varepsilon) - \varepsilon = \MKD_{\mathbf{C}}^\varepsilon\)．弱双対性の上界が達成されたので，これが最大値である．
:::
:::


:::fact
### Rem: ハード制約のソフト化

双対関数 \(E\) の各項\(-\varepsilon\, e^{(f_i + g_j - C_{i,j})/\varepsilon}\) は，\(f_i + g_j > C_{i,j}\) を強く罰する**指数ペナルティ**である．\(\varepsilon \to 0\) ではこのペナルティが「ハード制約」\(f_i + g_j \leq C_{i,j}\) に漸近し，非正則化 Kantorovich 問題の双対（後の章で扱う）へと連続的に移行する．正則化は，この制約を**ソフト化**するものと見なせる．
:::


双対が無制約かつ滑らかであることは，Sinkhorn 反復に明快な最適化的意味を与える．

:::theorem
### Prop: Sinkhorn はブロック座標上昇である

双対目的関数 \(E\) は凹であり，\(\mathbf{g}\) を固定して\(\mathbf{f}\) について \(E\) を最大化すると\(u_i = e^{f_i/\varepsilon} = a_i / (\mathbf{K}\mathbf{v})_i\)，\(\mathbf{f}\) を固定して \(\mathbf{g}\) について最大化すると\(v_j = e^{g_j/\varepsilon} = b_j / (\mathbf{K}^\top \mathbf{u})_j\)となる．すなわち Sinkhorn 反復は，双対問題に対する**厳密なブロック座標上昇**（block coordinate ascent）である．

:::details-embedded 証明
\(E\) の各項は \((\mathbf{f}, \mathbf{g})\) について線形項と\(-\varepsilon\,e^{(\cdot)/\varepsilon}\)（凹関数）の和なので，\(E\) は凹である．\(\mathbf{g}\) を固定すると，\(E\) は \(f_i\) について分離し，\(f_i\) に依存する部分は\(a_i f_i - \varepsilon\, e^{f_i/\varepsilon}(\mathbf{K}\mathbf{v})_i\)である（\((\mathbf{K}\mathbf{v})_i = \sum_j e^{(g_j - C_{i,j})/\varepsilon}\)）．\(f_i\) で偏微分して \(0\) とおくと

\[
 a_i - e^{f_i/\varepsilon}(\mathbf{K}\mathbf{v})_i = 0
 \;\Longleftrightarrow\;
 u_i = e^{f_i/\varepsilon} = \frac{a_i}{(\mathbf{K}\mathbf{v})_i},
\]

これは凹関数の唯一の最大点である．まとめて \(\mathbf{u} = \mathbf{a} \oslash (\mathbf{K}\mathbf{v})\)，すなわちアルゴリズム の第 3 行に一致する．\(\mathbf{g}\) についても同様に第 4 行を得る．
:::
:::


:::fact
### Rem: 勾配と周辺制約違反

\(\partial E / \partial f_i = a_i - e^{f_i/\varepsilon}(\mathbf{K}\mathbf{v})_i = a_i - (\mathbf{P}\ones_m)_i\) であり，双対勾配は**周辺制約の違反量**そのものである．Sinkhorn の 1 ステップはこの勾配を（ブロックごとに）厳密にゼロにする操作であり，停止判定に \(\norm{\mathbf{P}\ones_m - \mathbf{a}}_1\) を用いる根拠でもある．
:::


## 収束性


Sinkhorn 反復が（スケーリングの定数倍を除いて）一意の解に**線形収束**することを，本節では主張のみ述べる（証明は射影幾何を要するため割愛する）．鍵は，正行列が**Hilbert 射影計量**を縮小するというBirkhoff の縮小定理である．

:::definition
### Def: Hilbert 射影計量

正ベクトル \(\mathbf{u}, \mathbf{u}' \in \R_{>0}^n\) に対して，**Hilbert 射影計量**を

\[
 \dHil(\mathbf{u}, \mathbf{u}')
 \defeq
 \log \max_{i, k}
 \frac{u_i\, u'_k}{u_k\, u'_i}
\]

で定める．これは \(\dHil(\mathbf{u},\mathbf{u}') \geq 0\) を満たし，等号は \(\mathbf{u}' = \lambda\mathbf{u}\)（ある \(\lambda>0\)）と同値で，定数倍を同一視した射影空間 \(\R_{>0}^n / {\sim}\) 上の距離となる．
:::


:::theorem
### Thm: Birkhoff の縮小定理

正行列 \(\mathbf{K} \in \R_{>0}^{n \times m}\) は Hilbert 射影計量を縮小する：ある縮小率 \(\lambda(\mathbf{K}) \in [0,1)\) が存在して，任意の \(\mathbf{v}, \mathbf{v}' \in \R_{>0}^m\) で

\[
 \dHil(\mathbf{K}\mathbf{v}, \mathbf{K}\mathbf{v}')
 \leq \lambda(\mathbf{K})\, \dHil(\mathbf{v}, \mathbf{v}'),
 \qquad
 \lambda(\mathbf{K})
 = \frac{\sqrt{\eta(\mathbf{K})} - 1}{\sqrt{\eta(\mathbf{K})} + 1}
\]

が成り立つ．ここで\(\eta(\mathbf{K}) = \max_{i,j,k,\ell} \frac{K_{i,k}\, K_{j,\ell}}{K_{j,k}\, K_{i,\ell}}\)は成分比の最大歪みである．Gibbs カーネル \(K_{i,j} = e^{-C_{i,j}/\varepsilon}\) では\(\eta(\mathbf{K}) \leq e^{2\norm{\mathbf{C}}_\infty/\varepsilon}\)となり（\(\mathbf{C} \geq \mathbf{0}\) による），\(\varepsilon\) が小さいほど \(\lambda(\mathbf{K}) \to 1\) で収束は遅くなる．
:::


:::theorem
### Thm: Sinkhorn の線形収束

Sinkhorn 写像\(\mathcal{S}(\mathbf{v}) \defeq \mathbf{b} \oslash \bigl(\mathbf{K}^\top (\mathbf{a} \oslash (\mathbf{K}\mathbf{v}))\bigr)\)は，射影計量 \(\dHil\) に関して縮小率 \(\lambda(\mathbf{K})^2\) の縮小写像である：

\[
 \dHil(\mathcal{S}(\mathbf{v}), \mathcal{S}(\mathbf{v}'))
 \leq \lambda(\mathbf{K})^2\, \dHil(\mathbf{v}, \mathbf{v}').
\]

ゆえに射影空間上に一意の不動点 \([\mathbf{v}^*]\) が存在し，反復列は

\[
 \dHil(\mathbf{v}^{(\ell)}, \mathbf{v}^*)
 \leq \lambda(\mathbf{K})^{2\ell}\,
 \dHil(\mathbf{v}^{(0)}, \mathbf{v}^*)
\]

で線形収束する．対応する輸送計画 \(\mathbf{P}^{(\ell)}\) は正則化問題の一意解 \(\mathbf{P}_\varepsilon\) に収束する．
:::


:::fact
### Rem: 収束率の意味と停止判定

縮小率が \(\lambda(\mathbf{K})\) ではなく \(\lambda(\mathbf{K})^2\) になるのは，1 反復が \(\mathbf{K}\) と \(\mathbf{K}^\top\) による 2 度の縮小を含むためである（除算 \(\oslash\) は射影計量を変えない）．実装では各反復で周辺制約の違反量\(\norm{\mathbf{P}^{(\ell)}\ones_m - \mathbf{a}}_1\) を監視して停止する．これは備考[ref:Rem: 勾配と周辺制約違反|勾配と周辺制約違反] の通り双対勾配のノルムである．
:::


:::fact
### Rem: 本章のまとめと展望

エントロピー正則化の狭義凸性は，最適解を \(n+m\) 個のスケーリング変数へ縮約し（[ref:Prop: スケーリング形式|スケーリング形式]），無制約で滑らかな双対（[ref:Prop: エントロピー正則化の双対問題|エントロピー正則化の双対問題]）を生む．Sinkhorn 反復はその双対に対するブロック座標上昇であり（[ref:Prop: Sinkhorn はブロック座標上昇である|Sinkhorn はブロック座標上昇である]），Hilbert 計量の意味で線形収束する（[ref:Thm: Sinkhorn の線形収束|Sinkhorn の線形収束]）．

双対の指数ペナルティ（備考[ref:Rem: ハード制約のソフト化|ハード制約のソフト化]）を\(\varepsilon \to 0\) で硬化させると，非正則化 Kantorovich 問題の**双対**と**\(c\)-変換**が現れる．この古典双対・\(c\)-変換と，小さい \(\varepsilon\) における対数領域での数値安定化（ソフト最小値による \(c\)-変換のソフト化）は次章以降で扱い，そこから Brenier 定理・測地線・Wasserstein 幾何へと進む．
:::
