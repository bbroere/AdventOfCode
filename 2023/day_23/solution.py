# Kudos again to hyper-neutrino for reaffirming that there is no easy way to determine the longest path in a graph
# and reminding me of the tools I forgot about since my studies (https://github.com/hyper-neutrino)

def part_1(filename: str) -> int:
    grid = open(filename).read().splitlines()
    # start point is single . in first row and end point is single . in last row
    start = (grid[0].index('.'), 0)
    end = (grid[len(grid) - 1].index('.'), len(grid) - 1)
    # we will gather a list of poi
    # these poi are of interest because they are the only points where something will 'happen'
    # such being the start point, end point and every intersection where we have a choice
    # this will allow us to do path contraction on the graph that the grid actually is
    pois = [start, end]
    for r, row in enumerate(grid):
        for t, tile in enumerate(row):
            # we don't care about walls
            if tile == '#':
                continue
            # keep track of number of tiles in the neighbors we can travel to
            neighboring_free_tiles = 0
            for x, y in [(t, r - 1), (t, r + 1), (t - 1, r), (t + 1, r)]:
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] != '#':
                    neighboring_free_tiles += 1
            # now if this number is >= 3 we found an intersection, so we add it to the poi
            if neighboring_free_tiles >= 3:
                pois.append((t, r))
    # now construct the 'weighted' directed graph (due to slopes) where the weights are the distances between the poi
    graph = {p: {} for p in pois}
    # also create a quick dictionary that helps determine the way we can travel if we encounter a specific sign
    directions = {
        '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
        '<': [(-1, 0)],
        '>': [(1, 0)],
        '^': [(0, -1)],
        'v': [(0, 1)],
        '#': []
    }
    for x, y in pois:
        # make stack of points to loop through to flood the grid from this starting point
        stack = [(0, x, y)]
        # keep track of seen points to avoid backtracking
        seen = {(x, y)}
        while stack:
            n, xx, yy = stack.pop()
            # ignore n = 0 as we don't want an edge from a point to itself
            # so check if the point is a poi and if so add one direction to the graph
            # we don't go multi-directional as we have to account for the arrows
            # the other path will be added if it exists from the other poi
            if n != 0 and (xx, yy) in pois:
                graph[(x, y)][(xx, yy)] = n
                # now this branch is done
                continue
            # otherwise we look at all the places we can go and add those to the stack, keeping direction and the list
            # of seen points in mind
            for dx, dy in directions[grid[yy][xx]]:
                nx = xx + dx
                ny = yy + dy
                # if it is in range and not seen, add to stack with increased step of 1
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] != '#' and (nx, ny) not in seen:
                    stack.append((n + 1, nx, ny))
                    seen.add((nx, ny))

    # now we perform a depth-first search approach to find the longest path
    def depth_first_search(point: (int, int)):
        if point == end:
            # base case, done, takes 0 steps to get to the end
            return 0
        # neat trick with addition, it basically makes sure that if we don't find a path, this gets ignored
        current_max = -float("inf")
        # now loop over the pois next reachable points
        for next_reachable in graph[point]:
            # now the new max is the max of the current value and the max of the next poi's search + path to next poi
            current_max = max(current_max, depth_first_search(next_reachable) + graph[point][next_reachable])
        return current_max

    return depth_first_search(start)


# almost the same as part but with cycle detection and fewer issues with directions
# this is by no means fast, but longest path is just not a problem that has a better solution
def part_2(filename: str) -> int:
    grid = open(filename).read().splitlines()
    # start point is single . in first row and end point is single . in last row
    start = (grid[0].index('.'), 0)
    end = (grid[-1].index('.'), len(grid) - 1)
    # we will gather a list of poi
    # these poi are of interest because they are the only points where something will 'happen'
    # such being the start point, end point and every intersection where we have a choice
    # this will allow us to do path contraction on the graph that the grid actually is
    pois = [start, end]
    for r, row in enumerate(grid):
        for t, tile in enumerate(row):
            # we don't care about walls
            if tile == '#':
                continue
            # keep track of number of tiles in the neighbors we can travel to
            neighboring_free_tiles = 0
            for x, y in [(t, r - 1), (t, r + 1), (t - 1, r), (t + 1, r)]:
                if 0 <= x < len(grid[0]) and 0 <= y < len(grid) and grid[y][x] != '#':
                    neighboring_free_tiles += 1
            # now if this number is >= 3 we found an intersection, so we add it to the poi
            if neighboring_free_tiles >= 3:
                pois.append((t, r))
    # now construct the 'weighted' directed graph (due to slopes) where the weights are the distances between the poi
    graph = {p: {} for p in pois}
    # also create a quick dictionary that helps determine the way we can travel if we encounter a specific sign
    for x, y in pois:
        # make stack of points to loop through to flood the grid from this starting point
        stack = [(0, x, y)]
        # keep track of seen points to avoid backtracking
        seen = {(x, y)}
        while stack:
            n, xx, yy = stack.pop()
            # ignore n = 0 as we don't want an edge from a point to itself
            # so check if the point is a poi and if so add one direction to the graph
            # we don't go multi-directional as we have to account for the arrows
            # the other path will be added if it exists from the other poi
            if n != 0 and (xx, yy) in pois:
                graph[(x, y)][(xx, yy)] = n
                # now this branch is done
                continue
            # otherwise we look at all the places we can go and add those to the stack, keeping direction and the list
            # of seen points in mind
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx = xx + dx
                ny = yy + dy
                # if it is in range and not seen, add to stack with increased step of 1
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] != '#' and (nx, ny) not in seen:
                    stack.append((n + 1, nx, ny))
                    seen.add((nx, ny))
    # now we perform a depth-first search approach to find the longest path
    # we also need to keep track of a list of seen points to prevent cycles
    seen = set()

    def depth_first_search2(point: (int, int)):
        if point == end:
            # base case, done, takes 0 steps to get to the end
            return 0
        # neat trick with addition, it basically makes sure that if we don't find a path, this gets ignored
        current_max = -float("inf")
        # now loop over the pois next reachable points
        seen.add(point)
        for next_reachable in graph[point]:
            # now the new max is the max of the current value and the max of the next poi's search + path to next poi
            if next_reachable not in seen:
                current_max = max(current_max, depth_first_search2(next_reachable) + graph[point][next_reachable])
        seen.remove(point)
        return current_max

    return depth_first_search2(start)
