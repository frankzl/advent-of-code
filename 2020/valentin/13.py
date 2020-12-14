import sys
import time
from typing import List, Tuple

# Shuttle Search
#
# - Buses have ID that indicates the departure rhythm
# - Schedule based on timestamp = number of minutes since reference time
# - Timestamp 0: Every bus departs
# -
# -

t0 = time.perf_counter()

with open(sys.argv[1], "r") as f:
    lines: List[str] = [l[:-1] for l in f.readlines()]

t1 = time.perf_counter()

# Part 1: (ID of earliest bus that we can take) * (number of minutes we need to wait for the bus)


def find_earliest_and_time() -> Tuple[int, int]:
    depart_time: int = int(lines[0])
    buses: List[int] = [int(b) for b in lines[1].split(",") if b != "x"]

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
earliest_bus_id, time_to_wait = find_earliest_and_time()

t2 = time.perf_counter()


from util import tf

print(
    f"Result = {earliest_bus_id * time_to_wait}\n"
    f"Earliest bus = {earliest_bus_id}\n"
    f"Time to wait = {time_to_wait}\n"
    f"\n"
    f"Parse file: {tf(t1-t0)}\n"
    f"Find earliest and time: {tf(t2-t1)}\n"
    f"=====\n"
    f"Total: {tf(t2-t0)}"
)
