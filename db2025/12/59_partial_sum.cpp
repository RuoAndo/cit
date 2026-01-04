#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <numeric>    // std::partial_sum
#include <algorithm> // std::sort

int main() {
    // 元データ（例：amount 列）
    std::vector<long long> amount = {10, 20, 30, 40};

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL:
    //   SUM(amount) OVER (ORDER BY payment_date)
    //
    // C++:
    //   1) payment_date に相当するキーで sort（ORDER BY）
    //   2) std::partial_sum による累積和
    // ------------------------------------------------------------

    // ※ ここでは既に ORDER BY 済みと仮定
    // std::sort(amount.begin(), amount.end()); // 必要なら事前ソート

    // 累積和を格納する配列
    std::vector<long long> cumulative(amount.size());

    // ORDER BY 後の列に対する累積和（SUM OVER）
    std::partial_sum(amount.begin(), amount.end(), cumulative.begin());

    // 結果出力
    for (auto v : cumulative) {
        std::cout << v << " ";
    }
    std::cout << std::endl;

    return 0;
}
