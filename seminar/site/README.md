# 計算最適輸送セミナー Web 版

このサイトは **生成物** である。唯一の source of truth は `seminar/tex/*.tex`（LaTeX 原稿）であり、
本文を直すときは tex を編集する。サイトはそこから自動生成して読むためのビューにすぎない。

```
seminar/tex/{main,foundations}/*.tex  ← ★ ここだけを編集する（本編＋付録:前提知識）
      │  scripts/build.mjs      （tex → html を一括生成。md 中間表現はメモリ上のみ）
      ▼
seminar/site/dist/         ← 生成物（gitignore 済み）。デプロイ用サイト
  index.html / main/*.html / appendix/*.html / styles.css / app.js
```

`dist/` 配下の `*.html` は git で管理しない（`.gitignore` 済み）。コミットに乗るのは tex だけ。

外部 CDN から MathJax と Mermaid を読み込む。ネットワークがない環境では、数式と概念地図のソース文字列は表示されるが、レンダリングは行われない。

## 構成

- `scripts/build.mjs`: tex を解析し（内部で markdown 中間表現を経て）HTML を生成する単一スクリプト
- `dist/`: build.mjs の生成物（gitignore）。`index.html` + `main/` + `appendix/` + コピーした css/js
- `styles.css`: レイアウトと数理ブロックの見た目
- `app.js`: 用語パネル、章ナビ、Sinkhorn デモ

## ローカルで読む

リポジトリ直下で:

```sh
make site
```

`tex → html` を生成し、`seminar/site/dist/index.html` をブラウザで開く。
（`make` を使わない場合は `seminar/site` で `npm run build`。）

## 公開（GitHub Pages）

`main` に push すると `.github/workflows/pages.yml` が tex からサイトを生成し
GitHub Pages へ自動デプロイする。手元での生成・コミットは不要。

初回のみ、リポジトリの **Settings → Pages → Build and deployment → Source** を
**「GitHub Actions」** に設定する必要がある。

## 方針

本文は数学書風に事実を述べる。証明、補足、直感、実装上の注意は折りたたみで分離する。
