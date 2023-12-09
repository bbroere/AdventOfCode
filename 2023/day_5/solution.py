def part_1(filename: str) -> int:
    # split input into seeds and maps
    seeds, *maps = open(filename, 'r').read().split('\n\n')
    seeds = [int(x) for x in seeds.split(': ')[1].split()]
    maps = list(map(lambda t: list(map(lambda tt: [int(x) for x in tt.split()], t.split('\n')[1:])), maps))
    # running result
    res = []
    # loop over seeds
    for seed in seeds:
        loc = seed
        # determine each step with map
        for m in maps:
            # set temp location
            nloc = None
            # loop over every entry in the map
            for [dest_st, orig_st, size] in m:
                # if it is in the range, return the end location
                if orig_st <= loc < orig_st + size:
                    nloc = dest_st + loc - orig_st
            # if it is not in any range, return location
            if nloc is not None:
                loc = nloc
        # store end location
        res.append(loc)
    # return minimum
    return min(res)


def part_2(filename: str) -> int:
    # split input into seeds and maps
    seeds, *maps = open(filename, 'r').read().split('\n\n')
    seeds = [int(x) for x in seeds.split(': ')[1].split()]
    # split into ranges
    seeds = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, int(len(seeds)), 2)]
    maps = list(map(lambda t: list(map(lambda tt: [int(x) for x in tt.split()], t.split('\n')[1:])), maps))
    # set origins to seeds initially
    origins = seeds
    # loop over maps
    for m in maps:
        # keep temp array
        destinations = []
        # loop over all origins and get the range (remove is fine)
        while len(origins):
            start, end = origins.pop()
            # now loop over all the ranges in the map (using for-else!!)
            for [dest_st, orig_st, size] in m:
                # determine overlap
                o_start = max(start, orig_st)
                o_end = min(end, orig_st + size)
                # if there is overlap, set destination range
                if o_start < o_end:
                    destinations.append((o_start - orig_st + dest_st, o_end - orig_st + dest_st))
                    if o_start > start:
                        origins.append((start, o_start))
                    if o_end < end:
                        origins.append((o_end, end))
                    break  # if no overlap, append original origin pair
            else:
                # no overlap, so add original pair
                destinations.append((start, end))
        # new origins as we move up a map
        origins = destinations
    # return min (left side) of first range
    return min(origins)[0]
