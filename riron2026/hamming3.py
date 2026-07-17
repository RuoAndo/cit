# -*- coding: utf-8 -*-
"""
ハミング符号(7,4) 演習プログラム 入力対応版

機能:
- データビットをランダム生成 or 手入力
- 誤り位置をランダム生成 or 手入力
- 誤りなしも指定可能
"""

import random


def xor_str(values):
    return "⊕".join(map(str, values))


def print_line(title=None):
    print()
    print("=" * 60)
    if title:
        print(title)
        print("=" * 60)


def encode_hamming_74(data_bits):
    d1, d2, d3, d4 = data_bits

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    code = [p1, p2, d1, p3, d2, d3, d4]

    return code, (p1, p2, p3)


def calc_syndrome(received):
    b1, b2, b3, b4, b5, b6, b7 = received

    s1 = b1 ^ b3 ^ b5 ^ b7
    s2 = b2 ^ b3 ^ b6 ^ b7
    s3 = b4 ^ b5 ^ b6 ^ b7

    syndrome_value = s1 + 2 * s2 + 4 * s3

    return s1, s2, s3, syndrome_value


def introduce_error(code, error_pos):
    received = code.copy()

    if error_pos != 0:
        received[error_pos - 1] ^= 1

    return received


def correct_error(received, syndrome_value):
    corrected = received.copy()

    if syndrome_value != 0:
        corrected[syndrome_value - 1] ^= 1

    return corrected


def decode_hamming_74(code):
    return [code[2], code[4], code[5], code[6]]


def print_code_table(code, label):
    print(label)
    print()
    print("位置 :  1  2  3  4  5  6  7")
    print("役割 : p1 p2 d1 p3 d2 d3 d4")
    print("値   :", " ".join(f"{x:>2}" for x in code))


def show_check_matrix():
    print_line("検査行列 H")

    print("H =")
    print("[1 0 1 0 1 0 1]")
    print("[0 1 1 0 0 1 1]")
    print("[0 0 0 1 1 1 1]")
    print()
    print("受信語 r に対して")
    print("s = H r^T mod 2")
    print("を計算すると、シンドローム s が得られます。")


def show_parity_calculation(data_bits, parity_bits):
    d1, d2, d3, d4 = data_bits
    p1, p2, p3 = parity_bits

    print_line("パリティビットの計算")

    print("配置:")
    print("位置 :  1  2  3  4  5  6  7")
    print("役割 : p1 p2 d1 p3 d2 d3 d4")
    print()

    print("p1 = d1 ⊕ d2 ⊕ d4")
    print(f"   = {xor_str([d1, d2, d4])}")
    print(f"   = {p1}")
    print()

    print("p2 = d1 ⊕ d3 ⊕ d4")
    print(f"   = {xor_str([d1, d3, d4])}")
    print(f"   = {p2}")
    print()

    print("p3 = d2 ⊕ d3 ⊕ d4")
    print(f"   = {xor_str([d2, d3, d4])}")
    print(f"   = {p3}")


def show_syndrome_calculation(received, s1, s2, s3, syndrome_value):
    b1, b2, b3, b4, b5, b6, b7 = received

    print_line("シンドローム計算")

    print("受信語:")
    print("位置 :  1  2  3  4  5  6  7")
    print("記号 : b1 b2 b3 b4 b5 b6 b7")
    print("値   :", " ".join(f"{x:>2}" for x in received))
    print()

    print("s1 = b1 ⊕ b3 ⊕ b5 ⊕ b7")
    print(f"   = {xor_str([b1, b3, b5, b7])}")
    print(f"   = {s1}")
    print()

    print("s2 = b2 ⊕ b3 ⊕ b6 ⊕ b7")
    print(f"   = {xor_str([b2, b3, b6, b7])}")
    print(f"   = {s2}")
    print()

    print("s3 = b4 ⊕ b5 ⊕ b6 ⊕ b7")
    print(f"   = {xor_str([b4, b5, b6, b7])}")
    print(f"   = {s3}")
    print()

    print("シンドローム:")
    print(f"(s3 s2 s1) = ({s3} {s2} {s1})")
    print(f"2進数 {s3}{s2}{s1} = 10進数 {syndrome_value}")

    if syndrome_value == 0:
        print("→ 誤りなしと判断されます。")
    else:
        print(f"→ {syndrome_value} 番目のビットが誤りと判断されます。")


def get_data_bits():
    print_line("データ生成方法")
    print("1: ランダム")
    print("2: 手入力")

    mode = input("選択してください (1/2): ").strip()

    if mode == "2":
        while True:
            s = input("4ビットを入力してください 例 1011: ").strip()

            if len(s) == 4 and all(c in "01" for c in s):
                return [int(c) for c in s]

            print("入力エラー: 0と1だけで4文字入力してください。")

    return [random.randint(0, 1) for _ in range(4)]


def get_error_position():
    print_line("誤り発生方法")
    print("1: ランダム")
    print("2: 手入力")
    print()
    print("誤り位置の意味:")
    print("0: 誤りなし")
    print("1〜7: その位置のビットを反転")

    mode = input("選択してください (1/2): ").strip()

    if mode == "2":
        while True:
            try:
                pos = int(input("誤り位置を入力してください (0〜7): "))

                if 0 <= pos <= 7:
                    return pos

            except ValueError:
                pass

            print("入力エラー: 0〜7の整数を入力してください。")

    return random.randint(0, 7)


def run_exercise():
    print_line("ハミング符号(7,4) 演習プログラム")

    show_check_matrix()

    data_bits = get_data_bits()

    print_line("元データ")
    print("d1 d2 d3 d4")
    print(" ".join(map(str, data_bits)))

    code, parity_bits = encode_hamming_74(data_bits)

    show_parity_calculation(data_bits, parity_bits)

    print_line("生成されたハミング符号")
    print_code_table(code, "送信する符号語")

    true_error_pos = get_error_position()
    received = introduce_error(code, true_error_pos)

    print_line("誤り発生")

    if true_error_pos == 0:
        print("今回は誤りを発生させませんでした。")
    else:
        print(f"{true_error_pos} 番目のビットを反転しました。")

    print()
    print_code_table(received, "受信語")

    s1, s2, s3, syndrome_value = calc_syndrome(received)

    show_syndrome_calculation(
        received,
        s1,
        s2,
        s3,
        syndrome_value
    )

    corrected = correct_error(received, syndrome_value)

    print_line("訂正")

    print_code_table(received, "訂正前")

    print()

    if syndrome_value == 0:
        print("訂正は行いません。")
    else:
        print(f"{syndrome_value} 番目のビットを反転して訂正します。")

    print()
    print_code_table(corrected, "訂正後")

    decoded = decode_hamming_74(corrected)

    print_line("復号")

    print("3,5,6,7 番目のビットを取り出します。")
    print()

    print("復号データ:")
    print("d1 d2 d3 d4")
    print(" ".join(map(str, decoded)))

    print_line("判定")

    print("元データ:")
    print(" ".join(map(str, data_bits)))
    print()

    print("復号データ:")
    print(" ".join(map(str, decoded)))
    print()

    if decoded == data_bits:
        print("結果: 正しく復号できました。")
    else:
        print("結果: 復号に失敗しました。")

    print()
    print("実際の誤り位置:", true_error_pos)
    print("シンドロームが示した位置:", syndrome_value)

    if true_error_pos == syndrome_value:
        print("誤り位置の検出も正解です。")
    else:
        print("誤り位置の検出が一致しません。")


def main():
    while True:
        run_exercise()

        print()
        again = input("もう一度実行しますか？ (y/n): ").strip().lower()

        if again != "y":
            print("終了します。")
            break


if __name__ == "__main__":
    main()