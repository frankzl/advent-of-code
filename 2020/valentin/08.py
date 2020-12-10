import re
import sys
import time
from typing import List, Tuple

# Handheld Halting
#
# Operations
# acc = inc/dec global value `accumulator` by argument
# jmp = jump to instruction relative to current position
# nop = do nothing

# GLOBALS
accumulator: int = 0
program: List[Tuple[str, int]] = []

# Run the program until it reaches the same instruction a second time.
# Terminate and print accumulator value


def parse_instruction(instruction_line: str) -> Tuple[str, int]:
    # nop +0
    m = re.fullmatch(r"(\w+) (\+|-)(\d+)\n", instruction_line)
    if not m:
        raise ValueError(f"Invalid instruction: {instruction_line}")

    ins: str
    sgn: str
    num_us: str
    ins, sgn, num_us = m.groups()

    num: int = int(num_us)
    if sgn == "-":
        num = -num

    return ins, num


def execute(instruction_idx: int) -> int:
    global accumulator
    global program

    ins: str
    num: int
    ins, num = program[instruction_idx]

    if ins == "nop":
        return 1 + instruction_idx
    elif ins == "jmp":
        return num + instruction_idx
    elif ins == "acc":
        accumulator += num
        return 1 + instruction_idx
    else:
        raise ValueError(f"Unknown instruction: {ins}")


t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    for l in f:
        instruction: Tuple[str, int] = parse_instruction(l)
        program.append(instruction)

t1 = time.perf_counter()

instruction_index: int = 0
hit_counter: List[bool] = [False] * len(program)

while True:
    if hit_counter[instruction_index]:
        break

    hit_counter[instruction_index] = True
    instruction_index = execute(instruction_index)

t2 = time.perf_counter()


from util import tf

print(
    f"Accumulator value: {accumulator}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Execute: {tf(t2-t1)}\n"
    f"=========\n"
    f"Total: {tf(t2-t0)}"
)
