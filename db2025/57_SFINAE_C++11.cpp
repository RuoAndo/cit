#include <iostream>
#include <type_traits>
#include <utility>
#include <vector>
#include <string>

// size() を持つか判定する trait（SFINAE）
template <typename T, typename = void>
struct has_size : std::false_type {};

template <typename T>
struct has_size<T, std::void_t<decltype(std::declval<const T&>().size())>>
    : std::true_type {};

// size() がある型だけ有効
template <typename T, typename std::enable_if<has_size<T>::value, int>::type = 0>
void print_size(const T& x) {
    std::cout << "size() = " << x.size() << "\n";
}

// size() がない型だけ有効（フォールバック）
template <typename T, typename std::enable_if<!has_size<T>::value, int>::type = 0>
void print_size(const T&) {
    std::cout << "no size()\n";
}

int main() {
    std::vector<int> v{1,2,3};
    std::string s = "abc";
    int n = 42;

    print_size(v); // size() = 3
    print_size(s); // size() = 3
    print_size(n); // no size()
}
