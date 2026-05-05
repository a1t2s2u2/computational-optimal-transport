---
id: preliminaries
nav: 準備
eyebrow: 1. Foundations
title: 準備
---

最適輸送では点を動かす写像だけでなく、点集合上の確率測度を扱う。基礎語は位相、可測性、測度、押し出し、凸性に分かれる。

:::definition
### 定義: Polish 空間

距離空間 \((\X,d)\) が完備かつ可分であるとき、\(\X\) を [term:Polish 空間|polish] という。
:::

:::definition
### 定義: Borel \(\sigma\)-代数

距離 \(d\) が定める開集合全体を \(\mathcal{O}_d\) とする。

\[
  \Bb(\X) \defeq \sigma(\mathcal{O}_d)
\]

を \(\X\) 上の Borel \(\sigma\)-代数という。
:::

:::definition
### 定義: 押し出し

可測写像 \(T:\X\to\Y\) と確率測度 \(\alpha\in\Mm_+^1(\X)\) に対し、

\[
  (T_{\#}\alpha)(B) \defeq \alpha(T^{-1}(B))
  \qquad (B\in\Bb(\Y))
\]

で定まる測度 \(T_{\#}\alpha\) を \(\alpha\) の押し出しという。
:::

:::details 有限支持測度
点 \(x_1,\ldots,x_n\in\X\) と重み \(a_i\ge 0\), \(\sum_i a_i=1\) により

\[
  \alpha = \sum_{i=1}^n a_i\delta_{x_i}
\]

と書ける確率測度を有限支持測度という。離散 OT はこの場合の Kantorovich 問題そのものであり、単なる近似ではない。
:::
