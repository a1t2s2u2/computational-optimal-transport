---
id: justification
nav: 正則化の正当性
eyebrow: 6. Justification
title: 正則化の正当性
---

エントロピー正則化の正当化は、一意性、計算可能性、非正則化問題への極限という三点に集約される。

:::theorem
### 定理: \(\varepsilon\to0\) 極限

\(\varepsilon_k\to0\) とし、\(\mathbf{P}_{\varepsilon_k}\) を正則化問題の解とする。任意の収束部分列の極限は非正則化 OT の最適解である。さらに

\[
  \lim_{\varepsilon\to0}
  \mathrm{MK}_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
  =
  \mathrm{MK}_{\mathbf{C}}(\mathbf{a},\mathbf{b})
\]

が成り立つ。
:::

:::theorem
### 定理: \(\varepsilon\to+\infty\) 極限

\[
  \mathbf{P}_{\varepsilon}\to\mathbf{a}\mathbf{b}^{\top}.
\]

大きな正則化では、輸送計画は独立カップリングに近づく。
:::
