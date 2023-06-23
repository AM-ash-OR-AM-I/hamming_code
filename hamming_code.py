from functools import reduce
import math
import random
from typing import List
import numpy as np


def detect_error(syndrome_word: List[int]) -> int:
    set_bits = [i for i, bit in enumerate(syndrome_word) if bit]
    if not set_bits:
        return 0
    return reduce(
        lambda x, y: x ^ y,
        set_bits,
    )


def get_parity_bits(data_length: int) -> int:
    parity_bits = 0
    while pow(2, parity_bits) < data_length + parity_bits + 1:
        parity_bits += 1
    return parity_bits


def generate_hamming_sec_code(data_bits: List[int]) -> List[int]:
    n = len(data_bits)

    # Calculate the number of parity bits
    k = get_parity_bits(n)
    syndrome_list = [0] * (n + k + 1)
    check_bit_locations = set(2**i for i in range(k))
    index = 3

    # Insert the data bits
    for bit in data_bits:
        if index in check_bit_locations:
            index += 1
        syndrome_list[index] = bit
        index += 1

    # Calculate the parity bits
    check_bits = bin(detect_error(syndrome_list))[2:].zfill(k)[::-1]

    # Insert the parity bits
    for i, bit in enumerate(check_bits):
        syndrome_list[2**i] = int(bit)

    return syndrome_list


def convert_list_to_word(lst: List[int]) -> str:
    return "".join([str(bit) for bit in lst[: -len(lst) : -1]])


if __name__ == "__main__":
    for _ in range(1000):
        print(f"Test case: #{_}")
        data_bits = np.random.randint(0, 2, random.randint(2, 200))
        # print(data_bits.tolist())
        # print(len(data_bits))
        # data_bits = np.array([0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0])
        # data_word = "0101000000111001"
        # data_bits = [int(bit) for bit in data_word[::-1]]
        # print(data_bits)
        # data_bits = np.array([0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0])
        # print(data_bits.reshape(4, 4))
        # print(data_bits.tolist())
        try:
            syndrome_list = generate_hamming_sec_code(data_bits)
        except Exception as e:
            print(e)
            print(data_bits)
        for i in range(1, len(syndrome_list)):
            syndrome_list[i] = not syndrome_list[i]
            error_bit = detect_error(syndrome_list)
            syndrome_list[i] = not syndrome_list[i]
            assert (
                error_bit == i
            )  # If the error bit is not the same as the index, then the error is not detected
    # print("Successfully detected all errors!")
