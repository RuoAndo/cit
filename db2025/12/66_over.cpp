#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <algorithm>  // std::sort, std::stable_sort
#include <numeric>    // std::partial_sum（累積の例）

int main() {
    // 行データ例（payment_date順に並べたい支払いデータを想定）
    struct Row {
        long long payment_date; // 例：UNIX時間や連番（ORDER BYキー）
        long long amount;       // 例：支払額
        int payment_id;         // 同一日時の順序安定化用（任意）
    };

    std::vector<Row> rows = {
        {1700000300, 130, 3},
        {1700000100, 100, 1},
        {1700000200,  90, 2},
        {1700000300, 200, 4},
        {1700000400, 150, 5}
    };

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL:
    //   ... OVER (ORDER BY payment_date)
    //
    // C++:
    //   1) std::sort / std::stable_sort で payment_date による整列（ORDER BY）
    //   2) 整列後に 1パス走査で累積・差分・順位・前後参照などを計算
    // ------------------------------------------------------------

    // ORDER BY 相当（同一 payment_date 内の順序も決めたいなら tie-break を入れる）
    std::stable_sort(rows.begin(), rows.end(),
        [](const Row& a, const Row& b) {
            if (a.payment_date != b.payment_date) return a.payment_date < b.payment_date;
            return a.payment_id < b.payment_id; // 任意：安定化
        });

    // 整列後1パス走査：例として「累積和」と「前回差分」を同時に計算
    std::cout << "payment_date amount cumulative diff_from_prev\n";

    long long cumulative = 0;
    bool has_prev = false;
    long long prev_amount = 0;

    for (const auto& r : rows) {
        cumulative += r.amount;                      // SUM(...) OVER (ORDER BY ...) 相当（累積）
        long long diff = has_prev ? (r.amount - prev_amount) : 0; // LAG相当の差分（先頭は0扱い例）

        std::cout << r.payment_date << " "
                  << r.amount << " "
                  << cumulative << " "
                  << (has_prev ? diff : 0) << "\n";

        prev_amount = r.amount;
        has_prev = true;
    }

    return 0;
}
