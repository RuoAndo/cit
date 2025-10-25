# reduce_dims_cpu_2d_full.py
# SQLite: cpu_metrics.db / cpu_metrics_min からデータ読み込み
# → 数値列を標準化 → PCA(2D) → 散布図（色: temp_c）を保存＆表示
# 途中経過は [INFO HH:MM:SS] 形式で日本語ログ出力。
# 文字化け対策（UTF-8 / 日本語フォント）込み。

import os
import sys
import sqlite3
from datetime import datetime

# --- 文字化け対策: 標準出力をUTF-8化 ---
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import pandas as pd
import numpy as np
import matplotlib
matplotlib.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans CJK JP", "IPAGothic"]
matplotlib.rcParams["axes.unicode_minus"] = False  # マイナス記号の豆腐対策
import matplotlib.pyplot as plt

# scikit-learn があれば使い、無ければNumPyで代替
try:
    from sklearn.decomposition import PCA as SKPCA
    from sklearn.preprocessing import StandardScaler as SKScaler
    HAVE_SKLEARN = True
except Exception:
    HAVE_SKLEARN = False

# ===== 設定（必要に応じて書き換え） =====
DB_PATH   = "cpu_metrics.db"
TABLE     = "cpu_metrics_min"
LIMIT     = 5000                # 取得最大件数（時系列昇順で）
OUT_PNG   = "pca_2d.png"
USE_ONLY_MIN_COLS = True        # True: ['cpu_percent','mem_shared','temp_c'] だけでPCA
ALLOW_NULL_COLOR  = True        # temp_c が欠損でも色付けのため 0.0 で塗る
# =======================================

def log(msg: str):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[INFO {now}] {msg}")

def standardize_numpy(X: np.ndarray):
    mean = np.nanmean(X, axis=0)
    std  = np.nanstd(X, axis=0, ddof=0)
    std[std == 0] = 1.0
    return (X - mean) / std, mean, std

def pca_numpy(Xz: np.ndarray, k: int = 2):
    U, S, Vt = np.linalg.svd(Xz, full_matrices=False)
    V = Vt.T
    comps = V[:, :k]
    X_pca = Xz @ comps
    total = (S**2).sum()
    evr = (S[:k]**2) / total if total > 0 else np.zeros(k)
    return X_pca, evr, comps

def load_data():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"DBファイルが見つかりません: {DB_PATH}")
    log(f"DB読込開始: {DB_PATH} / {TABLE} / LIMIT={LIMIT}")

    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT * FROM {TABLE} ORDER BY ts ASC LIMIT {LIMIT}",
        con
    )
    con.close()

    if df.empty:
        raise SystemExit("データが見つかりません。")

    log(f"取得行数: {len(df)} 列数: {df.shape[1]}")

    # PCAに使う列を決める
    if USE_ONLY_MIN_COLS and all(c in df.columns for c in ["cpu_percent","mem_shared","temp_c"]):
        use_cols = ["cpu_percent","mem_shared","temp_c"]
        df_num = df[use_cols].copy()
        log(f"PCA対象列（固定）: {use_cols}")
    else:
        # 数値列を自動抽出
        df_num = df.select_dtypes(include=[np.number]).copy()
        log(f"PCA対象列（自動抽出 数値列）: {list(df_num.columns)}")

    # 欠損処理: 前方補完 → 残りを0埋め
    null_before = int(df_num.isna().sum().sum())
    df_num = df_num.fillna(method="ffill").fillna(0)
    null_after = int(df_num.isna().sum().sum())
    log(f"欠損値: 前 {null_before} → 後 {null_after}（前方補完→0埋め）")

    if df_num.shape[1] < 2:
        raise SystemExit("PCAには2列以上の数値列が必要です。")

    return df, df_num

def reduce_to_2d(df_num: pd.DataFrame):
    log("標準化開始")
    X = df_num.to_numpy(dtype=float)

    if HAVE_SKLEARN:
        scaler = SKScaler()
        Xz = scaler.fit_transform(X)
        log("標準化完了（scikit-learn）")
        log("PCA(2D) 開始（scikit-learn）")
        pca = SKPCA(n_components=2)
        X_pca = pca.fit_transform(Xz)
        evr = pca.explained_variance_ratio_
        comps = pca.components_.T
        log(f"PCA完了: 寄与率 = [{evr[0]:.4f}, {evr[1]:.4f}] / 合計 {evr.sum():.4f}")
    else:
        Xz, mean, std = standardize_numpy(X)
        log("標準化完了（NumPy）")
        log("PCA(2D) 開始（NumPy SVD）")
        X_pca, evr, comps = pca_numpy(Xz, k=2)
        log(f"PCA完了: 寄与率 = [{evr[0]:.4f}, {evr[1]:.4f}] / 合計 {evr.sum():.4f}")

    # 主成分寄与の上位特徴量を表示
    try:
        feature_names = df_num.columns.to_list()
        for i in range(2):
            w = np.abs(comps[:, i])
            top_idx = w.argsort()[::-1][:3]
            tops = ", ".join(f"{feature_names[j]}({w[j]:.3f})" for j in top_idx)
            log(f"PC{i+1} 主要寄与Top3: {tops}")
    except Exception:
        pass

    return X_pca

def plot_2d(df: pd.DataFrame, X_pca: np.ndarray):
    log("プロット作成")
    # 色は temp_c を利用（欠損は0.0）
    if "temp_c" in df.columns:
        color = df["temp_c"].fillna(0.0 if ALLOW_NULL_COLOR else df["temp_c"].median())
    else:
        color = np.zeros(len(df))

    plt.figure(figsize=(9, 6))
    sc = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=color, s=14)
    if "temp_c" in df.columns:
        cbar = plt.colorbar(sc)
        cbar.set_label("temp_c (°C)")

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA 2次元削減（cpu_metrics_min）")
    plt.tight_layout()

    try:
        plt.savefig(OUT_PNG, dpi=150)
        log(f"画像保存: {os.path.abspath(OUT_PNG)}")
    except Exception as e:
        log(f"画像保存に失敗: {e}")

    plt.show()
    log("プロット完了")

def main():
    df, df_num = load_data()
    X_pca = reduce_to_2d(df_num)
    plot_2d(df, X_pca)

if __name__ == "__main__":
    main()
