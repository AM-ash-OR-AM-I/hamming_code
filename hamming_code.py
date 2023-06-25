from functools import reduce
import math
import random
from typing import List
import numpy as np


def error_syndrome(syndrome_word: List[int]) -> int:
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
    sec_code = [0] * (n + k + 1)
    check_bit_locations = set(2**i for i in range(k))
    index = 3

    # Insert the data bits
    for bit in data_bits:
        if index in check_bit_locations:
            index += 1
        sec_code[index] = bit
        index += 1

    # Calculate the parity bits (syndrome word)
    parity_bits = bin(error_syndrome(sec_code))[2:].zfill(k)[::-1]
    print("Check bits in order of MSB -> LSB: ", parity_bits[::-1])

    # Insert the parity bits
    for i, bit in enumerate(parity_bits):
        sec_code[2**i] = int(bit)

    return sec_code


def convert_list_to_word(lst: List[int]) -> str:
    """
    Used to convert a list of bits to a string with MSB on the left and LSB on the right
    """
    return "".join([str(bit) for bit in lst[: -len(lst) : -1]])


def convert_word_to_list(word: str) -> List[int]:
    return [int(bit) for bit in word[::-1]]


def main():
    for _ in range(100):
        # print(f"Test case: #{_}")
        data_bits = np.random.randint(0, 2, random.randint(2, 200))
        try:
            sec_code_list = generate_hamming_sec_code(data_bits)
        except Exception as e:
            print(e)
            print(data_bits)
        for i in range(1, len(sec_code_list)):
            sec_code_list[i] = not sec_code_list[i]
            error_bit = error_syndrome(sec_code_list)
            sec_code_list[i] = not sec_code_list[i]
            assert (
                error_bit == i
            )  # If the error bit is not the same as the index, then the error is not detected
    print("Passed all test cases!")


if __name__ == "__main__":
    # main()
    data_bits = convert_word_to_list("11000010")
    sec_code_list = generate_hamming_sec_code(data_bits)
    print(convert_list_to_word(sec_code_list))
