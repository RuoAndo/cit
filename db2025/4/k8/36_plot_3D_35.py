# =====================================================================
# 日本語文字化け／豆腐対策 完全版ヘッダ
# ---------------------------------------------------------------------
# ・スクリプト自体は UTF-8 (BOMあり/なしどちらでも可) で保存してください。
# ・PowerShellでは以下を併用するとより確実です:
#     chcp 65001
#     $OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($true)
#     $env:PYTHONIOENCODING = "utf-8"
#     $env:PYTHONUTF8 = "1"
# =====================================================================

import sys, os

# --- 出力系UTF-8設定 ------------------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# --- Matplotlib 日本語フォント設定 ----------------------------------
import matplotlib
from matplotlib import font_manager

# マイナス記号が豆腐(□)になる問題を防止
matplotlib.rcParams["axes.unicode_minus"] = False

# システム／同梱フォント候補リスト（上ほど優先）
_JP_FONT_CANDIDATES = [
    "Yu Gothic", "Meiryo", "MS PGothic", "MS Gothic",
    "Noto Sans CJK JP", "Noto Sans JP", "IPAGothic", "TakaoPGothic"
]

# 同梱フォント（あれば最優先）
_LOCAL_FONT_FILE = "NotoSansCJKjp-Regular.otf"
_LOCAL_FONT_NAME = "Noto Sans CJK JP"  # 上記OTF登録名想定

def _choose_jp_font() -> str | None:
    """日本語フォントを自動検出／同梱優先"""
    # 1) 同梱フォント
    if os.path.exists(_LOCAL_FONT_FILE):
        try:
            font_manager.fontManager.addfont(_LOCAL_FONT_FILE)
            return _LOCAL_FONT_NAME
        except Exception:
            pass

    # 2) システムフォント
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in _JP_FONT_CANDIDATES:
        if name in installed:
            return name
    return None

# フォント決定・適用
_SELECTED_FONT = _choose_jp_font()
if _SELECTED_FONT:
    matplotlib.rcParams["font.family"] = [_SELECTED_FONT]

# --- 使用フォント情報を出力 ----------------------------------------
try:
    print(f"[FONT] 使用フォント: {_SELECTED_FONT or '（日本語フォント未検出）'}")
except Exception:
    pass

# =====================================================================
# ↑ここまでを既存スクリプトの import 群の直後に貼るだけでOK
# =====================================================================
