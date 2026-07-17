# ============================================================
# 教育用シフトレジスタ・LFSR・CRC・ハミング符号シミュレータ
# 日本語表示 + 1〜2秒ブレイク + y/N確認つき
# ============================================================

import random
import time
import sys


AUTO_MODE = False


def wait_next():
    global AUTO_MODE

    time.sleep(random.uniform(1.0, 2.0))

    if AUTO_MODE:
        return

    ans = input("\n次へ進みますか？ [Y/n/a] : ").strip().lower()

    if ans in ("", "y", "yes"):
        return

    if ans in ("a", "auto"):
        AUTO_MODE = True
        print("以後、自動実行します。")
        return

    if ans in ("n", "no"):
        print("\nシミュレーションを終了します。")
        sys.exit(0)

    print("入力が認識できません。続行します。")


def line(title=""):
    print("\n" + "=" * 60)
    if title:
        print(title)
        print("=" * 60)


def bits_to_str(bits):
    return "".join(str(b) for b in bits)


def xor_str(values):
    return " XOR ".join(str(v) for v in values)


def polynomial_to_string(exponents):
    terms = []

    for e in sorted(exponents, reverse=True):
        if e == 0:
            terms.append("1")
        elif e == 1:
            terms.append("x")
        else:
            terms.append(f"x^{e}")

    return " + ".join(terms)


def crc_polynomial_string(generator):
    degree = len(generator) - 1
    exponents = []

    for i, bit in enumerate(generator):
        if bit == 1:
            exponents.append(degree - i)

    return polynomial_to_string(exponents)


def lfsr_polynomial_string(register_size, taps):
    exponents = [register_size]

    for t in taps:
        exponents.append(register_size - 1 - t)

    exponents.append(0)
    return polynomial_to_string(sorted(set(exponents), reverse=True))


def print_register(reg, label="レジスタ"):
    n = len(reg)

    print(label)
    print("+----" * n + "+")
    print("".join(f"|R{n-1-i:<3}" for i in range(n)) + "|")
    print("+----" * n + "+")
    print("".join(f"| {b:<3}" for b in reg) + "|")
    print("+----" * n + "+")


class ShiftRegister:
    def __init__(self, size, init=None):
        self.reg = init[:] if init else [0] * size

    def shift_right_verbose(self, input_bit, clock):
        before = self.reg[:]
        output_bit = self.reg[-1]
        self.reg = [input_bit] + self.reg[:-1]

        line(f"基本シフトレジスタ クロック {clock}")
        print(f"入力ビット : {input_bit}")
        print(f"出力ビット : {output_bit}")

        print()
        print_register(before, "シフト前レジスタ")

        print()
        print_register(self.reg, "シフト後レジスタ")

        wait_next()
        return output_bit


class LFSR:
    def __init__(self, seed, taps):
        if all(b == 0 for b in seed):
            raise ValueError("LFSRの初期値をすべて0にはできません。")

        self.reg = seed[:]
        self.taps = taps

    def step_verbose(self, clock):
        before = self.reg[:]
        tap_values = [before[t] for t in self.taps]

        feedback = 0
        for v in tap_values:
            feedback ^= v

        output_bit = before[-1]
        self.reg = [feedback] + before[:-1]

        line(f"LFSR クロック {clock}")

        print("利用している規約多項式")
        print(f"G(x) = {lfsr_polynomial_string(len(before), self.taps)}")

        print()
        print("帰還タップ")
        print("tap positions =", self.taps)
        print("tap values    =", tap_values)

        print()
        print_register(before, "シフト前レジスタ")

        print()
        print("フィードバック計算")
        print(f"feedback = {xor_str(tap_values)} = {feedback}")

        print()
        print(f"出力ビット = {output_bit}")

        print()
        print_register(self.reg, "シフト後レジスタ")

        wait_next()
        return output_bit


def crc_verbose(data, generator):
    line("CRC計算")

    work = data[:] + [0] * (len(generator) - 1)

    print("入力データ")
    print(bits_to_str(data))

    print()
    print("生成多項式")
    print(f"G(x) = {crc_polynomial_string(generator)}")

    print()
    print("生成多項式ビット列")
    print(bits_to_str(generator))

    print()
    print("初期状態")
    print(bits_to_str(work))

    wait_next()

    for i in range(len(data)):
        line(f"CRC ステップ {i + 1}")
        print("現在の作業ビット列")
        print(bits_to_str(work))

        if work[i] == 1:
            print()
            print(f"左から {i + 1} 番目のビットが1なので、生成多項式をXORします。")

            before = work[:]

            for j in range(len(generator)):
                work[i + j] ^= generator[j]

            print()
            print("XOR前")
            print(bits_to_str(before))

            print("XORする位置")
            print(" " * i + bits_to_str(generator))

            print("XOR後")
            print(bits_to_str(work))

        else:
            print()
            print(f"左から {i + 1} 番目のビットが0なので、何もしません。")

        wait_next()

    remainder = work[-(len(generator) - 1):]
    codeword = data + remainder

    line("CRC結果")
    print("余り")
    print(bits_to_str(remainder))

    print()
    print("CRC付き符号語")
    print(bits_to_str(codeword))

    wait_next()
    return codeword, remainder


def crc_check_verbose(codeword, generator):
    line("CRC検査")

    work = codeword[:]

    print("受信語")
    print(bits_to_str(codeword))

    print()
    print("生成多項式")
    print(f"G(x) = {crc_polynomial_string(generator)}")

    wait_next()

    for i in range(len(codeword) - len(generator) + 1):
        if work[i] == 1:
            before = work[:]

            for j in range(len(generator)):
                work[i + j] ^= generator[j]

            line(f"CRC検査ステップ {i + 1}")
            print("XOR前 :", bits_to_str(before))
            print("XOR後 :", bits_to_str(work))

            wait_next()

    remainder = work[-(len(generator) - 1):]

    line("CRC検査結果")
    print("検査余り")
    print(bits_to_str(remainder))

    if any(remainder):
        print("判定 : 誤りあり")
    else:
        print("判定 : 誤りなし")

    wait_next()
    return remainder


def hamming74_encode_verbose(data):
    line("ハミング(7,4) 符号化")

    d1, d2, d3, d4 = data

    print("入力データ")
    print("D1 D2 D3 D4")
    print(f"{d1}  {d2}  {d3}  {d4}")

    p1_values = [d1, d2, d4]
    p2_values = [d1, d3, d4]
    p3_values = [d2, d3, d4]

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    print()
    print("パリティビット計算")
    print(f"P1 = D1 XOR D2 XOR D4 = {xor_str(p1_values)} = {p1}")
    print(f"P2 = D1 XOR D3 XOR D4 = {xor_str(p2_values)} = {p2}")
    print(f"P3 = D2 XOR D3 XOR D4 = {xor_str(p3_values)} = {p3}")

    code = [p1, p2, d1, p3, d2, d3, d4]

    print()
    print("配置")
    print("位置 : 1  2  3  4  5  6  7")
    print("内容 : P1 P2 D1 P3 D2 D3 D4")
    print("符号 :", "  ".join(str(b) for b in code))

    print()
    print("生成された符号語")
    print(bits_to_str(code))

    wait_next()
    return code


def hamming74_decode_verbose(received):
    line("ハミング(7,4) 復号")

    b = received[:]

    print("受信語")
    print(bits_to_str(b))

    s1_values = [b[0], b[2], b[4], b[6]]
    s2_values = [b[1], b[2], b[5], b[6]]
    s3_values = [b[3], b[4], b[5], b[6]]

    s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    s3 = b[3] ^ b[4] ^ b[5] ^ b[6]

    print()
    print("シンドローム計算")
    print(f"S1 = b1 XOR b3 XOR b5 XOR b7 = {xor_str(s1_values)} = {s1}")
    print(f"S2 = b2 XOR b3 XOR b6 XOR b7 = {xor_str(s2_values)} = {s2}")
    print(f"S3 = b4 XOR b5 XOR b6 XOR b7 = {xor_str(s3_values)} = {s3}")

    error_position = s1 + 2 * s2 + 4 * s3

    print()
    print("シンドローム")
    print(f"S = S3 S2 S1 = {s3}{s2}{s1}")
    print(f"誤り位置 = S1 + 2*S2 + 4*S3 = {error_position}")

    if error_position != 0:
        print()
        print(f"判定 : {error_position} ビット目に誤りがあります。")

        before = b[:]
        b[error_position - 1] ^= 1

        print()
        print("訂正前")
        print(bits_to_str(before))

        print("訂正後")
        print(bits_to_str(b))

    else:
        print()
        print("判定 : 誤りはありません。")

    decoded = [b[2], b[4], b[5], b[6]]

    print()
    print("復号データ")
    print(bits_to_str(decoded))

    wait_next()

    return {
        "syndrome": [s3, s2, s1],
        "error_position": error_position,
        "corrected_code": b,
        "decoded_data": decoded
    }


def inject_error(bits, position=None):
    y = bits[:]

    if position is None:
        position = random.randint(0, len(bits) - 1)

    y[position] ^= 1
    return y, position + 1


def main():
    line("教育用シミュレータ開始")

    print("操作方法")
    print("Enter または y : 次へ進む")
    print("n              : 終了")
    print("a              : 以後、自動実行")
    wait_next()

    # --------------------------------------------------------
    # 1. 基本シフトレジスタ
    # --------------------------------------------------------

    line("1. 基本シフトレジスタ")

    sr = ShiftRegister(size=8)
    input_bits = [1, 0, 1, 1, 0, 1]

    print("入力ビット列")
    print(bits_to_str(input_bits))
    wait_next()

    for clk, bit in enumerate(input_bits, start=1):
        sr.shift_right_verbose(bit, clk)

    # --------------------------------------------------------
    # 2. LFSR
    # --------------------------------------------------------

    line("2. LFSR")

    seed = [1, 0, 0, 1]
    taps = [0, 3]

    print("初期値")
    print(bits_to_str(seed))

    print()
    print("利用する規約多項式")
    print(f"G(x) = {lfsr_polynomial_string(len(seed), taps)}")

    wait_next()

    lfsr = LFSR(seed=seed, taps=taps)
    pn_sequence = []

    for clk in range(1, 11):
        pn_sequence.append(lfsr.step_verbose(clk))

    line("LFSR生成系列")
    print(bits_to_str(pn_sequence))
    wait_next()

    # --------------------------------------------------------
    # 3. CRC
    # --------------------------------------------------------

    line("3. CRC生成と検査")

    crc_data = [1, 0, 1, 1, 0, 1]
    generator = [1, 0, 1, 1]

    crc_codeword, crc_remainder_bits = crc_verbose(
        data=crc_data,
        generator=generator
    )

    crc_received, crc_error_position = inject_error(
        crc_codeword,
        position=3
    )

    line("CRC用 1ビット誤り挿入")
    print("送信語")
    print(bits_to_str(crc_codeword))

    print()
    print(f"誤り挿入位置 : {crc_error_position} ビット目")

    print()
    print("受信語")
    print(bits_to_str(crc_received))

    wait_next()

    crc_check_verbose(
        codeword=crc_received,
        generator=generator
    )

    # --------------------------------------------------------
    # 4. ハミング符号
    # --------------------------------------------------------

    line("4. ハミング符号")

    data = [1, 0, 1, 1]
    code = hamming74_encode_verbose(data)

    received, error_position = inject_error(
        code,
        position=5
    )

    line("ハミング符号用 1ビット誤り挿入")
    print("送信語")
    print(bits_to_str(code))

    print()
    print(f"誤り挿入位置 : {error_position} ビット目")

    print()
    print("受信語")
    print(bits_to_str(received))

    wait_next()

    result = hamming74_decode_verbose(received)

    # --------------------------------------------------------
    # まとめ
    # --------------------------------------------------------

    line("まとめ")

    print("LFSR")
    print(f"規約多項式 : G(x) = {lfsr_polynomial_string(len(seed), taps)}")
    print(f"生成系列   : {bits_to_str(pn_sequence)}")

    print()
    print("CRC")
    print(f"生成多項式 : G(x) = {crc_polynomial_string(generator)}")
    print(f"入力       : {bits_to_str(crc_data)}")
    print(f"CRC余り    : {bits_to_str(crc_remainder_bits)}")
    print(f"符号語     : {bits_to_str(crc_codeword)}")

    print()
    print("ハミング(7,4)")
    print(f"元データ   : {bits_to_str(data)}")
    print(f"符号語     : {bits_to_str(code)}")
    print(f"受信語     : {bits_to_str(received)}")
    print(f"誤り位置   : {result['error_position']} ビット目")
    print(f"訂正後     : {bits_to_str(result['corrected_code'])}")
    print(f"復号結果   : {bits_to_str(result['decoded_data'])}")

    print()
    print("シミュレーション完了")


if __name__ == "__main__":
    main()