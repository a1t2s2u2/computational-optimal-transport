# 計算最適輸送セミナー Web 版

Markdown を原稿の唯一の source of truth とし、`index.html` を生成する静的サイトである。

外部 CDN から MathJax と Mermaid を読み込む。ネットワークがない環境では、数式と概念地図のソース文字列は表示されるが、レンダリングは行われない。

## 構成

- `content/*.md`: 原稿本体
- `scripts/build.mjs`: Markdown から `index.html` を生成するスクリプト
- `index.html`: 生成物。直接編集しない
- `styles.css`: レイアウトと数理ブロックの見た目
- `app.js`: 用語パネル、章ナビ、Sinkhorn デモ

## 生成

```sh
node site/scripts/build.mjs
```

または:

```sh
cd site
npm run build
```

生成後、`site/index.html` をブラウザで開く。

## 方針

本文は数学書風に事実を述べる。証明、補足、直感、実装上の注意は折りたたみで分離する。
