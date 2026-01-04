#include <iostream>   // 入出力
#include <vector>     // std::vector
#include <algorithm>  // std::sort, std::unique

int main() {
    // 元データ（重複あり）
    std::vector<int> v = {5, 3, 3, 8, 5, 1, 8, 8};

    // ------------------------------------------------------------
    // SQLとの対応（概念）
    //
    // SQL（重複除去）:
    //   SELECT DISTINCT value FROM table ORDER BY value;
    //
    // C++:
    //   1) std::sort        : ORDER BY
    //   2) std::unique      : 連続する重複を前に詰める
    //   3) erase            : 末尾の不要部分を削除
    // ------------------------------------------------------------

    // ORDER BY 相当（必須）
    std::sort(v.begin(), v.end());

    // UNIQUE 相当（重複を「消す」のではなく「詰める」）
    auto new_end = std::unique(v.begin(), v.end());

    // 実際にサイズを縮める
    v.erase(new_end, v.end());

    // 結果表示
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << std::endl;

    return 0;
}
