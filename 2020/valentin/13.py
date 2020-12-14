import sys
import time
from typing import List, Tuple, Union

# pylint: disable=unsubscriptable-object

# Shuttle Search
#
# - Buses have ID that indicates the departure rhythm
# - Schedule based on timestamp = number of minutes since reference time
# - Timestamp 0: Every bus departs

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    lines: List[str] = [l[:-1] for l in f.readlines()]

t1 = time.perf_counter()

# Part 1: (ID of earliest bus that we can take) * (number of minutes we need to wait for the bus)


def find_earliest_and_time(depart_time: int, buses: List[int]) -> Tuple[int, int]:
    current_time: int = depart_time
    while True:
        for bus in buses:
            if current_time % bus == 0:
                earliest_bus_id = bus
                time_to_wait = current_time - depart_time
                return earliest_bus_id, time_to_wait
        current_time += 1


earliest_bus_id: int
time_to_wait: int
earliest_bus_id, time_to_wait = find_earliest_and_time(
    depart_time=int(lines[0]), buses=[int(b) for b in lines[1].split(",") if b != "x"]
)

t2 = time.perf_counter()

# Part 2: Find earliest timestamp so that each tick the next bus from the list departs (x is empty)

current_start: int = 0
if len(sys.argv) > 2:
    current_start = int(sys.argv[2])


def find_first_valid_timestamp() -> int:
    global current_start

    buses_and_skips: List[Union[int, str]] = [
        int(b) if b != "x" else b for b in lines[1].split(",")
    ]

    buses_with_offsets: List[Tuple[int, int]] = sorted(
        [(int(b), i) for (i, b) in enumerate(buses_and_skips) if b != "x"],
        key=lambda bi: bi[0],
        reverse=True,
    )

    # Idea: Go through buses, find earliest time for first, then second ... and restart if none is found.
    bus: int
    offset: int
    # We skip by the largest possible value in each step, a.k.a. the largest bus ID.
    base_skip: int
    skip_offset: int
    base_skip, skip_offset = buses_with_offsets[0]

    # As we skip with a bus that has an offset, we have to offset our tested value accordingly.
    current_start -= skip_offset

    # Sort again by offset, as this fails faster if the start is wrong.
    buses_with_offsets = sorted(buses_with_offsets, key=lambda bi: bi[1])

    while True:
        try:
            for bus, offset in buses_with_offsets:
                if (current_start + offset) % bus == 0:
                    continue

                # time_to_wait > offset means the schedule is invalid
                raise RuntimeError()

            # We found a valid slot
            return current_start
        except RuntimeError:
            current_start += base_skip


first_valid_timestamp: int = find_first_valid_timestamp()

t3 = time.perf_counter()


from util import tf

print(
    f"Part 1: {earliest_bus_id * time_to_wait}\n"
    f" (Earliest bus: {earliest_bus_id}, wait time: {time_to_wait}\n"
    f"Part 2: {first_valid_timestamp}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Part 1: Find earliest and time: {tf(t2-t1)}\n"
    f"Part 2: Find earliest valid timestamp: {tf(t3-t2)}\n"
    f"=====\n"
    f"Total: {tf(t3-t0)}"
)
