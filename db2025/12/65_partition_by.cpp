#include <iostream>      // 入出力
#include <vector>        // std::vector
#include <unordered_map> // std::unordered_map
#include <algorithm>     // std::sort

int main() {
    // 行データ例（payment の customer_id と amount を想定）
    struct Row {
        int customer_id;
        double amount;
        int payment_id;
    };

    std::vector<Row> rows = {
        {2, 7.99, 201}, {1, 5.99, 101}, {2, 1.99, 202}, {1, 2.99, 102},
        {3, 4.99, 301}, {1, 5.99, 103}, {3, 9.99, 303}, {2, 7.99, 203}
    };

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL（例：解析関数のPARTITION BY）:
    //   AVG(amount) OVER (PARTITION BY customer_id)
    //   RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC)
    //
    // C++（代表例）:
    //   A) キー別グルーピング（unordered_map<key, vector<row>>）
    //   B) キーソートによる区間化（sort で同キーを連続にして1パス処理）
    // ------------------------------------------------------------

    // ============================================================
    // A) キー別グルーピング：unordered_map で分ける
    // ============================================================
    std::unordered_map<int, std::vector<Row>> groups;
    groups.reserve(rows.size());

    for (const auto& r : rows) {
        groups[r.customer_id].push_back(r); // customer_id ごとに溜める
    }

    std::cout << "== A) Grouping by key (unordered_map) ==\n";
    for (auto& [cid, vec] : groups) {
        // 例：グループ内を amount DESC に並べる（ORDER BY 相当）
        std::sort(vec.begin(), vec.end(), [](const Row& a, const Row& b) {
            if (a.amount != b.amount) return a.amount > b.amount;
            return a.payment_id < b.payment_id;
        });

        std::cout << "customer_id=" << cid << " size=" << vec.size() << "\n";
        for (const auto& x : vec) {
            std::cout << "  payment_id=" << x.payment_id << " amount=" << x.amount << "\n";
        }
    }

    // ============================================================
    // B) キーソートによる区間化：sortして同キーを連続化→1パス
    //    メモリ効率がよく、解析関数の「パーティション区間」っぽい
    // ============================================================
    std::sort(rows.begin(), rows.end(), [](const Row& a, const Row& b) {
        if (a.customer_id != b.customer_id) return a.customer_id < b.customer_id; // PARTITION
        if (a.amount != b.amount) return a.amount > b.amount;                     // ORDER BY（例）
        return a.payment_id < b.payment_id;
    });

    std::cout << "\n== B) Key sort -> contiguous ranges (scan) ==\n";

    size_t i = 0;
    while (i < rows.size()) {
        int cid = rows[i].customer_id;

        // [i, j) が同一 customer_id の区間
        size_t j = i;
        while (j < rows.size() && rows[j].customer_id == cid) j++;

        std::cout << "customer_id=" << cid << " range=[" << i << "," << j << ") size=" << (j - i) << "\n";
        for (size_t k = i; k < j; ++k) {
            std::cout << "  payment_id=" << rows[k].payment_id << " amount=" << rows[k].amount << "\n";
        }

        // 次のパーティションへ
        i = j;
    }

    return 0;
}
