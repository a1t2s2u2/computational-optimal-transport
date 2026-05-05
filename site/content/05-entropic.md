---
id: entropic
nav: エントロピー正則化
eyebrow: 4. Entropic Regularization
title: エントロピー正則化
term: entropy
---

離散 Kantorovich 問題の目的関数にエントロピー項を加えると、最適解は一意になり、行列スケーリングで計算できる。

:::definition
### 定義: 離散エントロピー

\[
  \Hb(\mathbf{P})
  \defeq
  -\sum_{i,j}P_{ij}(\log P_{ij}-1),
  \qquad 0\log 0=0.
\]
:::

:::definition
### 定義: エントロピー正則化 OT

\[
  \mathrm{MK}_{\mathbf{C}}^{\varepsilon}(\mathbf{a},\mathbf{b})
  \defeq
  \min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \left\{
    \inner{\mathbf{C}}{\mathbf{P}}
    -\varepsilon \Hb(\mathbf{P})
  \right\}.
\]
:::

:::theorem
### 命題: 存在と一意性

任意の \(\varepsilon>0\) に対し、正則化問題は一意な最適解 \(\mathbf{P}_{\varepsilon}\) を持つ。

:::details-embedded 証明の骨格
輸送多面体は空でないコンパクト集合である。関数 \(x\mapsto x\log x-x\) は連続かつ狭義凸である。したがって目的関数は連続かつ狭義凸であり、最小値を一意に達成する。
:::
:::

:::theorem
### KL 射影としての定式化

\(K_{ij}=\exp(-C_{ij}/\varepsilon)\) とおくと、

\[
  \mathbf{P}_{\varepsilon}
  =
  \arg\min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \KLD(\mathbf{P}\Vert\mathbf{K}).
\]
:::
