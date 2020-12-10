import re
import sys
import time
from typing import Any, Dict, List, Tuple

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


def roll_back(invalid_changes: List[int]) -> int:
    """
    Roll back to the state before the last jmp or nop will be executed.

    returns: pointer to the last jmp or nop as the next instruction to execute
    """

    global instructions_executed
    global program
    global accumulator
    global hit_detector

    pointer: int
    while True:
        # Always roll back pointer and remove executed instruction from list
        pointer = instructions_executed.pop(-1)
        hit_detector[pointer] = False
        ins: str = program[pointer][0]

        if ins == "acc":
            # Reverse accumulation
            accumulator -= program[pointer][1]
            continue

        # ins is "jmp" or "nop"

        # Only stop if we have not tried to change this position before
        if pointer not in invalid_changes:
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
            instruction_index = state["instruction_index"]
            instructions_executed = state["instructions_executed"]
            hit_detector = state["hit_detector"]
            accumulator = state["accumulator"]

        # Roll back until first untried jmp or nop
        instruction_index = roll_back(past_changes)
        # Change position
        swap_jmp_nop(instruction_index)
        code_changed = True
        past_changes.append(instruction_index)

        # Save state to later revert if unsuccessful
        state["accumulator"] = accumulator
        state["instruction_index"] = instruction_index
        state["instructions_executed"] = instructions_executed.copy()
        state["hit_detector"] = hit_detector.copy()
        # The program is changed with the swap function

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
