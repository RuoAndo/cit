import random


class ShiftRegister:
    def __init__(self, size):
        self.reg = [0] * size

    def shift_right_verbose(self, bit, clock):
        before = self.reg[:]
        out = self.reg[-1]
        self.reg = [bit] + self.reg[:-1]

        print(f"\nCLK {clock}")
        print(f"  before : {before}")
        print(f"  input  : {bit}")
        print(f"  output : {out}")
        print(f"  after  : {self.reg}")

        return out


def hamming74_encode_verbose(data):
    d1, d2, d3, d4 = data

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4

    code = [p1, p2, d1, p3, d2, d3, d4]

    print("\n=== Hamming Encode ===")
    print("data =", data)
    print(f"p1 = d1 ^ d2 ^ d4 = {d1} ^ {d2} ^ {d4} = {p1}")
    print(f"p2 = d1 ^ d3 ^ d4 = {d1} ^ {d3} ^ {d4} = {p2}")
    print(f"p3 = d2 ^ d3 ^ d4 = {d2} ^ {d3} ^ {d4} = {p3}")
    print("code = [p1,p2,d1,p3,d2,d3,d4]")
    print("code =", code)

    return code


def hamming74_decode_verbose(received):
    b = received[:]

    print("\n=== Hamming Decode ===")
    print("received =", b)

    s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    s3 = b[3] ^ b[4] ^ b[5] ^ b[6]

    print(f"s1 = b1 ^ b3 ^ b5 ^ b7 = {b[0]} ^ {b[2]} ^ {b[4]} ^ {b[6]} = {s1}")
    print(f"s2 = b2 ^ b3 ^ b6 ^ b7 = {b[1]} ^ {b[2]} ^ {b[5]} ^ {b[6]} = {s2}")
    print(f"s3 = b4 ^ b5 ^ b6 ^ b7 = {b[3]} ^ {b[4]} ^ {b[5]} ^ {b[6]} = {s3}")

    error_pos = s1 + 2 * s2 + 4 * s3

    print(f"error position = s1 + 2*s2 + 4*s3 = {error_pos}")

    if error_pos != 0:
        print(f"bit {error_pos} is wrong")
        before = b[:]
        b[error_pos - 1] ^= 1
        print("before correction =", before)
        print("after correction  =", b)
    else:
        print("no error")

    decoded = [b[2], b[4], b[5], b[6]]

    print("decoded data =", decoded)

    return decoded


def lfsr_verbose(seed, taps, steps):
    reg = seed[:]

    print("\n=== LFSR Simulation ===")
    print("seed =", reg)
    print("taps =", taps)

    for clk in range(1, steps + 1):
        before = reg[:]

        feedback = 0
        tap_values = []

        for t in taps:
            feedback ^= reg[t]
            tap_values.append(reg[t])

        out = reg[-1]
        reg = [feedback] + reg[:-1]

        print(f"\nCLK {clk}")
        print("  before   :", before)
        print("  tap bits :", tap_values)
        print("  feedback :", feedback)
        print("  output   :", out)
        print("  after    :", reg)


def crc_verbose(data, generator):
    work = data[:] + [0] * (len(generator) - 1)

    print("\n=== CRC Calculation ===")
    print("data      =", data)
    print("generator =", generator)
    print("initial   =", work)

    for i in range(len(data)):
        print(f"\nStep {i + 1}")
        print("  current =", work)

        if work[i] == 1:
            print(f"  work[{i}] is 1, so XOR generator")
            before = work[:]

            for j in range(len(generator)):
                work[i + j] ^= generator[j]

            print("  before =", before)
            print("  after  =", work)
        else:
            print(f"  work[{i}] is 0, so skip")

    remainder = work[-(len(generator) - 1):]

    print("\nCRC remainder =", remainder)

    return remainder


def main():

    print("====================================")
    print("Detailed Shift Register Simulation")
    print("====================================")

    sr = ShiftRegister(8)
    input_bits = [1, 0, 1, 1, 0, 1]

    for clk, bit in enumerate(input_bits, start=1):
        sr.shift_right_verbose(bit, clk)

    lfsr_verbose(
        seed=[1, 0, 0, 1],
        taps=[0, 3],
        steps=10
    )

    data = [1, 0, 1, 1]
    code = hamming74_encode_verbose(data)

    received = code[:]
    received[5] ^= 1

    print("\n1-bit error inserted at bit 6")
    hamming74_decode_verbose(received)

    crc_verbose(
        data=[1, 0, 1, 1, 0, 1],
        generator=[1, 0, 1, 1]
    )


if __name__ == "__main__":
    main()