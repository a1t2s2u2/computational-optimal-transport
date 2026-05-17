---
id: ot-foundations
nav: Monge と Kantorovich
eyebrow: 2. OT Foundations
title: Optimal Transport の基礎理論
---


:::fact
### Rem: 本章の設定

\((\X, d_\X)\), \((\Y, d_\Y)\) は**完備可分な距離空間**（Polish 空間，
[ref:Def: Polish 空間|Polish 空間]）とする．
ボレル \(\sigma\)-代数 \(\Bb(\X)\) により \(\X\) を可測空間 \((\X, \Bb(\X))\) として扱う
（\(\Y\) についても同様）．\(\X\) 上の確率測度全体を \(\Mm_+^1(\X)\) と記す．

Polish 空間の3要素を確認する：

- **距離空間**．距離関数 \(d_\X \colon \X \times \X \to [0, \infty)\) が距離の公理 （[ref:Def: 距離空間|距離空間]）を満たし，\(d_\X\) から以下が順次定まる：

\[\begin{aligned}
 B_r(x)
 &\defeq \{y \in \X \mid d_\X(x, y) < r\}
 && \text{（開球，定義）} \\
 \mathcal{O}_{d_\X}
 &\defeq \{U \subset \X \mid \forall x \in U,\,
 \exists r > 0,\, B_r(x) \subset U\}
 && \text{（開集合の全体）} \\
 \Bb(\X)
 &\defeq \sigma(\mathcal{O}_{d_\X})
 && \text{（ボレル } \sigma\text{-代数，定義）}
\end{aligned}\]

ここで \(\sigma(\mathcal{O}_{d_\X})\) は，\(\mathcal{O}_{d_\X}\) を含む \(\X\) 上のすべての \(\sigma\)-代数の共通部分

\[
 \sigma(\mathcal{O}_{d_\X})
 \defeq \bigcap
 \bigl\{
 \mathcal{F} \subset 2^{\X}
 \;\big|\;
 \mathcal{F} \text{ は } \sigma\text{-代数, }
 \mathcal{O}_{d_\X} \subset \mathcal{F}
 \bigr\}
\]

として定まる．これにより可測空間 \((\X, \Bb(\X))\) （[ref:Def: 可測空間|可測空間]）が得られる．
- **完備性**． 列 \((x_n)_{n \geq 1} \subset \X\) が**Cauchy 列**であるとは， 任意の \(\varepsilon > 0\) に対してある \(N \in \N\) が存在して \(n, m \geq N \Longrightarrow d_\X(x_n, x_m) < \varepsilon\) が成り立つことをいう． \((\X, d_\X)\) が完備とは，任意の Cauchy 列 \((x_n) \subset \X\) が \(\X\) の点に収束する（[ref:Def: 収束列|収束列]）ことをいう． すなわち

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
 n \geq N \Longrightarrow d_\X(x_n, x) < \varepsilon.
\]

- **可分性**． \(D \subset \X\) が**稠密**であるとは，任意の空でない開集合 \(U \subset \X\) に対し \(D \cap U \neq \emptyset\) となることをいう （[ref:Def: 稠密集合|稠密集合]）． 距離空間ではこれは「任意の \(x \in \X\) と任意の \(\varepsilon > 0\) に対し \(\exists q \in D,\; d_\X(x, q) < \varepsilon\)」と同値． \((\X, d_\X)\) が可分とは可算な稠密部分集合 \(D \subset \X\) が 存在することをいう（[ref:Def: 可分性|可分性]）．すなわち

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
### Def: 最適割当問題

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
### Ex: 最適割当

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
### Clm: 最適解の存在

任意の \(n \in \N\) と任意の \(\mathbf{C} \in \R_+^{n \times n}\) に対して，
最適割当問題の最小値は達成される．

:::details-embedded 証明
\(\Perm(n)\) は \(|\Perm(n)| = n!\) の有限集合なので，集合

\[
 \left\{ \frac{1}{n}\sum_{i=1}^{n} C_{i, \sigma(i)} \;\middle|\; \sigma \in \Perm(n) \right\}
\]

は高々 \(n!\) 個の実数からなる空でない有限集合である．
\(\R\) の空でない有限部分集合は最小元を持つ（[ref:Clm: 有限集合の最小元|有限集合の最小元]）
ので，それを達成する \(\sigma^* \in \Perm(n)\) が存在する．
:::
:::


:::theorem
### Clm: 最適解が一意でない場合の存在

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


最適割当問題（[ref:Def: 最適割当問題|最適割当問題]）は有限の添字集合 \(\range{n}\) と
均一重み \(1/n\) を扱う離散的な輸送問題だった．次の対応で一般の Polish 空間
\(\X, \Y\) と任意の確率測度に拡張する：
これに基づく連続版の輸送問題が **Monge 問題**である．

:::definition
### Def: Monge 問題

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
### Ex: 実行可能集合の非凸性

\(\alpha = \beta = \tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_1\) とし，

\[
 T_1(x) = x,\qquad T_2(x) = -x,\qquad t = \tfrac{1}{2}
\]

をとる．\(\alpha\) の定義を代入し，[ref:Prop: Dirac 測度と離散測度の押し出し|Dirac 測度と離散測度の押し出し] (ii) を適用すると

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
### Ex: Monge 写像が存在しない場合

\(\alpha = \delta_0\)（質量 \(1\) が 1 点 \(0\) に集中）と
\(\beta = \tfrac{1}{2}\delta_{-1} + \tfrac{1}{2}\delta_1\)（2 点に質量 \(\tfrac{1}{2}\) ずつ分散）
を考える．任意の可測写像 \(T \colon \R \to \R\) について
[ref:Prop: Dirac 測度と離散測度の押し出し|Dirac 測度と離散測度の押し出し] (i) より

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


## Kantorovich 問題


### Kantorovich 緩和


**問題の定義**


:::definition
### Def: Kantorovich 問題

\(\X, \Y\) 上の確率測度 \(\alpha \in \Mm_+^1(\X)\), \(\beta \in \Mm_+^1(\Y)\) と
可測関数 \(c \colon \X \times \Y \to \R_+\) に対して，
**カップリング集合**

\[
 \Couplings(\alpha, \beta) \defeq
 \left\{ \pi \in \Mm_+^1(\X \times \Y) \;\middle|\;
 \begin{aligned}
 &\pi(A \times \Y) = \alpha(A) \quad \forall\, A \in \Bb(\X), \\
 &\pi(\X \times B) = \beta(B) \quad \forall\, B \in \Bb(\Y)
 \end{aligned}
 \right\}
\]

上で輸送コスト

\[
 \MK_c(\alpha, \beta) \defeq
 \inf_{\pi \in \Couplings(\alpha, \beta)}
 \int_{\X \times \Y} c(x, y) \, \d\pi(x, y)
\]

を最小化する問題を**Kantorovich 問題**という．
:::


:::fact
### Rem: 押し出しを用いたコンパクトな表現

カップリング条件は，射影（[ref:Def: 射影|射影]）
\(P_\X \colon (x,y) \mapsto x\)，\(P_\Y \colon (x,y) \mapsto y\) と
押し出し（[ref:Def: 押し出し|押し出し]）を用いると

\[
 (P_\X)\pushforward \pi = \alpha, \qquad (P_\Y)\pushforward \pi = \beta
\]

とコンパクトに書ける．実際，任意の \(A \in \Bb(\X)\) に対して

\[
 \bigl((P_\X)\pushforward \pi\bigr)(A)
 = \pi\bigl(P_\X^{-1}(A)\bigr)
 = \pi\bigl(\{(x,y) \mid x \in A\}\bigr)
 = \pi(A \times \Y),
\]

ゆえに \((P_\X)\pushforward \pi = \alpha\) は
\(\pi(A \times \Y) = \alpha(A)\)（\(\forall\, A \in \Bb(\X)\)）と同値である．
\(P_\Y\) についても同様．
:::


**離散化と線形計画への帰着**


:::definition
### Def: 離散 Kantorovich 問題

可測関数 \(c \colon \X \times \Y \to \R_+\) と，
Polish 空間 \(\X, \Y\) 上の点 \(x_1, \ldots, x_n \in \X\)，\(y_1, \ldots, y_m \in \Y\)
を台とする離散測度（[ref:Def: 離散測度|離散測度]）

\[\begin{aligned}
 \alpha &= \sum_{i=1}^n a_i\, \delta_{x_i}
 \quad (\mathbf{a} \in \R_{++}^n,\; \textstyle\sum_i a_i = 1), \\
 \beta &= \sum_{j=1}^m b_j\, \delta_{y_j}
 \quad (\mathbf{b} \in \R_{++}^m,\; \textstyle\sum_j b_j = 1)
\end{aligned}\]

に対して，行列 \(\mathbf{C} \defeq \bigl(c(x_i, y_j)\bigr)_{1 \leq i \leq n,\, 1 \leq j \leq m} \in \R_+^{n \times m}\) を定め，
**離散カップリング集合**

\[
 \CouplingsD(\mathbf{a}, \mathbf{b}) \defeq
 \left\{ \mathbf{P} \in \R_+^{n \times m} \;\middle|\;
 \mathbf{P}\ones_m = \mathbf{a},\;
 \mathbf{P}^\top\ones_n = \mathbf{b}
 \right\}
\]

を定める．
最小化問題

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 \defeq
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}}
\]

を**離散 Kantorovich 問題**という．
ここで \(\inner{\mathbf{C}}{\mathbf{P}} \defeq \sum_{i,j} C_{i,j} P_{i,j}\) はフロベニウス内積
（[ref:Def: フロベニウス内積|フロベニウス内積]）を表す．
:::


:::fact
### Rem: 周辺条件の展開

行列とベクトルの積の定義より，\((\mathbf{P}\ones_m)_i = \sum_{j=1}^m P_{i,j}\) であるから，

\[
 \mathbf{P}\ones_m = \mathbf{a}
 \iff
 \sum_{j=1}^m P_{i,j} = a_i \quad (\forall\, i = 1, \ldots, n).
\]

同様に \((\mathbf{P}^\top\ones_n)_j = \sum_{i=1}^n P_{i,j}\) より，

\[
 \mathbf{P}^\top\ones_n = \mathbf{b}
 \iff
 \sum_{i=1}^n P_{i,j} = b_j \quad (\forall\, j = 1, \ldots, m).
\]

すなわち，\(\mathbf{P}\) の各行の総和が \(\mathbf{a}\)，各列の総和が \(\mathbf{b}\) に等しいことを要求している．
:::


:::fact accent
### Ex: 工場からスーパーへの輸送

2 つの工場 \(x_1, x_2\) から 2 つのスーパー \(y_1, y_2\) へ商品を輸送する状況を考える．
各工場の供給割合を \(\mathbf{a} = (2/3,\; 1/3)^\top\)，
各スーパーの需要割合を \(\mathbf{b} = (1/3,\; 2/3)^\top\) とし，
輸送コスト行列を

\[
 \mathbf{C} =
 \begin{pmatrix}
 C_{1,1} & C_{1,2} \\
 C_{2,1} & C_{2,2}
 \end{pmatrix}
 =
 \begin{pmatrix}
 1 & 2 \\
 3 & 1
 \end{pmatrix}
\]

とする（図）．


コストの安い経路 \(x_1 \to y_1\)（コスト \(1\)）と \(x_2 \to y_2\)（コスト \(1\)）を
最大限利用し，残りを \(x_1 \to y_2\)（コスト \(2\)）で補うのが最適であり，

\[
 \mathbf{P}^{\star} =
 \begin{pmatrix}
 1/3 & 1/3 \\
 0 & 1/3
 \end{pmatrix},
 \qquad
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \inner{\mathbf{C}}{\mathbf{P}^{\star}}
 = \sum_{i,j} C_{i,j} P_{i,j}^{\star}
 = 1 \cdot \tfrac{1}{3} + 2 \cdot \tfrac{1}{3} + 3 \cdot 0 + 1 \cdot \tfrac{1}{3}
 = \tfrac{4}{3}.
\]
:::


\(\alpha, \beta\) は \(\X, \Y\) 上の離散確率測度であるから，
連続 Kantorovich 問題（[ref:Def: Kantorovich 問題|Kantorovich 問題]）の入力として有効である．
次の命題は，連続版の最適値 \(\MK_c(\alpha, \beta)\) と
離散版の最適値 \(\MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\) が一致することを保証する．

:::theorem
### Prop: 離散測度に対する最適値の一致

[ref:Def: 離散 Kantorovich 問題|離散 Kantorovich 問題] の \(\alpha, \beta, \mathbf{C}\) に対して，

\[
 \MK_c(\alpha, \beta) = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b}).
\]

:::details-embedded 証明
離散カップリング集合の各行列
\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) に対し，
\(X \times Y\) 上の測度を対応させる写像 \(\Phi\) を

\[
 \Phi \colon \CouplingsD(\mathbf{a}, \mathbf{b}) \to \Couplings(\alpha, \beta),
 \qquad
 \Phi(\mathbf{P}) \defeq \sum_{i=1}^n \sum_{j=1}^m P_{i,j}\, \delta_{(x_i, y_j)}
\]

で定義する．\(\Phi\) が全単射かつコストを保つことを示せば，
両問題の最適値の一致が従う．

**(i) 値域の確認．**
\(\Phi\) の式を定義しただけでは，\(\Phi(\mathbf{P})\) が
\(\Couplings(\alpha,\beta)\) の条件（\(\alpha,\beta\) を周辺分布とする確率測度であること）を
みたすかは自明でない．以下で計算して確かめる．
\(\Phi(\mathbf{P})(X \times Y) = \sum_{i,j} P_{i,j} = \sum_i a_i = 1\) より
\(\Phi(\mathbf{P}) \in \Mm_+^1(\X \times \Y)\)．
単点 \(\{x_k\}\) について

\[
 \Phi(\mathbf{P})(\{x_k\} \times \Y)
 = \sum_{j=1}^m P_{k,j}
 = a_k
 = \alpha(\{x_k\}).
\]

\(\alpha\) は \(\X \setminus X\) で零ゆえ，\(\sigma\)-加法性より
任意の \(A \in \Bb(\X)\) で \(\Phi(\mathbf{P})(A \times \Y) = \alpha(A)\)．
同様に \(\Phi(\mathbf{P})(\X \times B) = \beta(B)\)（\(\forall B \in \Bb(\Y)\)）．

**(ii) 単射性．**
\(\Phi(\mathbf{P})(\{(x_k, y_l)\}) = P_{k,l}\) より
\(\mathbf{P}\) は \(\Phi(\mathbf{P})\) から一意に定まる．

**(iii) 全射性．**
\(\pi \in \Couplings(\alpha, \beta)\) を任意にとる．
\(P_{i,j} \defeq \pi(\{(x_i, y_j)\}) \geq 0\) と定め，
\(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) かつ \(\Phi(\mathbf{P}) = \pi\) を示す．

*\(\Phi(\mathbf{P*) = \pi\) の確認．}
まず \(\pi\) の台が \(X \times Y\) に含まれることを示す．
周辺条件 \(\pi(A \times \Y) = \alpha(A)\)（\(\forall A \in \Bb(\X)\)）と
\(\alpha(\X \setminus X) = 0\) から

\[
 \pi\bigl((\X \setminus X) \times \Y\bigr) = \alpha(\X \setminus X) = 0,
\]

同様に \(\pi(\X \times (\Y \setminus Y)) = 0\)．
よって \(\pi\) は有限集合 \(X \times Y\) 上のみに質量を持つから，
\(\sigma\)-加法性より任意の \(A \in \Bb(\X \times \Y)\) について

\[
 \pi(A) = \sum_{(x_i,y_j) \in A} P_{i,j} = \Phi(\mathbf{P})(A),
\]

すなわち \(\Phi(\mathbf{P}) = \pi\)．

*\(\mathbf{P* \in \CouplingsD(\mathbf{a}, \mathbf{b})\) の確認．}
周辺条件 \(\pi(\{x_k\} \times \Y) = \alpha(\{x_k\}) = a_k\) から
\(\sum_j P_{k,j} = a_k\)，すなわち \(\mathbf{P}\ones_m = \mathbf{a}\)．
同様に \(\mathbf{P}^\top \ones_n = \mathbf{b}\)．
\(P_{i,j} \geq 0\) と合わせて \(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\)．

**(iv) コスト等式．**
\(\pi = \Phi(\mathbf{P}) = \sum_{i,j} P_{i,j} \delta_{(x_i, y_j)}\) に対し，
測度に関する積分の線形性（[ref:Prop: 積分の測度に関する線形性|積分の測度に関する線形性]）と
Dirac 測度に対する積分（[ref:Clm: Dirac 測度に対する積分|Dirac 測度に対する積分]）から

\[\begin{aligned}
 \int_{X \times Y} c(x, y) \, \d\pi(x, y)
 &= \sum_{i,j} P_{i,j} \int_{X \times Y} c(x, y) \, \d\delta_{(x_i, y_j)}(x, y)
 && \text{（命題）} \\
 &= \sum_{i,j} P_{i,j}\, c(x_i, y_j)
 && \text{（主張）} \\
 &= \sum_{i,j} C_{i,j} P_{i,j}
 = \inner{\mathbf{C}}{\mathbf{P}}.
\end{aligned}\]

以上より最適値の一致を示す．
(i) より \(\Phi(\mathbf{P}) \in \Couplings(\alpha, \beta)\) が確かめられ，
(ii)(iii) より \(\Phi\) は \(\CouplingsD(\mathbf{a}, \mathbf{b})\) から
\(\Couplings(\alpha, \beta)\) への全単射である．(iv) よりコストを保存する．
すなわち，連続版のカップリング \(\pi \in \Couplings(\alpha, \beta)\) と
離散版の行列 \(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) は
\(\pi = \Phi(\mathbf{P})\) を通じてコストを変えずに一対一対応する．
したがって，

\[\begin{aligned}
 \MK_c(\alpha, \beta)
 &= \inf_{\pi \in \Couplings(\alpha, \beta)}
 \int_{X \times Y} c(x, y) \, \d\pi(x, y) \\
 &= \inf_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \int_{X \times Y} c(x, y) \, \d(\Phi(\mathbf{P}))(x, y)
 \quad \text{（\(\Phi\) が全単射）} \\
 &= \inf_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \inner{\mathbf{C}}{\mathbf{P}}
 \quad \text{（(iv)）} \\
 &= \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b}).
\end{aligned}\]
:::
:::


:::definition
### Def: 線形計画問題

\(N, M \in \N\)，\(\mathbf{c} \in \R^N\)，\(\mathbf{A} \in \R^{M \times N}\)，\(\mathbf{b} \in \R^M\) を所与とする．
最小化問題

\[
 \min_{\substack{\mathbf{x} \in \R^N \\ \mathbf{A}\mathbf{x} = \mathbf{b},\; \mathbf{x} \geq \mathbf{0}}}\;
 \mathbf{c}^\top \mathbf{x}
\]

を**線形計画問題**（LP）という．
制約 \(\mathbf{A}\mathbf{x} = \mathbf{b}\)，\(\mathbf{x} \geq \mathbf{0}\) をみたす \(\mathbf{x} \in \R^N\) が存在するとき
LP は**実行可能**，最適値が \(-\infty\) でないとき**有界**であるという．
:::


:::fact
### Rem: 離散 Kantorovich 問題と線形計画

離散 Kantorovich 問題（[ref:Def: 離散 Kantorovich 問題|離散 Kantorovich 問題]）は
線形計画問題（[ref:Def: 線形計画問題|線形計画問題]）の特殊例である．
対応を明示するため，行列を列方向に並べてベクトル化する操作
\(\operatorname{vec} \colon \R^{n \times m} \to \R^{nm}\) を用いる．

\[
 \mathbf{p} \defeq \operatorname{vec}(\mathbf{P}) \in \R^{nm}_+,
 \qquad
 \mathbf{c} \defeq \operatorname{vec}(\mathbf{C}) \in \R^{nm}
\]

と置くと，フロベニウス内積は通常の内積に帰着する：

\[
 \inner{\mathbf{C}}{\mathbf{P}}
 = \sum_{i,j} C_{i,j} P_{i,j}
 = \mathbf{c}^\top \mathbf{p}.
\]

また，行和条件 \(\mathbf{P}\ones_m = \mathbf{a}\) と
列和条件 \(\mathbf{P}^\top \ones_n = \mathbf{b}\) は，
適切な \((n{+}m) \times nm\) 行列 \(\mathbf{A}\) を用いて
\(\mathbf{A}\mathbf{p} = \bigl[\begin{smallmatrix}\mathbf{a}\\ \mathbf{b}\end{smallmatrix}\bigr]\)
と書ける．
したがって離散 Kantorovich 問題は

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \min_{\substack{\mathbf{p} \in \R^{nm} \\
 \mathbf{A}\mathbf{p}
 = \left[\begin{smallmatrix}\mathbf{a}\\ \mathbf{b}\end{smallmatrix}\right],\;
 \mathbf{p} \geq \mathbf{0}}}\;
 \mathbf{c}^\top \mathbf{p}
\]

となり，[ref:Def: 線形計画問題|線形計画問題] の LP に他ならない．
:::


**最適解の存在と性質**


:::theorem
### Clm: 離散 Kantorovich 問題の解の存在

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
\(\mathbf{P}_0 \defeq \mathbf{a}\mathbf{b}^\top\) を考える．
これは各成分が \((P_0)_{i,j} = a_i b_j\) で定まる \(n \times m\) 行列であり，
\(a_i, b_j > 0\) より \(\mathbf{P}_0 \geq \mathbf{0}\) である．
行和について，\(\sum_j b_j = 1\) を用いて

\[
 (\mathbf{P}_0 \ones_m)_i
 = \sum_{j=1}^m a_i b_j
 = a_i \sum_{j=1}^m b_j
 = a_i,
\]

すなわち \(\mathbf{P}_0 \ones_m = \mathbf{a}\)．
同様に \(\sum_i a_i = 1\) から \(\mathbf{P}_0^\top \ones_n = \mathbf{b}\)．
よって \(\mathbf{P}_0 \in \CouplingsD(\mathbf{a}, \mathbf{b})\)．
（\(\mathbf{P}_0\) は連続版における独立カップリング \(\alpha \otimes \beta\)
の離散版に相当する．）

**(ii) コンパクト性．**
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の定義条件
\(\mathbf{P}\ones_m = \mathbf{a}\)，\(\mathbf{P}^\top \ones_n = \mathbf{b}\)，\(\mathbf{P} \geq \mathbf{0}\)
はいずれも各成分 \(P_{i,j}\) の連続関数による等式・不等式であるから，
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は \(\R^{n \times m}\) の閉集合である．
さらに，行和条件 \(\sum_j P_{i,j} = a_i\) と \(P_{i,j} \geq 0\) から
\(0 \leq P_{i,j} \leq a_i \leq 1\) が従い有界．
\(\R^{n \times m}\) における有界閉集合はコンパクト
（[ref:Thm: Heine-Borel の定理|Heine-Borel の定理]）．

**(iii) 連続性．**
\(\mathbf{P} \mapsto \inner{\mathbf{C}}{\mathbf{P}} = \sum_{i,j} C_{i,j} P_{i,j}\)
は線形写像であり，有限次元線形空間上で連続
（[ref:Def: 連続写像|連続写像]）．

以上 (i)--(iii) と Weierstrass の最大値の定理
（[ref:Thm: Weierstrass の最大値の定理|Weierstrass の最大値の定理]）より，
空でないコンパクト集合上の連続関数は最小値を達成する．
したがって最適解 \(\mathbf{P}^*\) が存在する．
:::
:::


:::theorem
### Clm: 最適解集合は凸かつコンパクト

最適解の集合

\[
 S^*
 \defeq
 \bigl\{ \mathbf{P}^* \in \CouplingsD(\mathbf{a}, \mathbf{b})
 \bigm|
 \inner{\mathbf{C}}{\mathbf{P}^*} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 \bigr\}
\]

は凸かつコンパクトである．

:::details-embedded 証明
**凸性．**
\(\mathbf{P}^*, \mathbf{Q}^* \in S^*\) と \(t \in [0,1]\) に対し，
\(\mathbf{R} \defeq t\mathbf{P}^* + (1-t)\mathbf{Q}^*\) は
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) の凸性から
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) に属し，

\[
 \inner{\mathbf{C}}{\mathbf{R}}
 = t\inner{\mathbf{C}}{\mathbf{P}^*} + (1-t)\inner{\mathbf{C}}{\mathbf{Q}^*}
 = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b}).
\]


**コンパクト性．**
\(S^* = \CouplingsD(\mathbf{a}, \mathbf{b}) \cap \{\mathbf{P} \mid \inner{\mathbf{C}}{\mathbf{P}} = \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})\}\)
はコンパクト集合と閉集合の共通部分．
:::
:::


:::fact accent
### Ex: 最適解の非一意性

\(n = m = 2\)，\(\mathbf{a} = \mathbf{b} = (1/2,\; 1/2)\) とし，
コスト行列を

\[
 \mathbf{C} = \begin{pmatrix} 1 & 3 \\ 3 & 5 \end{pmatrix}
\]

とする（\(C_{11} + C_{22} = 6 = C_{12} + C_{21}\)）．
周辺条件の連立を解くと自由変数は \(P_{1,1} \in [0,1/2]\) の1つで，
残りは \(P_{1,2} = P_{2,1} = 1/2 - P_{1,1}\)，\(P_{2,2} = P_{1,1}\) と定まる．
\(s \defeq 1 - 2P_{1,1} \in [0,1]\) とおけば \(\mathbf{P} = (1-s)\mathbf{P}_1 + s\mathbf{P}_2\) となり，
\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は

\[
 \mathbf{P}_1
 = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix},
 \qquad
 \mathbf{P}_2
 = \begin{pmatrix} 0 & 1/2 \\ 1/2 & 0 \end{pmatrix}
\]

を端点とする線分である．両者のコストはともに

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
\(S^* = \CouplingsD(\mathbf{a}, \mathbf{b})\) となる．

この非一意性は
\(C_{11} + C_{22} = C_{12} + C_{21}\) から生じる．
逆に \(C_{11} + C_{22} \neq C_{12} + C_{21}\) ならば
2頂点のコストが異なるため最適解は一意となる．
:::


:::fact
### Rem: エントロピー正則化による一意性の回復

離散 Kantorovich 問題の最適解は一般に一意でないが，
正則化パラメータ \(\varepsilon > 0\) を用いたエントロピー正則化

\[
 \min_{\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})}
 \left\{
 \inner{\mathbf{C}}{\mathbf{P}}
 - \varepsilon \Hb(\mathbf{P})
 \right\}
\]

は狭義凸最適化であり，最適解は一意に定まる．
:::


### Kantorovich 双対


:::definition
### Def: 双対ポテンシャル集合

\(c \colon \X \times \Y \to \R_+\) を可測コスト関数とする．
**双対実行可能集合**を

\[
 \Potentials(c) \defeq
 \bigl\{\, (f, g) \in L^1(\alpha) \times L^1(\beta)
 \;\big|\; f(x) + g(y) \leq c(x, y) \;\text{a.e.} \,\bigr\}
\]

と定義する．\((f, g)\) を**双対ポテンシャル**と呼ぶ．
:::


:::theorem
### Thm: Kantorovich 双対定理

\(\alpha \in \Mm_+^1(\X)\)，\(\beta \in \Mm_+^1(\Y)\)，
\(c \in \Cc(\X \times \Y, \R_+)\) に対して，

\[
 \MK_c(\alpha, \beta)
 = \sup_{(f,\, g)\,\in\, \Potentials(c)}
 \int_\X f \,\d\alpha + \int_\Y g \,\d\beta.
\]

:::details-embedded 証明
$(\geq)$ 任意の \((f, g) \in \Potentials(c)\) と \(\pi \in \Couplings(\alpha, \beta)\) に対して， \(f(x) + g(y) \leq c(x, y)\) を \(\pi\) について積分すると

\[
 \int_{\X \times \Y} c(x,y) \,\d\pi
 \geq \int_{\X \times \Y} \bigl(f(x) + g(y)\bigr) \,\d\pi
 = \int_\X f \,\d\alpha + \int_\Y g \,\d\beta.
\]

\(\pi\) と \((f, g)\) について下限・上限をとれば \(\MK_c(\alpha, \beta) \geq \sup_{\Potentials(c)}(\cdots)\)（弱双対性）．
$(\leq)$ 最適輸送計画の存在と汎関数解析的な双対性定理から等号が成立する （証明には弱収束と凸解析の道具を要するため，本ノートでは省略する）．
:::
:::


本節では連続版の証明に必要な準備（LP 双対の一般論）を整備し，
離散 Kantorovich 双対をその特殊ケースとして厳密に導出する．

Kantorovich 問題は線形計画問題（[ref:Def: 線形計画問題|線形計画問題]）に帰着される．
LP は双対問題を持ち，実行可能かつ有界な場合に主問題と双対問題の最適値が一致する
（強双対性，[ref:Thm: LP 強双対性|LP 強双対性]）．
本節ではまず LP 双対の一般論を整備し，離散 Kantorovich 双対をその特殊ケースとして導出する．

双対問題を論じる主な意義は次の2点にある．
第一に，強双対性（[ref:Thm: LP 強双対性|LP 強双対性]）より主問題の最適値は
双対問題の最大値に等しく，双対実行可能な \((\mathbf{f}, \mathbf{g})\) を1つ構成するだけで
主問題の最適値と一致する下界が得られる．
第二に，本章で扱うエントロピー正則化版では
双対変数が Sinkhorn アルゴリズムの更新変数に直接対応しており，
双対の構造の理解が Sinkhorn の導出の鍵になる．

:::definition
### Def: LP 双対問題

[ref:Def: 線形計画問題|線形計画問題] の LP に対し，

\[
 \max_{\mathbf{y} \in \R^M}
 \left\{
 \mathbf{b}^\top \mathbf{y}
 \;\middle|\;
 \mathbf{A}^\top \mathbf{y} \leq \mathbf{c}
 \right\}
\]

を**LP 双対問題**，元の最小化問題を**主問題**という．
\(\mathbf{y}\) を**双対変数**という．
双対の実行可能領域を
\(\mathcal{G} \defeq \{\mathbf{y} \in \R^M \mid \mathbf{A}^\top \mathbf{y} \leq \mathbf{c}\}\) と記す．
:::


:::theorem
### Clm: 弱双対性

主問題の実行可能解 \(\mathbf{x} \in \mathcal{F}\) と双対の実行可能解
\(\mathbf{y} \in \mathcal{G}\) に対して，\(\mathbf{c}^\top \mathbf{x} \geq \mathbf{b}^\top \mathbf{y}\)．
特に

\[
 \inf_{\mathbf{x} \in \mathcal{F}}\, \mathbf{c}^\top \mathbf{x}
 \;\geq\;
 \sup_{\mathbf{y} \in \mathcal{G}}\, \mathbf{b}^\top \mathbf{y}.
\]

:::details-embedded 証明
\(\mathbf{A}^\top \mathbf{y} \leq \mathbf{c}\) かつ \(\mathbf{x} \geq \mathbf{0}\) より
\((\mathbf{c} - \mathbf{A}^\top \mathbf{y})^\top \mathbf{x} \geq 0\)，すなわち

\[
 \mathbf{c}^\top \mathbf{x}
 \;\geq\;
 (\mathbf{A}^\top \mathbf{y})^\top \mathbf{x}
 = \mathbf{y}^\top(\mathbf{A}\mathbf{x})
 = \mathbf{y}^\top \mathbf{b}
 = \mathbf{b}^\top \mathbf{y}. \qedhere
\]
:::
:::


:::theorem
### Clm: Farkas の補題

\(\mathbf{A} \in \R^{M \times N}\)，\(\mathbf{b} \in \R^M\) に対して，
以下の二系のうちちょうど一方が解を持つ：

(I) \(\mathbf{A}\mathbf{x} = \mathbf{b}\)，\(\mathbf{x} \geq \mathbf{0}\) をみたす \(\mathbf{x} \in \R^N\) が存在する；
(II) \(\mathbf{A}^\top \mathbf{y} \leq \mathbf{0}\)，\(\mathbf{b}^\top \mathbf{y} > 0\) をみたす \(\mathbf{y} \in \R^M\) が存在する．
:::


:::fact
### Rem: Farkas の補題の証明について

Farkas の補題は，\(\R^N\) における有限生成凸錐の閉性と超平面分離定理を組み合わせることで証明される（Farkas, 1902）．
本セミナーでは標準結果として証明なしに引用する．
:::


:::theorem
### Thm: LP 強双対性

主問題が実行可能かつ有界ならば，双対問題も実行可能かつ有界であり，

\[
 \min_{\mathbf{x} \in \mathcal{F}}\; \mathbf{c}^\top \mathbf{x}
 \;=\;
 \max_{\mathbf{y} \in \mathcal{G}}\; \mathbf{b}^\top \mathbf{y}.
\]

:::details-embedded 証明
\(p^* \defeq \min_{\mathbf{x} \in \mathcal{F}} \mathbf{c}^\top \mathbf{x}\)（有限値），
\(d^* \defeq \sup_{\mathbf{y} \in \mathcal{G}} \mathbf{b}^\top \mathbf{y}\) とおく．
弱双対性（[ref:Clm: 弱双対性|弱双対性]）より \(d^* \leq p^*\) が成立する（\(\leq\) 方向）．

以下，\(d^* \geq p^*\) を示す．
任意の \(\varepsilon > 0\) に対して，変数 \((\mathbf{x}; s) \in \R^{N+1}\)，
\((\mathbf{x}; s) \geq \mathbf{0}\) に関する拡張された系

\[
 \mathbf{A}' (\mathbf{x}; s) = \mathbf{b}',
 \qquad
 \mathbf{A}' \defeq
 \begin{pmatrix} \mathbf{A} & \mathbf{0} \\ \mathbf{c}^\top & 1 \end{pmatrix}
 \in \R^{(M+1)\times(N+1)},
 \qquad
 \mathbf{b}' \defeq
 \begin{pmatrix} \mathbf{b} \\ p^* - \varepsilon \end{pmatrix}
 \in \R^{M+1}
\]

は解を持たない．
実際，もし解 \((\mathbf{x}, s)\) が存在すれば \(\mathbf{A}\mathbf{x} = \mathbf{b}\)，
\(s \geq 0\)，\(\mathbf{c}^\top \mathbf{x} = p^* - \varepsilon - s \leq p^* - \varepsilon\)
となり \(\mathbf{x} \in \mathcal{F}\) かつ \(\mathbf{c}^\top \mathbf{x} < p^*\) が成立して，
\(p^*\) の最適性に矛盾する．

上の系は解を持たないから，Farkas の補題（[ref:Clm: Farkas の補題|Farkas の補題]）を
\(\mathbf{A}' (\mathbf{x}; s) = \mathbf{b}'\)，\((\mathbf{x}; s) \geq \mathbf{0}\) に適用すると，
\((\mathbf{y}; \mu) \in \R^M \times \R\) が存在して

\[
 (\mathbf{A}')^\top (\mathbf{y}; \mu) \leq \mathbf{0},
 \qquad
 (\mathbf{b}')^\top (\mathbf{y}; \mu) > 0.
\]

\((\mathbf{A}')^\top = \begin{pmatrix} \mathbf{A}^\top & \mathbf{c} \\ \mathbf{0}^\top & 1 \end{pmatrix}\)
を計算すると，上の条件は

\[\begin{aligned}
 \mathbf{A}^\top \mathbf{y} + \mu\,\mathbf{c} &\leq \mathbf{0}, \\
 \mu &\leq 0, \\
 \mathbf{b}^\top \mathbf{y} + (p^* - \varepsilon)\,\mu &> 0
\end{aligned}\]

と同値になる．

**\(\mu = 0\) の場合．**
\(\mathbf{A}^\top \mathbf{y} \leq \mathbf{0}\) かつ \(\mathbf{b}^\top \mathbf{y} > 0\)
となり，Farkas の系 (II) が \(\mathbf{A}, \mathbf{b}\) に対して成立する．
しかし主問題の実行可能性から系 (I) が成立し，Farkas の補題により系 (II) は成立しない．矛盾．

**\(\mu < 0\) の場合．**
\(\lambda \defeq -\mu > 0\) とおく．\(\mathbf{A}^\top \mathbf{y} \leq \lambda\,\mathbf{c}\)，
すなわち \(\mathbf{A}^\top (\mathbf{y}/\lambda) \leq \mathbf{c}\) より
\(\mathbf{z} \defeq \mathbf{y}/\lambda \in \mathcal{G}\) は双対実行可能である．
\(\mathbf{b}^\top \mathbf{y} + (p^* - \varepsilon)\mu > 0\)，
すなわち \(\mathbf{b}^\top \mathbf{y} > \lambda(p^* - \varepsilon)\) より

\[
 \mathbf{b}^\top \mathbf{z}
 = \mathbf{b}^\top (\mathbf{y}/\lambda)
 > p^* - \varepsilon.
\]

ゆえに \(d^* \geq \mathbf{b}^\top \mathbf{z} > p^* - \varepsilon\)．

\(\varepsilon > 0\) は任意なので \(d^* \geq p^*\)．
弱双対性 \(d^* \leq p^*\) と合わせて \(d^* = p^*\)．
:::
:::


**離散版の双対問題**


:::definition
### Def: 離散双対実行可能集合

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
### Thm: Kantorovich 双対定理（離散版）

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

\(\mathbf{P} \geq 0\) の下で \(L\) を \(\mathbf{P}\) について最小化すると，
ある \((i,j)\) で \(C_{i,j} - f_i - g_j < 0\) なら
\(P_{i,j} \to +\infty\) により \(\inf_{\mathbf{P} \geq 0} L = -\infty\) となる．
一方，すべての \((i,j)\) で \(f_i + g_j \leq C_{i,j}\) なら，
最後の和は非負であり，\(\mathbf{P}=\mathbf{0}\) で最小値
\(\inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}\) を達成する．
よって双対問題は

\[
 \max_{(\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
\]

である．\(\CouplingsD(\mathbf{a}, \mathbf{b})\) は空でなく有界（[ref:Clm: 離散 Kantorovich 問題の解の存在|離散 Kantorovich 問題の解の存在]）であるから，
主問題は[ref:Def: 線形計画問題|線形計画問題] の LP として実行可能かつ有界である．
[ref:Thm: LP 強双対性|LP 強双対性] の強双対性より主問題と双対問題の最適値は一致する．
:::
:::


:::theorem
### Prop: 相補性条件

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

周辺条件 \(\sum_j P^*_{i,j} = a_i\)，\(\sum_i P^*_{i,j} = b_j\) を代入すると

\[\begin{aligned}
 \inner{\mathbf{f}^*}{\mathbf{a}} + \inner{\mathbf{g}^*}{\mathbf{b}}
 &= \sum_i f_i^* \Bigl(\sum_j P^*_{i,j}\Bigr)
 + \sum_j g_j^* \Bigl(\sum_i P^*_{i,j}\Bigr)
 = \sum_{i,j} (f_i^* + g_j^*) P^*_{i,j}.
\end{aligned}\]

したがって

\[
 \sum_{i,j}
 \bigl(C_{i,j} - f_i^* - g_j^*\bigr) P^*_{i,j}
 = 0.
\]

ここで \(C_{i,j} - f_i^* - g_j^* \geq 0\) は双対実行可能性
\((f^*, g^*) \in \PotentialsD(\mathbf{C})\)（[ref:Def: 離散双対実行可能集合|離散双対実行可能集合]）から，
\(P^*_{i,j} \geq 0\) はカップリングの定義から従うので，各項は非負である．
非負項の和が \(0\) であるから，各項が \(0\) である．
:::
:::


:::fact
### Rem: 双対変数と Sinkhorn アルゴリズムの接続

ここで導入した双対変数 \((\mathbf{f}, \mathbf{g})\) は，
本章で扱うエントロピー正則化 Kantorovich 問題においても
中心的な役割を果たす．
正則化版の最適解は双対変数を通じて陽に表現でき，
Sinkhorn アルゴリズムの反復はその双対変数の交互更新として解釈できる．
:::


**離散 \(C\)-変換と半双対**


:::definition
### Def: 離散 \(C\)-変換

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
### Clm: 離散半双対

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
（\(b_j > 0\) を用いる）．
[ref:Thm: Kantorovich 双対定理（離散版）|Kantorovich 双対定理（離散版）] の双対問題で
\(\mathbf{g}\) を消去すれば結論を得る．
:::
:::
