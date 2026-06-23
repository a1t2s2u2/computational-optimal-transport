# 最適輸送セミナー
#
# source of truth は各 tex/*.tex のみ。
# Web 版（site/）の md/html は生成物であり、編集も git 管理もしない。

.PHONY: site pdf givens-shortt-site givens-shortt-pdf

# --- Cuturi (seminar/) ---
site:
	node seminar/site/scripts/tex2md.mjs
	node seminar/site/scripts/build.mjs
	@echo "→ seminar/site/dist/index.html をブラウザで開いてください"

pdf:
	cd seminar/tex && latexmk

# --- Givens--Shortt ---
givens-shortt-site:
	node givens-shortt/site/scripts/tex2md.mjs
	node givens-shortt/site/scripts/build.mjs
	@echo "→ givens-shortt/site/dist/index.html をブラウザで開いてください"

givens-shortt-pdf:
	cd givens-shortt/tex && latexmk
