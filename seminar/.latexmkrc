# cuturi/translation/.latexmkrc を共有（preamble.tex の共有と同じ方針）
do "../cuturi/translation/.latexmkrc";

# seminar 側ではセミナー本編 main.tex に加え，発表回ごとの main_MMDD.tex も既定でビルドする．
# main_MMDD.tex は xr 経由で main.aux のラベルを引くため，main.tex を先に並べる．
@default_files = ('main.tex', 'main_0519.tex');
