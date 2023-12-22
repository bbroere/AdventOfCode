# Kudos to hyper-neutrino for reminding me of the awesome mathematical algorithms that make life easier
# (and part 2 actually terminate)
# (https://github.com/hyper-neutrino)

def calculate_loop_area(instructions: list[(str, int)]) -> int:
    # keep array of points visited along the path
    points = [(0, 0)]
    direction_map = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    # keep track of length of boundary
    boundary = 0
    # loop over all lines
    for instruction in instructions:
        # split up and don't care about the color
        direction, steps = instruction
        # get direction
        dx, dy = direction_map[direction]
        # take last point visited
        x, y = points[-1]
        # add new point to the list (...*steps helps as this is 0 in the direction you don't travel!)
        # note that we also don't care about negative values, it's fine!
        points.append((x + dx * steps, y + dy * steps))
        # increment boundary by steps taken
        boundary += steps
    # use shoelace formula to get the area on the inside of the polygon
    # A = (1/2) * | sum_{i=1}^n x_i * (y_{i+1} - y_{i-1} ) |
    # note that this includes only 'halves' of the outside as the coordinates of the points are in the center
    # you can't easily correct this as corners might contribute either 3/4 or 1/4, which you don't know
    area = abs(sum(points[i][0] * (points[i - 1][1] - points[i + 1][1]) for i in range(len(points) - 1))) // 2
    # now use picks theorem to find the number of integer points inside the polygon
    # A = i - 1 + b/2 where A is area and b is number of boundary points
    interior = area + 1 - (boundary // 2)
    # return boundary and interior combined!
    return interior + boundary


def part_1(filename: str) -> int:
    return calculate_loop_area([(x.split()[0], int(x.split()[1])) for x in open(filename).read().splitlines()])


def part_2(filename: str) -> int:
    instructions = []
    for x in open(filename).read().splitlines():
        # get hex code
        hex_code = x.split()[2]
        d = hex_code[-2]  # braces!
        # determine direction from last digit
        direction = 'R' if d == '0' else 'D' if d == '1' else 'L' if d == '2' else 'U'
        # convert distance to int from base 16
        distance = int(hex_code[2:7], 16)  # braces!
        # add to list
        instructions.append((direction, distance))
    return calculate_loop_area(instructions)
