#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <optional>   // std::optional（境界のNULL相当）

int main() {
    // 行データ例（payment_date順に並んでいる前提の amount 列）
    std::vector<long long> amount = {100, 130, 90, 200, 200, 150};

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL:
    //   amount - LAG(amount) OVER (ORDER BY payment_date) AS diff_from_prev
    //
    // C++（代表例）:
    //   A) prev 変数保持（1つ前の値を覚える）
    //   B) 配列 i-1 参照（ランダムアクセス可能なとき）
    //   C) リングバッファ（k遅れ参照やストリーム処理向け）
    // ------------------------------------------------------------

    // ============================================================
    // A) prev変数保持（最小構成）
    // ============================================================
    std::cout << "== A) prev variable ==\n";
    std::optional<long long> prev; // SQLのNULL相当（先頭行）

    for (size_t i = 0; i < amount.size(); ++i) {
        if (!prev.has_value()) {
            std::cout << "i=" << i << " amount=" << amount[i] << " diff=NULL\n";
        } else {
            long long diff = amount[i] - *prev;
            std::cout << "i=" << i << " amount=" << amount[i] << " diff=" << diff << "\n";
        }
        prev = amount[i];
    }

    // ============================================================
    // B) 配列 i-1 参照（単純・高速）
    // ============================================================
    std::cout << "\n== B) index i-1 ==\n";
    for (size_t i = 0; i < amount.size(); ++i) {
        if (i == 0) {
            std::cout << "i=" << i << " amount=" << amount[i] << " diff=NULL\n";
        } else {
            long long diff = amount[i] - amount[i - 1];
            std::cout << "i=" << i << " amount=" << amount[i] << " diff=" << diff << "\n";
        }
    }

    // ============================================================
    // C) リングバッファ（k遅れLAGに拡張しやすい）
    //    例：LAG(amount, k) を k=3 でやるイメージ
    // ============================================================
    std::cout << "\n== C) ring buffer (LAG k=3 example) ==\n";
    const size_t k = 3;
    std::vector<long long> ring(k);
    size_t filled = 0;
    size_t pos = 0;

    for (size_t i = 0; i < amount.size(); ++i) {
        if (filled < k) {
            std::cout << "i=" << i << " amount=" << amount[i] << " lag3=NULL\n";
            ring[pos] = amount[i];
            pos = (pos + 1) % k;
            filled++;
        } else {
            long long lagk = ring[pos];              // k個前
            long long diff = amount[i] - lagk;       // 差分も可能
            std::cout << "i=" << i << " amount=" << amount[i] << " lag3=" << lagk << " diff=" << diff << "\n";
            ring[pos] = amount[i];                   // 現在値で上書き
            pos = (pos + 1) % k;
        }
    }

    return 0;
}
