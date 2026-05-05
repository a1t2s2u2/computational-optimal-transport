---
id: overview
nav: 全体地図
eyebrow: Seminar Map
title: 計算最適輸送セミナー
lead: 測度論的な Kantorovich 問題を有限支持測度の行列問題として扱い、線形計画、双対、エントロピー正則化、Sinkhorn 反復へ接続する。
---

```mermaid
flowchart TD
  Set["集合・写像"] --> Top["位相空間"]
  Top --> Metric["距離空間"]
  Metric --> Polish["Polish 空間"]
  Top --> Borel["Borel sigma 代数"]
  Borel --> Measure["測度・確率測度"]
  Measure --> Integral["積分"]
  Measure --> Dirac["Dirac 測度"]
  Measure --> Push["押し出し"]
  Dirac --> DiscreteMeasure["有限支持測度"]
  Push --> Monge["Monge 問題"]
  Measure --> Coupling["カップリング"]
  Monge --> Kantorovich["Kantorovich 緩和"]
  Coupling --> Kantorovich
  DiscreteMeasure --> MatrixCoupling["行列カップリング P"]
  MatrixCoupling --> DiscreteOT["離散 Kantorovich 問題"]
  Kantorovich --> DiscreteOT
  DiscreteOT --> LP["線形計画標準形"]
  LP --> Dual["Kantorovich 双対"]
  Dual --> CTransform["C/c 変換"]
  LP --> Polytope["輸送多面体"]
  Polytope --> NetworkSimplex["ネットワーク単体法"]
  DiscreteOT --> Entropic["エントロピー正則化"]
  Entropic --> KL["KL 射影"]
  Entropic --> Gibbs["Gibbs カーネル"]
  KL --> Scaling["P = diag(u) K diag(v)"]
  Gibbs --> Scaling
  Scaling --> Sinkhorn["Sinkhorn 反復"]
  Sinkhorn --> LogDomain["対数領域 Sinkhorn"]
  Entropic --> Eps0["epsilon -> 0: 非正則化 OT"]
  Entropic --> EpsInf["epsilon -> infinity: 独立カップリング"]
  Kantorovich --> Wp["W_p 距離"]
  Wp --> Geodesic["Wasserstein 測地線"]
  Geodesic --> Curvature["変位凸性・曲率"]
```

:::grid two
:::fact
## Cuturi/Peyre と同じ主軸

Monge/Kantorovich、離散 OT、LP、双対、エントロピー正則化、Sinkhorn という流れは Computational Optimal Transport の標準的な構成である。
:::

:::fact accent
## 幾何は別の主文脈

測地線、変位補間、曲率、勾配流は Villani、Ambrosio-Gigli-Savare、Otto 計算の文脈が強い。
:::
:::
