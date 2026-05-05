---
id: monge-kantorovich
nav: Monge と Kantorovich
eyebrow: 2. OT Foundations
title: Monge 問題と Kantorovich 緩和
---

:::definition
### 定義: Monge 問題

\(\alpha\in\Mm_+^1(\X)\), \(\beta\in\Mm_+^1(\Y)\)、コスト \(c:\X\times\Y\to[0,\infty]\) に対して、

\[
  \inf_{T_{\#}\alpha=\beta}
  \int_{\X} c(x,T(x))\,d\alpha(x)
\]

を Monge 問題という。
:::

:::definition
### 定義: カップリング

\(\X\times\Y\) 上の確率測度 \(\pi\) が第一周辺 \(\alpha\)、第二周辺 \(\beta\) を持つとき、\(\pi\) を \(\alpha\) と \(\beta\) の [term:カップリング|coupling] という。全体を \(\Couplings(\alpha,\beta)\) と書く。
:::

:::theorem
### 定義: Kantorovich 問題

\[
  \mathrm{MK}_c(\alpha,\beta)
  \defeq
  \inf_{\pi\in\Couplings(\alpha,\beta)}
  \int_{\X\times\Y} c(x,y)\,d\pi(x,y).
\]

Monge 問題が写像を未知量にするのに対し、Kantorovich 問題はカップリングを未知量にする。
:::

:::details Monge から Kantorovich への埋め込み
\(T_{\#}\alpha=\beta\) を満たす Monge 写像 \(T\) があれば、\((\mathrm{id},T)_{\#}\alpha\) は \(\Couplings(\alpha,\beta)\) の元である。したがって Kantorovich 問題は Monge 問題を含む。
:::
