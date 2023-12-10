def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # keep running result
    res = 0
    # loop over lines
    for line in lines:
        # split up game
        game_start, rounds = line.split(": ")
        # split up all draws in red, green, blue (individual rounds don't matter)
        draws = rounds.replace(";", ",").split(", ")
        red_draws = filter(lambda d: "red" in d, draws)
        green_draws = filter(lambda d: "green" in d, draws)
        blue_draws = filter(lambda d: "blue" in d, draws)
        # determine the amount of r/g/b draws that went over limit
        reds_over_limit = filter(lambda t: t > 12, map(lambda t: int(t.split()[0]), red_draws))
        greens_over_limit = filter(lambda t: t > 13, map(lambda t: int(t.split()[0]), green_draws))
        blues_over_limit = filter(lambda t: t > 14, map(lambda t: int(t.split()[0]), blue_draws))
        # if these are all empty, add id to total
        if not bool(list(reds_over_limit)) and not bool(list(greens_over_limit)) and not bool(list(blues_over_limit)):
            res += int(game_start.split()[1])
    return res


def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # keep running result
    res = 0
    # loop over lines
    for line in lines:
        # split up game
        _, rounds = line.split(": ")
        # split up all draws in red, green, blue (individual rounds don't matter)
        draws = rounds.replace(";", ",").split(", ")
        red_draws = filter(lambda d: "red" in d, draws)
        green_draws = filter(lambda d: "green" in d, draws)
        blue_draws = filter(lambda d: "blue" in d, draws)
        # determine the max for all draws
        reds_max = max(map(lambda t: int(t.split()[0]), red_draws))
        greens_max = max(map(lambda t: int(t.split()[0]), green_draws))
        blues_max = max(map(lambda t: int(t.split()[0]), blue_draws))
        # calculate product and add to result
        res += reds_max * greens_max * blues_max
    return res
