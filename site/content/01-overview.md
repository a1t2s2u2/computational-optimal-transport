---
id: overview
nav: 全体地図
eyebrow: Seminar Map
title: 計算最適輸送セミナー
lead: 測度論的な Kantorovich 問題を有限支持測度の行列問題として扱い、線形計画、双対、エントロピー正則化、Sinkhorn 反復へ接続する。
---

矢印ラベルは概念間の関係を表す。一枚の巨大な図ではなく、基礎、離散化、Cuturi/Peyre の正則化、極限と幾何に分ける。

## 地図 1: 基礎から Kantorovich 問題

```mermaid
flowchart TB
  Metric -->|"完備性と可分性を仮定"| Polish
  Polish -->|"開集合から生成"| Borel
  Borel -->|"可測集合上に定義"| Prob
  Prob -->|"写像で測度を運ぶ"| Push
  Prob -->|"積空間上で周辺を固定"| Coupling
  Push -->|"制約 T#alpha = beta"| Monge
  Monge -->|"写像からカップリングへ緩和"| Kantorovich
  Coupling -->|"実行可能集合を与える"| Kantorovich
```

## 地図 2: 有限支持化と双対

```mermaid
flowchart TB
  Kantorovich["Kantorovich 問題"]
  DiscreteOT["離散 Kantorovich 問題"]
  MatrixPlan["行列カップリング P"]
  LP["線形計画"]
  Dual["Kantorovich 双対"]
  CTransform["C/c 変換"]
  NetworkSimplex["ネットワーク単体法"]

  Kantorovich -->|"有限支持なら厳密に一致"| DiscreteOT
  DiscreteOT -->|"カップリングを行列で表す"| MatrixPlan
  MatrixPlan -->|"行和・列和制約"| LP
  LP -->|"有限次元 LP 双対"| Dual
  Dual -->|"制約を飽和させる操作"| CTransform
  LP -->|"頂点をたどって解く"| NetworkSimplex
```

## 地図 3: Cuturi/Peyre のエントロピー正則化

```mermaid
flowchart TB
  DiscreteOT["離散 Kantorovich 問題"]
  EntropicOT["エントロピー正則化 OT"]
  Gibbs["Gibbs カーネル K"]
  KLProj["KL 射影"]
  Scaling["P = diag(u) K diag(v)"]
  Sinkhorn["Sinkhorn 反復"]
  DualAscent["双対の交互最大化"]
  LogDomain["対数領域 Sinkhorn"]

  DiscreteOT -->|"負エントロピーを加える"| EntropicOT
  EntropicOT -->|"K = exp(-C/epsilon) を使う"| Gibbs
  EntropicOT -->|"KL 最小化に書き換える"| KLProj
  Gibbs -->|"正行列をスケーリングする"| Scaling
  KLProj -->|"行制約・列制約へ交互射影"| Sinkhorn
  Scaling -->|"固定点反復として解く"| Sinkhorn
  DualAscent -->|"同じ更新式を与える"| Sinkhorn
  Sinkhorn -->|"小さい epsilon で安定化"| LogDomain
```

## 地図 4: 正則化の極限と幾何への接続

```mermaid
flowchart TB
  EntropicOT["エントロピー正則化 OT"]
  Eps0["epsilon -> 0"]
  EpsInf["epsilon -> infinity"]
  MaxEntropy["最大エントロピー OT 解"]
  Independent["独立カップリング ab^T"]
  Smooth["微分可能な損失"]
  Kantorovich["Kantorovich 問題"]
  Wp["W_p 距離"]
  Geodesic["Wasserstein 測地線"]
  Curvature["変位凸性・曲率"]

  EntropicOT -->|"正則化を消す"| Eps0
  Eps0 -->|"選ばれる極限"| MaxEntropy
  MaxEntropy -->|"非正則化問題の最適解"| Kantorovich
  EntropicOT -->|"エントロピーが支配"| EpsInf
  EpsInf -->|"収束先"| Independent
  EntropicOT -->|"双対ポテンシャルが勾配"| Smooth
  Kantorovich -->|"コストを d^p に特殊化"| Wp
  Wp -->|"距離空間として扱う"| Geodesic
  Geodesic -->|"凸性・曲率へ発展"| Curvature
```

有限と無限の行き来は、厳密な同一視と近似を分ける。

```mermaid
flowchart TB
  Continuous["連続測度 alpha, beta"]
  FiniteSupport["有限支持測度 sum a_i delta_x_i"]
  Empirical["経験測度・格子近似"]
  MatrixPlan["行列カップリング P"]
  ContinuousPlan["測度カップリング pi"]
  DiscreteProblem["有限次元 LP"]
  ContinuousProblem["測度上の Kantorovich 問題"]
  Convergence["近似誤差の収束解析"]

  Continuous -->|"最初から有限支持なら厳密同一視"| FiniteSupport
  Continuous -->|"サンプル化・格子化なら近似"| Empirical
  FiniteSupport -->|"pi = sum P_ij delta_(x_i,y_j)"| MatrixPlan
  MatrixPlan -->|"行和・列和が周辺分布"| DiscreteProblem
  Continuous -->|"積空間上の測度"| ContinuousPlan
  ContinuousPlan -->|"周辺が alpha, beta"| ContinuousProblem
  Empirical -->|"有限問題として解く"| DiscreteProblem
  DiscreteProblem -->|"元の連続問題へ戻すには必要"| Convergence
  Convergence -->|"経験測度や格子幅の極限"| ContinuousProblem
```

:::grid two
:::fact
## Cuturi/Peyre と同じ主軸

Monge/Kantorovich、離散 OT、LP、双対、エントロピー正則化、Gibbs カーネル、KL 射影、Sinkhorn という流れは Computational Optimal Transport の標準的な構成である。
:::

:::fact accent
## 幾何は別の主文脈

測地線、変位補間、曲率、勾配流は Villani、Ambrosio-Gigli-Savare、Otto 計算の文脈が強い。
:::
:::
