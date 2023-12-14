# Kudos to hyper-neutrino for the python tricks and making sure my part 2 solution does not take over 2 days
# (https://github.com/hyper-neutrino)

# keep cache of all counts as the number of computations blows up quickly
cache: dict[(str, tuple[int]), int] = {}


def count(configuration: str, failures_tuple: tuple[int]) -> int:
    # recursion base
    # case 1: end of line, so only valid if we don't need to add another failed spring ('#')
    # (so failure tuples is empty)
    if configuration == "":
        return 1 if failures_tuple == () else 0
    # case 2: if we have 0 '#'s left to put in somewhere, and we still have '#'s in the configuration,
    # return 0 as this can't be ok (so this option is not valid)
    # if we don't have '#'s anymore, there is only one solution, everything should be a '.', including all '?'s
    if failures_tuple == ():
        return 0 if '#' in configuration else 1
    # recursion
    # first check cache
    key = (configuration, failures_tuple)
    if key in cache:
        return cache[key]
    # keep running total
    res = 0
    # if the first character is a . (operational) or '?', we need to consider the state where the '?' is a '.'
    # and hence operational
    # we count the options if we just ignore this character, as it does not count towards the overall failure counts
    if configuration[0] in '.?':
        # so count for same failure tuple and first character of configuration removed
        res += count(configuration[1:], failures_tuple)
    # if the first character is a '#' (failure) or a '?', we consider that '?' is a '#' as well
    # we need to verify if this can be the start of a block of '#'s with length of failure_tuples[0]
    # if so, we found a solution for each of the possibilities that can be made in the remainder of the configuration
    if configuration[0] in '#?':
        # check if this place can be the start of a block and if so, count the options in the remainder of the string
        if (
                # we can't expect X broken springs is we only have less than X spaces
                failures_tuple[0] <= len(configuration) and
                # we also need to be sure there is no defined operational spring in the next number amount of places
                "." not in configuration[:failures_tuple[0]] and
                # the spring after this block needs to be operational (either '.', '?') or end of line
                (
                        # reach end of line
                        failures_tuple[0] == len(configuration) or
                        # it can't be knowingly broken as then the block would be too large
                        configuration[failures_tuple[0]] != '#'
                )
        ):
            # count for next block (note; +1 removes the '.' or '?' after the block as you don't want a new block
            # to start at that position (the '?' could be interpreted as a '#' where you don't want that)
            res += count(configuration[failures_tuple[0] + 1:], failures_tuple[1:])
    # store in cache
    cache[key] = res
    # return result
    return res


def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # running total
    res = 0
    # determine count for each line and add it
    for line in lines:
        # split it up
        configuration, failures_tuple = line.split()
        # use tuple to make sure we can't append/pop etc
        failures_tuple = tuple(map(int, failures_tuple.split(',')))
        # add result
        res += count(configuration, failures_tuple)
    return res


def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # running total
    res = 0
    # determine count for each line and add it
    for line in lines:
        # split it up
        config, failures_tuple = line.split()
        # use tuple to make sure we can't append/pop etc
        failures_tuple = tuple(map(int, failures_tuple.split(',')))
        # multiply config and failures_tuple, otherwise the same as part 1 (but added cache)
        config = "?".join([config] * 5)
        failures_tuple *= 5  # you can multiply list and tuples directly
        # add result
        res += count(config, failures_tuple)
    return res
