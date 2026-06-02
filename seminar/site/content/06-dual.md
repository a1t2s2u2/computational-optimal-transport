---
id: dual
nav: 古典双対
eyebrow: 6. Kantorovich Duality
title: 古典 Kantorovich 双対と c-変換
---


Kantorovich 問題は線形計画であり，制約付き凸最小化として**双対問題**（制約付き凹最大化）と対をなす．本章では非正則化問題の双対を整備し，最適輸送の台を特徴づける**相補性条件**と，双対を一変数に縮約する**\(c\)-変換**を導入する．これは第・章のエントロピー正則化・Sinkhorn が「ソフト化」していた対象の**硬い極限**にあたり，かつ Brenier 定理（次章）の出発点となる．

本章では離散の設定（\(\mathbf{a} \in \R_{\geq 0}^n\), \(\mathbf{b} \in \R_{\geq 0}^m\),\(\sum_i a_i = \sum_j b_j = 1\)）で議論する．コスト行列 \(\mathbf{C} \in \R_{\geq 0}^{n \times m}\) は一般のものでよい．

## Kantorovich 双対


:::definition
### Def: 双対実行可能集合

コスト行列 \(\mathbf{C}\) に対して，**Kantorovich 双対の実行可能集合**を

\[
 \PotentialsD(\mathbf{C})
 \defeq
 \left\{
 (\mathbf{f}, \mathbf{g}) \in \R^n \times \R^m
 \;\middle|\;
 f_i + g_j \leq C_{i,j}
 \quad (\forall\, i \in \range{n},\, j \in \range{m})
 \right\}
\]

で定める．\((\mathbf{f}, \mathbf{g})\) を**Kantorovich ポテンシャル**とよぶ．以下，行列 \((\mathbf{f} \oplus \mathbf{g})_{i,j} \defeq f_i + g_j\) と書く．
:::


:::theorem
### Prop: 弱双対性

任意の \(\mathbf{P} \in \CouplingsD(\mathbf{a}, \mathbf{b})\) と\((\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})\) に対して

\[
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 \leq
 \inner{\mathbf{C}}{\mathbf{P}}.
\]

:::details-embedded 証明
周辺条件 \(\sum_j P_{i,j} = a_i\), \(\sum_i P_{i,j} = b_j\) より

\[
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 = \sum_i f_i \sum_j P_{i,j} + \sum_j g_j \sum_i P_{i,j}
 = \sum_{i,j} (f_i + g_j) P_{i,j}
 \leq \sum_{i,j} C_{i,j} P_{i,j}
 = \inner{\mathbf{C}}{\mathbf{P}},
\]

最後の不等号は \(f_i + g_j \leq C_{i,j}\) と \(P_{i,j} \geq 0\) による．
:::
:::


:::theorem
### Thm: Kantorovich 双対定理

非正則化 Kantorovich 問題は双対を持ち，双対ギャップは生じない：

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 =
 \max_{(\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}.
\]

右辺の最大は達成される．

:::details-embedded 証明
主問題を Lagrange 関数で書く．周辺制約に乗数\(\mathbf{f} \in \R^n\), \(\mathbf{g} \in \R^m\) を割り当てると

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \min_{\mathbf{P} \geq \mathbf{0}}\;
 \max_{\mathbf{f}, \mathbf{g}}
 \Bigl\{
 \inner{\mathbf{C}}{\mathbf{P}}
 + \inner{\mathbf{a} - \mathbf{P}\ones_m}{\mathbf{f}}
 + \inner{\mathbf{b} - \mathbf{P}^\top\ones_n}{\mathbf{g}}
 \Bigr\}
\]

である（内側の \(\max\) は \(\mathbf{P}\) が周辺制約を破ると \(+\infty\) となり，満たすとき \(\inner{\mathbf{C}}{\mathbf{P}}\) に等しいので，右辺は主問題に一致する）．目的関数・制約はともに線形なので，有限次元線形計画の**強双対定理**により双対ギャップは生じず，\(\min\) と \(\max\) を交換できる：

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \max_{\mathbf{f}, \mathbf{g}}
 \Bigl\{
 \inner{\mathbf{a}}{\mathbf{f}} + \inner{\mathbf{b}}{\mathbf{g}}
 + \min_{\mathbf{P} \geq \mathbf{0}}
 \inner{\mathbf{C} - \mathbf{f} \oplus \mathbf{g}}{\mathbf{P}}
 \Bigr\}.
\]

ここで，行列 \(\mathbf{Q}\) に対し

\[
 \min_{\mathbf{P} \geq \mathbf{0}} \inner{\mathbf{Q}}{\mathbf{P}}
 =
 \begin{cases}
 0 & (\mathbf{Q} \geq \mathbf{0}),\\
 -\infty & (\text{それ以外})
 \end{cases}
\]

である（ある \(Q_{i,j} < 0\) なら対応する \(P_{i,j} \to +\infty\) で\(-\infty\)；\(\mathbf{Q} \geq \mathbf{0}\) なら \(\mathbf{P} = \mathbf{0}\) が最小）．したがって内側の最小が \(-\infty\) でない条件は\(\mathbf{C} - \mathbf{f} \oplus \mathbf{g} \geq \mathbf{0}\)，すなわち \((\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})\) であり，そのとき値は \(\inner{\mathbf{a}}{\mathbf{f}} + \inner{\mathbf{b}}{\mathbf{g}}\)．ゆえに主張の等式を得る．主問題は実行可能かつ有界な線形計画なので最適解を持ち，強双対性より双対の最大も達成される（\(c\)-変換による別証明は[ref:Prop: \(c\)-変換による一変数化|\(c\)-変換による一変数化] を見よ）．
:::
:::


:::fact
### Rem: ハード制約とそのソフト化

双対の制約 \(f_i + g_j \leq C_{i,j}\) は**ハード制約**である．エントロピー正則化の双対（[ref:Prop: エントロピー正則化の双対問題|エントロピー正則化の双対問題]）

\[
 \max_{\mathbf{f}, \mathbf{g}}
 \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 - \varepsilon \sum_{i,j} e^{(f_i + g_j - C_{i,j})/\varepsilon}
\]

は，このハード制約を指数ペナルティで**ソフト化**したものであった（備考[ref:Rem: ハード制約のソフト化|ハード制約のソフト化]）．\(\varepsilon \to 0\) では，\(f_i + g_j \leq C_{i,j}\) のときペナルティ項が \(0\) に，破ると \(-\infty\) に向かうので，本章の制約付き双対が回復する．
:::


:::fact
### Rem: 双対の解釈：集荷・配達価格

輸送業者が，地点 \(i\) での 1 単位の**集荷**に価格 \(f_i\)，地点 \(j\) への**配達**に価格 \(g_j\) を課すとする．総請求額は \(\inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}\)．依頼者がこれを受け入れる条件は，どの経路 \(i \to j\) も自前輸送コスト \(C_{i,j}\) を上回らないこと，すなわち \(f_i + g_j \leq C_{i,j}\)．業者はこの制約下で請求額を最大化する——これが双対問題である．
:::


## 相補性と最適輸送の台


:::theorem
### Prop: 相補性条件

\(\mathbf{P}^\star\) を主問題の最適解，\((\mathbf{f}^\star, \mathbf{g}^\star)\) を双対問題の最適解とする．このとき

\[
 P^\star_{i,j} > 0
 \;\Longrightarrow\;
 f^\star_i + g^\star_j = C_{i,j}.
\]

すなわち最適輸送の台は，双対制約が等号で成り立つ集合に含まれる：

\[
 \{(i,j) : P^\star_{i,j} > 0\}
 \subseteq
 \{(i,j) : f^\star_i + g^\star_j = C_{i,j}\}.
\]

:::details-embedded 証明
双対定理（[ref:Thm: Kantorovich 双対定理|Kantorovich 双対定理]）より\(\inner{\mathbf{C}}{\mathbf{P}^\star} = \inner{\mathbf{f}^\star}{\mathbf{a}} + \inner{\mathbf{g}^\star}{\mathbf{b}} = \sum_{i,j}(f^\star_i + g^\star_j)P^\star_{i,j}\)（弱双対性の証明と同じ周辺の入れ替え）．したがって

\[
 \sum_{i,j}\bigl(C_{i,j} - f^\star_i - g^\star_j\bigr)P^\star_{i,j} = 0.
\]

各項は，実行可能性 \(C_{i,j} - f^\star_i - g^\star_j \geq 0\) と\(P^\star_{i,j} \geq 0\) より非負であるから，総和が \(0\) ならすべての項が \(0\)．ゆえに \(P^\star_{i,j} > 0\) なら\(C_{i,j} - f^\star_i - g^\star_j = 0\)．
:::
:::


:::fact
### Rem: 台の特徴づけと Brenier への布石

相補性は，最適輸送が「等号集合」\(\{f^\star_i + g^\star_j = C_{i,j}\}\) の上にのみ質量を置くことを意味する．連続版では，この条件が\(\supp(\pi^\star) \subseteq \{(x,y) : f^\star(x) + g^\star(y) = c(x,y)\}\)となり，\(c(x,y) = \norm{x-y}^2\) のとき最適 \(y\) が \(\partial\phi(x)\) に属する——というBrenier 定理の台の特徴づけへつながる（次章）．
:::


## \(c\)-変換


双対は 2 つのポテンシャル \((\mathbf{f}, \mathbf{g})\) を持つが，一方を他方から最適に定める操作——**\(c\)-変換**——により一変数の最大化に縮約できる．

:::definition
### Def: \(c\)-変換

\(\mathbf{g} \in \R^m\) の**\(c\)-変換** \(\mathbf{g}^c \in \R^n\) を

\[
 (g^c)_i \defeq \min_{j \in \range{m}} \bigl(C_{i,j} - g_j\bigr)
\]

で定める．同様に \(\mathbf{f} \in \R^n\) に対し\((f^{\bar c})_j \defeq \min_{i \in \range{n}}(C_{i,j} - f_i)\) と定める．
:::


\(\mathbf{g}^c\) は，\(\mathbf{g}\) を固定したとき\(\PotentialsD(\mathbf{C})\) 内で \(\mathbf{f}\) にとれる**最大値**である：\(f_i + g_j \leq C_{i,j}\)（\(\forall j\)）は\(f_i \leq \min_j(C_{i,j} - g_j) = (g^c)_i\) と同値だからである．

:::theorem
### Prop: \(c\)-変換による一変数化

\[
 \MKD_{\mathbf{C}}(\mathbf{a}, \mathbf{b})
 = \max_{\mathbf{g} \in \R^m}
 \Bigl\{
 \inner{\mathbf{g}^c}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}
 \Bigr\}.
\]

:::details-embedded 証明
まず \((\mathbf{g}^c, \mathbf{g}) \in \PotentialsD(\mathbf{C})\)：

\[
 (g^c)_i + g_j
 = \min_k (C_{i,k} - g_k) + g_j
 \leq (C_{i,j} - g_j) + g_j
 = C_{i,j}.
\]

次に，任意の \((\mathbf{f}, \mathbf{g}) \in \PotentialsD(\mathbf{C})\) に対し\(f_i \leq (g^c)_i\) であり，\(\mathbf{a} \geq \mathbf{0}\) なので\(\inner{\mathbf{f}}{\mathbf{a}} \leq \inner{\mathbf{g}^c}{\mathbf{a}}\)．したがって \(\mathbf{g}\) を固定するごとに，\(\mathbf{f} = \mathbf{g}^c\) が目的関数を最大化する実行可能なポテンシャルである．[ref:Thm: Kantorovich 双対定理|Kantorovich 双対定理] の最大化を\(\mathbf{f}\) について先に解いた形が主張の式である．
:::
:::


:::fact
### Rem: \(c\)-凹関数と Legendre 変換

\(\mathbf{g}^c\) の形をしたベクトル（アフィン関数\(j \mapsto C_{i,j} - g_j\) の \(\min\)）を**\(c\)-凹**とよぶ．最適ポテンシャルは \(c\)-凹なものにとれるため，双対は \(c\)-凹ポテンシャルの有界集合上の最大化に帰着し，最大が達成される（[ref:Thm: Kantorovich 双対定理|Kantorovich 双対定理] の達成性）．\(C_{i,j} = \norm{x_i - y_j}^2\) の場合，\(c\)-変換は凸関数の **Legendre 変換**と対応し，これが Brenier 定理で最適写像を凸関数の勾配として特徴づける鍵となる（次章）．
:::


## Sinkhorn との対応：ソフト \(c\)-変換


エントロピー正則化（「エントロピー正則化」の章）とSinkhorn（「正則化問題の双対と Sinkhorn アルゴリズム」の章）は，この \(c\)-変換を**ソフト化**した反復として理解できる．\(\min\) をなめらかにした**ソフト最小値**を導入する．

:::definition
### Def: ソフト最小値

\(\mathbf{z} \in \R^m\) と \(\varepsilon > 0\) に対し

\[
 \smin_\varepsilon(\mathbf{z})
 \defeq
 -\varepsilon \log \sum_{j=1}^m e^{-z_j/\varepsilon}.
\]

これは \(\min_j z_j - \varepsilon\log m \leq \smin_\varepsilon(\mathbf{z}) \leq \min_j z_j\) を満たし，\(\varepsilon \to 0\) で\(\smin_\varepsilon(\mathbf{z}) \to \min_j z_j\) となる．
:::


:::definition
### Def: ソフト \(c\)-変換

\(\mathbf{g} \in \R^m\) の**ソフト \(c\)-変換**\(\mathbf{g}^{c_\varepsilon} \in \R^n\) を

\[
 (g^{c_\varepsilon})_i
 \defeq
 \smin_\varepsilon\bigl((C_{i,j} - g_j)_j\bigr)
 = -\varepsilon \log \sum_j e^{-(C_{i,j} - g_j)/\varepsilon}
\]

で定める．\(\varepsilon \to 0\) のとき \(\mathbf{g}^{c_\varepsilon} \to \mathbf{g}^c\)．
:::


:::theorem
### Prop: Sinkhorn はソフト交互 \(c\)-変換である

対数領域変数 \(f_i = \varepsilon\log u_i\), \(g_j = \varepsilon\log v_j\)で表すと，Sinkhorn の \(\mathbf{u}\) 更新\(\mathbf{u} = \mathbf{a} \oslash (\mathbf{K}\mathbf{v})\)（「正則化問題の双対と Sinkhorn アルゴリズム」の章）は

\[
 f_i \leftarrow (g^{c_\varepsilon})_i + \varepsilon\log a_i
\]

と書ける．\(\varepsilon \to 0\) のとき，\(\varepsilon\log a_i \to 0\)（\(a_i > 0\) は固定）なので，これは古典的 \(c\)-変換\(f_i \leftarrow (g^c)_i = \min_j(C_{i,j} - g_j)\) に収束する．

:::details-embedded 証明
\(u_i = a_i / (\mathbf{K}\mathbf{v})_i\) の両辺の対数を \(\varepsilon\) 倍すると\(f_i = \varepsilon\log a_i - \varepsilon\log(\mathbf{K}\mathbf{v})_i\)．Gibbs カーネル \(K_{i,j} = e^{-C_{i,j}/\varepsilon}\) と\(v_j = e^{g_j/\varepsilon}\) より

\[
 (\mathbf{K}\mathbf{v})_i
 = \sum_j e^{-C_{i,j}/\varepsilon} e^{g_j/\varepsilon}
 = \sum_j e^{-(C_{i,j} - g_j)/\varepsilon},
\]

ゆえに \(-\varepsilon\log(\mathbf{K}\mathbf{v})_i = (g^{c_\varepsilon})_i\)．したがって \(f_i = (g^{c_\varepsilon})_i + \varepsilon\log a_i\)．\(\varepsilon \to 0\) で \((g^{c_\varepsilon})_i \to (g^c)_i\) かつ\(\varepsilon\log a_i \to 0\)（\(a_i > 0\) 固定）なので\(f_i \to (g^c)_i\)．
:::
:::


:::fact
### Rem: 本章のまとめと展望

非正則化 Kantorovich 問題は双対\(\max_{(\mathbf{f},\mathbf{g}) \in \PotentialsD(\mathbf{C})} \inner{\mathbf{f}}{\mathbf{a}} + \inner{\mathbf{g}}{\mathbf{b}}\) を持ち（[ref:Thm: Kantorovich 双対定理|Kantorovich 双対定理]），最適輸送の台は相補性条件で特徴づけられた（[ref:Prop: 相補性条件|相補性条件]）．\(c\)-変換により双対は一変数化され（[ref:Prop: \(c\)-変換による一変数化|\(c\)-変換による一変数化]），Sinkhorn はそのソフト化（ソフト \(c\)-変換）の交互適用として古典双対に接続する（[ref:Prop: Sinkhorn はソフト交互 \(c\)-変換である|Sinkhorn はソフト交互 \(c\)-変換である]）．

次章では地の空間を \(\R^d\)，コストを \(\norm{x-y}^2\) とし，\(c\)-変換が Legendre 変換に，相補性条件が「最適写像は凸関数の勾配 \(T = \nabla\phi\)」という**Brenier の定理**に結実することを見る．これが測地線・Wasserstein 幾何の出発点となる．
:::
