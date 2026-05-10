---
id: preliminaries
nav: 準備
eyebrow: 1. Foundations
title: 準備
---

最適輸送では点を動かす写像だけでなく、点集合上の確率測度を扱う。基礎語は位相、可測性、測度、押し出し、凸性に分かれる。

:::definition
### 定義: 基本記号

\(\R\) は実数全体、\(\R_+\) は非負実数全体 \([0,\infty)\)、\(\R_{++}\) は正実数全体 \((0,\infty)\) を表す。\(\R^n\) は \(n\) 個の実数を並べたベクトル全体、\(\R^{n\times m}\) は \(n\) 行 \(m\) 列の実行列全体を表す。
:::

:::definition
### 定義: 距離空間

集合 \(\X\) と関数 \(d:\X\times\X\to\R_+\) が、すべての \(x,y,z\in\X\) について

\[
  d(x,y)=0 \Longleftrightarrow x=y,\qquad
  d(x,y)=d(y,x),\qquad
  d(x,z)\le d(x,y)+d(y,z)
\]

を満たすとき、\(d\) を距離、組 \((\X,d)\) を距離空間という。
\[
  B_r(x)\defeq\{y\in\X\mid d(x,y)<r\}
\]
を中心 \(x\)、半径 \(r\) の開球という。
:::

:::definition
### 定義: Polish 空間

距離空間 \((\X,d)\) において、任意の Cauchy 列が \(\X\) の点へ収束するとき、\(\X\) は完備であるという。ここで Cauchy 列とは、任意の \(\varepsilon>0\) に対してある \(N\) が存在し、\(k,\ell\ge N\) ならば \(d(x_k,x_\ell)<\varepsilon\) となる列である。

距離空間 \(\X\) が可算な稠密部分集合を持つとき、\(\X\) は可分であるという。可算とは、自然数で番号を付けられることをいう。部分集合 \(D\subset\X\) が稠密であるとは、任意の \(x\in\X\) と任意の \(r>0\) に対して \(B_r(x)\cap D\ne\emptyset\) となることをいう。

距離空間 \((\X,d)\) が完備かつ可分であるとき、\(\X\) を [term:Polish 空間|polish] という。
:::

:::definition
### 定義: \(\sigma\)-代数

集合 \(\X\) の部分集合族 \(\mathcal{F}\subset 2^{\X}\) が

1. \(\X\in\mathcal{F}\)
2. \(A\in\mathcal{F}\) ならば \(\X\setminus A\in\mathcal{F}\)
3. \(A_1,A_2,\ldots\in\mathcal{F}\) ならば \(\bigcup_{k=1}^{\infty}A_k\in\mathcal{F}\)

を満たすとき、\(\mathcal{F}\) を \(\sigma\)-代数という。
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
### 定義: 可測写像

集合 \(\X\) とその上の \(\sigma\)-代数 \(\mathcal{F}\) の組 \((\X,\mathcal{F})\) を可測空間という。\((\X,\mathcal{F})\), \((\Y,\mathcal{G})\) を可測空間とする。写像 \(T:\X\to\Y\) が、任意の \(B\in\mathcal{G}\) について \(T^{-1}(B)\in\mathcal{F}\) を満たすとき、\(T\) を可測写像という。
:::

:::definition
### 定義: 確率測度

\((\X,\mathcal{F})\) 上の関数 \(\alpha:\mathcal{F}\to[0,1]\) が、\(\alpha(\X)=1\) と可算加法性

\[
  \alpha\left(\bigcup_{k=1}^{\infty}A_k\right)
  =
  \sum_{k=1}^{\infty}\alpha(A_k)
\]

を互いに交わらない \(A_1,A_2,\ldots\in\mathcal{F}\) について満たすとき、\(\alpha\) を確率測度という。
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

:::definition
### 定義: 凸集合と凸関数

集合 \(S\subset\R^d\) が、任意の \(x,y\in S\), \(t\in[0,1]\) について \(tx+(1-t)y\in S\) を満たすとき、\(S\) を凸集合という。凸集合 \(S\) 上の関数 \(F:S\to\R\) が

\[
  F(tx+(1-t)y)\le tF(x)+(1-t)F(y)
\]

をすべての \(x,y\in S\), \(t\in[0,1]\) について満たすとき、\(F\) を凸関数という。不等号が \(x\ne y\), \(t\in(0,1)\) で常に狭義になるとき、\(F\) を狭義凸関数という。
:::

:::definition
### 定義: コンパクト集合

\(\R^d\) の部分集合 \(S\) がコンパクトであるとは、\(S\) の任意の点列が \(S\) 内の点へ収束する部分列を持つことをいう。
:::
