---
id: discrete-duality
nav: 離散化と双対
eyebrow: 3. Discrete OT
title: 離散化、線形計画、双対
---

有限支持測度 \(\alpha=\sum_i a_i\delta_{x_i}\), \(\beta=\sum_j b_j\delta_{y_j}\)（相異なる \(x_1,\ldots,x_n\in\X\), \(y_1,\ldots,y_m\in\Y\), \(\mathbf{a}\in\R_{++}^n\), \(\mathbf{b}\in\R_{++}^m\), \(\sum_i a_i=\sum_j b_j=1\)）では、[ref:カップリング]は行列 \(\mathbf{P}\in\R_+^{n\times m}\) で表される。

:::definition
### 定義: 輸送多面体

\[
  \Pi(\mathbf{a},\mathbf{b}) =
  \{\mathbf{P}\in\R_+^{n\times m}
  \mid
  \mathbf{P}\ones_m=\mathbf{a},
  \mathbf{P}^{\top}\ones_n=\mathbf{b}\}.
\]
:::

:::definition
### 定義: 線形計画

変数 \(x\in\R^d\) に対して、線形関数 \(c^\top x\) を線形等式・線形不等式で定まる集合上で最小化または最大化する問題を線形計画という。
:::

:::theorem
### 離散 Kantorovich 問題

\[
  \mathrm{MK}_{\mathbf{C}}(\mathbf{a},\mathbf{b})
  =
  \min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \inner{\mathbf{C}}{\mathbf{P}}.
\]

これは有限次元線形計画である。
:::

:::definition
### 定義: 双対問題

制約付き最小化問題に対して、制約をラグランジュ乗数で目的関数に組み込んで得られる最大化問題を双対問題という。元の最小化問題を主問題という。
:::

:::theorem
### 定理: 離散 Kantorovich 双対

\[
  \min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \sum_{i,j} C_{ij}P_{ij}
  =
  \max_{\mathbf{f},\mathbf{g}}
  \left\{
    \sum_i a_i f_i+\sum_j b_j g_j
    \mid f_i+g_j\le C_{ij}
  \right\}.
\]
:::

:::definition
### 定義: \(C\)-変換と \(c\)-変換

離散コスト行列 \(\mathbf{C}\) とベクトル \(\mathbf{f}\in\R^n\) に対して、

\[
  f^C_j\defeq \min_i(C_{ij}-f_i)
\]

を \(C\)-変換という。連続コスト \(c:\X\times\Y\to\R\) と関数 \(\varphi:\X\to\R\) に対して、

\[
  \varphi^c(y)\defeq \inf_{x\in\X}(c(x,y)-\varphi(x))
\]

を \(c\)-変換という。
:::

:::compare
:::column
### 有限次元

\(g_j=\min_i(C_{ij}-f_i)\) は \(C\)-変換である。
:::

:::column
### 連続版

\(\varphi^c(y)=\inf_x(c(x,y)-\varphi(x))\) は \(c\)-変換である。
:::
:::

:::details 相補性
最適な \(\mathbf{P},\mathbf{f},\mathbf{g}\) について

\[
  P_{ij}>0 \Longrightarrow f_i+g_j=C_{ij}.
\]

輸送が実際に流れる辺では双対制約が飽和する。
:::
