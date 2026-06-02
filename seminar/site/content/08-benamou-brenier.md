---
id: benamou-brenier
nav: 動的定式化
eyebrow: 8. Dynamic Formulation
title: 動的定式化：Benamou–Brenier
---


「測地線と変位補間」の章では，最適輸送写像 \(T=\nabla\phi\) に沿って
質量を一定速度で動かす**変位補間**が，\((\Pp_2(\R^d),\Wass_2)\) の測地線を
与えることを見た．本章では同じ測地線を，写像ではなく**流れ**として
捉え直す．すなわち各時刻の質量分布 \(\rho_t\) と速度場 \(v_t\) の対 \((\rho_t,v_t)\) を
未知関数とし，\(\Wass_2^2\) を
「端点をつなぐ流れの**運動エネルギー**の最小値」として特徴づける．
これが Benamou と Brenier による**動的定式化**である．

この視点には二つの利点がある．第一に，静的な Kantorovich 問題（質量の対応づけ）
では見えにくい**時間発展**が前面に出る．第二に，最小化すべき作用が
\(\Wass_2\) そのものを定義に含まないため，\(\Wass_2\) を
**偏微分方程式の制約つき最適化**として計算・離散化できる．
さらに本章で得る「測地線は最小作用の流れである」という描像は，
次章 Otto 計算で \(\Pp_2\) を形式的なリーマン多様体とみなす際の土台となり，
章末では生成モデル（Flow Matching）への橋渡しにも用いる．

## 連続の方程式


質量を時間とともに動かす「流れ」を，質量保存則のもとで定式化する．
直観的には，密度 \(\rho_t\) が速度場 \(v_t\) に乗って運ばれるとき，
湧き出しも吸い込みもなければ，各領域の質量変化は境界を通る流束で決まる．
これを測度値の弱形式で述べる．

:::definition
### Def: 連続の方程式

時間に依存する確率測度の族 \((\rho_t)_{t\in[0,1]} \subset \Pp_2(\R^d)\) と
ベクトル場の族 \((v_t)_{t\in[0,1]}\)（各 \(v_t : \R^d \to \R^d\)，
\(\int_0^1\!\int \norm{v_t}^2\,\d\rho_t\,\d t < \infty\)）の対が
**連続の方程式**

\[
 \partial_t \rho_t + \diverg(\rho_t v_t) = 0,
 \qquad t \in [0,1]
\]

を満たすとは，任意の試験関数 \(\xi \in \Cc_c^\infty(\R^d)\) に対して

\[
 \frac{\d}{\d t} \int_{\R^d} \xi\,\d\rho_t
 = \int_{\R^d} \inner{\nabla\xi(x)}{v_t(x)} \,\d\rho_t(x)
\]

が（\(t\) について分布の意味で）成り立つことをいう．
:::


:::fact
### Rem: 弱形式の意味

上の弱形式は，発散定理（部分積分）
\(\int \xi\,\diverg(\rho v) = -\int \inner{\nabla\xi}{v}\,\rho\) を，
\(\rho_t\) が密度を持たない場合まで含めて成り立たせるための定式化である．
試験関数 \(\xi\) に対して「観測量 \(\int\xi\,\d\rho_t\) の時間変化が
流束 \(\rho_t v_t\) で説明できる」ことを要求している．
\(\xi \equiv 1\) を（コンパクト台で近似して）代入すると右辺は \(0\) となり，
全質量 \(\int \d\rho_t = 1\) が保存される．
:::


連続側の議論では，「測地線と変位補間」の章の備考[ref:Rem: \(\Wass_2\) は距離である|\(\Wass_2\) は距離である]で
触れた測度の**分解**と**弱コンパクト性**を繰り返し用いる．
これらは測度論の重い定理であり，本セミナーでは主張のみを引用する．

:::theorem
### Clm: 分解と弱コンパクト性

\((1)\)（分解，disintegration）
\(\pi \in \Couplings(\alpha,\beta)\) は，第一周辺 \(\alpha\) に関する
条件付き測度の族 \((\pi_x)_{x}\) により
\(\d\pi(x,y) = \d\pi_x(y)\,\d\alpha(x)\) と一意に分解される．
\((2)\)（弱コンパクト性）
2 次モーメントが一様に有界な \(\Pp_2(\R^d)\) の部分集合は，
測度の弱収束 \(\rho_k \rightharpoonup \rho\)
（\(\int \xi\,\d\rho_k \to \int \xi\,\d\rho\)，\(\forall \xi \in \Cc_b(\R^d)\)）
の位相で相対コンパクトである（Prokhorov の定理）．
下半連続なコストに対し，これにより最適カップリングおよび
後述の最小作用の流れの存在が保証される．
:::


## 動的定式化と運動エネルギー


端点 \(\alpha,\beta\) をつなぐ流れの**運動エネルギー**を最小化する問題を立てる．

:::definition
### Def: Benamou--Brenier 作用（非凸形式）

\(\alpha,\beta \in \Pp_2(\R^d)\) に対し，連続の方程式を満たし
端点条件 \(\rho_0=\alpha\)，\(\rho_1=\beta\) をもつ流れ \((\rho_t,v_t)\) 全体を
\(\mathrm{CE}(\alpha,\beta)\) と書く．流れの**作用**（運動エネルギーの時間積分）を

\[
 \mathcal{A}(\rho,v)
 \defeq
 \int_0^1 \!\! \int_{\R^d} \norm{v_t(x)}^2 \,\d\rho_t(x)\,\d t
\]

と定め，動的最適輸送問題を

\[
 \mathcal{B}(\alpha,\beta)
 \defeq
 \inf_{(\rho,v)\,\in\,\mathrm{CE}(\alpha,\beta)} \mathcal{A}(\rho,v)
\]

で定める．
:::


:::fact
### Rem: なぜ運動エネルギーか

各粒子が時刻 \(t\) に速度 \(v_t\) をもつとき，
\(\int_0^1 \norm{v_t}^2\,\d t\) はその軌道の
**エネルギー**（長さの 2 乗のスケール）である．
Cauchy--Schwarz より，端点を固定した軌道のなかでエネルギーを最小にするのは
**等速直線運動**であり，その値は移動距離の 2 乗に等しい．
\(\mathcal{A}\) はこれを質量について平均したものなので，
\(\mathcal{B}(\alpha,\beta)\) が \(\Wass_2^2(\alpha,\beta)\) に一致することが期待される
（[ref:Thm: Benamou--Brenier|Benamou--Brenier]）．
:::


問題[ref:Def: Benamou--Brenier 作用（非凸形式）|Benamou--Brenier 作用（非凸形式）]は，被積分量 \(\norm{v_t}^2\rho_t\) が
\((\rho,v)\) について**凸でない**（積 \(\rho v\) を含む）という難点をもつ．
そこで変数を取り替えて凸化する．

## 運動量による凸化


速度 \(v_t\) の代わりに**運動量** \(m_t \defeq \rho_t v_t\) を未知関数にとる．
連続の方程式は \(m\) について線形
\(\partial_t \rho_t + \diverg(m_t) = 0\) となり，
運動エネルギー密度は
\(\norm{v_t}^2 \rho_t = \norm{m_t}^2/\rho_t\) と書ける．
そこで次の関数を導入する．

:::definition
### Def: 運動エネルギー密度関数

\(\theta : \R \times \R^d \to \R \cup \{+\infty\}\) を

\[
 \theta(a,b) \defeq
 \begin{cases}
 \dfrac{\norm{b}^2}{a}, & a > 0, \\[2mm]
 0, & (a,b) = (0,\mathbf{0}), \\[1mm]
 +\infty, & \text{それ以外（\(a\le 0\) かつ \((a,b)\neq(0,\mathbf 0)\)）}
 \end{cases}
\]

で定める．
:::


:::theorem
### Prop: \(\theta\) は凸かつ下半連続

\(\theta\) は次の**支持関数表現**をもつ：

\[
 \theta(a,b)
 = \sup\Bigl\{\, p\,a + \inner{q}{b} \;\Bigm|\;
 (p,q)\in\R\times\R^d,\ \ p + \tfrac14\norm{q}^2 \le 0 \,\Bigr\}.
\]

右辺はアフィン関数 \((a,b)\mapsto pa+\inner{q}{b}\) の上限であるから，
\(\theta\) は凸かつ下半連続であり，また 1 次同次
（\(\theta(\lambda a,\lambda b)=\lambda\,\theta(a,b)\)，\(\lambda>0\)）である．

:::details-embedded 証明
\(K\defeq\{(p,q): p+\tfrac14\norm{q}^2\le 0\}\) とおき，
右辺を \(\theta^\circ(a,b)\defeq\sup_{(p,q)\in K}(pa+\inner{q}{b})\) と書く．
各 \((p,q)\) に対して \((a,b)\mapsto pa+\inner{q}{b}\) はアフィンなので，
その上限 \(\theta^\circ\) は凸かつ下半連続である．
\(\theta=\theta^\circ\) を示す．

**\(a>0\) のとき．** \(q\) を固定すると，\(K\) の制約 \(p\le-\tfrac14\norm{q}^2\) と
\(a>0\) より最適な \(p\) は \(p=-\tfrac14\norm{q}^2\)．このとき
\(\theta^\circ(a,b)=\sup_q\bigl(-\tfrac14\norm{q}^2 a+\inner{q}{b}\bigr)\) で，
\(q\) について微分して \(-\tfrac12 a\,q+b=0\)，すなわち \(q=2b/a\)．
代入すると \(-\tfrac14\norm{2b/a}^2 a+\inner{2b/a}{b} =-\norm{b}^2/a+2\norm{b}^2/a=\norm{b}^2/a=\theta(a,b)\)．

**\((a,b)=(0,\mathbf 0)\) のとき．** 任意の \((p,q)\in K\) で \(pa+\inner qb=0\)，
ゆえ \(\theta^\circ=0=\theta\)．

**\(a\le0\) かつ \((a,b)\neq(0,\mathbf0)\) のとき．** \(a<0\) ならば
\(p\to-\infty\)（\(q=\mathbf0\)）で \(pa\to+\infty\)．\(a=0\) かつ \(b\neq\mathbf0\) ならば
\(q=tb\)（\(t\to+\infty\)，\(p=-\tfrac14 t^2\norm b^2\)）で
\(pa+\inner qb=t\norm b^2\to+\infty\)．いずれも \(\theta^\circ=+\infty=\theta\)．
1 次同次性は定義から直ちに従う．
:::
:::


凸化された問題は次のように書ける．

:::definition
### Def: Benamou--Brenier 問題（凸形式）

\(\alpha,\beta\in\Pp_2(\R^d)\) に対し，
\(\partial_t\rho_t+\diverg(m_t)=0\)，\(\rho_0=\alpha\)，\(\rho_1=\beta\) を満たす
対 \((\rho,m)\) 全体のうえで

\[
 \widetilde{\mathcal{B}}(\alpha,\beta)
 \defeq
 \inf_{(\rho,m)}
 \int_0^1\!\!\int_{\R^d} \theta\bigl(\rho_t(x),\,m_t(x)\bigr)\,\d x\,\d t .
\]

制約は \((\rho,m)\) について線形，被積分関数 \(\theta\) は凸なので，
これは**凸最適化問題**である．
\(m_t=\rho_t v_t\) の対応により
\(\widetilde{\mathcal{B}}(\alpha,\beta)=\mathcal{B}(\alpha,\beta)\) である．
:::


## Benamou--Brenier の定理


動的問題の最小値が静的な \(\Wass_2^2\) に一致し，
その最小化解が前章の測地線（変位補間）であることを述べる．

:::theorem
### Thm: Benamou--Brenier

\(\alpha,\beta\in\Pp_2(\R^d)\) に対し，

\[
 \Wass_2^2(\alpha,\beta)
 = \mathcal{B}(\alpha,\beta)
 = \inf_{(\rho,v)\in\mathrm{CE}(\alpha,\beta)}
 \int_0^1\!\!\int_{\R^d}\norm{v_t}^2\,\d\rho_t\,\d t .
\]

さらに \(\alpha\ll\Lcal^d\) のとき，下限は
変位補間（[ref:Def: McCann の変位補間|McCann の変位補間]）
\(\mu_t=\bigl((1-t)\Id+t\nabla\phi\bigr)_\sharp\alpha\) と，
それを運ぶ速度場により達成される．
:::


最小値の達成（下半連続性と存在）は[ref:Clm: 分解と弱コンパクト性|分解と弱コンパクト性]の
弱コンパクト性に依拠する解析的事実であり，証明は文献に譲る．
ここでは等式の二つの向きを与え，とくに測地線が最小化解であることを
形式計算で確認する．

:::theorem
### Clm: 下限の達成

作用 \(\mathcal{A}\) は弱収束に関して下半連続であり，
\(\mathrm{CE}(\alpha,\beta)\) 上で最小化解が存在する．

:::details-embedded 証明
**\(\Wass_2^2\ge\mathcal{B}\)（測地線が作る流れ）．**
\(\alpha\ll\Lcal^d\) とし，\(T=\nabla\phi\) を最適輸送写像
（[ref:Clm: Brenier の定理|Brenier の定理]）とする．各点 \(x\) の質量を直線
\(t\mapsto T_t(x)=(1-t)x+t\,\nabla\phi(x)\) に沿って一定速度で動かすと，
分布は変位補間 \(\mu_t=(T_t)_\sharp\alpha\) となる．
この粒子の速度は時刻によらず \(\dot T_t(x)=\nabla\phi(x)-x\) なので，
速度場 \(v_t\) を \(v_t\bigl(T_t(x)\bigr)\defeq\nabla\phi(x)-x\) で定めると
\((\mu_t,v_t)\) は連続の方程式を満たす．その作用は，押し出しの定義より

\[
 \mathcal{A}(\mu,v)
 = \int_0^1\!\!\int_{\R^d}\norm{v_t}^2\,\d\mu_t\,\d t
 = \int_0^1\!\!\int_{\R^d}\norm{\nabla\phi(x)-x}^2\,\d\alpha(x)\,\d t
 = \int_{\R^d}\norm{x-\nabla\phi(x)}^2\,\d\alpha(x).
\]

右辺は最適カップリングのコスト，すなわち \(\Wass_2^2(\alpha,\beta)\)
（「測地線と変位補間」の章の式 \((\ast)\)）に等しい．
よって \(\mathcal{B}(\alpha,\beta)\le\Wass_2^2(\alpha,\beta)\)．

**\(\Wass_2^2\le\mathcal{B}\)（流れが作るカップリング）．**
逆に \((\rho_t,v_t)\in\mathrm{CE}(\alpha,\beta)\) を任意にとる．
各粒子の軌道 \(\gamma_x:[0,1]\to\R^d\)（\(\dot\gamma_x(t)=v_t(\gamma_x(t))\)，
\(\gamma_x(0)=x\)）を考え，端点の対応 \((\gamma_x(0),\gamma_x(1))\) の押し出しは
\(\alpha,\beta\) をつなぐカップリング \(\pi\) を与える．
各軌道について Cauchy--Schwarz より
\(\norm{\gamma_x(1)-\gamma_x(0)}^2 \le\int_0^1\norm{\dot\gamma_x(t)}^2\,\d t\)
が成り立つので，質量について積分して

\[
 \Wass_2^2(\alpha,\beta)
 \le \int_{\R^d\times\R^d}\norm{x-y}^2\,\d\pi(x,y)
 \le \int_0^1\!\!\int_{\R^d}\norm{v_t}^2\,\d\rho_t\,\d t
 = \mathcal{A}(\rho,v).
\]

下限をとって \(\Wass_2^2(\alpha,\beta)\le\mathcal{B}(\alpha,\beta)\)．
二つの不等式から等式を得る．同時に，等号は各軌道が等速直線
\(\gamma_x(t)=(1-t)x+t\,\nabla\phi(x)\) のとき，
すなわち流れが変位補間のときに限り成り立つ．
:::
:::


:::fact
### Rem: 静的・動的・測地線の三位一体

本章で，同じ対象が三つの姿で結ばれた：
静的な Kantorovich 問題の最適値 \(\Wass_2^2\)（質量の対応），
動的な Benamou--Brenier 作用の最小値 \(\mathcal{B}\)（流れのエネルギー），
そして変位補間という測地線（曲線）である．
「測地線＝最小作用の等速直線運動の集まり」という描像は，
次章で \(\Pp_2\) を形式的なリーマン多様体とみなし，
曲線の長さ・速度・勾配流を論じるための出発点となる．
:::


## 応用：Flow Matching と Rectified Flow


本節は本筋（幾何）から離れ，動的定式化が近年の**生成モデル**と
どう結びつくかを述べる補足である．証明は与えず，対応関係のみを示す．

生成モデルの一つの目標は，扱いやすい基準分布 \(\alpha\)（標準正規分布など）から
データ分布 \(\beta\) への変換を学習することである．
**連続正規化フロー**は，速度場 \(v_t\) を時間に依存するニューラルネットで
表し，常微分方程式 \(\dot x(t)=v_t(x(t))\) で粒子を \(\alpha\) から \(\beta\) へ運ぶ．
このとき粒子の分布 \(\rho_t\) はまさに連続の方程式
（[ref:Def: 連続の方程式|連続の方程式]）
\(\partial_t\rho_t+\diverg(\rho_t v_t)=0\) に従う．
すなわち**生成は連続の方程式の解の構成にほかならない**．

:::fact
**Flow Matching との対応．**
Flow Matching は，端点 \(\alpha,\beta\) をつなぐ**参照流れ** \((\rho_t,v_t)\) を
あらかじめ固定し，ニューラル速度場 \(v_t^\theta\) をその参照速度場へ
回帰させる（\(\int_0^1\E\,\norm{v_t^\theta-v_t}^2\,\d t\) を最小化）枠組みである．
参照流れとして** Benamou--Brenier の最小作用の流れ**（＝変位補間，
[ref:Thm: Benamou--Brenier|Benamou--Brenier]）を選んだものが
**OT 流（OT-CFM）**であり，各粒子は直線
\(x_t=(1-t)x_0+t\,x_1\) を等速で進む．
これは本章の測地線そのものであり，
**Rectified Flow**（軌道を直線へ「整流」する手法）の幾何的な原型でもある．
直線軌道は速度場が時間にほとんど依存せず，
サンプリング時の数値積分が少ステップで済むという実用上の利点をもつ．
ただし \(\alpha,\beta\) から最適な対応 \(\pi\)（どの \(x_0\) をどの \(x_1\) に結ぶか）を
得るには静的 OT を解く必要があり，ここで「正則化問題の双対と Sinkhorn アルゴリズム」の章の
Sinkhorn が部品として再登場する．
:::


要するに，本章の「\(\Wass_2^2=\) 最小作用」という等式は，
生成モデルの言葉では「最適輸送に沿った流れが，最も素直で直線的な生成経路を与える」
という主張に翻訳される．次章の Otto 計算は，この流れを
**エネルギー汎関数の勾配流**としてさらに構造化し，
拡散モデルとの接続を開く．
