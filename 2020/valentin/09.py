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

# Find the first number that does not correspond to the encoding

buffer: List[int] = []
buffer_size: int = int(sys.argv[2])


def valid_number(num: int, buffer: List[int]) -> bool:
    for x, y in combinations(buffer, 2):
        if x + y == num:
            return True

    return False


t0 = time.perf_counter()

current_number: int = -1

with open(sys.argv[1], "r") as f:
    for l in f:
        current_number = int(l[:-1])

        # Start by filling the buffer
        if len(buffer) < buffer_size:
            buffer.append(current_number)
            continue

        if not valid_number(current_number, buffer):
            break

        # Move buffer
        buffer.pop(0)
        buffer.append(current_number)

t1 = time.perf_counter()


from util import tf

print(
    f"First invalid value: {current_number}\n"
    f"\n"
    f"Parse file and check: {tf(t1-t0)}\n"
    f"=========\n"
    f"Total: {tf(t1-t0)}"
)
