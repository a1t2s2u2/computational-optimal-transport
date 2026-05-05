---
id: entropic
nav: エントロピー正則化
eyebrow: 4. Entropic Regularization
title: エントロピー正則化
term: entropy
---

Cuturi/Peyre におけるエントロピー正則化は、離散 Kantorovich 問題に負エントロピーを加え、最適化問題の解を一意にする操作である。正則化された問題の解は Gibbs カーネルの KL 射影として表される。

以下、\(\mathbf{a}\in\R_{++}^n\), \(\mathbf{b}\in\R_{++}^m\), \(\sum_i a_i=\sum_j b_j=1\) および \(\mathbf{C}\in\R_+^{n\times m}\) を固定する。

:::definition
### 定義: 離散エントロピー

非負行列 \(\mathbf{P}\in\R_+^{n\times m}\) に対して、[term:離散エントロピー|entropy]を

\[
  \Hb(\mathbf{P})
  \defeq
  -\sum_{i,j}P_{ij}(\log P_{ij}-1)
\]

で定める。ただし \(0\log 0=0\) と約束する。通常の Shannon エントロピー \(-\sum_{i,j}P_{ij}\log P_{ij}\) とは、確率行列上では定数 \(1\) だけ異なる。
:::

:::definition
### 定義: エントロピー正則化された離散 OT

正則化パラメータ \(\varepsilon>0\) に対して、エントロピー正則化された離散 Kantorovich 問題を

\[
  \mathrm{MK}_{\mathbf{C}}^{\varepsilon}(\mathbf{a},\mathbf{b})
  \defeq
  \min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \left\{
    \inner{\mathbf{C}}{\mathbf{P}}
    -\varepsilon \Hb(\mathbf{P})
  \right\}
\]

で定める。ここで \(\varepsilon\) は線形コストとエントロピー項の相対的な重みである。
:::

:::definition
### 定義: 強凸性

凸集合 \(S\subset\R^d\) 上の関数 \(F:S\to\R\) が、ある \(\lambda>0\) に対して

\[
  F(tx+(1-t)y)
  \le
  tF(x)+(1-t)F(y)-\frac{\lambda}{2}t(1-t)\|x-y\|^2
\]

をすべての \(x,y\in S\), \(t\in[0,1]\) で満たすとき、\(F\) を \(\lambda\)-強凸という。強凸関数の最小解は高々一つである。
:::

:::theorem
### 命題: 存在と一意性

任意の \(\varepsilon>0\) に対し、エントロピー正則化問題は一意な最適解 \(\mathbf{P}_{\varepsilon}\) を持つ。

:::details-embedded 証明
輸送多面体 \(\Pi(\mathbf{a},\mathbf{b})\) は空でないコンパクト集合である。関数 \(x\mapsto x\log x-x\) は \([0,\infty)\) 上で連続であり、\((0,\infty)\) 上で狭義凸である。したがって目的関数

\[
  \mathbf{P}\mapsto
  \inner{\mathbf{C}}{\mathbf{P}}
  +\varepsilon\sum_{i,j}P_{ij}(\log P_{ij}-1)
\]

はコンパクト集合上で最小値を達成する。さらに負エントロピー項が凸性を強めるため、最小解は一意である。
:::
:::

:::definition
### 定義: KL ダイバージェンス

非負行列 \(\mathbf{P},\mathbf{K}\in\R_+^{n\times m}\) に対して、[term:KL ダイバージェンス|kl]を

\[
  \KLD(\mathbf{P}\Vert\mathbf{K})
  \defeq
  \sum_{i,j}
  \left(
    P_{ij}\log\frac{P_{ij}}{K_{ij}}
    -P_{ij}
    +K_{ij}
  \right)
\]

で定める。ただし \(0\log0=0\) とし、\(P_{ij}>0\) かつ \(K_{ij}=0\) となる成分がある場合は \(+\infty\) とする。
:::

:::definition
### 定義: Gibbs カーネル

コスト行列 \(\mathbf{C}\) と \(\varepsilon>0\) に対して、[term:Gibbs カーネル|gibbs]を

\[
  K_{ij}\defeq \exp\left(-\frac{C_{ij}}{\varepsilon}\right)
\]

で定める。コストが大きい成分ほど \(K_{ij}\) は小さい。
:::

:::definition
### 定義: KL 射影

集合 \(S\subset\R_+^{n\times m}\) と正行列 \(\mathbf{K}\) に対して、

\[
  \operatorname{Proj}^{\KLD}_{S}(\mathbf{K})
  \defeq
  \arg\min_{\mathbf{P}\in S}\KLD(\mathbf{P}\Vert\mathbf{K})
\]

を \(\mathbf{K}\) の \(S\) への KL 射影という。
:::

:::theorem
### 命題: 正則化 OT は KL 射影である

\(\mathbf{K}=\exp(-\mathbf{C}/\varepsilon)\) とすると、

\[
  \mathbf{P}_{\varepsilon}
  =
  \operatorname{Proj}^{\KLD}_{\Pi(\mathbf{a},\mathbf{b})}(\mathbf{K})
  =
  \arg\min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \KLD(\mathbf{P}\Vert\mathbf{K})
\]

である。

:::details-embedded 証明
\(\log K_{ij}=-C_{ij}/\varepsilon\) より、

\[
  \varepsilon\KLD(\mathbf{P}\Vert\mathbf{K})
  =
  \inner{\mathbf{C}}{\mathbf{P}}
  -\varepsilon\Hb(\mathbf{P})
  +\varepsilon\sum_{i,j}K_{ij}.
\]

最後の項は \(\mathbf{P}\) に依存しない。したがって二つの最小化問題は同じ最適解を持つ。
:::
:::
