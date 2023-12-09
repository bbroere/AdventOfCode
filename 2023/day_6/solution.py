import math


def part_1(filename: str) -> int:
    # split it up
    times, distances = open(filename, "r").read().split('\n')
    times = [int(x) for x in times.split()[1:]]
    distances = [int(x) for x in distances.split()[1:]]
    # running result
    res = 1
    # loop over races
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]
        # minimum winning holding time is determined by abc-formula
        # time = t, record = r, hold time = h, winning distance would be r + 1 and h would also be the velocity in mm/ms
        # velocity = distance / time = (r + 1) / (t - h) = h
        # so h^2 - th + (r + 1) = 0 -> abc formula (only minimum is required)
        # h = (t - sqrt(t^2 - 4 (r + 1) ) ) / 2
        min_winning_holding_time = math.ceil((time - math.sqrt(time * time - 4 * (distance + 1))) / 2)
        # determine number of winning ways (symmetrical)
        nof_winning_ways = (time - 2 * min_winning_holding_time + 1)
        # multiply running result
        res *= nof_winning_ways
    return res


# actually simpler than part 1 if you math :)
def part_2(filename: str) -> int:
    # get race time and distance
    time, distance = open(filename, "r").read().split('\n')
    time = int("".join(time.split()[1:]))
    distance = int("".join(distance.split()[1:]))
    # minimum winning holding time is determined by abc-formula
    # time = t, record = r, hold time = h, winning distance would be r + 1 and h would also be the velocity in mm/ms
    # velocity = distance / time = (r + 1) / (t - h) = h
    # so h^2 - th + (r + 1) = 0 -> abc formula (only minimum is required)
    # h = (t - sqrt(t^2 - 4 (r + 1) ) ) / 2
    min_winning_holding_time = math.ceil((time - math.sqrt(time * time - 4 * (distance + 1))) / 2)
    # determine number of winning ways (symmetrical)
    return time - 2 * min_winning_holding_time + 1
