import re
import sys
import time
from enum import Enum
from typing import Dict, List, Tuple, Union, cast

# pylint: disable=unsubscriptable-object

# Rain Risk
#
# - Input: Navigation instructions
#   + \w\d+
#     * Move N (north), S (south), E (east), W (west)
#     * Turn L (left), R (right), Move F (forward)
# - Starting position: Unknown, facing east


class RelDirection(Enum):
    FORWARD = "F"


# TODO!
DIR_TO_FACE: List[Tuple[int, str]] = list(zip(range(4), "NESW"))


class AbsDirection(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    LEFT = "L"
    RIGHT = "R"

    def to_facing(self) -> int:
        if self in [AbsDirection.LEFT, AbsDirection.RIGHT]:
            raise ValueError("LEFT and RIGHT are not facing!")
        return {
            AbsDirection.NORTH: 0,
            AbsDirection.EAST: 1,
            AbsDirection.SOUTH: 2,
            AbsDirection.WEST: 3,
        }[self]

    @staticmethod
    def from_facing(facing):
        # type: (int) -> AbsDirection
        if facing not in range(4):
            raise ValueError(f"Invalid facing value: {facing}")
        return {
            0: AbsDirection.NORTH,
            1: AbsDirection.EAST,
            2: AbsDirection.SOUTH,
            3: AbsDirection.WEST,
        }[facing]

    def get_trajectory_base(self) -> Tuple[int, int, int]:
        if self is AbsDirection.NORTH:
            return (-1, 0, 0)
        elif self is AbsDirection.SOUTH:
            return (1, 0, 0)
        elif self is AbsDirection.WEST:
            return (0, -1, 0)
        elif self is AbsDirection.EAST:
            return (0, 1, 0)
        elif self is AbsDirection.LEFT:
            return (0, 0, -1)
        elif self is AbsDirection.RIGHT:
            return (0, 0, 1)
        else:
            raise ValueError(f"Unknown self: {self.name}")


class Instruction:
    def __init__(self, instruction_s: str, value: int) -> None:
        self.value: int = value

        self.action: Union[AbsDirection, RelDirection]

        try:
            self.action = AbsDirection(instruction_s)
        except ValueError:
            # Intentionally provoke an exception if it does not match either
            self.action = RelDirection(instruction_s)

        if (self.action in [AbsDirection.LEFT, AbsDirection.RIGHT]) and not (
            self.value % 90 == 0
        ):
            raise ValueError("For LEFT and RIGHT, only multiples of 90 are allowed!")

    def get_trajectory(self, facing: int) -> Tuple[int, int, int]:
        """
        Translate the contained (action, value) pair to a trajectory.

        Returns: Trajectory in the form of (x, y, turn)
        """
        base_trajectory: Tuple[int, int, int]
        if type(self.action) is RelDirection:
            base_trajectory = AbsDirection.from_facing(facing).get_trajectory_base()
        else:
            self.action = cast(AbsDirection, self.action)
            base_trajectory = self.action.get_trajectory_base()

        r, c, a = base_trajectory  # row, col, angle
        # For a(ngle), the value is transformed to represent quarter turns with 1
        return (r * self.value, c * self.value, a * (self.value // 90))


class Ship:
    def __init__(self, row: int, col: int, facing: int) -> None:
        self.row: int = row
        self.col: int = col
        self.facing: int = facing

    def copy(self):
        # type: () -> Ship
        return Ship(row=self.row, col=self.col, facing=self.facing)

    def move(self, instruction: Instruction):
        trajectory: Tuple[int, int, int] = instruction.get_trajectory(self.facing)
        self.row += trajectory[0]
        self.col += trajectory[1]
        # From a list of valid values ([0,1,2,3]), select the one that appears
        # when going through in the direction the number of steps in trajectory.
        self.facing = list(range(4))[(self.facing + trajectory[2]) % 4]


t0 = time.perf_counter()

instructions: List[Instruction] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        m = re.fullmatch(r"(\w)(\d+)\n", l)
        if not m:
            raise ValueError(f"Invalid line: {l}")

        ins: str
        val_s: str
        ins, val_s = m.groups()
        val: int = int(val_s)

        instructions.append(Instruction(instruction_s=ins, value=val))

t1 = time.perf_counter()

ship_start: Ship = Ship(row=0, col=0, facing=AbsDirection("E").to_facing())
ship: Ship = ship_start.copy()

for instruction in instructions:
    ship.move(instruction)

t2 = time.perf_counter()

# Get Manhattan distance between original and final ship position


def manhattan_distance(start: Ship, end: Ship) -> int:
    north_south: int = abs(start.row - end.row)
    east_west: int = abs(start.col - end.col)
    return north_south + east_west


md: int = manhattan_distance(ship_start, ship)

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: Manhattan distance = {md}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Move ship: {tf(t2-t1)}\n"
    f"Calculate Manhattan distance: {tf(t3-t2)}\n"
    # f"Simulate: {tf(t4-t3)}\n"
    # f"Count occupied seats: {tf(t5-t4)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
