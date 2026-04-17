"""matplotlib の共通設定."""

from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する.

    macOS の ``Hiragino Sans``, Windows/Linux の ``Yu Gothic``/``Noto Sans CJK JP`` などを
    優先順に試す. マイナス記号の文字化け対策も行う.
    """
    candidates = [
        "Hiragino Sans",
        "Hiragino Maru Gothic Pro",
        "YuGothic",
        "Yu Gothic",
        "Noto Sans CJK JP",
        "IPAexGothic",
        "TakaoGothic",
    ]
    available = {f.name for f in matplotlib.font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    # PDF バックエンドで mathtext グリフ名の非 ASCII エンコードエラーを回避する.
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    # 日本語フォントは数式と衝突しやすいので mathtext は常に Computer Modern を使う.
    plt.rcParams["mathtext.fontset"] = "cm"
