#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <deque>      // std::deque
#include <numeric>    // 参考用（今回は手計算で更新）

int main() {
    // 行データ例（時系列に ORDER BY 済みの amount を想定）
    std::vector<long long> amount = {100, 130, 90, 200, 200, 150, 120};

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL（固定幅の行ウィンドウ例）:
    //   AVG(amount) OVER (
    //     ORDER BY payment_date
    //     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    //   ) AS moving_avg_3
    //
    // C++（代表例）:
    //   A) スライディングウィンドウ（固定幅）：キュー/リング＋sum更新
    //   B) deque：最大/最小など「単調キュー」向き（窓内集約の高速化）
    //   C) 尺取り法（two pointers）：条件を満たす可変幅ウィンドウ
    // ------------------------------------------------------------

    // ============================================================
    // A) スライディングウィンドウ（固定幅3）の移動平均
    // ============================================================
    std::cout << "== A) fixed window moving avg (k=3) ==\n";
    const size_t k = 3;
    std::deque<long long> q;  // 窓内要素（固定幅ならvector+indexでも可）
    long long sum = 0;

    for (size_t i = 0; i < amount.size(); ++i) {
        // 右端へ追加
        q.push_back(amount[i]);
        sum += amount[i];

        // 窓が大きすぎたら左端を捨てる
        if (q.size() > k) {
            sum -= q.front();
            q.pop_front();
        }

        // SQLのROWS BETWEEN 2 PRECEDING AND CURRENT ROW相当：
        // 先頭の数行は要素数がk未満（SQLでも窓が縮む）
        double avg = static_cast<double>(sum) / static_cast<double>(q.size());

        std::cout << "i=" << i
                  << " amount=" << amount[i]
                  << " window_size=" << q.size()
                  << " moving_avg=" << avg
                  << "\n";
    }

    // ============================================================
    // B) deque（単調キュー）：窓内最大値を O(1) 平均で取る例（k=3）
    //    ※ SQLでいう「MAX(...) OVER (ROWS BETWEEN ...)」相当の発想
    // ============================================================
    std::cout << "\n== B) deque monotonic queue (window max, k=3) ==\n";
    std::deque<size_t> dq; // 値ではなく index を保持（古い要素の期限切れ判定のため）

    for (size_t i = 0; i < amount.size(); ++i) {
        // 右端から：新要素より小さいものを捨てる（最大用の単調減少）
        while (!dq.empty() && amount[dq.back()] <= amount[i]) dq.pop_back();
        dq.push_back(i);

        // 左端から：窓の外に出たindexを捨てる
        if (!dq.empty() && dq.front() + k <= i) dq.pop_front();

        long long current_max = amount[dq.front()];
        std::cout << "i=" << i
                  << " amount=" << amount[i]
                  << " window_max=" << current_max
                  << "\n";
    }

    // ============================================================
    // C) 尺取り法（two pointers）：可変幅ウィンドウの例
    //    例：合計が S 以上になる最短区間長（正の値前提）
    //    ※ SQLでいう「条件付きウィンドウ」を手続き的に作る発想
    // ============================================================
    std::cout << "\n== C) two pointers (min length subarray with sum >= S) ==\n";
    const long long S = 300;

    size_t left = 0;
    long long cur = 0;
    size_t best = amount.size() + 1;

    for (size_t right = 0; right < amount.size(); ++right) {
        cur += amount[right];

        // 条件を満たす間、左端を縮めて最短化
        while (cur >= S) {
            best = std::min(best, right - left + 1);
            cur -= amount[left];
            left++;
        }
    }

    if (best == amount.size() + 1) {
        std::cout << "No subarray found (sum >= " << S << ")\n";
    } else {
        std::cout << "Min length with sum >= " << S << " : " << best << "\n";
    }

    return 0;
}
