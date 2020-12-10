import re
import sys
import time
from typing import Any, Callable, Dict, List, Tuple

# Handheld Halting
#
# Operations
# acc = inc/dec global value `accumulator` by argument
# jmp = jump to instruction relative to current position
# nop = do nothing

# GLOBALS
accumulator: int = 0
program: List[Tuple[str, int]] = []
instructions_executed: List[int] = []
hit_detector: List[bool]

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


def _roll_back_instruction(pointer: int) -> None:
    global program
    global accumulator
    global hit_detector

    ins: str
    val: int
    ins, val = program[pointer]

    if ins == "acc":
        # Reverse accumulation
        accumulator -= val

    hit_detector[pointer] = False


def roll_back(condition: Callable[[int], bool]):
    """ Roll back the state until the given condition is met based on the passed pointer. """

    global instructions_executed

    pointer: int
    # We assume that one instruction can always be safely rolled back.
    while True:
        # Always roll back pointer and remove executed instruction from list
        pointer = instructions_executed.pop(-1)
        # Reverse accumulation and reset hit_detector
        _roll_back_instruction(pointer)

        # Stop if condition is met
        if condition(pointer):
            break

    # Hit the state before the last unchanged jmp or nop

    # The instruction currently pointed to was rolled back
    return pointer


def swap_jmp_nop(pointer: int):
    """ Swap the instruction the pointer points to. """

    ins: Tuple[str, int] = program[pointer]

    if ins[0] == "jmp":
        program[pointer] = "nop", ins[1]
    else:
        program[pointer] = "jmp", ins[1]


t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    for l in f:
        instruction: Tuple[str, int] = parse_instruction(l)
        program.append(instruction)

hit_detector = [False] * len(program)

t1 = time.perf_counter()

instruction_index: int = 0
code_changed: bool = False  # Was an instruction changed, and if yes, which?
past_changes: List[int] = []  # Changed indices that did not fix the infinite loop

state: Dict[str, Any] = {}

while True:
    # Successfull termination
    if instruction_index >= len(program):
        break

    if hit_detector[instruction_index]:
        if code_changed:
            # Revert change again
            swap_jmp_nop(past_changes[-1])
            code_changed = False

            # Go back to state before the change was tried
            instruction_index = roll_back(lambda p: p == past_changes[-1])

        # Roll back until first untried jmp or nop
        instruction_index = roll_back(
            lambda p: program[p][0] in ["jmp", "nop"] and p not in past_changes
        )
        # Change position
        swap_jmp_nop(instruction_index)
        code_changed = True
        past_changes.append(instruction_index)

        # Continue running

    instructions_executed.append(instruction_index)
    hit_detector[instruction_index] = True
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
