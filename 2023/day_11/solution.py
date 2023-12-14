# Kudos to hyper-neutrino for the python tricks (https://github.com/hyper-neutrino)

def part_1(filename: str, multiplier: int = 2) -> int:
    lines = open(filename).read().splitlines()
    # loop over all lines and keep track of row and col numbers that are empty
    rows = [r for r, row in enumerate(lines) if all(c == '.' for c in row)]
    # zip grid makes it enumerate over the columns one by one!
    cols = [c for c, col in enumerate(zip(*lines)) if all(c == '.' for c in col)]
    # double for things loop over everything
    coordinates = [(r, c) for r, row in enumerate(lines) for c, col in enumerate(row) if col == "#"]
    # running result
    res = 0
    # loop over all pairs
    for i, (px, py) in enumerate(coordinates):
        for (qx, qy) in coordinates[:i]:  # this means only up to index i
            # add one for every distance between both the x and y coordinates, but multiplier times if this is empty
            # note the min/max for beginning/end of lines/columns
            for x in range(min(px, qx), max(px, qx)):
                res += multiplier if x in rows else 1
            for y in range(min(py, qy), max(py, qy)):
                res += multiplier if y in cols else 1
    return res


# same as part 1 but with added distance 1000000
def part_2(filename: str) -> int:
    return part_1(filename, 1000000)
