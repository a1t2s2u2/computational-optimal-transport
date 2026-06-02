---
id: geodesics
nav: 測地線
eyebrow: 7. Geodesics
title: 測地線と変位補間
---


「Wasserstein 距離」の章で，最適輸送が測度の空間に距離を定めることを見た．本章からは，その距離空間の**幾何**——とくに**測地線**——を扱う．測地線は「質量を中間点へ連続的に動かす」操作なので，地の空間を \(\R^d\) のような連続空間にとる必要がある（有限ビンの上では測地線が存在しない）．そこで本章では連続設定を最小限に導入し，最適輸送が定める測地線——**McCann の変位補間**——を構成する．途中で必要となる「最適カップリングは凸関数の勾配 \(\nabla\phi\) で与えられる」という事実（Brenier）は，証明せず補題として引用する（その役割は後の曲率の章で本質化する）．

## 連続設定と 2-Wasserstein 距離


地の空間を \(\R^d\)，地のコストを \(c(x,y) = \norm{x-y}^2\)（2 次コスト）とする．2 次モーメントが有限な確率測度の空間

\[
 \Pp_2(\R^d)
 \defeq
 \left\{
 \alpha \in \Mm_+^1(\R^d)
 \;\middle|\;
 \int_{\R^d} \norm{x}^2 \,\d\alpha(x) < \infty
 \right\}
\]

の上で議論する．

:::definition
### Def: 2-Wasserstein 距離

\(\alpha, \beta \in \Pp_2(\R^d)\) に対して，**2-Wasserstein 距離**を

\[
 \Wass_2(\alpha, \beta)
 \defeq
 \left(
 \inf_{\pi \in \Couplings(\alpha, \beta)}
 \int_{\R^d \times \R^d} \norm{x - y}^2 \,\d\pi(x, y)
 \right)^{1/2}
\]

で定める（連続 Kantorovich 問題；[ref:Def: Kantorovich 問題|Kantorovich 問題]）．
:::


:::fact
### Rem: \(\Wass_2\) は距離である

\(\Wass_2\) は \(\Pp_2(\R^d)\) 上の距離である．対称性・非退化性，および貼り合わせ補題による三角不等式の証明は，離散の場合（[ref:Thm: 離散 Wasserstein 距離の距離性|離散 Wasserstein 距離の距離性]）と同じ論法で，和を積分に，明示構成\(\mathbf{S} = \mathbf{P}\diag(1/\tilde{\mathbf{b}})\mathbf{Q}\) を分解（disintegration）による貼り合わせに置き換えればよい．また下半連続なコストに対し，\(\Pp_2(\R^d)\) 上で最適カップリングが存在する（弱位相でのコンパクト性による）．
:::


## 最適写像：Brenier の事実


測地線を写像で書くために，最適カップリングが**写像**で与えられるための事実を引用する．これは「古典 Kantorovich 双対と \(c\)-変換」の章の双対・\(c\)-変換・相補性の連続版の結実であり，証明は与えない．

:::theorem
### Clm: Brenier の定理

\(\alpha \in \Pp_2(\R^d)\) が Lebesgue 測度に関して絶対連続（密度を持つ，\(\alpha \ll \Lcal^d\)）とし，\(\beta \in \Pp_2(\R^d)\) とする．このとき \(\Wass_2(\alpha,\beta)\) を達成する最適カップリングはただ一つで，ある**凸関数** \(\phi : \R^d \to \R\) の勾配\(T = \nabla\phi\) による**写像**で与えられる：

\[
 \pi = (\Id, \nabla\phi)_\sharp \alpha,
 \qquad\text{すなわち}\qquad
 \beta = (\nabla\phi)_\sharp \alpha.
\]

この \(T = \nabla\phi\) を \(\alpha\) から \(\beta\) への**最適輸送写像**とよぶ．
:::


:::fact
### Rem: ch06 との対応

Brenier 写像が凸関数の勾配となるのは，「古典 Kantorovich 双対と \(c\)-変換」の章の構造の連続版である．2 次コストでは双対ポテンシャルの \(c\)-変換が**Legendre 変換**に対応し，相補性条件（[ref:Prop: 相補性条件|相補性条件]）\(\supp(\pi) \subseteq \{f(x)+g(y)=c(x,y)\}\) が，\(\phi(x) = \tfrac{\norm{x}^2}{2} - f(x)\) とおくと\(y \in \partial\phi(x)\)（劣微分）と書ける．\(\alpha\) が密度を持てば \(\phi\) は \(\alpha\)-ほとんど至るところ微分可能で，\(y = \nabla\phi(x)\) が一意に定まる．これが写像 \(T = \nabla\phi\) である．「凸関数の勾配」は，1 次元の単調増加関数の多次元への一般化にあたる．
:::


## 変位補間と測地線


距離空間の測地線をまず定義する．

:::definition
### Def: 定速測地線

距離空間 \((M, d_M)\) において，曲線\((\mu_t)_{t \in [0,1]}\) が端点 \(\mu_0, \mu_1\) を結ぶ**定速測地線**であるとは，任意の \(s, t \in [0,1]\) に対して

\[
 d_M(\mu_s, \mu_t) = |t - s|\, d_M(\mu_0, \mu_1)
\]

が成り立つことをいう．
:::


Brenier 写像 \(T = \nabla\phi\) に沿って質量を一定速度で動かすと，測地線が得られる．

:::definition
### Def: McCann の変位補間

\(\alpha \ll \Lcal^d\)，\(\beta \in \Pp_2(\R^d)\) とし，\(T = \nabla\phi\) を \(\alpha\) から \(\beta\) への最適輸送写像（[ref:Clm: Brenier の定理|Brenier の定理]）とする．\(t \in [0,1]\) に対し \(T_t \defeq (1-t)\Id + t\,T\) とおき，

\[
 \mu_t \defeq (T_t)_\sharp \alpha
 = \bigl((1-t)\Id + t\,\nabla\phi\bigr)_\sharp \alpha
\]

を**変位補間**とよぶ．\(\mu_0 = \alpha\)，\(\mu_1 = \beta\) である．
:::


:::theorem
### Thm: 変位補間は測地線である

変位補間 \((\mu_t)_{t \in [0,1]}\) は，\((\Pp_2(\R^d), \Wass_2)\) における\(\alpha\) と \(\beta\) を結ぶ定速測地線である：

\[
 \Wass_2(\mu_s, \mu_t) = |t - s|\, \Wass_2(\alpha, \beta)
 \qquad (\forall\, s, t \in [0,1]).
\]

:::details-embedded 証明
まず最適写像の定義より，\(\nabla\phi\) が \(\alpha\) から \(\beta\) への最適カップリングを与えるので

\[
 \Wass_2(\alpha, \beta)^2
 = \int_{\R^d} \norm{x - \nabla\phi(x)}^2 \,\d\alpha(x).
 \tag{\(\ast\)}
\]


**上界．**\(s \leq t\) とする．\((T_s, T_t)_\sharp \alpha\) は\(\mu_s = (T_s)_\sharp\alpha\) と \(\mu_t = (T_t)_\sharp\alpha\) のカップリングであるから，その劣最適性より

\[
 \Wass_2(\mu_s, \mu_t)^2
 \leq \int_{\R^d} \norm{T_s(x) - T_t(x)}^2 \,\d\alpha(x).
\]

\(T_s(x) - T_t(x) = (t - s)\bigl(x - \nabla\phi(x)\bigr)\) なので，\((\ast)\) より

\[
 \Wass_2(\mu_s, \mu_t)^2
 \leq (t - s)^2 \int_{\R^d} \norm{x - \nabla\phi(x)}^2 \,\d\alpha(x)
 = (t - s)^2\, \Wass_2(\alpha, \beta)^2,
\]

すなわち \(\Wass_2(\mu_s, \mu_t) \leq (t - s)\,\Wass_2(\alpha, \beta)\)．

**等号（測地線性）．**\(\Wass_2\) の三角不等式（備考[ref:Rem: \(\Wass_2\) は距離である|\(\Wass_2\) は距離である]）と上界より，\(0 \leq s \leq t \leq 1\) に対し

\[
 \Wass_2(\alpha, \beta)
 \leq \Wass_2(\mu_0, \mu_s) + \Wass_2(\mu_s, \mu_t) + \Wass_2(\mu_t, \mu_1)
 \leq \bigl(s + (t - s) + (1 - t)\bigr)\Wass_2(\alpha, \beta)
 = \Wass_2(\alpha, \beta).
\]

両端が等しいので途中の不等号はすべて等号でなければならず，とくに \(\Wass_2(\mu_s, \mu_t) = (t - s)\,\Wass_2(\alpha, \beta)\)．\(s, t\) の大小によらず \(|t-s|\,\Wass_2(\alpha,\beta)\) を得る．
:::
:::


:::fact
### Rem: 粒子の直線運動という描像

変位補間は，各点 \(x\) の質量を直線\(t \mapsto (1-t)x + t\,\nabla\phi(x)\) に沿って**一定速度**で動かす操作である．\(L^2\) 補間\((1-t)\alpha + t\beta\)（質量をその場で増減させる）とは異なり，\(\Wass_2\) 測地線は質量を空間的に**輸送**する点が特徴である．
:::


:::fact
### Rem: 変位凸性と曲率への布石

測地線が定まると，汎関数 \(F : \Pp_2(\R^d) \to \R\) の測地線に沿った凸性——**変位凸性**——を論じられる：\(F\) が**変位凸**とは，任意の測地線 \((\mu_t)\) に沿って\(t \mapsto F(\mu_t)\) が凸となることをいう．とくにエントロピー（自由エネルギー）汎関数の変位凸性は，\(T = \nabla\phi\) のヤコビアン \(\det(\partial^2\phi)\) の凹性（\(\phi\) が凸なので \(\partial^2\phi \succeq 0\)）から導かれ，これが Ricci 曲率下界・CD\((K,N)\) 条件と結びつく．この計算では Brenier 写像が凸関数の勾配であること（[ref:Clm: Brenier の定理|Brenier の定理]）が本質的に効く．動的定式化（Benamou--Brenier）と Otto 計算を経て，この曲率の主題へ進む．
:::
