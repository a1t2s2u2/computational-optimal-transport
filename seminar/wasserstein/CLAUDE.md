## seminar/wasserstein

Wasserstein 距離の理論と性質。複数の文献を横断的に参照し、現代的な記法で再構成する。
目標は (1) $W_p$ の距離性、(2) Gaussian 測度間の $W_2$ の閉形式（本編3章+付録2章）。

## 参考文献

- [A class of Wasserstein metrics for probability distributions, C. R. Givens & R. M. Shortt (1984)](https://doi.org/10.1307/mmj/1029003026) — 骨格となる定義・命題の出典
- [Optimal Transport: Old and New, C. Villani (2009)](https://doi.org/10.1007/978-3-540-71050-9) — 現代的記法・証明の補完
- [最適輸送理論とリッチ曲率, 桑江ほか (Encounter with Mathematics 第63回, 2015)](https://www.math.chuo-u.ac.jp/ENCwMATH/EwM63resume.pdf) — 日本語の解説、定義の補完（§1.4 が Wasserstein 距離）

原論文 PDF は `reference/` にある（givens-shortt-1984.pdf, kuwae-etal-2015.pdf）。
Villani の該当ページのスキャンは `reference/old_and_new/` にある（optimal_coupling: Th.4.1 まわり pp.43, 49／wasserstein_distance: Ch.6 pp.93–95。著作権のため git 追跡対象外）。

## 記法

- Givens–Shortt 原論文の記号は導入の読み替え表で対応する
- 文献間で定義が異なる場合は、最も一般的な定義を採用し、差異を注意として記載する
- 押し出し記法 $T_\sharp\mu$ は使わず、像測度 $\mu\circ T^{-1}$ と書く（定義箇所に文献との対応を注記済み）
- 空間は Villani に合わせて calligraphy で書く: $W_p$ の基礎空間は $(\mathcal{X},d)$、coupling・存在定理の2空間は $\mathcal{X},\mathcal{Y}$。付録の一般論の空間記号は $X,Y$ のまま
- 定着した名称のない補題は、内容を説明する日本語タイトルを付ける
- 記法の初出箇所には「記法 …」の注意を置く（例: $L_n\downarrow L^*$、$\norm{f}_{L^p(\mu)}$）

## 方針

- 前提知識は付録（`tex/foundations/`）で全網羅し、本文からは参照でリンクする
- $W_p$ は Villani (Definition 6.1) に合わせて $1\leq p<\infty$ のみ扱う（$W_\infty$ と $L^\infty$ 系の道具は導入しない）
- 最適 coupling の存在定理は Villani (2009) Theorem 4.1 の形で証明し、距離性（三角不等式・一致の公理）の証明に用いる
- Prokhorov の定理・Portmanteau 定理は証明なしで認める（ステートメントと引用元のみ明示。Villani Ch.4 / Billingsley 1999）
- 証明なしで認める標準定理はステートメントを明示して文献を挙げる

## サイト

- tex が source of truth。`make wasserstein-site` で content/md → dist/html を生成（生成物は追跡外）
- 定理番号は tex2md が LaTeX のカウンタ規則を再現して PDF と同期させている
