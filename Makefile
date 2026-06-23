# 最適輸送セミナー
#
# source of truth は各 tex/*.tex のみ。
# Web 版（site/）の md/html は生成物であり、編集も git 管理もしない。

.PHONY: site pdf ambrosio-site ambrosio-pdf

# --- Cuturi (seminar/) ---
site:
	node seminar/site/scripts/tex2md.mjs
	node seminar/site/scripts/build.mjs
	@echo "→ seminar/site/dist/index.html をブラウザで開いてください"

pdf:
	cd seminar/tex && latexmk

# --- Ambrosio (ambrosio/) ---
ambrosio-site:
	node ambrosio/site/scripts/tex2md.mjs
	node ambrosio/site/scripts/build.mjs
	@echo "→ ambrosio/site/dist/index.html をブラウザで開いてください"

ambrosio-pdf:
	cd ambrosio/tex && latexmk
