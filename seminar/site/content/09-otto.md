---
id: otto
nav: Otto 計算
eyebrow: 9. Otto Calculus
title: Otto 計算と勾配流
---


「動的定式化：Benamou--Brenier」の章で，\(\Wass_2^2\) が
「連続の方程式に従う流れの最小作用」であることを見た．
この事実は，確率測度の空間 \(\Pp_2(\R^d)\) を
**無限次元の（形式的な）リーマン多様体**とみなす視点を示唆する：
各点 \(\rho\) における「動く方向」は流れの初速度であり，
その「長さ」は運動エネルギーで測られ，
\(\Wass_2\) はこの計量が定める測地距離にほかならない．
この形式的幾何を整備したのが Otto の計算である．

本章の目標は二つある．第一に，\(\Pp_2\) の**接空間**と**Otto 計量**を
定め，曲線の速度・勾配を測度の空間で語れるようにすること．
第二に，この計量のもとで**エネルギー汎関数の勾配流**を考えると，
相対エントロピーの勾配流が**熱方程式**に一致する，という
Jordan--Kinderlehrer--Otto の結果に到達することである．
これは確率測度の動力学を変分原理で捉える枠組みであり，
章末では拡散モデルとの接続にも触れる．
なお本章は形式的なリーマン幾何として議論し，
厳密化（存在・収束）は文献に譲る．

## 接空間と Otto 計量


\(\Pp_2(\R^d)\) 内の曲線 \((\rho_t)\) の「速度」を定める．
連続の方程式（[ref:Def: 連続の方程式|連続の方程式]）
\(\partial_t\rho_t+\diverg(\rho_t v_t)=0\) は，
分布の変化 \(\partial_t\rho_t\) を速度場 \(v_t\) に結びつける．
ただし同じ \(\partial_t\rho_t\) を与える \(v_t\) は一意でない
（\(\diverg(\rho_t w)=0\) なる \(w\) を加えてもよい）．
運動エネルギー \(\int\norm{v_t}^2\d\rho_t\) を最小にする代表を選ぶと，
それは**勾配場** \(v_t=\nabla\psi_t\) になる．これが接ベクトルの正準な表示を与える．

:::theorem
### Clm: 接空間（Helmholtz 分解）

\(\rho\in\Pp_2(\R^d)\) における接空間を

\[
 \Tan_\rho\Pp_2
 \defeq \overline{\bigl\{\,\nabla\psi : \psi\in\Cc_c^\infty(\R^d)\,\bigr\}}^{\,L^2(\rho)}
\]

（\(L^2(\rho;\R^d)\) における勾配場の閉包）と定める．
任意のベクトル場 \(v\in L^2(\rho;\R^d)\) は

\[
 v = \nabla\psi + w,
 \qquad \nabla\psi\in\Tan_\rho\Pp_2,\quad \diverg(\rho w)=0,
\]

と直交分解され（\(\rho\)-重み付き Helmholtz 分解），
\(\nabla\psi\) は連続の方程式の制約
\(\diverg(\rho v)=\diverg(\rho\nabla\psi)\) を保ったまま
\(\int\norm{\,\cdot\,}^2\d\rho\) を最小にする代表である．
:::


:::definition
### Def: Otto 計量

曲線の速度 \(\partial_t\rho\) を，連続の方程式を通じて
接ベクトル \(\nabla\psi\in\Tan_\rho\Pp_2\) と同一視する：
\(\partial_t\rho=-\diverg(\rho\nabla\psi)\)．
二つの接ベクトル \(\nabla\psi_1,\nabla\psi_2\) に対する**Otto 計量**を

\[
 \inner{\nabla\psi_1}{\nabla\psi_2}_\rho
 \defeq
 \int_{\R^d}\inner{\nabla\psi_1(x)}{\nabla\psi_2(x)}\,\d\rho(x)
\]

で定める．対応するノルムは \(\norm{\nabla\psi}_\rho^2=\int\norm{\nabla\psi}^2\d\rho\)．
:::


:::fact
### Rem: \(\Wass_2\) は Otto 計量の測地距離

曲線 \((\rho_t)\) の長さを \(\int_0^1\norm{\partial_t\rho_t}_{\rho_t}\,\d t\) で測ると，
これは「動的定式化：Benamou--Brenier」の章の作用 \(\mathcal{A}(\rho,v)\)
（最小代表 \(v=\nabla\psi\) をとったもの）の平方根の時間積分にあたり，
Benamou--Brenier の[ref:Thm: Benamou--Brenier|Benamou--Brenier]は

\[
 \Wass_2(\alpha,\beta)
 = \inf\Bigl\{\textstyle\int_0^1\norm{\partial_t\rho_t}_{\rho_t}\,\d t
 : \rho_0=\alpha,\ \rho_1=\beta\Bigr\}
\]

と読み替えられる．すなわち \(\Wass_2\) は Otto 計量が定める**測地距離**であり，
測地線は前章の変位補間である．これが「\(\Pp_2\) をリーマン多様体とみなす」
という形式的視点の正当化（の骨子）である．
:::


## 第一変分と Wasserstein 勾配


リーマン多様体上の勾配流を語るには，汎関数の**勾配**が要る．
まず汎関数の微分（第一変分）を定め，それを Otto 計量で「勾配」に翻訳する．

:::definition
### Def: 第一変分

汎関数 \(F:\Pp_2(\R^d)\to\R\) の \(\rho\) における**第一変分**
\(\dfrac{\delta F}{\delta\rho}:\R^d\to\R\) とは，
質量 \(0\) の摂動 \(\chi\)（\(\int\chi\,\d x=0\)）に対して

\[
 \left.\frac{\d}{\d s}\right|_{s=0} F(\rho+s\chi)
 = \int_{\R^d} \frac{\delta F}{\delta\rho}(x)\,\chi(x)\,\d x
\]

を満たす関数をいう（存在するとき）．
:::


ユークリッド空間では勾配は微分そのものだが，
リーマン多様体では計量を通して接空間の元へ「持ち上げる」必要がある．
Otto 計量のもとでの勾配は次で与えられる．

:::theorem
### Clm: Wasserstein 勾配

\(F\) の Otto 計量に関する**勾配** \(\mathrm{grad}_{\Wass_2}F(\rho)\) は，
接ベクトル \(\nabla\bigl(\tfrac{\delta F}{\delta\rho}\bigr)\) に対応する：
曲線方向 \(\partial_t\rho=-\diverg(\rho\nabla\psi)\) に対して

\[
 \left.\frac{\d}{\d t}\right|_{0}F(\rho_t)
 = \inner{\,\mathrm{grad}_{\Wass_2}F(\rho)\,}{\nabla\psi}_\rho,
 \qquad
 \mathrm{grad}_{\Wass_2}F(\rho)=\nabla\Bigl(\tfrac{\delta F}{\delta\rho}\Bigr).
\]

:::details-embedded 証明
連続の方程式と部分積分，および第一変分の定義より

\[
 \frac{\d}{\d t}F(\rho_t)
 = \int \frac{\delta F}{\delta\rho}\,\partial_t\rho_t
 = -\int \frac{\delta F}{\delta\rho}\,\diverg(\rho_t\nabla\psi)
 = \int \inner{\nabla\Bigl(\tfrac{\delta F}{\delta\rho}\Bigr)}{\nabla\psi}\,\d\rho_t
 = \inner{\nabla\Bigl(\tfrac{\delta F}{\delta\rho}\Bigr)}{\nabla\psi}_{\rho_t}.
\]

これは勾配の定義（方向微分が計量内積で書ける）にほかならない．
:::
:::


## JKO スキームと勾配流


ユークリッド空間の勾配流 \(\dot x=-\nabla F(x)\) は，
**陰的 Euler 法**（最小化運動）
\(x^{k+1}=\argmin_x\bigl(\tfrac{1}{2\tau}\norm{x-x^k}^2+F(x)\bigr)\) の
\(\tau\to0\) 極限として特徴づけられる．
距離 \(\norm{x-x^k}\) を \(\Wass_2\) に置き換えると，測度の空間での勾配流が定義できる．
これが Jordan--Kinderlehrer--Otto（JKO）の最小化運動スキームである．

:::definition
### Def: JKO スキーム

汎関数 \(F:\Pp_2(\R^d)\to\R\)，時間刻み \(\tau>0\)，初期測度 \(\rho^0\) に対し，

\[
 \rho^{k+1}
 \in
 \argmin_{\rho\in\Pp_2(\R^d)}
 \left\{\,
 \frac{1}{2\tau}\,\Wass_2^2(\rho,\rho^k) + F(\rho)
 \,\right\}
 \qquad (k=0,1,2,\dots)
\]

により列 \((\rho^k)\) を定める．各ステップは
「\(\rho^k\) から \(\Wass_2\) で近く，かつ \(F\) を下げる」測度を選ぶ操作である．
:::


:::theorem
### Clm: JKO の収束と勾配流

\(F\) が適当な条件（下半連続・変位凸性など）を満たすとき，
時間刻み \(\tau\to0\) で，JKO 列の区分定数補間
\(\rho^\tau(t)\) は曲線 \((\rho_t)\) に収束し，その極限は
\(F\) の**Wasserstein 勾配流**

\[
 \partial_t\rho_t
 = -\,\mathrm{grad}_{\Wass_2}F(\rho_t)
 = \diverg\!\Bigl(\rho_t\,\nabla\tfrac{\delta F}{\delta\rho}(\rho_t)\Bigr)
\]

を満たす（[ref:Clm: Wasserstein 勾配|Wasserstein 勾配]を代入した形）．
:::


最後の偏微分方程式の右辺は，連続の方程式
\(\partial_t\rho+\diverg(\rho v)=0\) において
速度を \(v=-\nabla\tfrac{\delta F}{\delta\rho}\) にとったものである：
勾配流とは「自由エネルギー \(F\) を最も急に下げる向きに質量を流す」ことにほかならない．

## 熱方程式はエントロピーの勾配流


最も基本的な汎関数として**（負の）エントロピー**
（Lebesgue 測度に対する相対エントロピー）

\[
 \Hm(\rho) \defeq \int_{\R^d} \rho(x)\log\rho(x)\,\d x
\]

をとる．その Wasserstein 勾配流が熱方程式になることを示す．

:::theorem
### Thm: Jordan--Kinderlehrer--Otto

\(F=\Hm\) の Wasserstein 勾配流は**熱方程式**である：

\[
 \partial_t\rho_t = \Delta\rho_t .
\]

したがって熱拡散は，エントロピーを \(\Wass_2\) 計量のもとで
最も急に減少させる流れとして特徴づけられる．

:::details-embedded 証明
\(\Hm\) の第一変分を計算する．\(\frac{\d}{\d s}\int(\rho+s\chi)\log(\rho+s\chi) \big|_{s=0}=\int(\log\rho+1)\chi\) なので，
\(\tfrac{\delta\Hm}{\delta\rho}=\log\rho+1\)．よって

\[
 \nabla\tfrac{\delta\Hm}{\delta\rho}
 = \nabla\log\rho = \frac{\nabla\rho}{\rho}.
\]

[ref:Clm: JKO の収束と勾配流|JKO の収束と勾配流]の勾配流に代入すると

\[
 \partial_t\rho
 = \diverg\!\Bigl(\rho\,\nabla\log\rho\Bigr)
 = \diverg\!\Bigl(\rho\cdot\frac{\nabla\rho}{\rho}\Bigr)
 = \diverg(\nabla\rho)
 = \Delta\rho.
\]
:::
:::


:::fact
### Rem: ポテンシャル項と Fokker--Planck

外場ポテンシャル \(V:\R^d\to\R\) を加えた自由エネルギー
\(F(\rho)=\Hm(\rho)+\int V\,\d\rho\) をとると，
\(\tfrac{\delta F}{\delta\rho}=\log\rho+1+V\) より勾配流は

\[
 \partial_t\rho
 = \diverg\!\bigl(\rho\,\nabla(\log\rho+V)\bigr)
 = \Delta\rho + \diverg(\rho\,\nabla V),
\]

すなわち**Fokker--Planck 方程式**となる．
その定常解はギブス測度 \(\rho_\infty\propto e^{-V}\) で，
これは \(F\) の最小点でもある（エントロピーと位置エネルギーの釣り合い）．
確率の言葉では，これは過減衰 Langevin 拡散
\(\d X_t=-\nabla V(X_t)\,\d t+\sqrt2\,\d B_t\) の密度の発展である．
:::


## 応用：拡散モデルと Schrödinger ブリッジ


本節は本筋から離れ，勾配流の視点が**拡散モデル**と
**Schrödinger ブリッジ**にどう結びつくかを述べる補足である．
証明は与えず，対応のみを示す．

:::fact
**スコアベース拡散モデルとの対応．**
拡散モデルは，データ \(\rho_0\) にノイズを徐々に加える**前進過程**
（Fokker--Planck／Langevin，備考[ref:Rem: ポテンシャル項と Fokker--Planck|ポテンシャル項と Fokker--Planck]）と，
それを時間反転してノイズからデータを生成する**後退過程**からなる．
後退過程の駆動項にはスコア \(\nabla\log\rho_t\) が現れるが，
これはまさにエントロピー \(\Hm\) の Wasserstein 勾配
\(\nabla\tfrac{\delta\Hm}{\delta\rho}=\nabla\log\rho_t\)
（[ref:Thm: Jordan--Kinderlehrer--Otto|Jordan--Kinderlehrer--Otto]）である．
すなわち拡散モデルの学習対象「スコア」は，
**エントロピー勾配流の速度場**に等しい．
Flow Matching（前章 本節）が
最小作用の流れ（測地線）を学ぶのに対し，
拡散モデルはエントロピー勾配流に沿う速度場を学ぶ，と整理できる．
:::


:::fact
**Schrödinger ブリッジとの対応．**
「エントロピー正則化」の章・「正則化問題の双対と Sinkhorn アルゴリズム」の章の
エントロピー正則化 OT は，動的に見ると
「基準となるブラウン運動からの相対エントロピーを最小にしつつ
端点 \(\alpha,\beta\) をつなぐ確率過程を求める」
**Schrödinger 問題**に対応する．
これは Benamou--Brenier の作用に拡散項を加えた形（運動エネルギー＋エントロピー）であり，
正則化パラメータ \(\varepsilon\to0\) で動的最適輸送（前章）へ収束する．
近年の**拡散 Schrödinger ブリッジ**は，この問題を
反復射影（Sinkhorn の動的版）で解いて生成モデルに用いる枠組みであり，
本セミナーのエントロピー正則化と動的定式化がともに部品として効く．
:::


要するに，Otto 計算が与える「測度の動力学＝自由エネルギーの勾配流」という描像は，
測地線（Flow Matching）と拡散（スコア・Schrödinger）を
同じ変分原理のもとに並べる共通言語となる．
次章では，この勾配流の**凸性**——汎関数が測地線に沿って凸かどうか——を問い，
それが空間の**曲率**と結びつくことを見る．
