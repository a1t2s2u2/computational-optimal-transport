# proofgraph 起動方法

数学ブロック依存グラフの抽出・検証・可視化の起動手順。依存は
[uv](https://docs.astral.sh/uv/) で管理し（`proofgraph/pyproject.toml`）、
すべて単一の `pg.py` から起動する。

## 前提

| 必要なもの | 確認 |
|---|---|
| uv（`pyyaml` を自動解決） | `uv --version` |
| ブラウザ（viewer 表示用） | — |

初回に依存を取得する（以降の `uv run` は自動同期するため必須ではない）:

```bash
uv sync --project proofgraph
```

仮想環境は `proofgraph/.venv`、バージョンは `uv.lock` で固定される。

---

## いちばん簡単な起動（推奨）

```bash
cd proofgraph
uv run pg.py
```

これだけで **抽出 → 検証 → ローカルサーバ起動** まで通す。ブラウザで
**http://localhost:8000/viewer/** を開く。停止は `Ctrl+C`。

> `pg.py` は `__file__` 基準でパスを解決するので、どのディレクトリから実行してもよい。
> リポジトリルートからは `uv run --project proofgraph python proofgraph/pg.py` とする。

## 個別サブコマンド

```bash
cd proofgraph
uv run pg.py extract     # tex → out/graph.json（出力例: nodes=153 edges=98 space-annotated=8）
uv run pg.py validate    # graph.json の健全性検証（エラーで終了コード 1・CI 用）
uv run pg.py build       # 抽出 → 検証 のみ（サーバを起動しない・CI 用）
uv run pg.py serve        # サーバのみ起動（--port で変更可）
```

- `out/` は `.gitignore` 済み。tex を編集したら `extract` を再実行する。
- viewer は `fetch` 制限のため **必ずサーバ経由**で開く（`file://` 直開きは不可）。

## viewer の操作

- **フォーカス（推奨）**: 左の「フォーカス」を `直接` または `推移` にしてノードをクリックすると、
  その**依存先（上流＝青辺）と被依存（下流＝紫辺）だけ**に絞り込んで再配置する。
  「全体表示に戻す」または右パネルのボタンで解除。依存関係を読むときの主役機能。
- **章ごとにグループ化**: ノードを章コンテナ（淡色タイル）にまとめ、どの章の結果かを一目で示す。
- **ラベル**: 既定は「自動」で、俯瞰時は非表示・ズーム / ホバー / 選択 / フォーカス時のみ表示（過密回避）。
  常に出したいときは「常時表示」。
- **空間で層別**: 選んだ空間で成り立つ結果のみ強調（強い空間を要する結果は淡色化）。
- **種類 / 章 / 辺の種類**: チェックで表示切替（uses=実線, proof=破線）。
- **ノードをクリック**: statement・証明ルート(A/B)・依存/被依存を右パネルに表示。
- ルートの「辺を強調」「支持集合」ボタン: そのルートが支える全ブロックを緑強調。

## サンプルデータ（抽出不要のデモ）

viewer は `?data=` で読み込むグラフを差し替えられる。セミナー抽出結果がなくても、
同梱のサンプル（微分積分の小さな例）で UI を試せる:

- **http://localhost:8000/viewer/?data=sample.graph.json**

左パネル「データ」からセミナー（実データ）／サンプルを切り替えられる。
独自の `graph.json` を `viewer/` 配下に置けば `?data=foo.json` で読める。

## トラブルシュート

- **viewer が真っ白／データを読み込めない**: `file://` で開いていないか確認。`uv run pg.py` の
  サーバ経由で開く。実データを見るには先に `uv run pg.py extract` を実行しておく。
- **`ModuleNotFoundError: tex2md`**: `extractor.py` が `seminar/site/scripts` を `sys.path` に
  追加する。`pg.py` 経由なら問題ない。
- **validate がエラー**: 循環は `\blockmeta{route.X=...}` で別証明ルートを明示して解消する
  （[README.md](README.md) の「AND/OR による循環解消」を参照）。
