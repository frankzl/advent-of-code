import sys
import time
from functools import reduce
from typing import List, Set

# Customs declaration
#
# - 26 y/n questions labeled a-z
# - If anyone from a group answers y, it counts for the group.
# - Each person has a single line, groups are separated by a blank line


def unique_yess(group: List[str]) -> int:
    yess: Set[str] = set()
    for answer in "".join(group):
        yess.add(answer)
    return len(yess)


def all_yess_classic(group: List[str]) -> int:
    yess: Set[str] = set(group[0])
    for person in group[1:]:
        yess = yess.intersection(set(person))
    return len(yess)


def all_yess(group: List[str]) -> int:
    yess: Set[str] = reduce(lambda x, y: x.intersection(y), group[1:], set(group[0]))
    return len(yess)


t0 = time.perf_counter()

# 1. Find the questions combined for the group which were answered y.
# 2. Count the number.

groups: List[List[str]] = []

with open(sys.argv[1], "r") as f:
    group: List[str] = []
    for l in f:
        if l == "\n":
            groups.append(group)
            group = []
            continue

        group.append(l[:-1])

    # The last group is not followed by an empty line
    groups.append(group)

t1 = time.perf_counter()

total_yess: int = 0

for group in groups:
    total_yess += all_yess(group)

t2 = time.perf_counter()


from util import tf

print(
    f"Sum of agreed yess: {total_yess}\n\n"
    f"Parse groups: {tf(t1-t0)}\n"
    f"Count yess: {tf(t2-t1)}\n"
    f"Total: {tf(t2-t0)}"
)
