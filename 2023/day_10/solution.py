from collections import deque


# Kudo's to hyper-neutrino for the python knowledge (https://github.com/hyper-neutrino)
def part_1(filename: str) -> int:
    grid = open(filename).read().splitlines()
    # first find start
    sc, sr = None, None
    for j, row in enumerate(grid):
        for i, character in enumerate(row):
            if character == "S":
                sc, sr = i, j
                # if this break happens, the else is skipped and the break for big for is called
                # otherwise the else is called and the break is below it is skipped
                break
        else:
            continue
        break
    # keep track of the path
    path_coordinates = {(sr, sc)}
    # queue for breath-first-search
    queue = deque([(sr, sc)])
    # keep going until queue is empty
    while queue:
        # get first character of queue (get left, add right)
        j, i = queue.popleft()
        character = grid[j][i]

        # now we check if the character can go up
        # this means the character must be a pipe with opening at the top
        # also the character it points to needs to accept from the bottom
        if j > 0 and character in "S|JL" and grid[j - 1][i] in "|7F" and (j - 1, i) not in path_coordinates:
            path_coordinates.add((j - 1, i))
            queue.append((j - 1, i))
        # same as above, but for going down
        if j < len(grid) - 1 and character in "S|7F" and grid[j + 1][i] in "|JL" and (j + 1, i) not in path_coordinates:
            path_coordinates.add((j + 1, i))
            queue.append((j + 1, i))
        # going right
        if i > 0 and character in "S-J7" and grid[j][i - 1] in "-LF" and (j, i - 1) not in path_coordinates:
            path_coordinates.add((j, i - 1))
            queue.append((j, i - 1))
        # going left
        if (i < len(grid[j]) - 1 and character in "S-LF" and grid[j][i + 1] in "-J7" and
                (j, i + 1) not in path_coordinates):
            path_coordinates.add((j, i + 1))
            queue.append((j, i + 1))
    # the result is the half of the path rounded down
    return len(path_coordinates) // 2


# we do roughly the same as in part 1 to determine the path
def part_2(filename: str) -> int:
    grid = open(filename).read().splitlines()
    # first find start
    sc, sr = None, None
    for j, row in enumerate(grid):
        for i, character in enumerate(row):
            if character == "S":
                sc, sr = i, j
                # if this break happens, the else is skipped and the break for big for is called
                # otherwise the else is called and the break is below it is skipped
                break
        else:
            continue
        break
    # keep track of the path
    path_coordinates = {(sr, sc)}
    # queue for breath-first-search
    queue = deque([(sr, sc)])
    # we need to know what S is, so we keep a set of all options and filter down the road
    maybe_s = {"|", "-", "J", "L", "7", "F"}
    # keep going until queue is empty
    while queue:
        j, i = queue.popleft()
        character = grid[j][i]

        # now we check if the character can go up
        # this means the character must be a pipe with opening at the top
        # also the character it points to needs to accept from the bottom
        if j > 0 and character in "S|JL" and grid[j - 1][i] in "|7F" and (j - 1, i) not in path_coordinates:
            path_coordinates.add((j - 1, i))
            queue.append((j - 1, i))
            if character == "S":
                # the &= operator takes intersection!
                maybe_s &= {"|", "J", "L"}
        # same as above, but for going down
        if j < len(grid) - 1 and character in "S|7F" and grid[j + 1][i] in "|JL" and (j + 1, i) not in path_coordinates:
            path_coordinates.add((j + 1, i))
            queue.append((j + 1, i))
            if character == "S":
                maybe_s &= {"|", "7", "F"}
        # going right
        if i > 0 and character in "S-J7" and grid[j][i - 1] in "-LF" and (j, i - 1) not in path_coordinates:
            path_coordinates.add((j, i - 1))
            queue.append((j, i - 1))
            if character == "S":
                maybe_s &= {"-", "J", "7"}
        # going left
        if (i < len(grid[j]) - 1 and character in "S-LF" and grid[j][i + 1] in "-J7" and
                (j, i + 1) not in path_coordinates):
            path_coordinates.add((j, i + 1))
            queue.append((j, i + 1))
            if character == "S":
                maybe_s &= {"-", "L", "F"}

    # maybe_s now only contains one element, which is S, so set it in the grid
    assert len(maybe_s) == 1
    (S,) = maybe_s
    grid = [row.replace("S", S) for row in grid]
    # also set all points that are not part of the path to a . for simplicity
    grid = ["".join(ch if (r, c) in path_coordinates else "." for c, ch in enumerate(row)) for r, row in
            enumerate(grid)]

    # keep track of all the points that are considered outside
    outside = set()
    # loop over the grid
    for j, row in enumerate(grid):
        # start assuming it is outside
        within = False
        # this is the 'direction' of the pipe of pipe we could be traveling along
        # if up we have L---, if not up we have F---
        # if an up ends with J, we don't count it as a crossing of the line
        # same if a down ends in 7
        # otherwise it counts as a crossing (logically)
        # we count the amount of crossings, if this is even on the left side of the point, it must be outside
        up = None
        for i, character in enumerate(row):
            # when we find a |, we can assume we came from a . as -| does not make sense for example
            # hence we assume that we are not traveling along a line
            # we also crossed a line, so we swap within
            if character == "|":
                assert up is None
                within = not within
            # requires nothing, as we are traveling along a line
            elif character == "-":
                assert up is not None
            # again, not traveling, but starting to travel
            # so set up to the value that is appropriate (L-----J is up, F----7 is down)
            elif character in "LF":
                assert up is None
                up = character == "L"
            # ends traveling alone a line
            elif character in "7J":
                assert up is not None
                # now check if we crossed a line (i.e. L--7 or F--J)
                if character != ("J" if up else "7"):
                    within = not within
                up = None
            # do nothing
            elif character == ".":
                pass
            else:
                raise RuntimeError(f"unexpected character (horizontal): {character}")
            # now if it is not set, add the coordinates to the outsides nodes
            if not within:
                outside.add((j, i))
    # | on sets gives union
    # result is the total amount of nodes minus path and outside nodes
    # note we use the union as path coordinates can also be considered outside, so this is easiest
    return len(grid) * len(grid[0]) - len(outside | path_coordinates)
