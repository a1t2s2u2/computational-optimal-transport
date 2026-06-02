# proofgraph — 数学ブロック依存グラフ + 空間レイヤ

セミナー資料（`seminar/tex/ch*.tex`）の Def / Prop / Thm / Claim / Rem / Ex ブロックの
**依存関係**を抽出し、**空間ごとに層別**して俯瞰し、証明の **AND/OR 分岐（ルート A / B）** を
表現するためのツール群。

既存の TeX パーサ（`seminar/site/scripts/tex2md.py`）を再利用して構築している。

## パイプライン

```
seminar/tex/ch*.tex  ──(\blockmeta 注釈)──▶  extractor.py  ──▶  out/graph.json
                                                                   │
                                              ┌────────────────────┴────────────┐
                                              ▼                                  ▼
                                         validate.py                       viewer/(Web)
                                      (循環/空間/ルート)                  (可視化・層別・フォーカス)
```

## 使い方

依存は [uv](https://docs.astral.sh/uv/) で管理する（`proofgraph/pyproject.toml`）。
すべて単一の `pg.py` から起動する。

```bash
cd proofgraph
uv run pg.py            # 抽出 → 検証 → viewer サーバ起動（既定）
```

ブラウザで **http://localhost:8000/viewer/** が開ける。個別実行や CI 向けは
[USAGE.md](USAGE.md) を参照。抽出不要のデモは `?data=sample.graph.json` で開ける。

## `\blockmeta` 注釈スキーマ

各ブロックの `\begin{env}{title}{label}` の**直後の行**に 1 つ置く。PDF には一切出力されない
（`preamble.tex` で `\newcommand{\blockmeta}[1]{}` と定義）。

```latex
\begin{theorem}{Kantorovich 双対定理}{sem-kantorovich-duality}
\blockmeta{space=normed; route.A=prop:sem-weak-duality-classical; route.B=prop:sem-c-transform-reduction}
  ...
\end{theorem}
```

| キー | 意味 | 値 |
|---|---|---|
| `space`   | このブロックが成り立つ前提空間 | `spaces.yaml` のキー（カンマ区切り可） |
| `uses`    | statement レベルの依存（前提） | `prefix:label`（カンマ区切り）。省略時は body 内 `\ref` から自動補完 |
| `route.X` | 証明ルート X が依存するブロック集合（連言 AND） | `prefix:label`（カンマ区切り） |

- **複数の `route.*` は選言（OR）＝同値な別証明**を表す。1 本でも健全（接地可能）なら定理は接地される。
- `route.*` も `uses` も省略すると、proof 内 / body 内の `\ref` から自動補完される（`_auto` ルート）。
- 参照接頭辞は `def, clm, thm, prop, rem, ex` のみ依存として扱う（`ch:/sec:/eq:/alg:` は除外）。

## 空間語彙（`spaces.yaml`）

空間タグと `refines`（強弱の半順序）を定義する。例: `normed refines [vector, metric]`
（ノルム空間はベクトル空間かつ誘導距離で距離空間）。`validate.py` はこの推移閉包で
「弱い空間の結果が、より強い空間を要する結果に依存していないか」を検査する。

## 検証項目（`validate.py`）

1. **dangling ref**: 存在しないブロックを指す依存（エラー）。
2. **循環 / 接地不能**: uses + AND/OR ルートで接地できないノード（エラー）。
   未定義依存を充足扱いにして判定するので、純粋な循環だけが残る。
3. **空間前提充足**: 弱い空間の結果が強い空間に依存していないか（警告）。
4. **ルート健全性**: 証明を持つノードが健全なルートを最低 1 本持つか（警告）。

### 設計メモ: AND/OR による循環解消

ch06 の Kantorovich 双対定理は、本文中に「$c$-変換による別証明を見よ」という**前方ポインタ**を
含む。自動抽出ではこれが証明依存と誤認され、$c$-変換命題が逆に双対定理を使うため**循環**する。
`route.A`（LP 強双対、弱双対性を使う）と `route.B`（$c$-変換）を明示すると、ルート A が定理を
独立に接地し、OR 解決で循環が解ける。これが本ツールが扱う「ルート A / ルート B」構造の実例。

## viewer の主な操作

- **フォーカス**: ノードを選ぶと、その依存先（上流＝青辺）と被依存（下流＝紫辺）だけに絞って
  再配置する。`直接`（1 ホップ）/ `推移閉包`（全前後）を選べる。依存関係を読む主役機能。
- **章ごとにグループ化**: ノードを章コンテナにまとめ、どの章の結果かを示す。
- **ラベル自動**: 俯瞰時は非表示、ズーム / ホバー / 選択 / フォーカス時のみ表示（過密回避）。
- **空間で層別 / 種類・章・辺フィルタ / 支持集合の強調** も従来どおり。

## 状態

- [x] Phase 0: 注釈スキーマ・空間語彙
- [x] Phase 1: 抽出器 `extractor.py` / 検証器 `validate.py` / モデル `model.py`
- [x] Phase 2: 可視化 viewer（Cytoscape.js）
- [x] Phase 3: AND/OR ルートの支持集合可視化
- [x] Phase 4: フォーカス（依存近傍に絞り込み）・章グループ化・ラベル自動表示
