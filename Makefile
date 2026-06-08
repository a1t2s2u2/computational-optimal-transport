# 計算最適輸送セミナー
#
# source of truth は seminar/tex/*.tex のみ。
# Web 版（seminar/site/dist）の html は生成物であり、編集も git 管理もしない。
#
#   make site   tex → *.html を生成し、ローカルで確認できる状態にする
#   make pdf    main.tex から PDF を生成する（latexmk）

.PHONY: site pdf

site:
	node seminar/site/scripts/build.mjs
	@echo "→ seminar/site/dist/index.html をブラウザで開いてください"

pdf:
	cd seminar/tex && latexmk
