#include <iostream>     // 入出力
#include <vector>       // std::vector
#include <string>       // std::string
#include <unordered_map>// std::unordered_map
#include <utility>      // std::pair
#include <iomanip>      // std::setprecision

int main() {
    // 行データ例（payment の customer_id と amount を想定）
    struct Row {
        int customer_id;
        double amount;
    };
    std::vector<Row> rows = {
        {1, 2.99}, {1, 5.99}, {2, 1.99}, {2, 7.99}, {1, 3.99}, {3, 4.99}
    };

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL:
    //   AVG(amount) OVER (PARTITION BY customer_id)
    //
    // C++（代表例）:
    //   A) グループ別に合計と件数を保持するハッシュ（2パス集計）
    //   B) オンライン平均（Welford法）で逐次更新（1パス）
    // ------------------------------------------------------------

    // ============================================================
    // A) 2パス集計：unordered_map で (sum, count) を保持
    // ============================================================

    // 1パス目：customer_id ごとの (sum, count) を作る
    std::unordered_map<int, std::pair<double, long long>> agg; // {id -> {sum, count}}
    agg.reserve(rows.size());

    for (const auto& r : rows) {
        auto& sc = agg[r.customer_id];
        sc.first  += r.amount; // sum
        sc.second += 1;        // count
    }

    // 2パス目：各行に「その customer の平均」を付与して表示
    std::cout << "== Two-pass (hash sum+count) ==\n";
    std::cout << std::fixed << std::setprecision(2);
    for (const auto& r : rows) {
        const auto& sc = agg.at(r.customer_id);
        double avg = sc.first / static_cast<double>(sc.second);
        double diff = r.amount - avg; // 例：平均との差（外れ値検出の足場）
        std::cout << "customer_id=" << r.customer_id
                  << " amount=" << r.amount
                  << " avg=" << avg
                  << " diff=" << diff
                  << "\n";
    }

    // ============================================================
    // B) オンライン平均：Welford法（1パスで平均を更新）
    //    ※「各行に最終平均を付ける」用途は本来2パスが素直
    //      Welfordは「逐次で平均・分散を追う」用途に強い
    // ============================================================

    struct Welford {
        long long n = 0;   // 件数
        double mean = 0.0; // 平均
        double M2 = 0.0;   // 分散用の累積（必要なら）
        void add(double x) {
            n++;
            double delta = x - mean;
            mean += delta / static_cast<double>(n);
            double delta2 = x - mean;
            M2 += delta * delta2; // 分散が必要なときに使う
        }
        double variance() const { return (n > 1) ? (M2 / static_cast<double>(n - 1)) : 0.0; }
    };

    std::unordered_map<int, Welford> w; // {id -> online stats}
    w.reserve(rows.size());

    std::cout << "\n== Online (Welford) per row ==\n";
    for (const auto& r : rows) {
        auto& s = w[r.customer_id];
        s.add(r.amount);
        // ここで出す mean は「その時点までの逐次平均」
        std::cout << "customer_id=" << r.customer_id
                  << " amount=" << r.amount
                  << " running_mean=" << s.mean
                  << " n=" << s.n
                  << "\n";
    }

    return 0;
}
