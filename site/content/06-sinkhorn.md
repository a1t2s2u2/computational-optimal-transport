---
id: sinkhorn
nav: Sinkhorn
eyebrow: 5. Sinkhorn
title: Sinkhorn アルゴリズム
term: sinkhorn
---

:::theorem
### 定理: スケーリング形式

正則化問題の最適解は、正ベクトル \(\mathbf{u},\mathbf{v}\) により

\[
  \mathbf{P}_{\varepsilon}
  =
  \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})
\]

と表される。
:::

:::algorithm
### Sinkhorn 反復

1. \(\mathbf{v}^{(0)}=\ones_m\)
2. \(\mathbf{u}\leftarrow\mathbf{a}\oslash(\mathbf{K}\mathbf{v})\)
3. \(\mathbf{v}\leftarrow\mathbf{b}\oslash(\mathbf{K}^{\top}\mathbf{u})\)
4. \(\mathbf{P}=\diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})\)
:::

:::demo sinkhorn

:::details 対数領域 Sinkhorn
小さい \(\varepsilon\) では \(K_{ij}=\exp(-C_{ij}/\varepsilon)\) が数値的に不安定になる。\(f_i=\varepsilon\log u_i\), \(g_j=\varepsilon\log v_j\) を更新することで、log-sum-exp 型の安定な計算になる。
:::
