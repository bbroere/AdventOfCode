def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # start by transposing
    lines = list(map("".join, zip(*lines)))
    # split by '#' which gives groups of '.' and 'O' characters
    line_groups = [line.split("#") for line in lines]
    # sort these groups (reversed s.t. 'O' comes before '.' and mash them together again
    line_groups = [["".join(sorted(list(g), reverse=True)) for g in group] for group in line_groups]
    # finally merge them on '#' again
    lines = ["#".join(groups) for groups in line_groups]
    # re-transpose
    lines = list(map("".join, zip(*lines)))
    # now count weights of the lines by summing over the amount of 'O's in the line and multiply it by index
    line_weights = list(line.count("O") * (len(lines) - j) for j, line in enumerate(lines))
    # sum of these is the result
    return sum(line_weights)


# Kudos to hyper-neutrino for the python tricks with the tuples (which are a LOT faster than dicts which I used first)
# (https://github.com/hyper-neutrino)

# cycled the grid 4 times, applying 'gravity' on each step
def cycle_grid(lines: tuple[str]) -> tuple[str]:
    # 4 times in total
    for _ in range(4):
        # start by transposing
        lines = tuple(map("".join, zip(*lines)))
        # split by '#' which gives groups of '.' and 'O' characters
        line_groups = [line.split("#") for line in lines]
        # sort these groups (reversed s.t. 'O' comes before '.' and mash them together again
        line_groups = [["".join(sorted(tuple(g), reverse=True)) for g in group] for group in line_groups]
        # finally merge them on '#' again
        lines = ["#".join(groups) for groups in line_groups]
        # now we flip all the rows, s.t. we end up with a (because we already transposed it) 90 degree clockwise rotation
        lines = [line[::-1] for line in lines]
    # return it as a tuple
    return tuple(lines)


def part_2(filename: str) -> int:
    # read just as in part 1 but make it a tuple to use in the cache (lists cannot be in sets)
    lines = tuple(open(filename).read().splitlines())
    # cache of all configurations we've seen, starting with the og
    cache = {lines}
    # also keep it in a list to iterate through it later
    states = [lines]
    # current amount of iterations
    it = 0
    # now loop, max 1bln times, but assume there is a cycle in there somewhere
    while True:
        # perform cycle
        lines = cycle_grid(lines)
        # add to iteration
        it += 1
        # if we've seen it before, done!
        if lines in cache:
            break
        else:
            # otherwise add to cache and list
            cache.add(lines)
            states.append(lines)
    # determine when it was first seen and the length of the cycle
    first_seen = states.index(lines)
    cycle_length = it - first_seen
    # we can determine the final grid by subtracting the initial (first_seen-1) elements and doing some modulo
    # calculations with modulo length of cycle
    final_grid = states[(1000000000 - first_seen) % cycle_length + first_seen]
    # now count weights of the lines by summing over the amount of 'O's in the line and multiply it by index
    line_weights = list(line.count("O") * (len(lines) - j) for j, line in enumerate(final_grid))
    # sum of these is the result
    return sum(line_weights)
