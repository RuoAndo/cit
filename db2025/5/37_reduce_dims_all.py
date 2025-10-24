# reduce_dims_cpu.py
# SQLite DBからCPU/メモリ特徴量を読み込み、PCA→2Dまたは3Dに次元削減して表示

import sqlite3, pandas as pd, numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

DB_PATH  = "cpu_metrics.db"
TABLE    = "cpu_metrics_min"
LIMIT    = 5000
DIM      = 3     # 2 or 3 次元で表示

def load_data():
    con = sqlite3.connect(DB_PATH)
    # 可能なカラムを自動検出（数値列のみ）
    df = pd.read_sql_query(f"SELECT * FROM {TABLE} ORDER BY ts ASC LIMIT {LIMIT}", con)
    con.close()
    # 数値化できる列だけ抽出
    df_num = df.select_dtypes(include=[np.number]).fillna(method="ffill").fillna(0)
    print(f"[INFO] Loaded {len(df)} rows, {df_num.shape[1]} numeric cols.")
    return df, df_num

def reduce_and_plot(df, df_num):
    # 標準化 → PCA
    X_std = StandardScaler().fit_transform(df_num)
    pca = PCA(n_components=DIM)
    X_pca = pca.fit_transform(X_std)
    print(f"[INFO] Explained variance ratio: {pca.explained_variance_ratio_}")

    if DIM == 3:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111, projection="3d")
        sc = ax.scatter(X_pca[:,0], X_pca[:,1], X_pca[:,2],
                        c=df.get("temp_c", pd.Series(0)), cmap="coolwarm", s=15)
        plt.colorbar(sc, label="temp_c (°C)")
        ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_zlabel("PC3")
    else:
        plt.figure(figsize=(8,6))
        plt.scatter(X_pca[:,0], X_pca[:,1],
                    c=df.get("temp_c", pd.Series(0)), cmap="coolwarm", s=20)
        plt.colorbar(label="temp_c (°C)")
        plt.xlabel("PC1"); plt.ylabel("PC2")

    plt.title("PCA 次元削減（cpu_metrics_min）")
    plt.tight_layout()
    plt.show()

def main():
    df, df_num = load_data()
    reduce_and_plot(df, df_num)

if __name__ == "__main__":
    main()
