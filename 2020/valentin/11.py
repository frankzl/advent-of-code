import sys
import time
from typing import Callable, Dict, List

# Seating System
#
# - 2D layout
# - Floor (.), empty seat (L), or occupied seat (#)
# - Placement rules
#   + Empty seat with no occupied seats around: Occupied
#   + Occupied seat with 4+ occupied seats adjacend: Emptied
#   + Otherwise: stable
#   + Floor is stable

# Part 1: Simulate until situation is stable; how many seats are occupied?

t0 = time.perf_counter()

seat_map: List[List[str]] = []

with open(sys.argv[1], "r") as f:
    for l in f:
        seat_map.append(list(l[:-1]))

t1 = time.perf_counter()


is_occupied_seat: Callable[[str], bool] = lambda x: x == "#"
is_empty_seat: Callable[[str], bool] = lambda x: x == "L"
is_seat: Callable[[str], bool] = lambda x: is_occupied_seat(x) or is_empty_seat(x)


def get_seat_positions(seat_map: List[List[str]]) -> Dict[int, List[int]]:
    seat_positions: Dict[int, List[int]] = {i: [] for i in range(len(seat_map))}

    for i in range(len(seat_map)):
        for j in range(len(seat_map[i])):
            if is_seat(seat_map[i][j]):
                seat_positions[i].append(j)

    return seat_positions


def simulate_seat(seat_map: List[List[str]], row: int, col: int) -> bool:
    min_row: int = max(0, row - 1)
    min_col: int = max(0, col - 1)
    max_row: int = min(row + 1, len(seat_map) - 1)
    max_col: int = min(col + 1, len(seat_map[max_row]) - 1)

    occupied: int = 0
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if i == row and j == col:
                continue

            if is_occupied_seat(seat_map[i][j]):
                occupied += 1

    own_seat: str = seat_map[row][col]
    if is_empty_seat(own_seat) and occupied == 0:
        seat_map[row][col] = "#"
        return True
    elif is_occupied_seat(own_seat) and occupied >= 4:
        seat_map[row][col] = "L"
        return True
    else:
        return False


def simulate(seat_positions: Dict[int, List[int]]) -> bool:
    """ Simulate one round. Returns if any change happened. """
    global seat_map

    change_occurred: bool = False

    for i, js in seat_positions.items():
        for j in js:
            change_occurred |= simulate_seat(seat_map, row=i, col=j)

    return change_occurred


seat_positions: Dict[int, List[int]] = get_seat_positions(seat_map=seat_map)

for row in seat_map:
    print(row)

print("\n")

for i in range(len(seat_map)):
    for j in range(len(seat_map[i])):
        print(simulate_seat(seat_map, i, j), end="")
    print()

while simulate(seat_positions):
    pass

t2 = time.perf_counter()

occupied_seats: int = sum([row.count("#") for row in seat_map])

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: Occupied seats = {occupied_seats}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Simulate: {tf(t2-t1)}\n"
    f"Count occupied seats: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
