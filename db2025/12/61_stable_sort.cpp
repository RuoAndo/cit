#include <iostream>      // 入出力
#include <vector>        // std::vector
#include <algorithm>     // std::stable_sort, std::sort
#include <unordered_map> // std::unordered_map
#include <iomanip>       // 表示整形

int main() {
    // 行データ例（payment の customer_id と amount を想定）
    struct Row {
        int customer_id;
        double amount;
        int payment_id;
    };

    std::vector<Row> rows = {
        {1, 5.99, 101}, {1, 2.99, 102}, {1, 5.99, 103},
        {2, 7.99, 201}, {2, 1.99, 202}, {2, 7.99, 203},
        {3, 4.99, 301}, {3, 4.99, 302}, {3, 9.99, 303}
    };

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL（例：顧客ごとの支払い順位）:
    //   RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC)
    //
    // C++（代表例）:
    //   1) PARTITION BY 相当：customer_id ごとに分ける（ここではソートで連続区間化）
    //   2) ORDER BY 相当：amount DESC（同キーは安定ソートで順序維持も可能）
    //   3) RANK 相当：同額は同順位、次の順位が飛ぶ（1,1,3,…）
    //
    // 参考：
    //   DENSE_RANK 相当は「飛ばない」（1,1,2,…）
    // ------------------------------------------------------------

    // ============================================================
    // A) ソート後走査による順位付け（RANK / DENSE_RANK 両対応）
    // ============================================================

    // stable_sort を使い、同順位（同額）の内部順序（payment_idなど）を保ちやすくする
    std::stable_sort(rows.begin(), rows.end(),
        [](const Row& a, const Row& b) {
            if (a.customer_id != b.customer_id) return a.customer_id < b.customer_id; // PARTITION
            if (a.amount != b.amount) return a.amount > b.amount;                     // ORDER BY amount DESC
            return a.payment_id < b.payment_id;                                       // 追加の安定化（任意）
        });

    std::cout << "== RANK / DENSE_RANK via sort + scan ==\n";
    std::cout << std::fixed << std::setprecision(2);

    int current_customer = -1;
    double prev_amount = 0.0;

    int row_index_in_group = 0; // 1-basedで使う（RANKの飛び計算用）
    int rank = 0;               // RANK（飛ぶ）
    int dense_rank = 0;         // DENSE_RANK（飛ばない）

    for (const auto& r : rows) {
        // 新しいグループ開始（PARTITION切り替え）
        if (r.customer_id != current_customer) {
            current_customer = r.customer_id;
            prev_amount = r.amount;

            row_index_in_group = 1;
            rank = 1;
            dense_rank = 1;
        } else {
            row_index_in_group++;

            // 同額なら同順位、違えば順位更新
            if (r.amount != prev_amount) {
                // RANK：現在の行番号が順位になる（同額があれば飛ぶ）
                rank = row_index_in_group;

                // DENSE_RANK：値が変わった回数で連番
                dense_rank++;

                prev_amount = r.amount;
            }
        }

        std::cout << "customer_id=" << r.customer_id
                  << " payment_id=" << r.payment_id
                  << " amount=" << r.amount
                  << " rank=" << rank
                  << " dense_rank=" << dense_rank
                  << "\n";
    }

    // ============================================================
    // B) 座標圧縮（同じ値に同じ順位番号を割り当てる準備）
    //    ※ここでは「amount のユニーク値」→「順位用ID」へ変換する例
    // ============================================================

    std::vector<double> values;
    values.reserve(rows.size());
    for (const auto& r : rows) values.push_back(r.amount);

    // amount のユニーク値作成（降順で圧縮IDを作りたいので降順ソート）
    std::sort(values.begin(), values.end(), std::greater<double>());
    values.erase(std::unique(values.begin(), values.end()), values.end());

    // 値→圧縮ID（1始まり）
    std::unordered_map<double, int> compress;
    compress.reserve(values.size());
    for (int i = 0; i < (int)values.size(); ++i) {
        compress[values[i]] = i + 1; // 大きいほど小さいID（降順）
    }

    std::cout << "\n== Coordinate compression for amount (global) ==\n";
    for (double v : values) {
        std::cout << "amount=" << v << " -> id=" << compress[v] << "\n";
    }

    return 0;
}
