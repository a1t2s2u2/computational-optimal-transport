/- 自動生成 by proofgraph/lean_gen.py。
   \blockmeta{lean=...} の対応先が Mathlib に実在するかを #check で検証する。
   Mathlib キャッシュ取得後に `lake build Ot.Generated.MathlibCheck` で確認。 -/
import Mathlib

namespace Ot.MathlibCheck

-- def:sem-separable
#check @TopologicalSpace.SeparableSpace
-- def:sem-metric-space
#check @MetricSpace
-- def:sem-normed-space
#check @NormedAddCommGroup
-- def:sem-complete-metric
#check @CompleteSpace
-- def:sem-polish
#check @PolishSpace

end Ot.MathlibCheck
