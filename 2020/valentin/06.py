import sys
import time
from typing import List, Set

# Customs declaration
#
# - 26 y/n questions labeled a-z
# - If anyone from a group answers y, it counts for the group.
# - Each person has a single line, groups are separated by a blank line


def unique_yess(group: List[str]) -> str:
    yess: Set[str] = set()
    for answer in "".join(group):
        yess.add(answer)
    return "".join(yess)


def all_yess(group: List[str]) -> str:
    yess: Set[str] = set(group[0])
    for person in group[1:]:
        yess = yess.intersection(set(person))
    return "".join(yess)


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
    yess = all_yess(group)
    total_yess += len(yess)

t2 = time.perf_counter()


from util import tf

print(
    f"Sum of agreed yess: {total_yess}\n\n"
    f"Parse groups: {tf(t1-t0)}\n"
    f"Count yess: {tf(t2-t1)}\n"
    f"Total: {tf(t2-t0)}"
)
