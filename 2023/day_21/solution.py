import math
from copy import copy


def part_1(filename: str, extra_steps: int = 64) -> int:
    lines = open(filename).read().splitlines()
    # make grid, get S and replace S
    grid = [[*line] for line in lines]
    ((s_y, s_x),) = [(i, row.index('S')) for i, row in enumerate(grid) if 'S' in row]
    grid[s_y][s_x] = '.'
    # call function and return
    return len(determine_occupied_after_steps(grid, [(s_y, s_x)], extra_steps))


# extended with list of starting points for part 2
def determine_occupied_after_steps(grid: list[list[str]], starting_points: list[(int, int)], nof_steps: int) \
        -> set[(int, int)]:
    # start set of occupied points in only starting point
    occupied_points = {*starting_points}
    # now loop
    for _ in range(nof_steps):
        new_occupied_points = set()
        # set new occupied points, keeping boundary in mind
        for (x_p, y_p) in occupied_points:
            if 0 < x_p and grid[y_p][x_p - 1] == '.':
                new_occupied_points.add((x_p - 1, y_p))
            if x_p < len(grid[0]) - 1 and grid[y_p][x_p + 1] == '.':
                new_occupied_points.add((x_p + 1, y_p))
            if 0 < y_p and grid[y_p - 1][x_p] == '.':
                new_occupied_points.add((x_p, y_p - 1))
            if y_p < len(grid) - 1 and grid[y_p + 1][x_p] == '.':
                new_occupied_points.add((x_p, y_p + 1))
        occupied_points = copy(new_occupied_points)
    # return amount of occupied points
    return occupied_points


def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # make grid, get S and replace S
    grid = [[*line] for line in lines]
    ((s_y, s_x),) = [(i, row.index('S')) for i, row in enumerate(grid) if 'S' in row]
    grid[s_y][s_x] = '.'
    # some constants
    L = len(grid)
    I = int((L - 1) / 2)
    T = 26501365
    # a couple of assumptions
    # we start in the middle of the grid, and the grid is square
    assert s_x == s_y == I == (len(grid[0]) - 1) / 2
    # also the entire row and column of S are walkable
    assert all([grid[s_y][t] == '.' and grid[t][s_x] == '.' for t in range(L)])
    # also the outside border is completely walkable
    assert all([
        grid[0][t] == '.' and grid[L - 1][t] == '.' and grid[t][L - 1] == '.' and grid[t][0] == '.' for t in range(L)
    ])
    # lastly, every other row and column has at least one # in it
    assert sum([1 if '#' not in row else 0 for row in grid]) == 3
    assert sum([1 if '#' not in col else 0 for col in list(zip(*grid))]) == 3
    # also, the length from the center to one of the outside borders is odd
    assert I % 2 == 1
    # together, these assumptions mean that we can calculate how big our grid will end up being
    # as we know we need to take T steps, we can end up T places away from the starting point in every
    # direction
    # we can reach the side of the first grid in I = (L-1) / 2 steps, so we have (T - I) steps remaining
    # if we divide this by the length of the grid and round it up, we get how many grids to each size we will travel to
    # in each of the cardinal directions (we see this is even)
    # note that this is exactly an even amount of grids, so we end at the end of a grid if that makes sense
    nof_grids_to_x = math.ceil((T - I) / L)  # this number seems to be 202300, so my guess is this is correct
    assert nof_grids_to_x == (T - I) // L
    assert nof_grids_to_x % 2 == 0
    # together, this will form a flattened star-shaped grid of grids where the grids on the outside are only partially
    # travelled all the other grids can be traveled through completely as long as we took the minimum amount of steps
    # needed to (in theory) travel to all points
    # we can determine this number of steps needed for a single (the original) grid but that does not seem needed
    # herein lies another assumption all but the outside grids will be completely travelled
    # note that neighboring (cardinal only) grids will, in the end, have the opposite state of tiles reachable
    # this is because the width of the grid is odd, and thus the mirror point of a point in one of the directions will
    # have the same state
    # as we know, a point can't be reachable both on an even and an odd step, it is either one or the other, that's just
    # how stepping along cardinal directions in a grid works (think of chess)
    # so what we need to do is determine the amount of even and odd reachable plots is for our base grid in the end
    # if we know this, we can determine how many 'even' and 'odd' grids we have (minus the outside border)
    # another crucial observation for the outside border is that we only need travel through these grids starting from
    # the position directly from the centers of the adjacent grids (special exception below!)
    # this is because the + in the center of the grids is empty and we know that those, together with the outside box,
    # are the only empty rows and columns
    # as the star is flattened, the last grids along the star shape also enter another set of grids, marked with X below
    #   X*X
    #  X***X
    # X*****X
    # *******
    # X*****X
    #  X***X
    #   X*X

    # now start with the outside border
    # what we also need to think about for the grids on the outside border is what the step count is when we first enter
    # as seen from the central starting position, we enter grid n on the right on step I + n * L + 1
    # also note that we enter every grid on the outside ring on the same moment, being on step
    last_entry_step = I + (nof_grids_to_x - 1) * L + 1
    # so we still need to do T - last_entry_step steps in the last grids after we enter them
    steps_in_last_grids = T - last_entry_step
    # for the small extra X grids in the above explanation, we also still need to do some steps
    # as we can assume we enter these parts from a corner of the grid tile, we need to travel there from  the other
    # outside grids, which we enter centered on a boundary line
    # this means we still need to take I steps to get into that grid before we enter the new one, which leaves us with
    steps_in_lastest_grids = steps_in_last_grids - I - 1

    # we will now build a map of the possibilities on the boundary with their counts
    boundary_grids = {
        "left_entry": (
            1,
            len(determine_occupied_after_steps(copy(grid), [(0, s_y)], steps_in_last_grids))
        ),
        "right_entry": (
            1,
            len(determine_occupied_after_steps(copy(grid), [(L - 1, s_y)], steps_in_last_grids))
        ),
        "bottom_entry": (
            1,
            len(determine_occupied_after_steps(copy(grid), [(s_x, L - 1)], steps_in_last_grids))
        ),
        "top_entry": (
            1,
            len(determine_occupied_after_steps(copy(grid), [(s_x, 0)], steps_in_last_grids))
        ),
        "left_bottom_entry": (
            nof_grids_to_x - 1,
            len(determine_occupied_after_steps(copy(grid), [(0, s_y), (s_x, L - 1)], steps_in_last_grids))
        ),
        "left_top_entry": (
            nof_grids_to_x - 1,
            len(determine_occupied_after_steps(copy(grid), [(0, s_y), (s_x, 0)], steps_in_last_grids))
        ),
        "right_bottom_entry": (
            nof_grids_to_x - 1,
            len(determine_occupied_after_steps(copy(grid), [(L - 1, s_y), (s_x, L - 1)], steps_in_last_grids))
        ),
        "right_top_entry": (
            nof_grids_to_x - 1,
            len(determine_occupied_after_steps(copy(grid), [(L - 1, s_y), (s_x, 0)], steps_in_last_grids))
        ),
        "left_bottom_corner_entry": (
            nof_grids_to_x,
            len(determine_occupied_after_steps(copy(grid), [(0, L - 1)], steps_in_lastest_grids))
        ),
        "left_top_corner_entry": (
            nof_grids_to_x,
            len(determine_occupied_after_steps(copy(grid), [(0, 0)], steps_in_lastest_grids))
        ),
        "right_bottom_corner_entry": (
            nof_grids_to_x,
            len(determine_occupied_after_steps(copy(grid), [(L - 1, L - 1)], steps_in_lastest_grids))
        ),
        "right_top_corner_entry": (
            nof_grids_to_x,
            len(determine_occupied_after_steps(copy(grid), [(L - 1, 0)], steps_in_lastest_grids))
        ),
    }
    # now sum all the occupied points for the boundary
    boundary_total = sum(t[0] * t[1] for t in boundary_grids.values())

    # we first determine the number of evens and odds for a completely filled grid (once)
    e_pts = determine_occupied_after_steps(copy(grid), [(s_x, s_y)], 2 * len(grid) + 10)
    total_even = len(e_pts)
    o_pts = determine_occupied_after_steps(copy(grid), list(copy(e_pts)), 1)
    total_odd = len(o_pts)
    assert len(e_pts.intersection(o_pts)) == 0

    # now for the inner part
    # we can calculate that we have:
    # 1 + 4 * ((nof_grids_to_x - 1) + (nof_grids_to_x - 2) + .... + 1) = 1 + 4 * (1/2) * (nof_grids_to_x - 1) * (nof_grids_to_x)
    # grids in total of which we need to determine the amount of even and odd state grids
    # we know we take an odd amount of steps, so the central one is odd and it is surrounded by even
    # we can calculate the amount of even inner grids as follows:
    nof_even_grids = 4 * sum(i if i % 2 == 1 else 0 for i in range(nof_grids_to_x))
    # the amount of odd grids can be calculated also
    nof_odd_grids = int(1 + 4 * (1 / 2) * (nof_grids_to_x - 1) * nof_grids_to_x - nof_even_grids)
    # with this we get
    inner_total = nof_even_grids * total_even + nof_odd_grids * total_odd
    return boundary_total + inner_total
