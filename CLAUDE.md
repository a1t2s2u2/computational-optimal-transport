## 参考とする論文
[Computational Optimal Transport, Gabriel Peyré, Marco Cuturi](https://arxiv.org/abs/1803.00567)

## フォルダ構成
- `chapters/`: 教科書化された日本語版本編．`main.tex` がエントリ，`preamble.tex` を持つ
- `seminar/`: セミナーでの発表原稿（板書レベル）．`../chapters/preamble.tex` を共有
- `arXiv-1803.00567v4/`: 元論文ソース（参照用，整理対象外）

## ビルド方法
各ディレクトリの `.latexmkrc` で uplatex + dvipdfmx + `$out_dir = 'out'` が設定済み．中間生成物はすべて `out/` 配下に閉じ込められる．
- 教科書: `cd chapters && latexmk`
- セミナー: `cd seminar && latexmk`
- クリーン: `latexmk -c`（中間ファイル削除）/ `latexmk -C`（PDF も含めて完全クリーン）

## セミナー方針
- 離散と連続の**両方を行き来する**構成
- 連続側の理論的土台として $\X, \Y$ は **Polish 空間**を仮定（disintegration, tightness, Wasserstein 幾何のため）
- 離散側は有限次元 LP・組合せ論で完結し，Polish 仮定は形式的な役割に留まる

## tex コーディング規約
- Cuturi の論文構成と記法に従うこと
- 未定義の用語や概念は、必ず定義すること
- コミット時 / PR時 には co-authored-by や ClaudeCode は記載しない
