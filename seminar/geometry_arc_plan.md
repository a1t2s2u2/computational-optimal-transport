# Wasserstein 幾何アーク 設計ドキュメント（ch05–ch11）

測地線・Otto 計算・曲率（CD(K,N)）に到達するための章立て・依存関係・必要補題を整理する。
執筆は本ドキュメントに沿って段階的に行う。各章は ch01–ch04 と同じ
**定義先行・証明付きセミナー様式**（tcolorbox 定理環境、である調、Cuturi 記法準拠、未定義概念は定義）で書く。

- 既存到達点: ch01 準備 / ch02 OT 基礎（割当・Monge・Kantorovich **主問題**）/ ch03 エントロピー正則化 / ch04 正則化双対と Sinkhorn（core にスリム化済み）
- 連続側は CLAUDE.md 方針どおり $\mathcal{X},\mathcal{Y}$ を Polish 空間と仮定。
- ビルド: `seminar/tex/` で `latexmk`（uplatex→dvi→pdf, `out/`）。参考文献機構は未使用（`\cite` 不可、人名は地の文で）。

---

## 更新（2026-06-01）— 実際の章立て（決定を反映）

以下の詳細設計（ch05–ch11）は初版。**実装は次の決定で更新済み**：

- **「基本は離散」**: ch05・ch06 は**離散のみ**。連続は ch07 で最小導入。
  - ch05 Wasserstein 距離は**離散版だけ**に集約（連続 §5.3/§5.4 は削除済み）。
  - ch06 古典 Kantorovich 双対・$c$-変換は**離散**で自己完結（強双対・相補性・$c$-変換・soft $c$-変換で Sinkhorn 回収）。
- **決定B: Brenier は独立章にしない**。必要事実（最適写像 $T=\nabla\phi$、ヤコビアン $\det\partial^2\phi$）を、使う章に**インライン補題**として引用ベースで入れる。Brenier の目的は曲率（変位凸性）の計算エンジン。

**実際の章立て（ch07 以降）**:
- **ch07 測地線・McCann 変位補間**（済）: 連続 $\Wass_2$ 最小導入＋Brenier を補題引用＋測地線性を完全証明。
- **ch08 Benamou–Brenier 動的定式化**: 連続の方程式・作用最小化・$\Wass_2$ の動的特徴づけ。
- **ch09 Otto 計算・勾配流**: 形式リーマン構造・接空間 $\{\nabla\psi\}$・JKO・熱方程式＝エントロピー勾配流。
- **ch10 曲率（変位凸性・CD$(K,N)$）**: Brenier のヤコビアン事実をインラインで使い、エントロピーの変位凸性 ↔ Ricci 下界。

以下の初版設計（ch07 Brenier 独立章 等）は参考。番号は上記に読み替えること。

---

## 全体の依存グラフ

```
ch02 主問題 ─┬─────────────► ch05 Wasserstein 距離 ─────────┐
             │                                              │
             └─► ch06 古典 Kantorovich 双対・c-変換 ──► ch07 Brenier 定理
                  ▲ (ch04 の c-変換の橋を回収)                │
                                                             ▼
                                              ch08 測地線・McCann 変位補間
                                                             │
                                                             ▼
                                              ch09 Benamou–Brenier 動的定式化
                                                             │
                                                             ▼
                                              ch10 Otto 計算・勾配流
                                                             │
                                                             ▼
                                              ch11 曲率：変位凸性と CD(K,N)
```

**推奨執筆順**: ch05 → ch06 →（ここまでで Sinkhorn の c-変換の宿題も回収）→ ch07 → ch08 → ch09 → ch10 → ch11。
ch05 と ch06 は互いに独立で、どちらからでも・並行でも書ける。
**ch06 は ch04 が先送りにした「soft-min → c-変換」を回収する高レバレッジ章**であり、幾何にも Sinkhorn にも効く共通部品。

---

## 横断的に必要な連続側の準備（ch01 に無い道具）

「測地線・Otto・曲率」に進むには、ch01 の準備に無い連続側の道具をいくつか追加する必要がある。
各章の冒頭補助節として導入するか、ch01 を増補する。

| 準備項目 | 内容 | 主に必要な章 | 配置案 |
|---|---|---|---|
| **凸解析** | Legendre 変換 $\phi^*(y)=\sup_x\langle x,y\rangle-\phi(x)$、劣微分 $\partial\phi$、凸関数の a.e. 微分可能性（Rademacher） | ch07 | ch07 冒頭の補助節 |
| **測度の分解（disintegration）** | 条件付き測度・gluing の連続版構成 | ch05, ch08 | ch05 冒頭 or ch01 測度論節を増補 |
| **測度の弱収束** | $\alpha_k\rightharpoonup\alpha$、Prokhorov の定理 | ch05 | ch01 を増補（Polish の弱収束） |
| **連続の方程式（測度値・弱形式）** | $\partial_t\rho+\nabla\cdot(\rho v)=0$ の弱解、測度の流れ | ch09, ch10 | ch09 冒頭の補助節 |
| **押し出しの密度公式** | $T_\sharp$ の Jacobian、Monge–Ampère | ch07 | ch07 内（ch01 押し出しを拡張） |
| **Minkowski 不等式** | $p$ 乗ノルムの三角不等式 | ch05 | ch01 に無ければ補題で追加 |

> 方針: 重い定理（Rademacher, Prokhorov, disintegration, Benamou–Brenier の下半連続性）は **主張のみ述べて証明は文献に譲る**（ch01 が Heine–Borel 等を引用するのと同じ運用）。セミナーの主眼である「OT 由来の構成・等式」は証明する。

---

## ch05 Wasserstein 距離

- **目的・主結果**: OT が測度間の距離を定めることを示す。$p$-Wasserstein 距離
  $\mathrm{W}_p(\mathbf{a},\mathbf{b})\defeq\MKD_{\mathbf{D}^p}(\mathbf{a},\mathbf{b})^{1/p}$（離散）、
  $\mathcal{W}_p(\alpha,\beta)\defeq\MK_{d^p}(\alpha,\beta)^{1/p}$（連続）が距離の公理を満たす。
- **依存**: ch02（主問題 $\MKD,\MK$、カップリング）、ch01（距離空間、Polish）。
- **必要補題（必要補願）**:
  1. 地の距離 $\mathbf{D}$（distance matrix）/ $d$ の定義と $\mathbf{C}=\mathbf{D}^p$ の設定。
  2. **gluing lemma**: 離散は $\mathbf{S}=\mathbf{P}\diag(1/\tilde{\mathbf{b}})\mathbf{Q}\in\Couplings(\mathbf{a},\mathbf{c})$ を明示構成（$\tilde{\mathbf{b}}$ はゼロ成分回避）。連続は disintegration による貼り合わせ（主張）。
  3. **Minkowski 不等式**（三角不等式の最終段）。
  4. $\mathcal{W}_p(\delta_x,\delta_y)=d(x,y)$（weak distance の根拠）。
  5. 弱収束の定義と「$\mathcal{W}_p$ 収束 ⇔ 弱収束 + $p$ 次モーメント収束」（主張のみ、Villani）。
- **連続/離散**: 離散で完全証明 → 連続へ gluing で一般化（disintegration は主張）。
- **証明方針／割愛**: 対称性・正定値性は完全証明。三角不等式は離散完全証明＋連続は方針。弱収束同値は引用。
- **原典**: theory.tex §2.4（prop-metric-histo, prop-metric-measure, 弱収束 rem）。
- **新規マクロ**: `\Wass`(=$\mathcal{W}$), `\WassD`(=$\mathrm{W}$), `\dist`, `\distD`（**すべて予約済み**）, `\Pp`(=$\mathcal{P}_p$, 予約済み)。

## ch06 古典 Kantorovich 双対・c-変換

- **目的・主結果**: 非正則化 Kantorovich の双対
  $\MKD_{\mathbf{C}}(\mathbf{a},\mathbf{b})=\max_{(\mathbf{f},\mathbf{g})\in\PotentialsD(\mathbf{C})}\langle\mathbf{f},\mathbf{a}\rangle+\langle\mathbf{g},\mathbf{b}\rangle$、
  ハード制約 $f_i+g_j\le C_{ij}$、相補性、$c$-変換。
- **依存**: ch02（主問題）。ch04 §4.3（正則化双対との対比；ch04 の soft-min→c-変換の宿題を回収）。
- **必要補題（必要補願）**:
  1. LP 強双対（離散）— ch04 §4.3 と同じ Lagrangian 手法で $\min_{\mathbf{P}\ge0}$ を評価し $\mathbf{C}-\mathbf{f}\oplus\mathbf{g}\ge0$ を導く（自己完結に証明可能）。
  2. Kantorovich ポテンシャル、**相補性条件** $\{P^\star>0\}\subset\{f_i+g_j=C_{ij}\}$。
  3. **$c$-変換** $f^c(y)=\min_x\,c(x,y)-f(x)$、$c$-凹性、$f^{cc}$。
  4. **ch04 回収**: $\smin_\varepsilon\to\min$（$\varepsilon\to0$）で正則化双対のソフト $c$-変換が古典 $c$-変換に収束。
  5. 連続版双対 $\mathcal{R}(c)$ と sup 達成（$c=d^p$ で Lipschitz 正則性→コンパクト化）。Kantorovich–Rubinstein（$p=1$）を特例として。
- **連続/離散**: 離散は強双対＋相補性を完全証明。連続は双対等式と $c$-変換を提示、sup 達成は方針＋引用。
- **証明方針／割愛**: LP 強双対は min–max 交換で証明（離散）。連続の存在は Lipschitz 正則性経由で方針。
- **原典**: theory.tex §2.5（prop-duality-discr, eq-mk-pd-rel, 連続双対 rem, c-変換）。
- **新規マクロ**: `\Potentials`(=$\mathcal{R}$), `\PotentialsD`(=$\mathbf{R}$)（**予約済み**）, `\smin`（予約済み・再利用）。$f\oplus g$ 用に `\oplus` はそのまま。

## ch07 Brenier 定理

- **目的・主結果**: $\mathcal{X}=\mathcal{Y}=\mathbb{R}^d$, $c(x,y)=\|x-y\|^2$, $\alpha\ll\mathrm{Leb}$ ならば、最適カップリングは Monge 写像 $T=\nabla\phi$（$\phi$ 凸）に台を持ち一意。Monge=Kantorovich の一致（緩和のタイト性）。
- **依存**: ch06（双対・$c$-変換・相補性）、ch05（$\mathcal{W}_2$）、ch02（Monge/Kantorovich）、**凸解析の準備**。
- **必要補題（必要補願）**:
  1. $\int c\,d\pi$ を $\langle x,y\rangle$ 最大化へ帰着（$C_{\alpha,\beta}$ 定数項の分離）。
  2. Legendre 変換 $\psi=\phi^*$ への双対の書き換え、$\phi(x)=\tfrac{\|x\|^2}{2}-f(x)$。
  3. 凸関数の a.e. 微分可能性（**Rademacher**、引用）、$\alpha\ll\mathrm{Leb}$ で $\alpha$-a.e. 一意。
  4. 相補性 $\Rightarrow y\in\partial\phi(x)$、$T=\nabla\phi$。
  5. （任意）Monge–Ampère 方程式 $\det(\partial^2\phi)\,\rho_\beta(\nabla\phi)=\rho_\alpha$。
- **連続/離散**: 連続のみ（$\mathbb{R}^d$）。
- **証明方針／割愛**: Cuturi の sketch ベースで主要段を提示。Rademacher・劣微分の細部は引用（Santambrogio）。
- **原典**: theory.tex §2.5（rem-exist-mongemap：Brenier、rem:MA：Monge–Ampère）。
- **新規マクロ**: 凸解析用に追加（例 `\Leg`=Legendre, `\subdiff`=$\partial$）。$\nabla\phi$ は標準。

## ch08 測地線・McCann 変位補間

- **目的・主結果**: $(\mathcal{P}_2(\mathbb{R}^d),\mathcal{W}_2)$ の定速測地線を構成。変位補間
  $\mu_t=((1-t)\,\mathrm{Id}+t\,T)_\sharp\alpha$（$T=\nabla\phi$）が一意の定速測地線。
- **依存**: ch07（Brenier $T=\nabla\phi$）、ch05（$\mathcal{W}_2$ 距離）。
- **必要補題（必要補願）**:
  1. 一般距離空間の**定速測地線**の定義 $\mathcal{W}_2(\mu_s,\mu_t)=|t-s|\,\mathcal{W}_2(\mu_0,\mu_1)$。
  2. 変位補間の**上界**（補間カップリングの劣最適性）と、三角不等式からの**等号**で測地線性を確立。
  3. 一意性（Brenier 一意性から）。
  4. **変位凸性**（汎関数 $t\mapsto F(\mu_t)$ の凸性）の定義 — ch11 への布石。
- **連続/離散**: 連続（$\mathbb{R}^d$）。離散点群の例も可。
- **証明方針／割愛**: 測地線性は完全証明可能（上界＋三角不等式）。一般 Polish 空間での測地線の存在は引用。
- **原典**: McCann（1997）、Santambrogio Ch.5–7、Villani(2009) Part I。
- **新規マクロ**: 変位補間記号（例 $\mu_t$、$\mathrm{Id}$ は予約済み `\Id`）。

## ch09 Benamou–Brenier 動的定式化

- **目的・主結果**: 動的定式化
  $\mathcal{W}_2^2(\alpha,\beta)=\inf\{\int_0^1\!\!\int\|v_t\|^2 d\rho_t\,dt : \partial_t\rho+\nabla\cdot(\rho v)=0,\ \rho_0=\alpha,\rho_1=\beta\}$。
  Otto 計量の土台。
- **依存**: ch08（測地線）、ch05、**連続の方程式の準備**。
- **必要補題（必要補願）**:
  1. **連続の方程式**（測度値・弱形式）の定義。
  2. 運動量 $m=\rho v$ による**凸化**（作用汎関数を $(\rho,m)$ の凸問題に）。
  3. 最小作用曲線 = 測地線（変位補間が最小化解）。
  4. 下限達成と $\mathcal{W}_2$ 一致（Benamou–Brenier 定理、主張＋方針）。
- **連続/離散**: 連続。離散はスタッガード格子（dynamic.tex §3.2、任意）。
- **証明方針／割愛**: 連続側の下半連続性・存在は重いので**主張＋方針＋引用**（dynamic.tex, AGS）。測地線との対応は形式計算で提示。
- **原典**: dynamic.tex §3.1（Continuous Formulation）。
- **新規マクロ**: 速度場 $v$、運動量 $m$、連続の方程式・作用汎関数の記号。

## ch10 Otto 計算・勾配流

- **目的・主結果**: $\mathcal{P}_2$ の形式的リーマン構造（**Otto 計量**）。接空間
  $T_\rho\mathcal{P}_2=\overline{\{\nabla\psi\}}$、勾配流（minimizing movement / **JKO スキーム**）、
  熱方程式＝相対エントロピーの $\mathcal{W}_2$ 勾配流。
- **依存**: ch09（Benamou–Brenier が計量の土台）、ch05。
- **必要補題（必要補願）**:
  1. Otto 計量の定義（連続の方程式の水平リフト）と**接空間の特徴づけ**（Helmholtz 分解）。
  2. **JKO スキーム** $\rho^{k+1}=\argmin_\rho\frac{1}{2\tau}\mathcal{W}_2^2(\rho,\rho^k)+F(\rho)$。
  3. 主結果: **熱方程式 = 相対エントロピー $\mathrm{Hm}$ の勾配流**。
- **連続/離散**: 連続（形式的）。
- **証明方針／割愛**: 形式的リーマン幾何として提示。厳密化（AGS の枠組み）と JKO 収束は引用。
- **原典**: Otto（2001）、JKO（1998）、AGS。dynamic.tex の周辺。
- **新規マクロ**: `\Tan`(=接空間, **予約済み**), `\Hm`(=相対エントロピー, **予約済み**)。

## ch11 曲率：変位凸性と CD(K,N)

- **目的・主結果**: **Ricci 曲率下界 ↔ エントロピーの変位凸性**（Lott–Sturm–Villani）。
  測度距離空間の synthetic Ricci 条件 **CD(K,N)** の定義と例。
- **依存**: ch08（変位補間）、ch10（エントロピー・勾配流）、ch05。
- **必要補題（必要補願）**:
  1. 相対エントロピー $\mathrm{Hm}(\rho\,|\,\mathrm{vol})$、Rényi エントロピー汎関数。
  2. **$\lambda$-変位凸性**（測地線に沿う凸性）の定義。
  3. Bakry–Émery / LSV: リーマン多様体で $\mathrm{Ric}\ge K$ ⟺ エントロピーが $K$-変位凸（主張）。
  4. **CD(K,N) 条件**（測度距離空間）の定義。
  5. 例: $\mathbb{R}^d$（$K=0$）、球面、Gauss 測度。
- **連続/離散**: 連続（多様体・測度距離空間）。
- **証明方針／割愛**: 非常に高度。**定義・主張・例を中心**に、証明は最小限＋引用（Villani(2009) Part III、AGS、Sturm、Lott–Villani）。
- **原典**: Villani "Optimal Transport: Old and New"、Lott–Villani、Sturm。
- **新規マクロ**: `\Ric`(=Ricci, **予約済み**), `\CD`(=CD(K,N), **予約済み**), `\Hm`(予約済み)。

---

## マクロの所在（予約済み一覧）

preamble に予約済みで本アークで活用するもの:
`\Wass`,`\WassD`（Wasserstein）, `\dist`,`\distD`（地の距離）, `\Pp`(=$\mathcal{P}_p$),
`\Ric`,`\CD`,`\Tan`,`\Hm`（幾何・曲率）, `\smin`(c-変換のソフト版), `\Potentials`,`\PotentialsD`（双対）, `\dHil`（Hilbert 計量, ch04 で使用中）, `\Id`,`\diag`,`\pushforward`。

新規に追加が要るもの（章執筆時）: 凸解析（Legendre・劣微分）、連続の方程式・速度場・運動量、変位補間の記号。

## スコープ調整メモ

- **章の併合余地**: ch06–ch07（双対＋Brenier）や ch09–ch10（動的＋Otto）は、分量次第で各 1 章に併合可能。まずは ch05・ch06 を独立章として確定するのが堅実。
- **最小到達経路**: 「測地線まで」なら ch05→ch06→ch07→ch08 の 4 章で到達。Otto・曲率（ch09–ch11）はその先の発展。
- **Sinkhorn との関係**: ch06 を書くと ch04 の「$c$-変換は後章で扱う」前方参照が回収され、双対の全体像（ハード制約 ↔ ソフト化）が完結する。
