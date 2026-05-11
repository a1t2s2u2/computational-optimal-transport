---
id: preliminaries
nav: 準備
eyebrow: 1. Foundations
title: 準備
---


:::definition
### 定義: 冪集合

集合 \(\Omega\) に対し，\(\Omega\) の部分集合全体を

\[
 2^{\Omega} \defeq \{A \mid A \subset \Omega\}
\]

と書き，\(\Omega\) の**冪集合**という．
:::


## 位相空間


:::definition
### 定義: 位相空間

集合 \(\Omega\) と部分集合族 \(\mathcal{O} \subset 2^{\Omega}\) の組
\((\Omega, \mathcal{O})\) が**位相空間**であるとは，
次の3条件を満たすことをいう：

(i) \(\emptyset, \Omega \in \mathcal{O}\)，
(ii) \(U_1, \ldots, U_n \in \mathcal{O} \Longrightarrow \bigcap_{k=1}^{n} U_k \in \mathcal{O}\)（有限交叉で閉じる），
(iii) \(\{U_\lambda\}_{\lambda \in \Lambda} \subset \mathcal{O} \Longrightarrow \bigcup_{\lambda \in \Lambda} U_\lambda \in \mathcal{O}\) （任意濃度の和集合で閉じる）．

\(\mathcal{O}\) の元を**開集合**，\(\mathcal{O}\) を \(\Omega\) 上の**位相**という．
ある開集合 \(U \in \mathcal{O}\) を用いて \(F = \Omega \setminus U\) と書ける
\(F \subset \Omega\) を**閉集合**という．
:::


:::definition
### 定義: 稠密集合

位相空間 \((\Omega, \mathcal{O})\) の部分集合 \(D \subset \Omega\) が**稠密**とは，
任意の空でない開集合 \(U \in \mathcal{O}\) に対して \(D \cap U \neq \emptyset\)
となることをいう．
:::


:::definition
### 定義: 可分性

位相空間 \((\Omega, \mathcal{O})\) が可算な稠密部分集合
（[ref:定義: 稠密集合|稠密集合]）をもつとき，
\((\Omega, \mathcal{O})\) は**可分**であるという．
:::


## 距離空間


:::definition
### 定義: 距離空間

集合 \(\Omega\) と関数 \(d \colon \Omega \times \Omega \to [0, \infty)\) の組
\((\Omega, d)\) が**距離空間**であるとは，
次の3条件がすべての \(x, y, z \in \Omega\) に対して成り立つことをいう：

(i) 同一性：\(d(x, y) = 0 \iff x = y\)，
(ii) 対称性：\(d(x, y) = d(y, x)\)，
(iii) 三角不等式：\(d(x, z) \leq d(x, y) + d(y, z)\)．

関数 \(d\) を \(\Omega\) 上の**距離関数**という．
:::


:::definition
### 定義: 開球

距離空間 \((\Omega, d)\) 上の点 \(x \in \Omega\) と半径 \(r \in \R_{++}\) に対して，
中心 \(x\)，半径 \(r\) の**開球**を

\[
 B_r(x) \defeq \{y \in \Omega \mid d(x, y) < r\}
\]

で定める．
:::


距離空間 \((\Omega, d)\) における開集合（[ref:定義: 位相空間|位相空間]）は，
開球 \(B_r(x)\) を用いて次のように特徴付けられる：
\(U \subset \Omega\) が開集合であるとは，任意の \(x \in U\) に対し
\(B_r(x) \subset U\) をみたす \(r \in \R_{++}\) が存在することをいう．


:::definition
### 定義: 収束列

距離空間 \((\Omega, d)\) における列 \((x_n)_{n \geq 1} \subset \Omega\) が
点 \(x \in \Omega\) に**収束**するとは，
任意の \(\varepsilon > 0\) に対してある \(N \in \N\) が存在して
\(n \geq N \Longrightarrow d(x_n, x) < \varepsilon\) となることをいう．
このとき \(\lim_{n \to \infty} x_n = x\) または \(x_n \to x\) と書く．
:::


:::definition
### 定義: 完備性

距離空間 \((\Omega, d)\) の列 \((x_n)_{n \geq 1} \subset \Omega\) が
**Cauchy 列**であるとは，
任意の \(\varepsilon > 0\) に対してある \(N \in \N\) が存在して
\(n, m \geq N \Longrightarrow d(x_n, x_m) < \varepsilon\) となることをいう．
\((\Omega, d)\) が**完備**であるとは，
\(\Omega\) における任意の Cauchy 列が \(\Omega\) の点に収束する
（[ref:定義: 収束列|収束列]）ことをいう．すなわち

\[
 \forall (x_n)_{n \geq 1} \subset \Omega \text{ Cauchy 列},\;
 \exists x \in \Omega,\;
 x_n \to x.
\]

収束の定義に展開すれば

\[
 \forall (x_n)_{n \geq 1} \subset \Omega \text{ Cauchy 列},\;
 \exists x \in \Omega,\;
 \forall \varepsilon > 0,\;
 \exists N \in \N,\;
 n \geq N \Longrightarrow d(x_n, x) < \varepsilon.
\]
:::


:::definition
### 定義: Polish 空間

完備かつ可分な距離空間を**Polish 空間**という．
例：\(\R^d\) はユークリッド距離に関して Polish 空間である
（\(\Q^d\) が可算稠密部分集合を与える）．
:::


## 測度論


### 可測空間と確率測度


:::definition
### 定義: \(\sigma\)-代数

集合 \(\Omega\) の部分集合族 \(\mathcal{F} \subset 2^{\Omega}\) が
**\(\sigma\)-代数**であるとは，
以下の3条件を満たすことをいう：

(i) \(\Omega \in \mathcal{F}\)，
(ii) \(A \in \mathcal{F} \Longrightarrow A^c \in \mathcal{F}\)（補集合で閉じる），
(iii) \(A_1, A_2, \ldots \in \mathcal{F} \Longrightarrow \bigcup_{k=1}^{\infty} A_k \in \mathcal{F}\)（可算合併で閉じる）．
:::


:::definition
### 定義: 可測空間

集合 \(\Omega\) と \(\Omega\) 上の \(\sigma\)-代数 \(\mathcal{F}\) の組
\((\Omega, \mathcal{F})\) を**可測空間**という．
\(\mathcal{F}\) の元を**可測集合**という．
:::


:::definition
### 定義: 可測写像

可測空間 \((\Omega_1, \mathcal{F}_1)\) から \((\Omega_2, \mathcal{F}_2)\) への
写像 \(T \colon \Omega_1 \to \Omega_2\) が**可測**であるとは，
\(T^{-1}(A) \in \mathcal{F}_1\) がすべての \(A \in \mathcal{F}_2\) に対して成り立つことをいう．
:::


:::definition
### 定義: ボレル \(\sigma\)-代数

位相空間 \((\Omega, \mathcal{O})\) のすべての開集合
（[ref:定義: 位相空間|位相空間]）
を含む最小の \(\sigma\)-代数を
**ボレル \(\sigma\)-代数**といい，\(\Bb(\Omega)\) と記す．
:::


:::definition
### 定義: 可測関数

可測空間 \((\Omega, \mathcal{F})\) から \((\R, \Bb(\R))\) への可測写像
\(f \colon \Omega \to \R\)（[ref:定義: 可測写像|可測写像]）を
**可測関数**という．
特に Polish 空間 \(\X\) にボレル \(\sigma\)-代数 \(\Bb(\X)\) を入れた
可測空間上の可測関数を**ボレル可測関数**ともいう．
:::


:::definition
### 定義: 積可測空間

距離空間 \((\X, d_\X)\), \((\Y, d_\Y)\) に対して，
積空間 \(\X \times \Y\) に**積距離**

\[
 d\bigl((x, y), (x', y')\bigr) \defeq d_\X(x, x') + d_\Y(y, y')
\]

を入れたときのボレル \(\sigma\)-代数を \(\Bb(\X \times \Y)\) と記し，
可測空間 \((\X \times \Y, \Bb(\X \times \Y))\) を
\((\X, \Bb(\X))\) と \((\Y, \Bb(\Y))\) の**積可測空間**という．
:::


:::definition
### 定義: 測度

可測空間 \((\Omega, \mathcal{F})\) 上の**測度**とは，
関数 \(\mu \colon \mathcal{F} \to [0, \infty]\) であって，
次の 2 条件を満たすものをいう：

(i) \(\mu(\emptyset) = 0\)，
(ii) 互いに素な可測集合 \(A_1, A_2, \ldots \in \mathcal{F}\) に対して \(\mu\bigl(\bigcup_{k=1}^{\infty} A_k\bigr) = \sum_{k=1}^{\infty} \mu(A_k)\) （可算加法性）．
:::


:::definition
### 定義: 確率測度

可測空間 \((\Omega, \mathcal{F})\) 上の測度 \(\mu\) が \(\mu(\Omega) = 1\) を満たすとき，
\(\mu\) を**確率測度**という．
\(\Omega\) 上の確率測度の全体を \(\Mm_+^1(\Omega)\) と記す．
:::


### 測度に対する積分


:::definition
### 定義: 指示関数

集合 \(\Omega\) の部分集合 \(A \subset \Omega\) に対して，
**指示関数** \(\mathbf{1}_A \colon \Omega \to \{0, 1\}\) を

\[
 \mathbf{1}_A(y) \defeq
 \begin{cases}
 1 & y \in A, \\
 0 & y \notin A
 \end{cases}
\]

で定める．
:::


:::definition
### 定義: 単関数

可測空間 \((\Omega, \mathcal{F})\) 上の関数 \(s \colon \Omega \to \R_+\) が
**単関数**であるとは，互いに素な可測集合
\(A_1, \ldots, A_m \in \mathcal{F}\) と非負定数 \(c_1, \ldots, c_m \geq 0\) を用いて

\[
 s = \sum_{k=1}^{m} c_k \mathbf{1}_{A_k}
\]

と表せることをいう．
:::


:::definition
### 定義: 非負可測関数の積分

可測空間 \((\Omega, \mathcal{F})\) 上の測度 \(\mu\) に対し，
非負可測関数の積分を以下の 2 段階で定める：

(i) 単関数 \(s = \sum_{k=1}^{m} c_k \mathbf{1}_{A_k}\) （[ref:定義: 単関数|単関数]）の積分を

\[
 \int_\Omega s \, \d\mu \defeq \sum_{k=1}^{m} c_k \, \mu(A_k)
\]

で定める．
(ii) 非負可測関数 \(f \colon \Omega \to [0, \infty]\) の積分を

\[
 \int_\Omega f \, \d\mu \defeq
 \sup\!\left\{ \int_\Omega s \, \d\mu
 \;\middle|\; s \text{ は単関数}, \; 0 \leq s \leq f \right\}
\]

で定める．この値は常に \([0, +\infty]\) に存在し well-defined である．
:::


:::theorem
### 命題: 単調収束定理と単関数近似

可測空間 \((\Omega, \mathcal{F})\) 上の測度 \(\mu\) に対して次が成り立つ．

(i) **単関数近似**：任意の非負可測関数 \(f \colon \Omega \to [0, \infty]\) に対して， 各点で \(f_n \uparrow f\) を満たす単関数の単調増加列 \((f_n)_{n \geq 1}\) が存在する．
(ii) **単調収束定理**： 非負可測関数の単調増加列 \(f_n \uparrow f\) に対して \(\int f_n \, \d\mu \uparrow \int f \, \d\mu\)．
:::


:::theorem
### 命題: 積分の測度に関する線形性

可測空間 \((\Omega, \mathcal{F})\) 上の測度 \(\mu_1, \ldots, \mu_n\)，
非負係数 \(a_1, \ldots, a_n \geq 0\)，および非負可測関数
\(f \colon \Omega \to [0, \infty]\) に対して，

\[
 \int_\Omega f \, \d\!\Bigl(\sum_{i=1}^{n} a_i \mu_i\Bigr)
 = \sum_{i=1}^{n} a_i \int_\Omega f \, \d\mu_i.
\]

ここで測度の和・スカラー倍は可測集合 \(A \in \mathcal{F}\) に対して
\((\mu_1 + \mu_2)(A) \defeq \mu_1(A) + \mu_2(A)\)，
\((a\mu)(A) \defeq a\, \mu(A)\) で定まる測度である．

:::details-embedded 証明
単関数 \(s = \sum_{k} c_k \mathbf{1}_{A_k}\) について，
単関数積分の定義と測度の和・スカラー倍の定義から

\[
 \int s \, \d\!\Bigl(\sum_i a_i \mu_i\Bigr)
 = \sum_k c_k \Bigl(\sum_i a_i \mu_i\Bigr)(A_k)
 = \sum_k c_k \sum_i a_i \mu_i(A_k)
 = \sum_i a_i \sum_k c_k \mu_i(A_k)
 = \sum_i a_i \int s \, \d\mu_i.
\]

一般の非負可測関数 \(f\) に対しては，
[ref:命題: 単調収束定理と単関数近似|単調収束定理と単関数近似] により単関数の単調増加列 \(f_n \uparrow f\) が取れ，
単調収束定理を両辺に適用すれば結論が得られる．
:::
:::


### Dirac 測度と押し出し


:::definition
### 定義: Dirac 測度

可測空間 \((\Omega, \mathcal{F})\) 上の点 \(x \in \Omega\) に対して，
**Dirac 測度** \(\delta_x \in \Mm_+^1(\Omega)\) を

\[
 \delta_x(A) \defeq
 \begin{cases}
 1 & x \in A, \\
 0 & x \notin A
 \end{cases}
 \qquad (\forall\, A \in \mathcal{F})
\]

で定義する．
:::


:::theorem
### 主張: Dirac 測度に対する積分

任意の非負可測関数 \(f \colon \X \to [0, \infty]\) に対して，

\[
 \int_\X f \, \d\delta_x = f(x).
\]

:::details-embedded 証明
\(A \in \Bb(\X)\) に対し単関数積分の定義より
\(\int \mathbf{1}_A \, \d\delta_x = \delta_x(A) = \mathbf{1}_A(x)\)．
単関数 \(f = \sum_k c_k \mathbf{1}_{A_k}\) に対しては積分の線形性から

\[
 \int_\X f \, \d\delta_x
 = \sum_k c_k \, \delta_x(A_k)
 = \sum_k c_k \, \mathbf{1}_{A_k}(x)
 = f(x).
\]

一般の非負可測関数 \(f\) に対しては，
[ref:命題: 単調収束定理と単関数近似|単調収束定理と単関数近似] により単関数の単調増加列 \(f_n \uparrow f\) が取れ，
単調収束定理から

\[
 \int_\X f \, \d\delta_x
 = \lim_{n \to \infty} \int_\X f_n \, \d\delta_x
 = \lim_{n \to \infty} f_n(x)
 = f(x).
\]
:::
:::


:::definition
### 定義: 離散測度

Polish 空間 \(\X\) 上のボレル確率測度 \(\mu \in \Mm_+^1(\X)\) が
**離散測度**であるとは，
ある \(n \in \N\)，相異なる \(x_1, \ldots, x_n \in \X\)，
および \(a_1, \ldots, a_n > 0\)（\(\sum_{i=1}^n a_i = 1\)）が存在して

\[
 \mu = \sum_{i=1}^{n} a_i\, \delta_{x_i}
\]

と表せることをいう．
:::


:::theorem
### 主張: 離散測度の表示の一意性

離散測度 \(\mu = \sum_{i=1}^{n} a_i\, \delta_{x_i}\) の表示について
\(a_i = \mu(\{x_i\})\) が成り立ち，
\(n\) および対 \(\{(x_i, a_i)\}_{i=1}^{n}\) は \(\mu\) から
添字の入れ替えを除いて一意に定まる．

:::details-embedded 証明
\(x_1, \ldots, x_n\) は相異なるから
\(\delta_{x_i}(\{x_k\}) = \mathbf{1}[i = k]\)．
ゆえに

\[
 \mu(\{x_k\}) = \sum_{i=1}^{n} a_i\, \delta_{x_i}(\{x_k\}) = a_k.
\]

もう一通りの表示
\(\mu = \sum_{j=1}^{m} b_j\, \delta_{y_j}\)
（相異なる \(y_j \in \X\)，\(b_j > 0\)，\(\sum_j b_j = 1\)）が存在したとすると，
各 \(y_j\) について \(\mu(\{y_j\}) = b_j > 0\) より
\(y_j \in \{x_1, \ldots, x_n\}\)．対称性から \(\{y_j\} \subset \{x_i\}\) かつ
\(\{x_i\} \subset \{y_j\}\) ゆえ集合として一致．
したがって \(m = n\) かつある置換 \(\sigma \in \Perm(n)\) で \(y_{\sigma(i)} = x_i\)，
\(b_{\sigma(i)} = a_i\)．
:::
:::


:::definition
### 定義: 押し出し

可測写像 \(T \colon \X \to \Y\) と測度 \(\mu \in \Mm_+^1(\X)\) に対して，
\(T\) による \(\mu\) の**押し出し** \(T\pushforward \mu \in \Mm_+^1(\Y)\) を

\[
 (T\pushforward \mu)(A) \defeq \mu(T^{-1}(A))
 \qquad (\forall\, A \in \Bb(\Y))
\]

で定義する．
:::


:::theorem
### 命題: Dirac 測度と離散測度の押し出し

可測写像 \(T \colon \X \to \Y\) に対して，次が成り立つ．

(i) 任意の点 \(x \in \X\) に対して \(T\pushforward \delta_x = \delta_{T(x)}\)．
(ii) 任意の点 \(x_1, \ldots, x_n \in \X\) と係数 \(a_1, \ldots, a_n \geq 0\) に対して

\[
 T\pushforward \Bigl(\sum_{i=1}^{n} a_i\, \delta_{x_i}\Bigr)
 = \sum_{i=1}^{n} a_i\, \delta_{T(x_i)}.
\]

:::details-embedded 証明
(i) 任意の \(A \in \Bb(\Y)\) に対して，押し出しの定義より
\((T\pushforward \delta_x)(A) = \delta_x(T^{-1}(A))\)．
\(x \in T^{-1}(A) \iff T(x) \in A\) なので，

\[
 \delta_x(T^{-1}(A)) =
 \begin{cases}
 1 & x \in T^{-1}(A), \text{ すなわち } T(x) \in A \\
 0 & x \notin T^{-1}(A), \text{ すなわち } T(x) \notin A
 \end{cases}
 \;=\; \delta_{T(x)}(A).
\]


(ii) 任意の \(A \in \Bb(\Y)\) に対して，

\[\begin{aligned}
 \Bigl(T\pushforward \sum_i a_i \delta_{x_i}\Bigr)(A)
 &= \Bigl(\sum_i a_i \delta_{x_i}\Bigr)(T^{-1}(A))
 && \text{（押し出しの定義）} \\
 &= \sum_i a_i\, \delta_{x_i}(T^{-1}(A))
 && \text{（測度の和・スカラー倍）} \\
 &= \sum_i a_i\, \delta_{T(x_i)}(A)
 && \text{（(i) より）}
\end{aligned}\]
:::
:::


## 線形代数


:::definition
### 定義: 有限集合と濃度

集合 \(S\) が**有限集合**であるとは，ある \(n \in \N\) と
全単射 \(f \colon \range{n} \to S\) が存在することをいう．
この \(n\) を \(S\) の**濃度**といい \(|S|\) で表す．
:::


:::theorem
### 主張: 有限集合の最小元

\(\R\) の空でない有限部分集合 \(S\)（[ref:定義: 有限集合と濃度|有限集合と濃度]）には
最小元が存在する：

\[
 \exists\, s^* \in S \;\;\text{s.t.}\;\; \forall\, s \in S,\; s^* \leq s.
\]

:::details-embedded 証明
\(|S|\) に関する帰納法で示す．

**\(|S| = 1\) の時．** \(S\) の唯一の元がそのまま最小元．

**\(|S| \geq 2\) の時．**
\(\R\) の任意の空でない有限部分集合 \(T\) について \(|T| < |S|\) ならば最小元を持つと仮定する．
\(a \in S\) を任意に取り \(S' \defeq S \setminus \{a\}\) とおくと \(|S'| = |S| - 1\) なので，
仮定が \(S'\) に対して適用でき最小元 \(b \in S'\) を持つ．
\(a, b \in \R\) より \(b \leq a\) か \(a < b\) のいずれかが成り立つので，

\[
 s^* \defeq
 \begin{cases}
 b & (b \leq a), \\
 a & (a < b)
 \end{cases}
\]

とおけば \(s^* \in S\) かつ任意の \(s \in S\) について \(s^* \leq s\)．
:::
:::


:::definition
### 定義: 置換

\(n \in \N\) について，全単射
\(\sigma \colon \range{n} \to \range{n}\) を \(\range{n}\) 上の**置換**という．
置換全体の集合を

\[
 \Perm(n) \defeq \{\sigma \colon \range{n} \to \range{n} \mid \sigma \text{ は全単射}\}
\]

で表す．\(\Perm(n)\) は \(|\Perm(n)| = n!\) の有限集合
（[ref:定義: 有限集合と濃度|有限集合と濃度]）である．
:::


:::definition
### 定義: フロベニウス内積

同じサイズの2つの行列 \(\mathbf{A}, \mathbf{B} \in \R^{n \times m}\) に対し，
**フロベニウス内積**を

\[
 \inner{\mathbf{A}}{\mathbf{B}}
 \defeq \tr(\mathbf{A}^\top \mathbf{B})
 = \sum_{i=1}^{n} \sum_{j=1}^{m} A_{i,j} B_{i,j}
\]

で定める．
:::


:::definition
### 定義: 凸集合

ベクトル空間 \(V\) の部分集合 \(S \subset V\) が**凸**であるとは，
任意の \(v_1, v_2 \in S\) と任意の \(t \in [0,1]\) に対して

\[
 t v_1 + (1-t) v_2 \in S
\]

が成り立つことをいう．
:::


:::definition
### 定義: 凸関数と狭義凸関数

凸集合 \(S \subset V\) 上の関数 \(f \colon S \to \R\) が
**凸関数**であるとは，任意の \(v_1, v_2 \in S\) と
任意の \(t \in [0,1]\) に対して

\[
 f\bigl(t v_1 + (1-t)v_2\bigr)
 \leq
 t f(v_1) + (1-t) f(v_2)
\]

が成り立つことをいう．さらに，任意の相異なる
\(v_1 \neq v_2\) と任意の \(t \in (0,1)\) に対して

\[
 f\bigl(t v_1 + (1-t)v_2\bigr)
 <
 t f(v_1) + (1-t) f(v_2)
\]

が成り立つとき，\(f\) は**狭義凸関数**であるという．
:::


:::definition
### 定義: 凸多面体

行列 \(\mathbf{A} \in \R^{k \times d}\) とベクトル \(\mathbf{b} \in \R^k\) に対して，
線形等式・不等式制約で定まる \(\R^d\) の部分集合

\[
 \{\mathbf{x} \in \R^d \mid
 \mathbf{A}\mathbf{x} = \mathbf{b},\; \mathbf{x} \geq \mathbf{0}\}
\]

を**凸多面体**という．凸多面体は凸集合である．
:::
