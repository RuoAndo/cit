# plot_pay_count_sql_hardcoded.py
# ------------------------------------------------------------
# SQLite DB (mydata.db) を開き、SQLで顧客別の支払回数(pay_count)を集計して可視化
#   SQL: SELECT customer_id, COUNT(*) AS pay_count FROM payment GROUP BY customer_id;
# 依存: pandas, matplotlib
# ------------------------------------------------------------
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ===== 設定（必要ならここだけ編集）========================================
DB_PATH = Path("mydata.db")     # 例: r"C:\Users\user\data\mydata.db"
OUT_DIR = Path("./")  # 出力先
TOP_N   = 30                               # 上位N本の棒グラフ
SHOW    = True                             # その場表示: True / 非表示: False
# =========================================================================

SQL = """
SELECT customer_id, COUNT(*) AS pay_count
FROM payment
GROUP BY customer_id
"""

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) DB接続 & SQL集計
    if not DB_PATH.exists():
        raise FileNotFoundError(f"DBが見つかりません: {DB_PATH}")
    with sqlite3.connect(str(DB_PATH)) as conn:
        df = pd.read_sql_query(SQL, conn)

    # 2) CSV保存
    csv_path = OUT_DIR / "pay_count.csv"
    df.to_csv(csv_path, index=False)

    # 3) 可視化（各図は単独プロット、色指定なし）
    # 3-1) 上位Nの棒グラフ
    topn = df.sort_values("pay_count", ascending=False).head(TOP_N)
    plt.figure()
    plt.bar(topn["customer_id"].astype(str), topn["pay_count"])
    plt.title(f"Top {len(topn)} Customers by Pay Count")
    plt.xlabel("customer_id")
    plt.ylabel("pay_count")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "pay_count_topN_bar.png")
    if SHOW:
        plt.show()
    plt.close()

    # 3-2) 全体分布ヒストグラム
    plt.figure()
    plt.hist(df["pay_count"], bins=30)
    plt.title("Distribution of Pay Count per Customer")
    plt.xlabel("pay_count")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "pay_count_hist.png")
    if SHOW:
        plt.show()
    plt.close()

    print(f"Saved: {csv_path}")
    print(f"Saved: {OUT_DIR / 'pay_count_topN_bar.png'}")
    print(f"Saved: {OUT_DIR / 'pay_count_hist.png'}")

if __name__ == "__main__":
    main()
