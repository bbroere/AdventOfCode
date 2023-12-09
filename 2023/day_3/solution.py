def part_1(filename: str) -> int:
    lines = open(filename, "r").read().split('\n')
    # keep running total
    res = 0
    # loop over lines as index
    for i in range(len(lines)):
        # start at beginning
        j = 0
        while j < len(lines[i]):
            # set result and neighbors array
            r = ""
            neighbors = []
            # while we find a digit, add to r and add neighbors
            while j < len(lines[i]) and lines[i][j].isdigit():
                r += lines[i][j]
                # determine one line above and one below (if possible)
                nls = lines[max(0, i - 1):min(max(0, i - 1) + 3, len(lines) - 1)]
                for nl in nls:
                    # this adds duplicates, but who cares as this array will be small anyway
                    neighbors.extend(nl[max(0, j - 1):min(max(0, j - 1) + 3, len(lines[0]) - 1)])
                # increment index
                j += 1
            # if there is a special symbol, add to res
            if len(list(filter(lambda t: not t.isdigit() and not t == '.', neighbors))) > 0:
                res += int(r)
            # and continue
            j += 1
    return res


def part_2(filename: str) -> int:
    lines = open(filename, "r").read().split('\n')
    # keep running total
    res = 0
    # determine gear locations and set ration to 1
    gear_loc_ratios: dict[(int, int), int] = {}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "*":
                gear_loc_ratios[(i, j)] = 1
    # keep track of all neighbors
    all_neighbors: list[(int, int)] = []
    # loop over lines as index
    for i in range(len(lines)):
        # start at beginning
        j = 0
        while j < len(lines[i]):
            # set result and neighbors array
            r = ""
            # keep track of neighbors in set (don't want duplicates here)
            neighbor_locs = set()
            # while we find a digit, add to r and add neighbors
            while j < len(lines[i]) and lines[i][j].isdigit():
                r += lines[i][j]
                # determine for one line above and one below (if possible) the neighbors
                for s in range(max(0, i - 1), min(max(0, i - 1) + 3, len(lines) - 1)):
                    for t in range(max(0, j - 1), min(max(0, j - 1) + 3, len(lines[0]) - 1)):
                        # add to neighbors
                        neighbor_locs.add((s, t))
                # increment index
                j += 1
            # on per-number basis add to global list
            all_neighbors.extend(list(neighbor_locs))
            # if neighbor loc is gear, multiply the ratio
            for loc in neighbor_locs:
                if gear_loc_ratios.get(loc) is not None:
                    gear_loc_ratios[loc] *= int(r)
            j += 1
    # filter all gears s.t. exactly two neighbors have been found and add to result
    for g in filter(lambda ge: all_neighbors.count(ge) == 2, gear_loc_ratios.keys()):
        res += gear_loc_ratios[g]
    return res
