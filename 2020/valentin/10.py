import sys
import time
from collections import Counter
from typing import List

# Adapter Array
#
# - List of joltage adapters
# - Can take inputs of 1-3 jolts below their rated joltage
# - In addition, the device can take a joltage of max(joltages) + 3
# - Charging outlet has rating of 0

# A) Find a chain that connects all adapters from the socket (0) to the device (max + 3)
#    and multiply the number of 1-jolt steps with the number of 3-jolt steps.

adapters: List[int] = []

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    for l in f:
        adapters.append(int(l[:-1]))

# Add end (device = max+3) to list
adapters.append(max(adapters) + 3)

t1 = time.perf_counter()

adapters.sort()

t2 = time.perf_counter()

deltas: Counter = Counter({x: 0 for x in [1, 2, 3]})
last_adapter: int = 0

for next_adapter in adapters:
    delta: int = next_adapter - last_adapter
    if delta not in deltas:
        raise ValueError(f"Delta of {delta} found: {next_adapter} - {last_adapter}")

    deltas[delta] += 1
    last_adapter = next_adapter

t3 = time.perf_counter()

result: int = deltas[1] * deltas[3]

t4 = time.perf_counter()


from util import tf

print(
    f"Part 1: Result = {result}\n"
    f"\n"
    f"Parse file and collect adapters: {tf(t1-t0)}\n"
    f"Sort: {tf(t2-t1)}\n"
    f"Count deltas: {tf(t3-t2)}\n"
    f"Get result: {tf(t4-t3)}\n"
    f"=====\n"
    f"Total: {tf(t4-t0)}"
)
