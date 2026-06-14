# -*- coding: utf-8 -*-
"""
ハミング符号(7,4) 長いビット列シミュレーション
詳細出力・0.5秒ブレーク版
"""

import random
import time


PAUSE_SEC = 0.5
DETAIL_BLOCKS = 5
PROGRESS_EVERY = 100


def pause():
    time.sleep(PAUSE_SEC)


def line(title=None):
    print()
    print("=" * 70)
    if title:
        print(title)
        print("=" * 70)
    pause()


def bits_to_str(bits):
    return "".join(map(str, bits))


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


def correct_error(received):
    corrected = received.copy()
    s1, s2, s3, syndrome_value = calc_syndrome(received)

    if syndrome_value != 0:
        corrected[syndrome_value - 1] ^= 1

    return corrected, s1, s2, s3, syndrome_value


def decode_hamming_74(code):
    return [code[2], code[4], code[5], code[6]]


def split_blocks(bits, block_size):
    return [
        bits[i:i + block_size]
        for i in range(0, len(bits), block_size)
    ]


def pad_bits(bits, block_size=4):
    remainder = len(bits) % block_size

    if remainder == 0:
        return bits, 0

    pad_len = block_size - remainder
    return bits + [0] * pad_len, pad_len


def add_random_errors(encoded_bits, error_probability):
    received = encoded_bits.copy()
    error_positions = []

    for i in range(len(received)):
        if random.random() < error_probability:
            received[i] ^= 1
            error_positions.append(i)

    return received, error_positions


def bit_error_count(a, b):
    return sum(x != y for x, y in zip(a, b))


def show_encoding_detail(block_index, data_block, parity_bits, encoded_block):
    d1, d2, d3, d4 = data_block
    p1, p2, p3 = parity_bits

    print()
    print("-" * 70)
    print(f"符号化詳細 ブロック {block_index}")
    print("-" * 70)
    pause()

    print("元データ4ビット:")
    print(f"d1 d2 d3 d4 = {d1}  {d2}  {d3}  {d4}")
    pause()

    print()
    print("パリティ計算:")
    print(f"p1 = d1⊕d2⊕d4 = {d1}⊕{d2}⊕{d4} = {p1}")
    pause()
    print(f"p2 = d1⊕d3⊕d4 = {d1}⊕{d3}⊕{d4} = {p2}")
    pause()
    print(f"p3 = d2⊕d3⊕d4 = {d2}⊕{d3}⊕{d4} = {p3}")
    pause()

    print()
    print("配置:")
    print("位置 :  1  2  3  4  5  6  7")
    print("役割 : p1 p2 d1 p3 d2 d3 d4")
    print("値   :", " ".join(f"{x:>2}" for x in encoded_block))
    pause()


def show_decoding_detail(
    block_index,
    original_block,
    encoded_block,
    received_block,
    corrected_block,
    decoded_block,
    s1,
    s2,
    s3,
    syndrome_value
):
    print()
    print("-" * 70)
    print(f"復号詳細 ブロック {block_index}")
    print("-" * 70)
    pause()

    print("元データ4ビット :", bits_to_str(original_block))
    print("送信符号語7ビット:", bits_to_str(encoded_block))
    print("受信語7ビット    :", bits_to_str(received_block))
    pause()

    print()
    print("シンドローム計算:")
    print("s1 = b1⊕b3⊕b5⊕b7")
    print(f"   = {received_block[0]}⊕{received_block[2]}⊕{received_block[4]}⊕{received_block[6]}")
    print(f"   = {s1}")
    pause()

    print("s2 = b2⊕b3⊕b6⊕b7")
    print(f"   = {received_block[1]}⊕{received_block[2]}⊕{received_block[5]}⊕{received_block[6]}")
    print(f"   = {s2}")
    pause()

    print("s3 = b4⊕b5⊕b6⊕b7")
    print(f"   = {received_block[3]}⊕{received_block[4]}⊕{received_block[5]}⊕{received_block[6]}")
    print(f"   = {s3}")
    pause()

    print()
    print(f"(s3 s2 s1) = ({s3} {s2} {s1})")
    print(f"2進数 {s3}{s2}{s1} = 10進数 {syndrome_value}")
    pause()

    if syndrome_value == 0:
        print("判定: 誤りなし")
    else:
        print(f"判定: {syndrome_value} 番目のビットを反転して訂正")
    pause()

    print()
    print("訂正後7ビット:", bits_to_str(corrected_block))
    print("復号4ビット  :", bits_to_str(decoded_block))
    pause()

    if decoded_block == original_block:
        print("結果: このブロックは正しく復号できました。")
    else:
        print("結果: このブロックは復号に失敗しました。")
    pause()


def get_int_input(prompt, default_value):
    s = input(prompt).strip()
    if s == "":
        return default_value
    return int(s)


def get_float_input(prompt, default_value):
    s = input(prompt).strip()
    if s == "":
        return default_value
    return float(s)


def run_simulation():
    line("ハミング符号(7,4) 長いビット列シミュレーション")

    n_bits = get_int_input(
        "元データのビット数を入力してください 例 4000 / Enterで4000: ",
        4000
    )

    error_probability = get_float_input(
        "ビット誤り確率を入力してください 例 0.01 / Enterで0.01: ",
        0.01
    )

    line("1. 元データ生成")

    original_bits = [
        random.randint(0, 1)
        for _ in range(n_bits)
    ]

    print("ランダムな元データを生成しました。")
    print("元データ長:", n_bits, "ビット")
    print("先頭80ビット:")
    print(bits_to_str(original_bits[:min(80, n_bits)]))
    pause()

    line("2. 4ビット単位に分割")

    padded_bits, pad_len = pad_bits(original_bits, 4)
    data_blocks = split_blocks(padded_bits, 4)

    print("ハミング(7,4)は4ビット単位で符号化します。")
    print("不足分がある場合は0でパディングします。")
    print("パディング数:", pad_len)
    print("4ビットブロック数:", len(data_blocks))
    pause()

    line("3. ハミング(7,4)符号化")

    encoded_blocks = []

    for i, block in enumerate(data_blocks, start=1):
        encoded_block, parity_bits = encode_hamming_74(block)
        encoded_blocks.append(encoded_block)

        if i <= DETAIL_BLOCKS:
            show_encoding_detail(i, block, parity_bits, encoded_block)
        elif i % PROGRESS_EVERY == 0:
            print(f"{i}/{len(data_blocks)} ブロック符号化完了")
            pause()

    encoded_bits = [
        bit
        for block in encoded_blocks
        for bit in block
    ]

    print()
    print("符号化完了")
    print("符号化前ビット数:", len(padded_bits))
    print("符号化後ビット数:", len(encoded_bits))
    print("符号化率:", f"{len(padded_bits) / len(encoded_bits):.4f}")
    pause()

    line("4. 通信路でランダム誤りを発生")

    received_bits, error_positions = add_random_errors(
        encoded_bits,
        error_probability
    )

    print("各ビットを確率 p で反転しました。")
    print("設定した誤り確率 p:", error_probability)
    print("発生した誤り数:", len(error_positions))
    print("通信路BER:", len(error_positions) / len(encoded_bits))
    pause()

    print()
    print("先頭20個の誤り位置 0始まり:")
    print(error_positions[:20])
    pause()

    received_blocks = split_blocks(received_bits, 7)

    line("5. ブロックごとの訂正・復号")

    corrected_blocks = []
    decoded_blocks = []

    no_syndrome_blocks = 0
    detected_error_blocks = 0
    success_blocks = 0
    failed_blocks = 0

    for block_index, received_block in enumerate(received_blocks, start=1):
        original_block = data_blocks[block_index - 1]
        encoded_block = encoded_blocks[block_index - 1]

        corrected_block, s1, s2, s3, syndrome_value = correct_error(received_block)
        decoded_block = decode_hamming_74(corrected_block)

        corrected_blocks.append(corrected_block)
        decoded_blocks.append(decoded_block)

        if syndrome_value == 0:
            no_syndrome_blocks += 1
        else:
            detected_error_blocks += 1

        if decoded_block == original_block:
            success_blocks += 1
        else:
            failed_blocks += 1

        if block_index <= DETAIL_BLOCKS:
            show_decoding_detail(
                block_index,
                original_block,
                encoded_block,
                received_block,
                corrected_block,
                decoded_block,
                s1,
                s2,
                s3,
                syndrome_value
            )

        elif block_index % PROGRESS_EVERY == 0:
            print(
                f"{block_index}/{len(received_blocks)} ブロック復号完了 "
                f"| 検出={detected_error_blocks} "
                f"| シンドローム0={no_syndrome_blocks} "
                f"| 成功={success_blocks} "
                f"| 失敗={failed_blocks}"
            )
            pause()

    line("6. 復号結果の連結")

    decoded_bits_padded = [
        bit
        for block in decoded_blocks
        for bit in block
    ]

    if pad_len > 0:
        decoded_bits = decoded_bits_padded[:-pad_len]
        print("パディング分を削除しました。")
    else:
        decoded_bits = decoded_bits_padded
        print("パディングはありません。")

    pause()

    line("7. 元データとの比較")

    before_channel_errors = len(error_positions)
    after_decode_errors = bit_error_count(original_bits, decoded_bits)

    total_blocks = len(data_blocks)
    encoded_length = len(encoded_bits)

    ber_before = before_channel_errors / encoded_length
    ber_after = after_decode_errors / n_bits

    print("元データと復号データをビット単位で比較しました。")
    print("復号後に残った誤り数:", after_decode_errors)
    print("復号後BER:", ber_after)
    pause()

    line("最終結果")

    print("元データ長:", n_bits, "ビット")
    print("パディング:", pad_len, "ビット")
    print("4ビットブロック数:", total_blocks)
    print("符号化後ビット数:", encoded_length, "ビット")
    print()

    print("設定したビット誤り確率:", error_probability)
    print("通信路で発生した誤り数:", before_channel_errors)
    print("通信路BER:", ber_before)
    print()

    print("シンドローム0のブロック数:", no_syndrome_blocks)
    print("シンドローム非0のブロック数:", detected_error_blocks)
    print()

    print("復号成功ブロック数:", success_blocks)
    print("復号失敗ブロック数:", failed_blocks)
    print("ブロック成功率:", success_blocks / total_blocks)
    print()

    print("復号後に残った誤り数:", after_decode_errors)
    print("復号後BER:", ber_after)
    print()

    if after_decode_errors == 0:
        print("結果: すべて正しく復号できました。")
    else:
        print("結果: 一部のビットは正しく復号できませんでした。")
        print("理由: ハミング(7,4)は、1ブロック中の1ビット誤りまでは訂正できます。")
        print("      しかし、同じ7ビットブロック内で2ビット以上誤ると、")
        print("      誤訂正や復号失敗が起きることがあります。")

    pause()

    line("先頭部分の確認")

    show_len = min(80, n_bits)

    print("元データ:")
    print(bits_to_str(original_bits[:show_len]))
    print()

    print("復号結果:")
    print(bits_to_str(decoded_bits[:show_len]))
    print()

    if original_bits[:show_len] == decoded_bits[:show_len]:
        print("先頭部分は一致しています。")
    else:
        print("先頭部分に不一致があります。")

    pause()


def main():
    while True:
        run_simulation()

        print()
        again = input("もう一度シミュレーションしますか？ (y/n): ").strip().lower()

        if again != "y":
            print("終了します。")
            break


if __name__ == "__main__":
    main()