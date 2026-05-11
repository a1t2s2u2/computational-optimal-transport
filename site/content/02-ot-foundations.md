---
id: ot-foundations
nav: Monge と Kantorovich
eyebrow: 2. OT Foundations
title: Optimal Transport の基礎理論
---


:::fact
### 本章の設定

\(\X, \Y\) は**完備可分な距離空間**（Polish 空間，
[ref:定義: Polish 空間|Polish 空間]）とする．距離関数を \(d\) と書き，
ボレル \(\sigma\)-代数 \(\Bb(\X)\) により \(\X\) を可測空間 \((\X, \Bb(\X))\) として扱う
（\(\Y\) についても同様）．\(\X\) 上の確率測度全体を \(\Mm_+^1(\X)\) と記す．

Polish 空間の3要素を確認する：

- **距離空間**．距離関数 \(d \colon \X \times \X \to [0, \infty)\) が距離の公理 （[ref:定義: 距離空間|距離空間]）を満たし，\(d\) から以下が順次定まる：

\[\begin{aligned}
 B_r(x)
 &\defeq \{y \in \X \mid d(x, y) < r\}
 && \text{（開球，定義）} \\
 \mathcal{O}_d
 &\defeq \{U \subset \X \mid \forall x \in U,\,
 \exists r > 0,\, B_r(x) \subset U\}
 && \text{（開集合の全体）} \\
 \Bb(\X)
 &\defeq \sigma(\mathcal{O}_d)
 && \text{（ボレル } \sigma\text{-代数，定義）}
\end{aligned}\]

ここで \(\sigma(\mathcal{O}_d)\) は，\(\mathcal{O}_d\) を含む \(\X\) 上のすべての \(\sigma\)-代数の共通部分

\[
 \sigma(\mathcal{O}_d)
 \defeq \bigcap
 \bigl\{
 \mathcal{F} \subset 2^{\X}
 \;\big|\;
 \mathcal{F} \text{ は } \sigma\text{-代数, }
 \mathcal{O}_d \subset \mathcal{F}
 \bigr\}
\]

として定まる．これにより可測空間 \((\X, \Bb(\X))\) （[ref:定義: 可測空間|可測空間]）が得られる．
- **完備性**． 列 \((x_n)_{n \geq 1} \subset \X\) が**Cauchy 列**であるとは， 任意の \(\varepsilon > 0\) に対してある \(N \in \N\) が存在して \(n, m \geq N \Longrightarrow d(x_n, x_m) < \varepsilon\) が成り立つことをいう． \((\X, d)\) が完備とは，任意の Cauchy 列 \((x_n) \subset \X\) が \(\X\) の点に収束する（[ref:定義: 収束列|収束列]）ことをいう． すなわち

\[
 \forall (x_n) \subset \X \text{ Cauchy 列},\;
 \exists x \in \X,\; x_n \to x.
\]

収束の定義に展開すれば

\[
 \forall (x_n) \subset \X \text{ Cauchy 列},\;
 \exists x \in \X,\;
 \forall \varepsilon > 0,\;
 \exists N \in \N,\;
 n \geq N \Longrightarrow d(x_n, x) < \varepsilon.
\]

- **可分性**． \(D \subset \X\) が**稠密**であるとは，任意の空でない開集合 \(U \subset \X\) に対し \(D \cap U \neq \emptyset\) となることをいう （[ref:定義: 稠密集合|稠密集合]）． 距離空間ではこれは「任意の \(x \in \X\) と任意の \(\varepsilon > 0\) に対し \(\exists q \in D,\; d(x, q) < \varepsilon\)」と同値． \((\X, d)\) が可分とは可算な稠密部分集合 \(D \subset \X\) が 存在することをいう（[ref:定義: 可分性|可分性]）．すなわち

\[
 \exists D \subset \X \text{ 可算},\;
 \forall U \subset \X \text{ 空でない開集合},\;
 D \cap U \neq \emptyset.
\]


離散版では確率測度の表示に現れる点集合
\(S \defeq \{x_1, \ldots, x_n\} \subset \X\) は有限集合となる．
\(S\) にどの距離 \(d\) を入れた距離空間 \((S, d)\) も
自動で Polish 空間となる（\(\X\) の可測構造は \(S\) に制限することで継承される）：

- **完備性．** \(n = 1\) なら \(S = \{x_1\}\) ゆえ 任意の列は \(y_k = x_1\) (\(\forall k\)) なる定値列であり， \(d(y_k, x_1) = 0\) より \(x_1\) に収束する． 以下 \(n \geq 2\) とする．相異なる 2 点間の距離の最小値を \(\delta \defeq \min_{i \neq j} d(x_i, x_j)\) とおく． これは有限個の正数の最小値なので \(\delta > 0\)． 任意の Cauchy 列 \((y_k)_{k \geq 1} \subset S\) に対し， Cauchy 条件で \(\varepsilon \defeq \delta / 2\) を取ると， ある \(N \in \N\) が存在して \(k, l \geq N \Longrightarrow d(y_k, y_l) < \delta / 2 < \delta\)． 一方 \(S\) の相異なる 2 点の距離は \(\delta\) 以上だから， \(d(y_k, y_l) < \delta\) は \(y_k = y_l\) を強制する． ゆえに列 \((y_k)\) は \(N\) 以降すべて同一の点となり，その点に収束する．
- **可分性．** \(S\) 自身が有限（特に可算）集合であり， 自身の中で稠密だから可分．

したがって本章の Polish 強化は連続側で必要となる一方，
離散版には追加制約を課さない．
:::


## 最適割当問題


:::definition
### 定義: 最適割当問題

\(n \in \N\)，置換 \(\sigma \in \Perm(n)\)，
および行列 \(\mathbf{C} \in \R_+^{n \times n}\) に対して，

\[
 \min_{\sigma \in \Perm(n)} \frac{1}{n} \sum_{i=1}^{n} C_{i, \sigma(i)}
\]

を達成する \(\sigma\) を求める問題を**最適割当問題**という．
:::


添字 \(i\) から \(j\) への**輸送コスト**を \(C_{i,j}\) と解釈すれば，
\(\sigma(i) = j\) は \(i\) を \(j\) に割り当てることを意味し，
目的関数 \(\frac{1}{n}\sum_i C_{i, \sigma(i)}\) はその割当の平均輸送コストを表す．

:::fact accent
### 例: 最適割当

\(n = 2\) とし，置換 \(\sigma \in \Perm(2)\) と行列

\[
 \mathbf{C} =
 \begin{pmatrix}
 1 & 4 \\
 2 & 1
 \end{pmatrix} \in \R_+^{2 \times 2}
\]

を考える．\(\Perm(2) = \{(1,2),\, (2,1)\}\) の \(2! = 2\) 通りの割当を以下に図示する．


各割当のコストをまとめると，
よって \(\sigma = (1, 2)\) が最小コスト \(1\) を達成し，最適である．
:::


:::theorem
### 主張: 最適解の存在

任意の \(n \in \N\) と任意の \(\mathbf{C} \in \R_+^{n \times n}\) に対して，
最適割当問題の最小値は達成される．

:::details-embedded 証明
\(\Perm(n)\) は \(|\Perm(n)| = n!\) の有限集合なので，集合

\[
 \left\{ \frac{1}{n}\sum_{i=1}^{n} C_{i, \sigma(i)} \;\middle|\; \sigma \in \Perm(n) \right\}
\]

は高々 \(n!\) 個の実数からなる空でない有限集合である．
\(\R\) の空でない有限部分集合は最小元を持つ（[ref:主張: 有限集合の最小元|有限集合の最小元]）
ので，それを達成する \(\sigma^* \in \Perm(n)\) が存在する．
:::
:::


:::theorem
### 主張: 最適解が一意でない場合の存在

任意の \(n \geq 2\) に対して，
異なる \(\sigma_1, \sigma_2 \in \Perm(n)\) がともに最小値を達成するような
\(\mathbf{C} \in \R_+^{n \times n}\) が存在する．

:::details-embedded 証明
\(C_{i,j} \defeq 1\)（\(i, j = 1, \ldots, n\)）と定めると，任意の \(\sigma \in \Perm(n)\) に対して
\(\frac{1}{n}\sum_{i=1}^{n} C_{i, \sigma(i)} = 1\)．
異なる \(\sigma_1, \sigma_2 \in \Perm(n)\) を取れば，
いずれも最小値 \(1\) を達成する．
:::
:::


## Monge 問題


最適割当問題（[ref:定義: 最適割当問題|最適割当問題]）は有限の添字集合 \(\range{n}\) と
均一重み \(1/n\) を扱う離散的な輸送問題だった．次の対応で一般の Polish 空間
\(\X, \Y\) と任意の確率測度に拡張する：
これに基づく連続版の輸送問題が **Monge 問題**である．

:::definition
### 定義: Monge 問題

\(\X, \Y\) 上の確率測度 \(\alpha \in \Mm_+^1(\X)\), \(\beta \in \Mm_+^1(\Y)\) と
可測関数 \(c \colon \X \times \Y \to \R_+\) に対して，
**Monge 問題**とは

\[
 \inf_{T}
 \left\{
 \int_{\X} c(x, T(x)) \, \d\alpha(x)
 \;\middle|\;
 T \colon \X \to \Y \text{ は可測}, \;
 T\pushforward \alpha = \beta
 \right\}
\]

を求める問題である．
:::


\(c(x, y)\) を \(x\) から \(y\) への**輸送コスト**と解釈すれば，
写像 \(T \colon \X \to \Y\) は \(x\) にある質量を \(T(x)\) へ送ることを意味し，
目的関数 \(\int_\X c(x, T(x)) \, \d\alpha(x)\) はその輸送の総コストを表す．
この問題には次節で示す通り，実行可能集合の **非凸性** と
**解の非存在**という本質的な困難があり，
**Kantorovich 緩和**はこれらをカップリングによって解消する．


### Monge 問題の本質的困難


**困難1：実行可能集合の非凸性**


\(\X = \Y = \R\) とする．
このとき可測写像 \(T \colon \R \to \R\) の全体は，点ごとの和・スカラー倍
\((tT_1 + (1-t)T_2)(x) \defeq t\, T_1(x) + (1-t)\, T_2(x)\)
によりベクトル空間をなす．この空間の部分集合としての
Monge 問題の実行可能集合

\[
 \mathcal{T}(\alpha, \beta)
 \defeq \left\{ T \colon \X \to \Y \;\middle|\;
 T \text{ は可測},\; T\pushforward \alpha = \beta \right\}
\]

は一般に**凸でない**．

:::fact accent
### 例: 実行可能集合の非凸性

\(\alpha = \beta = \tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_1\) とし，

\[
 T_1(x) = x,\qquad T_2(x) = -x,\qquad t = \tfrac{1}{2}
\]

をとる．\(\alpha\) の定義を代入し，[ref:命題: Dirac 測度と離散測度の押し出し|Dirac 測度と離散測度の押し出し] (ii) を適用すると

\[\begin{aligned}
 {T_1}\pushforward \alpha
 &= {T_1}\pushforward \bigl(\tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_{1}\bigr)
 && \text{（\(\alpha\) の定義）} \\
 &= \tfrac{1}{2}\delta_{T_1(-1)} + \tfrac{1}{2}\delta_{T_1(1)}
 && \text{（命題 (ii)）} \\
 &= \tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_{1} = \beta
 && \text{（\(T_1(x) = x\) より）}.
\end{aligned}\]

同様に

\[\begin{aligned}
 {T_2}\pushforward \alpha
 &= {T_2}\pushforward \bigl(\tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_{1}\bigr)
 && \text{（\(\alpha\) の定義）} \\
 &= \tfrac{1}{2}\delta_{T_2(-1)} + \tfrac{1}{2}\delta_{T_2(1)}
 && \text{（命題 (ii)）} \\
 &= \tfrac{1}{2}\delta_{1} + \tfrac{1}{2}\delta_{-1} = \beta
 && \text{（\(T_2(x) = -x\) より \(T_2(-1) = 1,\, T_2(1) = -1\)）}.
\end{aligned}\]

よって \(T_1, T_2 \in \mathcal{T}(\alpha, \beta)\) である．

一方，\(\bar{T} = \tfrac{1}{2}T_1 + \tfrac{1}{2}T_2\) は
\(\bar{T}(x) = \tfrac{1}{2}x + \tfrac{1}{2}(-x) = 0\)
すなわち \(0\) を値にとる定値写像であり，
\(\bar{T}\pushforward\alpha = \delta_0 \neq \beta\)．
よって \(\bar{T} \notin \mathcal{T}(\alpha, \beta)\) であり，
\(\mathcal{T}(\alpha, \beta)\) は凸でない．
:::


**困難2：解の非存在**


:::fact accent
### 例: Monge 写像が存在しない場合

\(\alpha = \delta_0\)（質量 \(1\) が 1 点 \(0\) に集中）と
\(\beta = \tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_1\)（2 点に質量 \(\tfrac{1}{2}\) ずつ分散）
を考える．任意の可測写像 \(T \colon \R \to \R\) について
[ref:命題: Dirac 測度と離散測度の押し出し|Dirac 測度と離散測度の押し出し] (i) より

\[
 T\pushforward \alpha = T\pushforward \delta_0 = \delta_{T(0)}
\]

となる．これは点 \(T(0)\) に質量 \(1\) を集中させた測度ゆえ
\(\delta_{T(0)}(\{T(0)\}) = 1\)．一方 \(\beta\) は任意の単点 \(\{y\}\) に対し
\(\beta(\{y\}) \in \{0,\, \tfrac{1}{2}\}\)（\(y = \pm 1\) のとき \(\tfrac{1}{2}\)，
それ以外で \(0\)）しか与えないので，どの \(T(0) \in \R\) をとっても
\(\delta_{T(0)} \neq \beta\) である．
したがって \(T\pushforward \alpha = \beta\) をみたす \(T\) は存在せず，
\(\mathcal{T}(\alpha, \beta) = \emptyset\)（下図）．
:::


## Kantorovich 緩和


### カップリング


:::definition
### 定義: カップリング

\(\X, \Y\) 上の確率測度 \(\alpha \in \Mm_+^1(\X)\), \(\beta \in \Mm_+^1(\Y)\)
に対し，写像

\[
 P_\X \colon \X \times \Y \to \X,\; (x, y) \mapsto x,
 \qquad
 P_\Y \colon \X \times \Y \to \Y,\; (x, y) \mapsto y
\]

を用いて，\(\alpha\) と \(\beta\) の**カップリング**の集合を

\[
 \Couplings(\alpha, \beta) \defeq
 \left\{ \pi \in \Mm_+^1(\X \times \Y) \;\middle|\;
 (P_\X)\pushforward \pi = \alpha, \;
 (P_\Y)\pushforward \pi = \beta \right\}
\]

で定める．
:::


### Kantorovich 問題


:::definition
### 定義: Kantorovich 問題

\(\X, \Y\) 上の確率測度 \(\alpha \in \Mm_+^1(\X)\), \(\beta \in \Mm_+^1(\Y)\) と
可測関数 \(c \colon \X \times \Y \to \R_+\) に対して，
\(\alpha, \beta\) のカップリング
\(\pi \in \Couplings(\alpha, \beta)\)（[ref:定義: カップリング|カップリング]）に
わたって積分 \(\int_{\X \times \Y} c(x, y) \, \d\pi(x, y)\) を
最小化する問題

\[
 \MK_c(\alpha, \beta) \defeq
 \inf_{\pi \in \Couplings(\alpha, \beta)}
 \int_{\X \times \Y} c(x, y) \, \d\pi(x, y)
\]

を**Kantorovich 問題**という．
:::


### 離散版


\(\alpha, \beta\) がともに離散測度（[ref:定義: 離散測度|離散測度]）

\[
 \alpha = \sum_{i=1}^n a_i\, \delta_{x_i},
 \qquad
 \beta = \sum_{j=1}^m b_j\, \delta_{y_j}
\]

（相異なる \(x_1, \ldots, x_n \in \X\)，\(y_1, \ldots, y_m \in \Y\)，
\(\mathbf{a} \in \R_{++}^n\)，\(\mathbf{b} \in \R_{++}^m\)，
\(\sum_i a_i = \sum_j b_j = 1\)）の場合を考え，行列
\(\mathbf{C} \in \R_+^{n \times m}\) の成分を \(C_{i,j} \defeq c(x_i, y_j)\) で定める．
このときカップリング集合 \(\Couplings(\alpha, \beta)\) は有限次元の行列集合
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) と同一視でき，Kantorovich 問題は
有限次元線形計画として書き直せる．以下，対応・最適化問題・解の存在を順に確かめる．

:::theorem
### 主張: 離散カップリングの行列表示

集合

\[
 \CouplingsD(\mathbf{a}, \mathbf{b}) \defeq
 \left\{ \mathbf{P} \in \R_+^{n \times m} \;\middle|\;
 \mathbf{P} \ones_m = \mathbf{a},\;
 \mathbf{P}^\top \ones_n = \mathbf{b} \right\}
\]

に対し，写像

\[
 \Phi \colon \CouplingsD(\mathbf{a}, \mathbf{b}) \to \Couplings(\alpha, \beta),
 \qquad
 \Phi(\mathbf{P}) \defeq \sum_{i=1}^n \sum_{j=1}^m P_{i,j}\, \delta_{(x_i, y_j)}
\]

は全単射であり，逆写像は
\(\Phi^{-1}(\pi) = (\pi(\{(x_i, y_j)\}))_{i,j}\) で与えられる．

:::details-embedded 証明
以下の3点を示す．

**(i) \(\Phi(\mathbf{P**) \in \Couplings(\alpha, \beta)\).}
\(\Phi(\mathbf{P})(\X \times \Y) = \sum_{i,j} P_{i,j} = \sum_i a_i = 1\) より
\(\Phi(\mathbf{P}) \in \Mm_+^1(\X \times \Y)\)．
単点 \(\{x_k\}\) について

\[
 \bigl((P_\X)\pushforward \Phi(\mathbf{P})\bigr)(\{x_k\})
 = \Phi(\mathbf{P})(\{x_k\} \times \Y)
 = \sum_{j=1}^m P_{k,j}
 = a_k
 = \alpha(\{x_k\}).
\]

\(\alpha\) は \(\X \setminus \{x_1, \ldots, x_n\}\) で零ゆえ，
両辺はすべての可測集合 \(A \in \Bb(\X)\) で一致し
\((P_\X)\pushforward \Phi(\mathbf{P}) = \alpha\)．同様に \(\beta\) について．

**(ii) 単射性．**
\(\Phi(\mathbf{P})(\{(x_k, y_l)\}) = P_{k,l}\) より
\(\mathbf{P}\) は \(\Phi(\mathbf{P})\) から一意に定まる．

**(iii) 全射性．**
\(\pi \in \Couplings(\alpha, \beta)\) を任意にとる．
\(\alpha(\X \setminus \{x_1, \ldots, x_n\}) = 0\) と周辺条件
\((P_\X)\pushforward \pi = \alpha\) から

\[
 \pi\bigl((\X \setminus \{x_1, \ldots, x_n\}) \times \Y\bigr)
 = \alpha(\X \setminus \{x_1, \ldots, x_n\}) = 0,
\]

同様に \(\pi(\X \times (\Y \setminus \{y_1, \ldots, y_m\})) = 0\)．
したがって \(\pi\) は \(\{(x_i, y_j)\}_{i, j}\) の補集合で零となり，
\(P_{i,j} \defeq \pi(\{(x_i, y_j)\}) \geq 0\) とおけば
\(\pi = \sum_{i,j} P_{i,j} \delta_{(x_i, y_j)}\)．
単点 \(\{x_k\}\) における周辺条件
\(a_k = \alpha(\{x_k\}) = \pi(\{x_k\} \times \Y) = \sum_j P_{k,j}\)
から \(\mathbf{P}\ones_m = \mathbf{a}\)．同様に \(\mathbf{P}^\top \ones_n = \mathbf{b}\)．
ゆえに \(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) かつ \(\Phi(\mathbf{P}) = \pi\)．
:::
:::


:::theorem
### 主張: 離散カップリング集合は凸多面体

\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は凸多面体（[ref:定義: 凸多面体|凸多面体]）をなす．

:::details-embedded 証明
\(\mathbf{P} \in \R^{n \times m}\) を列方向に並べたベクトル
\(\mathbf{p} \in \R^{nm}\) を考えると，
周辺条件 \(\mathbf{P}\ones_m = \mathbf{a}\)，\(\mathbf{P}^\top \ones_n = \mathbf{b}\)
はある行列 \(\mathbf{A} \in \R^{(n+m) \times nm}\) と
\(\mathbf{r} \defeq [\mathbf{a}^\top, \mathbf{b}^\top]^\top \in \R^{n+m}\) を用いて
\(\mathbf{A}\mathbf{p} = \mathbf{r}\) と書ける（具体的構成は
）．したがって

\[
 \CouplingsD(\mathbf{a}, \mathbf{b})
 \;\cong\;
 \{\mathbf{p} \in \R^{nm} \mid
 \mathbf{A}\mathbf{p} = \mathbf{r},\; \mathbf{p} \geq \mathbf{0}\}
\]

であり，これは凸多面体の[ref:定義: 凸多面体|凸多面体]の形である．
:::
:::


:::theorem
### 主張: 離散 Kantorovich 問題

[ref:主張: 離散カップリングの行列表示|離散カップリングの行列表示] の対応 \(\Phi\) で
\(\pi = \Phi(\mathbf{P})\) と書くと

\[
 \int_{\X \times \Y} c(x, y) \, \d\pi(x, y) = \inner{\mathbf{C}}{\mathbf{P}}
\]

が成り立つ．したがって連続版 Kantorovich 問題
（[ref:定義: Kantorovich 問題|Kantorovich 問題]）の下限は**離散 Kantorovich 問題**

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 \defeq
 \inf_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}}
\]

に等しい：\(\MK_c(\alpha, \beta) = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\)．

:::details-embedded 証明
[ref:主張: 離散カップリングの行列表示|離散カップリングの行列表示] より
\(\pi = \sum_{i,j} P_{i,j} \delta_{(x_i, y_j)}\)．
測度に関する積分の線形性（[ref:命題: 積分の測度に関する線形性|積分の測度に関する線形性]）と
Dirac 測度に対する積分（[ref:主張: Dirac 測度に対する積分|Dirac 測度に対する積分]）から

\[\begin{aligned}
 \int_{\X \times \Y} c(x, y) \, \d\pi(x, y)
 &= \sum_{i,j} P_{i,j} \int_{\X \times \Y} c(x, y) \, \d\delta_{(x_i, y_j)}(x, y)
 && \text{（命題）} \\
 &= \sum_{i,j} P_{i,j}\, c(x_i, y_j)
 && \text{（主張）} \\
 &= \sum_{i,j} C_{i,j} P_{i,j}
 = \inner{\mathbf{C}}{\mathbf{P}}.
\end{aligned}\]

\(\Phi\) の全単射性から \(\pi \in \Couplings(\alpha, \beta)\) にわたる下限と
\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) にわたる下限は等しい．
:::
:::


これは \(nm\) 個の変数と \(n + m\) 本の等式制約を持つ有限次元の線形計画である．

:::fact accent
### 例: Monge 写像が存在しない場合の解消

[ref:例: Monge 写像が存在しない場合|Monge 写像が存在しない場合] では
\(\alpha = \delta_0\)，\(\beta = \frac{1}{2}\delta_{-1} + \frac{1}{2}\delta_1\)
に対して Monge 写像が存在しないことを見た．
Kantorovich 問題（[ref:定義: Kantorovich 問題|Kantorovich 問題]）の枠組みで考え直す．

離散表現は \(\mathbf{a} = (1)\)，\(\mathbf{b} = (1/2,\; 1/2)\) であり，
カップリング \(\mathbf{P} \in \R_+^{1 \times 2}\) は
\(\mathbf{P}\ones_2 = 1\)，\(\mathbf{P}^\top \ones_1 = \mathbf{b}\)
を満たす必要がある．行が1つしかないため \(P_{1,j} = b_j\) が強制され，

\[
 \mathbf{P} = \begin{pmatrix} 1/2 & 1/2 \end{pmatrix}
\]

が唯一の実行可能カップリングである．
コスト \(c(x,y) = |x - y|\) から
\(\mathbf{C} = (|0-(-1)|,\; |0-1|) = (1,\; 1)\) であり，
最適値は

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \inner{\mathbf{C}}{\mathbf{P}}
 = 1 \cdot \tfrac{1}{2} + 1 \cdot \tfrac{1}{2} = 1.
\]

Monge 問題と異なり，質量分割を許す Kantorovich の枠組みでは
実行可能解が存在し，最適値が定まる．
:::


**解の存在．**

\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は凸多面体
（[ref:主張: 離散カップリング集合は凸多面体|離散カップリング集合は凸多面体]）をなす．
有界閉集合上の連続関数は最小値を達成するから，下限は最小値となり最適解が存在する．

:::theorem
### 主張: 離散 Kantorovich 問題の解の存在

任意の \(\mathbf{a} \in \R_{++}^n\)，\(\mathbf{b} \in \R_{++}^m\)
（\(\sum_i a_i = \sum_j b_j = 1\)）と \(\mathbf{C} \in \R_+^{n \times m}\) に対して，
離散 Kantorovich 問題の下限は最小値として達成される：

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})} \inner{\mathbf{C}}{\mathbf{P}}
 = \inner{\mathbf{C}}{\mathbf{P}^*}
\]

をみたす \(\mathbf{P}^* \in \CouplingsD(\mathbf{a}, \mathbf{b})\) が存在する．

:::details-embedded 証明
以下の3点を示せばよい：
(i) \(\CouplingsD(\mathbf{a}, \mathbf{b}) \neq \emptyset\)，
(ii) \(\CouplingsD(\mathbf{a}, \mathbf{b}) \subset \R^{n \times m}\) はコンパクト，
(iii) 目的関数 \(\mathbf{P} \mapsto \inner{\mathbf{C}}{\mathbf{P}}\) は連続．

**(i) 非空性．**
積測度に相当する \(\mathbf{P}_0 \defeq \mathbf{a}\mathbf{b}^\top\)，すなわち
\((P_0)_{i,j} = a_i b_j\) をとると，
\((\mathbf{P}_0 \ones_m)_i = a_i \sum_j b_j = a_i\)，
\((\mathbf{P}_0^\top \ones_n)_j = b_j \sum_i a_i = b_j\)
ゆえ \(\mathbf{P}_0 \in \CouplingsD(\mathbf{a}, \mathbf{b})\)．

**(ii) コンパクト性．**
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は線形等式
\(\mathbf{P}\ones_m = \mathbf{a}\), \(\mathbf{P}^\top \ones_n = \mathbf{b}\)
と非負性 \(\mathbf{P} \geq 0\) で定まる \(\R^{n \times m}\) の閉集合．
さらに各成分は \(0 \leq P_{i,j} \leq \min(a_i, b_j) \leq 1\) をみたすから有界．
\(\R^{n \times m}\) における有界閉集合はコンパクト．

**(iii) 連続性．**
\(\mathbf{P} \mapsto \inner{\mathbf{C}}{\mathbf{P}} = \sum_{i,j} C_{i,j} P_{i,j}\)
は線形写像であり，有限次元線形空間上で連続．

\(\R^{n \times m}\) 上の連続関数は空でないコンパクト集合上で最小値を達成する
（Weierstrass の最大値の定理）．したがって最適解 \(\mathbf{P}^*\) が存在する．
:::
:::


**最適解の構造．**


最適解が一意とは限らないことを確認し，最適解集合の構造を調べる．

:::theorem
### 主張: 最適解集合は輸送多面体の面をなす

最適解の集合

\[
 S^*
 \defeq
 \bigl\{ \mathbf{P}^* \in \CouplingsD(\mathbf{a}, \mathbf{b})
 \bigm|
 \inner{\mathbf{C}}{\mathbf{P}^*} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 \bigr\}
\]

は凸かつコンパクトであり，\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の面をなす：
\(\mathbf{P}, \mathbf{Q} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) と
\(t \in (0,1)\) に対して
\(t\mathbf{P} + (1-t)\mathbf{Q} \in S^*\) ならば
\(\mathbf{P}, \mathbf{Q} \in S^*\)．

:::details-embedded 証明
**凸性．**
\(\mathbf{P}^*, \mathbf{Q}^* \in S^*\) と \(t \in [0,1]\) に対し，
\(\mathbf{R} \defeq t\mathbf{P}^* + (1-t)\mathbf{Q}^*\) は
[ref:主張: 離散カップリング集合は凸多面体|離散カップリング集合は凸多面体] の凸性から
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) に属し，

\[
 \inner{\mathbf{C}}{\mathbf{R}}
 = t\inner{\mathbf{C}}{\mathbf{P}^*} + (1-t)\inner{\mathbf{C}}{\mathbf{Q}^*}
 = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b}).
\]


**面の性質．**
\(t\mathbf{P} + (1-t)\mathbf{Q} \in S^*\)
（\(\mathbf{P}, \mathbf{Q} \in \CouplingsD(\mathbf{a}, \mathbf{b})\)，
\(t \in (0,1)\)）とする．
\(\inner{\mathbf{C}}{\mathbf{P}},\, \inner{\mathbf{C}}{\mathbf{Q}} \geq \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\)
かつ
\(t\inner{\mathbf{C}}{\mathbf{P}} + (1-t)\inner{\mathbf{C}}{\mathbf{Q}} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\)
が成り立つには等号
\(\inner{\mathbf{C}}{\mathbf{P}} = \inner{\mathbf{C}}{\mathbf{Q}} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\)
が必要である．

**コンパクト性．**
\(S^* = \CouplingsD(\mathbf{a}, \mathbf{b}) \cap \{\mathbf{P} \mid \inner{\mathbf{C}}{\mathbf{P}} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\}\)
はコンパクト集合と閉集合の共通部分．
:::
:::


目的関数が線形であるため，有界凸多面体上の最小値は
頂点（端点）で達成される：

:::theorem
### 主張: 頂点での最適解の達成

\(S^*\) は \(\CouplingsD(\mathbf{a}, \mathbf{b})\) の
頂点を少なくとも1つ含む．

:::details-embedded 証明
[ref:主張: 最適解集合は輸送多面体の面をなす|最適解集合は輸送多面体の面をなす] より
\(S^*\) は凸多面体 \(\CouplingsD(\mathbf{a}, \mathbf{b})\)
の空でない面であり，それ自身も凸多面体をなすから頂点を持つ．
\(\mathbf{P}^*\) を \(S^*\) の頂点とし，
\(\mathbf{P}^* = t\mathbf{P} + (1-t)\mathbf{Q}\)
（\(\mathbf{P}, \mathbf{Q} \in \CouplingsD(\mathbf{a}, \mathbf{b})\)，
\(t \in (0,1)\)）と書けたとする．
面の性質から \(\mathbf{P}, \mathbf{Q} \in S^*\)．
\(\mathbf{P}^*\) は \(S^*\) の頂点であるから
\(\mathbf{P} = \mathbf{Q} = \mathbf{P}^*\)．
よって \(\mathbf{P}^*\) は
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の頂点でもある．
:::
:::


:::fact
### 最適輸送計画のスパース性

\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の頂点は
非零成分を高々 \(n + m - 1\) 個しか持たない
（
[ref:命題: 頂点の木構造|頂点の木構造]）．
全成分数 \(nm\) と比べ，
[ref:主張: 頂点での最適解の達成|頂点での最適解の達成] が保証する
頂点最適解は大幅にスパースである．
:::


次の例は，非自明な状況で最適解が一意にならないことを示す．

:::fact accent
### 例: 最適解の非一意性

\(n = m = 2\)，\(\mathbf{a} = \mathbf{b} = (1/2,\; 1/2)\) とし，
コスト行列を

\[
 \mathbf{C} = \begin{pmatrix} 1 & 3 \\ 3 & 5 \end{pmatrix}
\]

とする（\(C_{11} + C_{22} = 6 = C_{12} + C_{21}\)）．
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は2つの頂点

\[
 \mathbf{P}_1
 = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix},
 \qquad
 \mathbf{P}_2
 = \begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}
\]

を結ぶ線分であり，両者のコストはともに

\[
 \inner{\mathbf{C}}{\mathbf{P}_1}
 = \tfrac{1}{2} + \tfrac{5}{2} = 3,
 \qquad
 \inner{\mathbf{C}}{\mathbf{P}_2}
 = \tfrac{3}{2} + \tfrac{3}{2} = 3
\]

で等しい．
したがって任意の \(t \in [0, 1]\) に対して
\(t\mathbf{P}_1 + (1-t)\mathbf{P}_2\) が最適であり，
最適面 \(S^*\) は輸送多面体全体に等しい．

この非一意性は
\(C_{11} + C_{22} = C_{12} + C_{21}\) から生じる．
逆に \(C_{11} + C_{22} \neq C_{12} + C_{21}\) ならば
2頂点のコストが異なるため最適解は一意となる．
:::


:::fact
### エントロピー正則化による一意性の回復

離散 Kantorovich 問題の非一意性は
目的関数 \(\inner{\mathbf{C}}{\mathbf{P}}\) の線形性に由来する．
で導入する
エントロピー正則化

\[
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}} - \varepsilon \Hb(\mathbf{P})
\]

では，\(\varepsilon > 0\) のとき目的関数が
狭義凸（[ref:定義: 凸関数と狭義凸関数|凸関数と狭義凸関数]）となるため，
最適解は常に一意に定まる
（[ref:命題: 正則化問題の解の存在と一意性|正則化問題の解の存在と一意性]）．
これは計算上の利点
（Sinkhorn アルゴリズムの収束先が一意）
だけでなく，理論上も解の選択の曖昧さを解消する意義を持つ．
:::


**連続版の存在．**


:::fact
### Polish 空間上の Kantorovich 問題の解の存在

\(\X, \Y\) が Polish 空間で
コスト関数 \(c \colon \X \times \Y \to [0, +\infty]\) が
下半連続であるとき，
Kantorovich 問題（[ref:定義: Kantorovich 問題|Kantorovich 問題]）の下限は
最小値として達成される：

\[
 \MK_c(\alpha, \beta)
 = \min_{\pi \in \Couplings(\alpha, \beta)}
 \int_{\X \times \Y} c(x, y) \, \d\pi(x, y).
\]

証明は以下の4段階による：

1. \(\Couplings(\alpha, \beta)\) は確率測度の 弱収束の位相で**緊密**（tight）である． 周辺 \(\alpha, \beta\) がそれぞれ Polish 空間上で緊密であることから， 任意の \(\varepsilon > 0\) に対して コンパクト集合 \(K_\X \times K_\Y \subset \X \times \Y\) で \(\sup_{\pi \in \Couplings(\alpha, \beta)} \pi((\X \times \Y) \setminus (K_\X \times K_\Y)) < \varepsilon\) とできる．
2. **Prokhorov の定理**により， Polish 空間上の緊密な確率測度族は弱位相で相対コンパクトである．
3. \(\Couplings(\alpha, \beta)\) は弱位相で閉集合であるから （弱収束の極限は周辺条件を保存するため）， 相対コンパクトかつ閉 = コンパクト．
4. 下半連続コスト汎関数 \(\pi \mapsto \int c \, \d\pi\) は弱収束に関して下半連続であり， 空でないコンパクト集合上で最小値を達成する．

詳細は C. Villani,
*Optimal Transport: Old and New*, Springer, 2009, Chapter 4 を参照．
:::


## Kantorovich 双対


Kantorovich 問題は線形計画であり，双対問題を持つ．
離散版では有限次元線形計画の双対性により双対問題を完全に導出できる．
連続版では，双対制約を整理する操作として \(c\)-変換が現れる．

### 離散版の双対問題


:::definition
### 定義: 離散双対実行可能集合

コスト行列 \(\mathbf{C} \in \R^{n \times m}\) に対し，
**離散 Kantorovich 双対ポテンシャル**の実行可能集合を

\[
 \PotentialsD(\mathbf{C})
 \defeq
 \left\{(\mathbf{f}, \mathbf{g}) \in \R^n \times \R^m
 \;\middle|\;
 f_i + g_j \leq C_{i,j}
 \quad(\forall\, i \in \range{n},\, j \in \range{m})
 \right\}
\]

と定める．\(\mathbf{f}\) と \(\mathbf{g}\) を
**双対ポテンシャル**または**双対変数**という．
:::


:::theorem
### 定理: Kantorovich 双対定理（離散版）

\(\mathbf{a} \in \R_{++}^n\)，\(\mathbf{b} \in \R_{++}^m\)，
\(\sum_i a_i = \sum_j b_j = 1\)，および
\(\mathbf{C} \in \R_+^{n \times m}\) に対して，

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 =
 \max_{(\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}.
\]

:::details-embedded 証明
主問題は

\[
 \min_{\mathbf{P} \geq 0}
 \left\{
 \inner{\mathbf{C}}{\mathbf{P}}
 \;\middle|\;
 \mathbf{P}\ones_m = \mathbf{a},\;
 \mathbf{P}^\top \ones_n = \mathbf{b}
 \right\}
\]

である．等式制約に対するラグランジュ乗数を
\(\mathbf{f} \in \R^n\)，\(\mathbf{g} \in \R^m\) とし，
ラグランジュ関数を

\[
 L(\mathbf{P}, \mathbf{f}, \mathbf{g})
 \defeq
 \inner{\mathbf{C}}{\mathbf{P}}
 + \inner{\mathbf{f}}{\mathbf{a} - \mathbf{P}\ones_m}
 + \inner{\mathbf{g}}{\mathbf{b} - \mathbf{P}^\top\ones_n}
\]

とおく．これを整理すると

\[
 L(\mathbf{P}, \mathbf{f}, \mathbf{g})
 =
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 + \sum_{i=1}^n \sum_{j=1}^m
 \bigl(C_{i,j} - f_i - g_j\bigr) P_{i,j}.
\]

\(\mathbf{P} \geq 0\) の下で \(L\) を \(\mathbf{P}\) について下から評価すると，
ある \((i,j)\) で \(C_{i,j} - f_i - g_j < 0\) なら
\(P_{i,j} \to +\infty\) により \(\inf_{\mathbf{P} \geq 0} L = -\infty\) となる．
一方，すべての \((i,j)\) で \(f_i + g_j \leq C_{i,j}\) なら，
最後の和は非負であり，\(\mathbf{P}=\mathbf{0}\) で下限
\(\inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}\) を達成する．
よって双対問題は

\[
 \max_{(\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
\]

である．主問題は空でない有界な輸送多面体上の線形計画なので，
有限次元線形計画の強双対性により主問題と双対問題の最適値は一致する．
:::
:::


:::theorem
### 命題: 相補性条件

\(\mathbf{P}^* \in \CouplingsD(\mathbf{a}, \mathbf{b})\) と
\((\mathbf{f}^*, \mathbf{g}^*) \in \PotentialsD(\mathbf{C})\) が
それぞれ主問題と双対問題の最適解ならば，

\[
 P^*_{i,j} > 0
 \quad\Longrightarrow\quad
 f^*_i + g^*_j = C_{i,j}.
\]

同値に，すべての \((i,j)\) について

\[
 P^*_{i,j}\bigl(C_{i,j} - f^*_i - g^*_j\bigr) = 0.
\]

:::details-embedded 証明
強双対性より

\[
 \inner{\mathbf{C}}{\mathbf{P}^*}
 =
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}.
\]

主問題の周辺条件から

\[
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 =
 \sum_{i,j} (f_i^* + g_j^*) P^*_{i,j}.
\]

したがって

\[
 \sum_{i,j}
 \bigl(C_{i,j} - f_i^* - g_j^*\bigr) P^*_{i,j}
 = 0.
\]

ここで各項は
\(C_{i,j} - f_i^* - g_j^* \geq 0\) と \(P^*_{i,j} \geq 0\)
の積なので非負である．非負項の和が \(0\) であるから，各項が \(0\) である．
:::
:::


### 離散 \(C\)-変換と半双対


:::definition
### 定義: 離散 \(C\)-変換

コスト行列 \(\mathbf{C} \in \R^{n \times m}\) と
ベクトル \(\mathbf{f} \in \R^n\) に対して，
\(\mathbf{f}\) の**離散 \(C\)-変換**
\(\mathbf{f}^{\,C} \in \R^m\) を

\[
 (\mathbf{f}^{\,C})_j
 \defeq
 \min_{i \in \range{n}} \bigl(C_{i,j} - f_i\bigr)
 \qquad (j \in \range{m})
\]

で定める．同様に，\(\mathbf{g} \in \R^m\) の
**離散 \(\bar C\)-変換** \(\mathbf{g}^{\,\bar C} \in \R^n\) を

\[
 (\mathbf{g}^{\,\bar C})_i
 \defeq
 \min_{j \in \range{m}} \bigl(C_{i,j} - g_j\bigr)
 \qquad (i \in \range{n})
\]

で定める．最小値は有限集合上の最小値なので必ず存在する．
:::


:::theorem
### 主張: 離散半双対

離散 Kantorovich 問題の双対値は

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 =
 \max_{\mathbf{f} \in \R^n}
 \left\{
 \inner{\mathbf{f}}{\mathbf{a}}
 + \inner{\mathbf{f}^{\,C}}{\mathbf{b}}
 \right\}
\]

と書ける．この形を**半双対**という．

:::details-embedded 証明
\(\mathbf{f}\) を固定する．双対制約
\(f_i + g_j \leq C_{i,j}\) がすべての \(i\) で成り立つことは，
各 \(j\) について

\[
 g_j \leq \min_i (C_{i,j} - f_i) = (\mathbf{f}^{\,C})_j
\]

と同値である．したがって，固定した \(\mathbf{f}\) に対し，
制約を満たす \(\mathbf{g}\) のうち目的関数
\(\inner{\mathbf{g}}{\mathbf{b}}\) を最大にするものは
\(\mathbf{g} = \mathbf{f}^{\,C}\) である
（\(\mathbf{b} \geq 0\) を用いる）．
[ref:定理: Kantorovich 双対定理（離散版）|Kantorovich 双対定理（離散版）] の双対問題で
\(\mathbf{g}\) を消去すれば結論を得る．
:::
:::


### 連続版の \(c\)-変換


離散 \(C\)-変換では，有限個の候補に対して
\(\min_i(C_{i,j} - f_i)\) を取った．連続版では，添字 \(i\) が点
\(x \in \X\) に置き換わり，最小値ではなく下限を取る．

:::definition
### 定義: \(c\)-変換

\(\X, \Y\) を集合，\(c \colon \X \times \Y \to \R \cup \{+\infty\}\)
をコスト関数とする．関数 \(f \colon \X \to \R \cup \{-\infty\}\) に対して，
\(f\) の**\(c\)-変換** \(f^c \colon \Y \to \R \cup \{-\infty\}\) を

\[
 f^c(y)
 \defeq
 \inf_{x \in \X} \bigl(c(x,y) - f(x)\bigr)
 \qquad (y \in \Y)
\]

で定める．同様に，\(g \colon \Y \to \R \cup \{-\infty\}\) に対して

\[
 g^{\bar c}(x)
 \defeq
 \inf_{y \in \Y} \bigl(c(x,y) - g(y)\bigr)
 \qquad (x \in \X)
\]

を**\(\bar c\)-変換**という．
:::


:::fact
### 連続版双対の形

連続版でも，双対制約は

\[
 f(x) + g(y) \leq c(x,y)
 \qquad (\forall\, x \in \X,\; y \in \Y)
\]

である．固定した \(f\) に対して制約を満たす最大の \(g\) は
\(g = f^c\) で与えられるので，形式的には

\[
 \MK_c(\alpha,\beta)
 =
 \sup_f
 \left\{
 \int_\X f \,\d\alpha + \int_\Y f^c \,\d\beta
 \right\}
\]

という半双対が現れる．この等式を厳密な定理として述べるには，
\(f, g\) の可積分性や \(c\) の正則性に関する仮定が必要である．
:::
