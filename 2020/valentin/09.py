import sys
import time
from itertools import combinations
from typing import List

# Encoding Error
#
# XMAS encoding
# - preamble of 25 numbers
# - any following number must be sum of two numbers from the preamble
# - sliding window, so for each index, the previous 25 numbers are its preamble

# Part 1: Find the first number that does not correspond to the encoding

buffer_size: int = int(sys.argv[2])
numbers: List[int] = []


def valid_number(num: int, buffer: List[int]) -> bool:
    for x, y in combinations(buffer, 2):
        if x + y == num:
            return True

    return False


t0 = time.perf_counter()

invalid_value: int = -1

with open(sys.argv[1], "r") as f:
    for l in f:
        value: int = int(l[:-1])

        # Only start checking when buffer is large enough
        if (
            (len(numbers) >= buffer_size)
            and (invalid_value != -1)
            and (not valid_number(value, numbers[-(1 + buffer_size) : -1]))
        ):
            invalid_value = value

        numbers.append(value)

t1 = time.perf_counter()

# Part 2: Find encryption weakness:
#   a) Identify the first contiguous set of numbers that sum up to the invalid number.
#   b) Add together the smallest and largest number in the range.

range_start: int = -1
range_end: int = -1

for i in range(len(numbers)):
    # j is the excluded stop index, meaning we need to start at i + 2 that nums[i:j] are at least 2 values
    for j in range(i + 2, len(numbers)):
        range_sum: int = sum(numbers[i:j])
        if range_sum == invalid_value:
            range_start = i
            range_end = j - 1
            break

encryption_weakness: int = numbers[range_start] + numbers[range_end]

t2 = time.perf_counter()


from util import tf

print(
    f"Part 1: Invalid number = {encryption_weakness}\n"
    f"Part 2: Encryption weakness = {encryption_weakness}\n"
    f"\n"
    f"Parse file and find invalid value: {tf(t1-t0)}\n"
    f"Identify encryption weakness: {tf(t2-t1)}\n"
    f"=========\n"
    f"Total: {tf(t2-t0)}"
)
