---
id: justification
nav: 正則化の正当性
eyebrow: 6. Justification
title: 正則化の正当性
---

Cuturi/Peyre におけるエントロピー正則化の正当性は、非正則化 OT への極限、Sinkhorn による計算可能性、滑らかな損失関数としての微分可能性に分かれる。

:::definition
### 定義: 最大エントロピー最適解

非正則化問題

\[
  \min_{\mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})}
  \inner{\mathbf{C}}{\mathbf{P}}
\]

の最適解全体を

\[
  \mathcal{S}_0
  \defeq
  \left\{
    \mathbf{P}\in\Pi(\mathbf{a},\mathbf{b})
    \mid
    \inner{\mathbf{C}}{\mathbf{P}}
    =
    \mathrm{MK}_{\mathbf{C}}(\mathbf{a},\mathbf{b})
  \right\}
\]

とする。\(\mathcal{S}_0\) の中で \(\Hb(\mathbf{P})\) を最大にする元を最大エントロピー最適解という。
:::

:::theorem
### 定理: \(\varepsilon\to0\) 極限

\(\varepsilon\to0\) のとき、正則化解 \(\mathbf{P}_{\varepsilon}\) は[ref:最大エントロピー最適解]へ収束する。特に

\[
  \lim_{\varepsilon\to0}
  \mathrm{MK}_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
  =
  \mathrm{MK}_{\mathbf{C}}(\mathbf{a},\mathbf{b})
\]

である。

:::details-embedded 証明
非正則化問題の任意の最適解を \(\mathbf{P}\) とする。正則化解の最適性より

\[
  \inner{\mathbf{C}}{\mathbf{P}_{\varepsilon}}
  -\varepsilon\Hb(\mathbf{P}_{\varepsilon})
  \le
  \inner{\mathbf{C}}{\mathbf{P}}
  -\varepsilon\Hb(\mathbf{P})
\]

である。一方、\(\mathbf{P}\) は非正則化問題の最適解なので

\[
  0
  \le
  \inner{\mathbf{C}}{\mathbf{P}_{\varepsilon}}
  -
  \inner{\mathbf{C}}{\mathbf{P}}
  \le
  \varepsilon
  \left(
    \Hb(\mathbf{P}_{\varepsilon})-\Hb(\mathbf{P})
  \right).
\]

輸送多面体はコンパクトで、\(\Hb\) はその上で有界である。したがってコスト差は \(0\) に収束する。さらに上の不等式を \(\varepsilon\) で割って極限を取ると、極限点は非正則化最適解の中でエントロピーを最大化する。
:::
:::

:::theorem
### 定理: \(\varepsilon\to+\infty\) 極限

\[
  \mathbf{P}_{\varepsilon}\to\mathbf{a}\mathbf{b}^{\top}.
\]

ここで \((\mathbf{a}\mathbf{b}^{\top})_{ij}=a_i b_j\) である。この行列は、ソースとターゲットを独立に結合するカップリングである。
:::

:::definition
### 定義: Hilbert 射影距離

正ベクトル \(\mathbf{x},\mathbf{y}\in\R_{++}^n\) に対して、

\[
  d_H(\mathbf{x},\mathbf{y})
  \defeq
  \log
  \max_{i,j}
  \frac{x_i y_j}{x_j y_i}
\]

を Hilbert 射影距離という。\(d_H(\mathbf{x},\mathbf{y})=0\) は、\(\mathbf{x}\) と \(\mathbf{y}\) が正の定数倍で一致することを意味する。
:::

:::definition
### 定義: 縮小写像

距離空間 \((S,d)\) 上の写像 \(T:S\to S\) が、ある \(\lambda\in[0,1)\) に対して

\[
  d(Tx,Ty)\le \lambda d(x,y)
\]

をすべての \(x,y\in S\) で満たすとき、\(T\) を縮小写像という。
:::

:::theorem
### 定理: Birkhoff の縮小定理

全成分が正である行列を正行列という。正行列 \(\mathbf{K}\) によって定まる写像 \(\mathbf{x}\mapsto\mathbf{K}\mathbf{x}\) は、Hilbert 射影距離に関して縮小写像である。すなわち、ある \(\lambda\in[0,1)\) が存在して

\[
  d_H(\mathbf{K}\mathbf{x},\mathbf{K}\mathbf{y})
  \le
  \lambda d_H(\mathbf{x},\mathbf{y})
\]

が成り立つ。
:::

:::theorem
### 定理: Sinkhorn 反復の収束

\(\mathbf{K}\in\R_{++}^{n\times m}\), \(\mathbf{a}\in\R_{++}^n\), \(\mathbf{b}\in\R_{++}^m\) のとき、Sinkhorn 反復が生成する行列

\[
  \mathbf{P}^{(\ell)}
  =
  \diag(\mathbf{u}^{(\ell)})\mathbf{K}\diag(\mathbf{v}^{(\ell)})
\]

は正則化問題の一意解 \(\mathbf{P}_{\varepsilon}\) に収束する。

:::details-embedded 証明の概要
収束解析では [ref:Hilbert 射影距離]を使う。Sinkhorn 反復は正ベクトル全体 \(\R_{++}^n\), \(\R_{++}^m\) の上で [ref:Birkhoff の縮小定理]を利用するため、スケーリングベクトルは定数倍の自由度を除いて一意な極限へ収束する。
:::
:::

:::definition
### 定義: 微分可能性と勾配

関数 \(F:\R^d\to\R\) が点 \(x\) で微分可能であるとは、あるベクトル \(\nabla F(x)\in\R^d\) が存在して

\[
  F(x+h)
  =
  F(x)
  +
  \inner{\nabla F(x)}{h}
  +
  o(\|h\|)
\]

を満たすことをいう。このベクトル \(\nabla F(x)\) を \(F\) の勾配という。
:::

:::theorem
### 命題: 正則化 OT は滑らかな損失になる

\(\varepsilon>0\) のとき、\(\mathrm{MK}_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})\) は入力の周辺分布に関して微分可能である。最適な双対ポテンシャルを \((\mathbf{f}^{\star},\mathbf{g}^{\star})\) とすると、定数倍の不定性を除いて

\[
  \nabla_{\mathbf{a}}
  \mathrm{MK}_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
  =
  \mathbf{f}^{\star},
  \qquad
  \nabla_{\mathbf{b}}
  \mathrm{MK}_{\mathbf{C}}^\varepsilon(\mathbf{a},\mathbf{b})
  =
  \mathbf{g}^{\star}
\]

である。損失関数とは、最小化の対象として使う関数である。この性質により、正則化 OT は最適化や機械学習の損失関数として扱いやすい。
:::
