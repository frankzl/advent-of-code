import sys
import time
from collections import deque
from typing import Deque, List

# pylint: disable=unsubscriptable-object

# Rambunctious Recitation
#
# - Puzzle input: Starting numbers
# - Memory game
# - Players take turns saying numbers
#   + Start from starting number
#   + Then consider last spoken number
#     * If it was spoken for the first time, say 0
#     * Else, say number of turns since the number was last spoken

# Part 1: Find 2020th number spoken

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    lines: List[str] = f.readlines()

first_line_cut: str = lines[0][:-1]
numbers: Deque[int] = deque(reversed([int(n) for n in first_line_cut.split(",")]))

t1 = time.perf_counter()

number_spoken: int = len(numbers)
number_2020: int = -1

while True:
    try:
        idx: int = numbers.index(numbers[0], 1)
        numbers.appendleft(idx)
    except ValueError:
        numbers.appendleft(0)

    number_spoken += 1

    if number_spoken >= 2020:
        number_2020 = numbers[0]
        t2 = time.perf_counter()
        break

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: 2020th number = {number_2020}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Part 1: Find 2020th: {tf(t2-t1)}\n"
    f"=====\n"
    f"Total: {tf(t2-t0)}"
)
