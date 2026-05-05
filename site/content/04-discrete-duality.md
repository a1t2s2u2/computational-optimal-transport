---
id: discrete-duality
nav: 離散化と双対
eyebrow: 3. Discrete OT
title: 離散化、線形計画、双対
---

有限支持測度 \(\alpha=\sum_i a_i\delta_{x_i}\), \(\beta=\sum_j b_j\delta_{y_j}\) では、カップリングは行列 \(\mathbf{P}\in\R_+^{n\times m}\) で表される。

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
