#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <algorithm>  // std::sort, std::unique

int main() {
    // 元データ（重複あり）
    std::vector<int> v = {5, 3, 3, 8, 5, 1, 8, 8};

    // ------------------------------------------------------------
    // SQL対応（概念）
    //
    // SQL:
    //   SELECT DISTINCT value FROM table ORDER BY value;
    //
    // C++:
    //   ORDER BY   -> std::sort
    //   DISTINCT   -> std::unique + erase
    // ------------------------------------------------------------

    // ORDER BY 相当
    std::sort(v.begin(), v.end());

    // DISTINCT（論理）：重複を前に詰めるだけ
    auto new_end = std::unique(v.begin(), v.end());

    // DISTINCT（物理）：不要部分を削除して完成
    v.erase(new_end, v.end());

    // 結果表示
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    return 0;
}
