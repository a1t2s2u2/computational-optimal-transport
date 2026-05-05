---
id: sinkhorn
nav: Sinkhorn
eyebrow: 5. Sinkhorn
title: Sinkhorn アルゴリズム
term: sinkhorn
---

Cuturi/Peyre の Sinkhorn アルゴリズムは、Gibbs カーネルを行方向と列方向に交互にスケーリングし、指定された周辺ヒストグラムを持つ行列へ収束させる反復である。

:::definition
### 定義: 対角行列とスケーリングベクトル

ベクトル \(\mathbf{u}\in\R^n\) に対して、\(\diag(\mathbf{u})\) は対角成分が \(u_1,\ldots,u_n\)、非対角成分が \(0\) の行列である。正ベクトル \(\mathbf{u}\in\R_{++}^n\), \(\mathbf{v}\in\R_{++}^m\) を用いて

\[
  \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})
\]

と書く操作を、\(\mathbf{K}\) の行方向と列方向のスケーリングという。
:::

:::theorem
### 命題: スケーリング形式

正則化問題の最適解は、正ベクトル \(\mathbf{u}\in\R_{++}^n\), \(\mathbf{v}\in\R_{++}^m\) により

\[
  \mathbf{P}_{\varepsilon}
  =
  \diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})
\]

と表される。

:::details-embedded 証明
周辺制約を目的関数に組み込む補助変数として、ラグランジュ乗数 \(\mathbf{f}\in\R^n\), \(\mathbf{g}\in\R^m\) を導入する。最適解で偏微分が \(0\) になる条件を一階条件という。この場合の一階条件は

\[
  C_{ij}+\varepsilon\log P_{ij}-f_i-g_j=0
\]

である。したがって

\[
  P_{ij}
  =
  \exp(f_i/\varepsilon)
  \exp(-C_{ij}/\varepsilon)
  \exp(g_j/\varepsilon).
\]

\(u_i=\exp(f_i/\varepsilon)\), \(v_j=\exp(g_j/\varepsilon)\) とおけば、主張を得る。
:::
:::

:::definition
### 定義: 成分ごとの積と除算

同じ長さのベクトル \(\mathbf{x},\mathbf{y}\) に対して、

\[
  (\mathbf{x}\odot\mathbf{y})_i\defeq x_i y_i,
  \qquad
  (\mathbf{x}\oslash\mathbf{y})_i\defeq \frac{x_i}{y_i}
\]

で定まる演算を、それぞれ成分ごとの積、成分ごとの除算という。
:::

:::algorithm
### Sinkhorn 反復

\[
  \mathbf{P}=\diag(\mathbf{u})\mathbf{K}\diag(\mathbf{v})
\]

が周辺条件 \(\mathbf{P}\ones_m=\mathbf{a}\), \(\mathbf{P}^{\top}\ones_n=\mathbf{b}\) を満たすことは

\[
  \mathbf{u}\odot(\mathbf{K}\mathbf{v})=\mathbf{a},
  \qquad
  \mathbf{v}\odot(\mathbf{K}^{\top}\mathbf{u})=\mathbf{b}
\]

と同値である。したがって以下の反復を行う。

1. \(\mathbf{v}^{(0)}=\ones_m\)
2. \(\mathbf{u}^{(\ell+1)}\leftarrow\mathbf{a}\oslash(\mathbf{K}\mathbf{v}^{(\ell)})\)
3. \(\mathbf{v}^{(\ell+1)}\leftarrow\mathbf{b}\oslash(\mathbf{K}^{\top}\mathbf{u}^{(\ell+1)})\)
4. \(\mathbf{P}^{(\ell)}=\diag(\mathbf{u}^{(\ell)})\mathbf{K}\diag(\mathbf{v}^{(\ell)})\)
:::

:::definition
### 定義: KL 交互射影

二つの集合 \(S_1,S_2\) があるとき、ある点を \(S_1\) へ KL 射影し、次に \(S_2\) へ KL 射影し、この操作を繰り返す方法を KL 交互射影という。Sinkhorn 反復は、行和制約

\[
  S_{\mathrm{row}}\defeq\{\mathbf{P}\mid \mathbf{P}\ones_m=\mathbf{a}\}
\]

と列和制約

\[
  S_{\mathrm{col}}\defeq\{\mathbf{P}\mid \mathbf{P}^{\top}\ones_n=\mathbf{b}\}
\]

への KL 交互射影である。
:::

:::definition
### 定義: 正則化双対問題

関数

\[
  Q(\mathbf{f},\mathbf{g})
  \defeq
  \inner{\mathbf{f}}{\mathbf{a}}
  +\inner{\mathbf{g}}{\mathbf{b}}
  -\varepsilon
  \sum_{i,j}
  \exp\left(\frac{f_i+g_j-C_{ij}}{\varepsilon}\right)
\]

を正則化双対目的関数という。正則化双対問題とは \(Q\) を \(\mathbf{f}\in\R^n\), \(\mathbf{g}\in\R^m\) について最大化する問題である。このとき \(\mathbf{f},\mathbf{g}\) を双対ポテンシャルという。
:::

:::theorem
### 命題: Sinkhorn は双対の交互最大化である

正則化双対目的関数 \(Q(\mathbf{f},\mathbf{g})\) において、\(\mathbf{g}\) を固定して \(\mathbf{f}\) を最大化し、次に \(\mathbf{f}\) を固定して \(\mathbf{g}\) を最大化する操作は、Sinkhorn 反復と同値である。

:::details-embedded 対応
\(u_i=\exp(f_i/\varepsilon)\), \(v_j=\exp(g_j/\varepsilon)\) とおくと、双対の一階条件は

\[
  \mathbf{u}\odot(\mathbf{K}\mathbf{v})=\mathbf{a},
  \qquad
  \mathbf{v}\odot(\mathbf{K}^{\top}\mathbf{u})=\mathbf{b}.
\]

これは Sinkhorn の固定点条件である。
:::
:::

:::demo sinkhorn

:::definition
### 定義: soft-min

ベクトル \(\mathbf{z}=(z_1,\ldots,z_m)\) と \(\varepsilon>0\) に対して、

\[
  \operatorname{smin}_{\varepsilon}(\mathbf{z})
  \defeq
  -\varepsilon\log\sum_{j=1}^m e^{-z_j/\varepsilon}
\]

を soft-min という。\(\varepsilon\to0\) で \(\operatorname{smin}_{\varepsilon}(\mathbf{z})\to\min_j z_j\) である。
:::

:::definition
### 定義: 対数領域 Sinkhorn

双対ポテンシャル

\[
  f_i\defeq \varepsilon\log u_i,
  \qquad
  g_j\defeq \varepsilon\log v_j
\]

を直接更新する Sinkhorn 反復を対数領域 Sinkhorn という。更新式は

\[
  f_i
  \leftarrow
  \varepsilon\log a_i
  +
  \operatorname{smin}_{\varepsilon}(C_{i1}-g_1,\ldots,C_{im}-g_m),
\]

\[
  g_j
  \leftarrow
  \varepsilon\log b_j
  +
  \operatorname{smin}_{\varepsilon}(C_{1j}-f_1,\ldots,C_{nj}-f_n).
\]
:::

:::details 数値安定性
小さい \(\varepsilon\) では \(K_{ij}=\exp(-C_{ij}/\varepsilon)\) が計算機上で \(0\) として扱われることがある。この現象を underflow という。対数領域 Sinkhorn は、指数関数の値そのものではなく対数を用いることで underflow を避ける。
:::
