import sys
import time
from typing import Callable, Dict, Iterable, List, Optional, Tuple

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


def iterate(seat_map: List[List[str]]) -> Iterable[Tuple[int, int, str]]:
    for i in range(len(seat_map)):
        for j in range(len(seat_map[i])):
            yield i, j, seat_map[i][j]


t1 = time.perf_counter()


is_occupied_seat: Callable[[str], bool] = lambda x: x == "#"
is_empty_seat: Callable[[str], bool] = lambda x: x == "L"
is_seat: Callable[[str], bool] = lambda x: is_occupied_seat(x) or is_empty_seat(x)


def get_seat_positions(seat_map: List[List[str]]) -> Dict[int, List[int]]:
    seat_positions: Dict[int, List[int]] = {i: [] for i in range(len(seat_map))}

    for i, j, seat in iterate(seat_map):
        if is_seat(seat):
            seat_positions[i].append(j)

    return seat_positions


def simulate_seat(seat_map: List[List[str]], row: int, col: int) -> Optional[str]:
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
        return "#"
    elif is_occupied_seat(own_seat) and occupied >= 4:
        return "L"
    else:
        return None


def simulate(seat_positions: Dict[int, List[int]]) -> bool:
    """ Simulate one round. Returns flag denoting if any change happened. """
    global seat_map

    # We need a copy to not influence later seats with in-place modifications.
    changes: List[Tuple[int, int, str]] = []

    for i, js in seat_positions.items():
        # change_occurred |= any([simulate_seat(seat_map_copy, row=i, col=j) for j in js])
        for j in js:
            if change := simulate_seat(seat_map, row=i, col=j):
                changes.append((i, j, change))

    for i, j, new_seat in changes:
        seat_map[i][j] = new_seat

    return len(changes) > 0


seat_positions: Dict[int, List[int]] = get_seat_positions(seat_map=seat_map)

t2 = time.perf_counter()

while simulate(seat_positions):
    pass

t3 = time.perf_counter()

occupied_seats: int = sum([row.count("#") for row in seat_map])

t4 = time.perf_counter()


from util import tf

print(
    f"Part 1: Occupied seats = {occupied_seats}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Get seat positions: {tf(t2-t1)}\n"
    f"Simulate: {tf(t3-t2)}\n"
    f"Count occupied seats: {tf(t4-t3)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
