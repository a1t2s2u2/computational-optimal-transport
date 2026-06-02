/- 自動生成 by proofgraph/lean_gen.py — 手で編集しないこと。

   各数学ブロックを opaque Prop として宣言し、依存構造を Lean の項として
   組み上げる。`sorry` は未証明 obligation。`lake build` が非循環性・
   依存存在・obligation 数を型検査として検証する。 -/

namespace Ot.Generated

-- 各ブロックの statement（内容は抽象化した Prop プレースホルダ）
opaque def_sem_power_set : Prop
opaque def_sem_topological_space : Prop
opaque def_sem_dense : Prop
opaque def_sem_separable : Prop
opaque def_sem_metric_space : Prop
opaque def_sem_normed_space : Prop
opaque def_sem_open_ball : Prop
opaque def_sem_convergence : Prop
opaque def_sem_complete_metric : Prop
opaque def_sem_polish : Prop
opaque def_sem_continuous : Prop
opaque prop_sem_preimage_closed : Prop
opaque def_sem_bounded : Prop
opaque def_sem_compact : Prop
opaque clm_sem_bolzano_weierstrass : Prop
opaque thm_sem_heine_borel : Prop
opaque thm_sem_weierstrass : Prop
opaque prop_sem_finite_dim_linear_continuous : Prop
opaque thm_sem_mvt : Prop
opaque def_sem_sigma_algebra : Prop
opaque def_sem_measurable_space : Prop
opaque def_sem_measurable_map : Prop
opaque def_sem_borel : Prop
opaque def_sem_measurable_function : Prop
opaque def_sem_product_measurable : Prop
opaque def_sem_projection : Prop
opaque def_sem_measure : Prop
opaque def_sem_probability_measure : Prop
opaque def_sem_indicator : Prop
opaque def_sem_simple_function : Prop
opaque def_sem_nonneg_integral : Prop
opaque prop_sem_mct : Prop
opaque prop_sem_measure_linearity : Prop
opaque def_sem_dirac : Prop
opaque clm_sem_dirac_integral : Prop
opaque def_sem_discrete_measure : Prop
opaque clm_sem_discrete_measure_uniqueness : Prop
opaque def_sem_pushforward : Prop
opaque prop_sem_dirac_pushforward : Prop
opaque def_sem_finite : Prop
opaque clm_sem_finite_min : Prop
opaque def_sem_permutation : Prop
opaque def_sem_linear_function : Prop
opaque def_sem_ones_vector : Prop
opaque def_sem_frobenius_inner : Prop
opaque def_sem_convex : Prop
opaque def_sem_convex_function : Prop
opaque prop_sem_strict_convex_unique_min : Prop
opaque rem_sem_ch2_setup : Prop
opaque def_sem_assignment : Prop
opaque ex_sem_assignment_cost_example : Prop
opaque clm_sem_assignment_existence : Prop
opaque clm_sem_uniqueness : Prop
opaque def_sem_monge : Prop
opaque ex_sem_nonconvex : Prop
opaque ex_sem_monge_noexist : Prop
opaque def_sem_kantorovich : Prop
opaque rem_sem_marginal_pushforward : Prop
opaque prop_sem_discrete_kantorovich : Prop
opaque rem_sem_distinct_points : Prop
opaque ex_sem_factory_supermarket : Prop
opaque clm_sem_discrete_kantorovich_existence : Prop
opaque clm_sem_coupling_convex : Prop
opaque clm_sem_optimal_face : Prop
opaque ex_sem_nonunique_example : Prop
opaque rem_sem_lp_uniqueness : Prop
opaque rem_sem_entropy_uniqueness_preview : Prop
opaque def_sem_discrete_entropy : Prop
opaque rem_sem_entropy_convention : Prop
opaque rem_sem_phi_continuous : Prop
opaque def_sem_entropic_ot : Prop
opaque clm_sem_neg_entropy_strict_convex : Prop
opaque prop_sem_entropic_existence_unique : Prop
opaque def_sem_kl_divergence : Prop
opaque def_sem_gibbs_kernel : Prop
opaque prop_sem_entropic_kl_projection : Prop
opaque thm_sem_entropic_convergence_eps_zero : Prop
opaque rem_sem_entropic_convergence_eps_infty : Prop
opaque prop_sem_entropic_positive_solution : Prop
opaque def_sem_marginal_tangent : Prop
opaque prop_sem_tangent_orthogonal : Prop
opaque prop_sem_scaling_form : Prop
opaque rem_sem_dual_scaling_correspondence : Prop
opaque prop_sem_matrix_scaling : Prop
opaque prop_sem_sinkhorn_welldefined : Prop
opaque rem_sem_scaling_ambiguity : Prop
opaque prop_sem_entropic_dual : Prop
opaque rem_sem_soft_constraint : Prop
opaque prop_sem_block_coordinate_ascent : Prop
opaque rem_sem_gradient_marginal : Prop
opaque def_sem_hilbert_metric : Prop
opaque thm_sem_birkhoff : Prop
opaque thm_sem_sinkhorn_linear_convergence : Prop
opaque rem_sem_convergence_meaning : Prop
opaque rem_sem_ch4_summary : Prop
opaque def_sem_ground_metric : Prop
opaque def_sem_wasserstein_discrete : Prop
opaque clm_sem_minkowski : Prop
opaque thm_sem_wasserstein_is_distance : Prop
opaque rem_sem_wasserstein_p_leq_1 : Prop
opaque rem_sem_ch5_summary : Prop
opaque def_sem_dual_feasible : Prop
opaque prop_sem_weak_duality_classical : Prop
opaque thm_sem_kantorovich_duality : Prop
opaque rem_sem_hard_vs_soft : Prop
opaque rem_sem_dual_interpretation : Prop
opaque prop_sem_complementary_slackness : Prop
opaque rem_sem_support_characterization : Prop
opaque def_sem_c_transform_def : Prop
opaque prop_sem_c_transform_reduction : Prop
opaque rem_sem_c_concave : Prop
opaque def_sem_soft_min_ch6 : Prop
opaque def_sem_soft_c_transform : Prop
opaque prop_sem_sinkhorn_soft_c : Prop
opaque rem_sem_ch6_summary : Prop
opaque def_sem_w2_def : Prop
opaque rem_sem_w2_is_metric : Prop
opaque clm_sem_brenier : Prop
opaque rem_sem_brenier_from_dual : Prop
opaque def_sem_constant_speed_geodesic : Prop
opaque def_sem_mccann_interpolation : Prop
opaque thm_sem_mccann_geodesic : Prop
opaque rem_sem_particle_picture : Prop
opaque rem_sem_displacement_convexity_preview : Prop
opaque def_sem_continuity_equation : Prop
opaque rem_sem_ce_weak_meaning : Prop
opaque clm_sem_disintegration : Prop
opaque def_sem_bb_action : Prop
opaque rem_sem_why_kinetic : Prop
opaque def_sem_theta : Prop
opaque prop_sem_theta_convex : Prop
opaque def_sem_bb_convex : Prop
opaque thm_sem_benamou_brenier : Prop
opaque clm_sem_bb_existence : Prop
opaque rem_sem_bb_trinity : Prop
opaque clm_sem_tangent_space : Prop
opaque def_sem_otto_inner : Prop
opaque rem_sem_otto_w2 : Prop
opaque def_sem_first_variation : Prop
opaque clm_sem_w2_grad_formula : Prop
opaque def_sem_jko_scheme : Prop
opaque clm_sem_jko_limit : Prop
opaque thm_sem_jko_heat : Prop
opaque rem_sem_fokker_planck : Prop
opaque def_sem_k_displacement_convex : Prop
opaque rem_sem_k_as_curvature : Prop
opaque clm_sem_jacobian_concave : Prop
opaque rem_sem_why_convex_gradient : Prop
opaque thm_sem_entropy_displacement_convex : Prop
opaque rem_sem_renyi_functional : Prop
opaque def_sem_cd_kn : Prop
opaque clm_sem_lsv : Prop
opaque rem_sem_cd_significance : Prop

-- 各ブロックの『証明済み性』。foundational は axiom、証明付きは依存から導出。
axiom def_sem_power_set_pf : def_sem_power_set
axiom def_sem_topological_space_pf : def_sem_topological_space
axiom def_sem_dense_pf : def_sem_dense
-- 可分性
theorem def_sem_separable_pf : def_sem_separable := by
  have _ := def_sem_dense_pf
  sorry
axiom def_sem_metric_space_pf : def_sem_metric_space
-- ノルム空間
theorem def_sem_normed_space_pf : def_sem_normed_space := by
  have _ := def_sem_metric_space_pf
  sorry
axiom def_sem_open_ball_pf : def_sem_open_ball
axiom def_sem_convergence_pf : def_sem_convergence
-- 完備性
theorem def_sem_complete_metric_pf : def_sem_complete_metric := by
  have _ := def_sem_convergence_pf
  sorry
axiom def_sem_polish_pf : def_sem_polish
axiom def_sem_continuous_pf : def_sem_continuous
-- 連続写像による閉集合の引き戻し
theorem prop_sem_preimage_closed_pf : prop_sem_preimage_closed := by
  have _ := def_sem_continuous_pf
  sorry
axiom def_sem_bounded_pf : def_sem_bounded
axiom def_sem_compact_pf : def_sem_compact
axiom clm_sem_bolzano_weierstrass_pf : clm_sem_bolzano_weierstrass
-- Heine-Borel の定理
theorem thm_sem_heine_borel_pf : thm_sem_heine_borel := by
  have _ := clm_sem_bolzano_weierstrass_pf
  have _ := def_sem_bounded_pf
  have _ := def_sem_compact_pf
  have _ := def_sem_topological_space_pf
  sorry
-- Weierstrass の最大値の定理
theorem thm_sem_weierstrass_pf : thm_sem_weierstrass := by
  have _ := def_sem_continuous_pf
  sorry
axiom prop_sem_finite_dim_linear_continuous_pf : prop_sem_finite_dim_linear_continuous
axiom thm_sem_mvt_pf : thm_sem_mvt
axiom def_sem_sigma_algebra_pf : def_sem_sigma_algebra
axiom def_sem_measurable_space_pf : def_sem_measurable_space
axiom def_sem_measurable_map_pf : def_sem_measurable_map
-- ボレル $\sigma$-代数
theorem def_sem_borel_pf : def_sem_borel := by
  have _ := def_sem_topological_space_pf
  sorry
-- 可測関数
theorem def_sem_measurable_function_pf : def_sem_measurable_function := by
  have _ := def_sem_measurable_map_pf
  sorry
axiom def_sem_product_measurable_pf : def_sem_product_measurable
-- 射影
theorem def_sem_projection_pf : def_sem_projection := by
  have _ := def_sem_measurable_map_pf
  have _ := def_sem_product_measurable_pf
  sorry
axiom def_sem_measure_pf : def_sem_measure
axiom def_sem_probability_measure_pf : def_sem_probability_measure
axiom def_sem_indicator_pf : def_sem_indicator
axiom def_sem_simple_function_pf : def_sem_simple_function
-- 非負可測関数の積分
theorem def_sem_nonneg_integral_pf : def_sem_nonneg_integral := by
  have _ := def_sem_simple_function_pf
  sorry
axiom prop_sem_mct_pf : prop_sem_mct
-- 積分の測度に関する線形性
theorem prop_sem_measure_linearity_pf : prop_sem_measure_linearity := by
  have _ := prop_sem_mct_pf
  sorry
axiom def_sem_dirac_pf : def_sem_dirac
-- Dirac 測度に対する積分
theorem clm_sem_dirac_integral_pf : clm_sem_dirac_integral := by
  have _ := prop_sem_mct_pf
  sorry
axiom def_sem_discrete_measure_pf : def_sem_discrete_measure
-- 離散測度の表示の一意性
theorem clm_sem_discrete_measure_uniqueness_pf : clm_sem_discrete_measure_uniqueness := sorry
axiom def_sem_pushforward_pf : def_sem_pushforward
-- Dirac 測度と離散測度の押し出し
theorem prop_sem_dirac_pushforward_pf : prop_sem_dirac_pushforward := sorry
axiom def_sem_finite_pf : def_sem_finite
-- 有限集合の最小元
theorem clm_sem_finite_min_pf : clm_sem_finite_min := by
  have _ := def_sem_finite_pf
  sorry
-- 置換
theorem def_sem_permutation_pf : def_sem_permutation := by
  have _ := def_sem_finite_pf
  sorry
axiom def_sem_linear_function_pf : def_sem_linear_function
axiom def_sem_ones_vector_pf : def_sem_ones_vector
axiom def_sem_frobenius_inner_pf : def_sem_frobenius_inner
axiom def_sem_convex_pf : def_sem_convex
axiom def_sem_convex_function_pf : def_sem_convex_function
-- 狭義凸関数の最小点の一意性
theorem prop_sem_strict_convex_unique_min_pf : prop_sem_strict_convex_unique_min := sorry
-- 本章の設定
theorem rem_sem_ch2_setup_pf : rem_sem_ch2_setup := by
  have _ := def_sem_borel_pf
  have _ := def_sem_convergence_pf
  have _ := def_sem_dense_pf
  have _ := def_sem_measurable_space_pf
  have _ := def_sem_metric_space_pf
  have _ := def_sem_open_ball_pf
  have _ := def_sem_polish_pf
  have _ := def_sem_separable_pf
  sorry
axiom def_sem_assignment_pf : def_sem_assignment
axiom ex_sem_assignment_cost_example_pf : ex_sem_assignment_cost_example
-- 最適解の存在
theorem clm_sem_assignment_existence_pf : clm_sem_assignment_existence := by
  have _ := clm_sem_finite_min_pf
  sorry
-- 最適解が一意でない場合の存在
theorem clm_sem_uniqueness_pf : clm_sem_uniqueness := sorry
axiom def_sem_monge_pf : def_sem_monge
-- 実行可能集合の非凸性
theorem ex_sem_nonconvex_pf : ex_sem_nonconvex := by
  have _ := prop_sem_dirac_pushforward_pf
  sorry
-- Monge 写像が存在しない場合
theorem ex_sem_monge_noexist_pf : ex_sem_monge_noexist := by
  have _ := prop_sem_dirac_pushforward_pf
  sorry
axiom def_sem_kantorovich_pf : def_sem_kantorovich
-- 押し出しを用いたコンパクトな表現
theorem rem_sem_marginal_pushforward_pf : rem_sem_marginal_pushforward := by
  have _ := def_sem_projection_pf
  have _ := def_sem_pushforward_pf
  sorry
-- 連続 Kantorovich 問題の離散化
theorem prop_sem_discrete_kantorovich_pf : prop_sem_discrete_kantorovich := by
  have _ := clm_sem_dirac_integral_pf
  have _ := def_sem_frobenius_inner_pf
  have _ := prop_sem_measure_linearity_pf
  sorry
axiom rem_sem_distinct_points_pf : rem_sem_distinct_points
axiom ex_sem_factory_supermarket_pf : ex_sem_factory_supermarket
-- 離散 Kantorovich 問題の解の存在
theorem clm_sem_discrete_kantorovich_existence_pf : clm_sem_discrete_kantorovich_existence := by
  have _ := def_sem_linear_function_pf
  have _ := prop_sem_finite_dim_linear_continuous_pf
  have _ := prop_sem_preimage_closed_pf
  have _ := thm_sem_heine_borel_pf
  have _ := thm_sem_weierstrass_pf
  sorry
-- 離散カップリング集合は凸
theorem clm_sem_coupling_convex_pf : clm_sem_coupling_convex := sorry
-- 最適解集合は凸かつコンパクト
theorem clm_sem_optimal_face_pf : clm_sem_optimal_face := by
  have _ := clm_sem_coupling_convex_pf
  have _ := prop_sem_preimage_closed_pf
  sorry
axiom ex_sem_nonunique_example_pf : ex_sem_nonunique_example
axiom rem_sem_lp_uniqueness_pf : rem_sem_lp_uniqueness
axiom def_sem_discrete_entropy_pf : def_sem_discrete_entropy
axiom rem_sem_entropy_convention_pf : rem_sem_entropy_convention
axiom rem_sem_phi_continuous_pf : rem_sem_phi_continuous
axiom def_sem_entropic_ot_pf : def_sem_entropic_ot
-- 負エントロピーの狭義凸性
theorem clm_sem_neg_entropy_strict_convex_pf : clm_sem_neg_entropy_strict_convex := by
  have _ := rem_sem_phi_continuous_pf
  have _ := thm_sem_mvt_pf
  sorry
-- 正則化解の存在と一意性
theorem prop_sem_entropic_existence_unique_pf : prop_sem_entropic_existence_unique := by
  have _ := clm_sem_coupling_convex_pf
  have _ := clm_sem_discrete_kantorovich_existence_pf
  have _ := clm_sem_neg_entropy_strict_convex_pf
  have _ := rem_sem_phi_continuous_pf
  sorry
axiom def_sem_kl_divergence_pf : def_sem_kl_divergence
axiom def_sem_gibbs_kernel_pf : def_sem_gibbs_kernel
-- 正則化 OT は KL 射影である
theorem prop_sem_entropic_kl_projection_pf : prop_sem_entropic_kl_projection := sorry
-- $\varepsilon \to 0$ による非正則化 OT への収束
theorem thm_sem_entropic_convergence_eps_zero_pf : thm_sem_entropic_convergence_eps_zero := by
  have _ := clm_sem_neg_entropy_strict_convex_pf
  have _ := clm_sem_optimal_face_pf
  have _ := prop_sem_strict_convex_unique_min_pf
  sorry
axiom rem_sem_entropic_convergence_eps_infty_pf : rem_sem_entropic_convergence_eps_infty
-- 正則化解の正値性
theorem prop_sem_entropic_positive_solution_pf : prop_sem_entropic_positive_solution := sorry
axiom def_sem_marginal_tangent_pf : def_sem_marginal_tangent
-- 方向空間の直交補空間
theorem prop_sem_tangent_orthogonal_pf : prop_sem_tangent_orthogonal := sorry
-- スケーリング形式
theorem prop_sem_scaling_form_pf : prop_sem_scaling_form := by
  have _ := def_sem_gibbs_kernel_pf
  have _ := prop_sem_entropic_positive_solution_pf
  have _ := prop_sem_tangent_orthogonal_pf
  have _ := rem_sem_entropy_convention_pf
  sorry
axiom rem_sem_dual_scaling_correspondence_pf : rem_sem_dual_scaling_correspondence
-- 行列スケーリング方程式
theorem prop_sem_matrix_scaling_pf : prop_sem_matrix_scaling := sorry
-- 反復の整合性と計算量
theorem prop_sem_sinkhorn_welldefined_pf : prop_sem_sinkhorn_welldefined := sorry
-- スケーリング変数の定数倍の自由度
theorem rem_sem_scaling_ambiguity_pf : rem_sem_scaling_ambiguity := by
  have _ := prop_sem_entropic_existence_unique_pf
  have _ := prop_sem_matrix_scaling_pf
  sorry
-- エントロピー正則化の双対問題
theorem prop_sem_entropic_dual_pf : prop_sem_entropic_dual := by
  have _ := prop_sem_scaling_form_pf
  have _ := rem_sem_entropy_convention_pf
  sorry
axiom rem_sem_soft_constraint_pf : rem_sem_soft_constraint
-- Sinkhorn はブロック座標上昇である
theorem prop_sem_block_coordinate_ascent_pf : prop_sem_block_coordinate_ascent := sorry
axiom rem_sem_gradient_marginal_pf : rem_sem_gradient_marginal
axiom def_sem_hilbert_metric_pf : def_sem_hilbert_metric
axiom thm_sem_birkhoff_pf : thm_sem_birkhoff
axiom thm_sem_sinkhorn_linear_convergence_pf : thm_sem_sinkhorn_linear_convergence
-- 収束率の意味と停止判定
theorem rem_sem_convergence_meaning_pf : rem_sem_convergence_meaning := by
  have _ := rem_sem_gradient_marginal_pf
  sorry
-- 本章のまとめと展望
theorem rem_sem_ch4_summary_pf : rem_sem_ch4_summary := by
  have _ := prop_sem_block_coordinate_ascent_pf
  have _ := prop_sem_entropic_dual_pf
  have _ := prop_sem_scaling_form_pf
  have _ := rem_sem_soft_constraint_pf
  have _ := thm_sem_sinkhorn_linear_convergence_pf
  sorry
-- 地の距離行列
theorem def_sem_ground_metric_pf : def_sem_ground_metric := by
  have _ := def_sem_metric_space_pf
  sorry
axiom def_sem_wasserstein_discrete_pf : def_sem_wasserstein_discrete
-- Minkowski の不等式（重み付き）
theorem clm_sem_minkowski_pf : clm_sem_minkowski := sorry
-- 離散 Wasserstein 距離の距離性
theorem thm_sem_wasserstein_is_distance_pf : thm_sem_wasserstein_is_distance := by
  have _ := clm_sem_discrete_kantorovich_existence_pf
  have _ := clm_sem_minkowski_pf
  sorry
axiom rem_sem_wasserstein_p_leq_1_pf : rem_sem_wasserstein_p_leq_1
-- 本章のまとめと展望
theorem rem_sem_ch5_summary_pf : rem_sem_ch5_summary := by
  have _ := thm_sem_wasserstein_is_distance_pf
  sorry
axiom def_sem_dual_feasible_pf : def_sem_dual_feasible
-- 弱双対性
theorem prop_sem_weak_duality_classical_pf : prop_sem_weak_duality_classical := sorry
-- Kantorovich 双対定理
theorem thm_sem_kantorovich_duality_pf : thm_sem_kantorovich_duality := by
  have _ := prop_sem_weak_duality_classical_pf
  sorry
-- ハード制約とそのソフト化
theorem rem_sem_hard_vs_soft_pf : rem_sem_hard_vs_soft := by
  have _ := prop_sem_entropic_dual_pf
  have _ := rem_sem_soft_constraint_pf
  sorry
axiom rem_sem_dual_interpretation_pf : rem_sem_dual_interpretation
-- 相補性条件
theorem prop_sem_complementary_slackness_pf : prop_sem_complementary_slackness := by
  have _ := thm_sem_kantorovich_duality_pf
  sorry
axiom rem_sem_support_characterization_pf : rem_sem_support_characterization
axiom def_sem_c_transform_def_pf : def_sem_c_transform_def
-- $c$-変換による一変数化
theorem prop_sem_c_transform_reduction_pf : prop_sem_c_transform_reduction := by
  have _ := thm_sem_kantorovich_duality_pf
  sorry
-- $c$-凹関数と Legendre 変換
theorem rem_sem_c_concave_pf : rem_sem_c_concave := by
  have _ := thm_sem_kantorovich_duality_pf
  sorry
axiom def_sem_soft_min_ch6_pf : def_sem_soft_min_ch6
axiom def_sem_soft_c_transform_pf : def_sem_soft_c_transform
-- Sinkhorn はソフト交互 $c$-変換である
theorem prop_sem_sinkhorn_soft_c_pf : prop_sem_sinkhorn_soft_c := sorry
-- 本章のまとめと展望
theorem rem_sem_ch6_summary_pf : rem_sem_ch6_summary := by
  have _ := prop_sem_c_transform_reduction_pf
  have _ := prop_sem_complementary_slackness_pf
  have _ := prop_sem_sinkhorn_soft_c_pf
  have _ := thm_sem_kantorovich_duality_pf
  sorry
-- 2-Wasserstein 距離
theorem def_sem_w2_def_pf : def_sem_w2_def := by
  have _ := def_sem_kantorovich_pf
  sorry
-- $\Wass_2$ は距離である
theorem rem_sem_w2_is_metric_pf : rem_sem_w2_is_metric := by
  have _ := thm_sem_wasserstein_is_distance_pf
  sorry
axiom clm_sem_brenier_pf : clm_sem_brenier
-- ch06 との対応
theorem rem_sem_brenier_from_dual_pf : rem_sem_brenier_from_dual := by
  have _ := prop_sem_complementary_slackness_pf
  sorry
axiom def_sem_constant_speed_geodesic_pf : def_sem_constant_speed_geodesic
-- McCann の変位補間
theorem def_sem_mccann_interpolation_pf : def_sem_mccann_interpolation := by
  have _ := clm_sem_brenier_pf
  sorry
-- 変位補間は測地線である
theorem thm_sem_mccann_geodesic_pf : thm_sem_mccann_geodesic := by
  have _ := rem_sem_w2_is_metric_pf
  sorry
axiom rem_sem_particle_picture_pf : rem_sem_particle_picture
-- 変位凸性と曲率への布石
theorem rem_sem_displacement_convexity_preview_pf : rem_sem_displacement_convexity_preview := by
  have _ := clm_sem_brenier_pf
  sorry
axiom def_sem_continuity_equation_pf : def_sem_continuity_equation
axiom rem_sem_ce_weak_meaning_pf : rem_sem_ce_weak_meaning
axiom clm_sem_disintegration_pf : clm_sem_disintegration
axiom def_sem_bb_action_pf : def_sem_bb_action
axiom def_sem_theta_pf : def_sem_theta
-- $\theta$ は凸かつ下半連続
theorem prop_sem_theta_convex_pf : prop_sem_theta_convex := sorry
axiom def_sem_bb_convex_pf : def_sem_bb_convex
-- Benamou--Brenier
theorem thm_sem_benamou_brenier_pf : thm_sem_benamou_brenier := by
  have _ := def_sem_mccann_interpolation_pf
  sorry
-- 下限の達成
theorem clm_sem_bb_existence_pf : clm_sem_bb_existence := by
  have _ := clm_sem_brenier_pf
  sorry
axiom rem_sem_bb_trinity_pf : rem_sem_bb_trinity
axiom clm_sem_tangent_space_pf : clm_sem_tangent_space
axiom def_sem_otto_inner_pf : def_sem_otto_inner
-- $\Wass_2$ は Otto 計量の測地距離
theorem rem_sem_otto_w2_pf : rem_sem_otto_w2 := by
  have _ := thm_sem_benamou_brenier_pf
  sorry
axiom def_sem_first_variation_pf : def_sem_first_variation
-- Wasserstein 勾配
theorem clm_sem_w2_grad_formula_pf : clm_sem_w2_grad_formula := sorry
axiom def_sem_jko_scheme_pf : def_sem_jko_scheme
-- JKO の収束と勾配流
theorem clm_sem_jko_limit_pf : clm_sem_jko_limit := by
  have _ := clm_sem_w2_grad_formula_pf
  sorry
-- Jordan--Kinderlehrer--Otto
theorem thm_sem_jko_heat_pf : thm_sem_jko_heat := by
  have _ := clm_sem_jko_limit_pf
  sorry
axiom rem_sem_fokker_planck_pf : rem_sem_fokker_planck
-- $K$-変位凸性
theorem def_sem_k_displacement_convex_pf : def_sem_k_displacement_convex := by
  have _ := def_sem_mccann_interpolation_pf
  sorry
axiom rem_sem_k_as_curvature_pf : rem_sem_k_as_curvature
axiom clm_sem_jacobian_concave_pf : clm_sem_jacobian_concave
axiom rem_sem_why_convex_gradient_pf : rem_sem_why_convex_gradient
-- $\R^d$ 上でのエントロピーの変位凸性
theorem thm_sem_entropy_displacement_convex_pf : thm_sem_entropy_displacement_convex := by
  have _ := clm_sem_jacobian_concave_pf
  sorry
-- 次元つきの精密化
theorem rem_sem_renyi_functional_pf : rem_sem_renyi_functional := by
  have _ := clm_sem_jacobian_concave_pf
  sorry
axiom def_sem_cd_kn_pf : def_sem_cd_kn
-- Lott--Sturm--Villani の同値性
theorem clm_sem_lsv_pf : clm_sem_lsv := by
  have _ := thm_sem_entropy_displacement_convex_pf
  sorry
-- この同値性の意義
theorem rem_sem_cd_significance_pf : rem_sem_cd_significance := by
  have _ := clm_sem_jacobian_concave_pf
  sorry
-- エントロピー正則化による一意性の回復
theorem rem_sem_entropy_uniqueness_preview_pf : rem_sem_entropy_uniqueness_preview := by
  have _ := def_sem_discrete_entropy_pf
  sorry
-- なぜ運動エネルギーか
theorem rem_sem_why_kinetic_pf : rem_sem_why_kinetic := by
  have _ := thm_sem_benamou_brenier_pf
  sorry

end Ot.Generated
