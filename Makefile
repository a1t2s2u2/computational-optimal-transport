# 最適輸送セミナー
#
# source of truth は各 tex/*.tex のみ。
# Web 版（site/）の md/html は生成物であり、編集も git 管理もしない。

.PHONY: site pdf wasserstein-site wasserstein-pdf

# --- Cuturi ---
site:
	node seminar/cuturi/site/scripts/tex2md.mjs
	node seminar/cuturi/site/scripts/build.mjs
	@echo "→ seminar/cuturi/site/dist/index.html をブラウザで開いてください"

pdf:
	cd seminar/cuturi/tex && latexmk

# --- Wasserstein ---
wasserstein-site:
	node seminar/wasserstein/site/scripts/tex2md.mjs
	node seminar/wasserstein/site/scripts/build.mjs
	@echo "→ seminar/wasserstein/site/dist/index.html をブラウザで開いてください"

wasserstein-pdf:
	cd seminar/wasserstein/tex && latexmk
