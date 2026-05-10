---
id: geometry
nav: Wasserstein 幾何
eyebrow: Geometry
title: Wasserstein 幾何への接続
---

コストを距離の \(p\) 乗に固定すると、Kantorovich 最適値は \(p\)-Wasserstein 距離を定める。

:::definition
### 定義: \(W_p\)

\[
  W_p(\alpha,\beta)
  =
  \left(
    \inf_{\pi\in\Couplings(\alpha,\beta)}
    \int_{\X\times\X} d(x,y)^p\,d\pi(x,y)
  \right)^{1/p}.
\]
:::

:::compare
:::column
### Cuturi/Peyre 側

計算可能な OT、Sinkhorn、近似、統計、応用が中心である。
:::

:::column
### Villani/AGS 側

測地線、変位補間、変位凸性、勾配流、曲率が中心である。
:::
:::
