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

# end / device = max+3
device: int = max(adapters) + 3

t1 = time.perf_counter()

adapters.sort()

# Part 1


def count_joltage_steps(adapters: List[int]) -> int:
    deltas: Counter = Counter({x: 0 for x in [1, 2, 3]})
    last_adapter: int = 0

    for next_adapter in adapters:
        delta: int = next_adapter - last_adapter
        if delta not in deltas:
            raise ValueError(f"Delta of {delta} found: {next_adapter} - {last_adapter}")

        deltas[delta] += 1
        last_adapter = next_adapter

    return deltas[1] * deltas[3]


# result: int = count_joltage_steps(adapters + [device])

# B) Find all possible chains that connect the socket to the device
#    and count the number of distinct chains.

# Part 2


def count_distinct_chains(adapters: List[int], start: int, end: int) -> int:
    # Recurse into possible steps and sum up
    chain_count: int = 0

    for i in range(len(adapters)):
        adp: int = adapters[i]
        delta: int = adp - start

        if delta <= 0:
            raise ValueError("Invalid step")
        elif delta > 3:
            # Input list is sorted, so we have reached the end
            break

        # Valid if delta in [1, 3]
        chain_count += count_distinct_chains(adapters[i + 1 :], start=adp, end=end)

    # Recursion end: List is empty
    if not adapters and ((end - start) in [1, 2, 3]):
        return 1

    return chain_count


chain_count: int = count_distinct_chains(adapters, start=0, end=device)

t2 = time.perf_counter()


from util import tf

print(
    f"Number of distinct chains = {chain_count}\n"
    f"\n"
    f"Parse file and collect adapters: {tf(t1-t0)}\n"
    f"Count chains: {tf(t2-t1)}\n"
    f"=====\n"
    f"Total: {tf(t2-t0)}"
)
