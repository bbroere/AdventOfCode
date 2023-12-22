from heapq import heappop, heappush


# Kudos to hyper-neutrino for the python tricks involving heapq, making my life so much easier
# (https://github.com/hyper-neutrino)

def reach_end(grid: list[list[int]], max_in_direction: int, min_in_direction: int) -> int:
    # keep track of processed elements
    processed = set()
    # queue values are (heat loss, row, column, row direction, col direction, # times moved in this dir)
    queue = [(0, 0, 0, 1, 0, 0)]
    # as long as the queue not is empty, we continue (we have to reach the end at some point right?)
    while queue:
        # heappop gets priority element based on smallest first (yay!)
        # this means we get element with the smallest first element in the array each time
        heat_loss, row, col, row_dir, col_dir, steps = heappop(queue)
        # check if we reached the end and return in that case if we've done enough steps
        if row == len(grid) - 1 and col == len(grid[0]) - 1 and steps >= min_in_direction:
            return heat_loss
        # check if already processed
        # heat loss not here as we don't want increasing values each time
        # as the queue gives us a priority search, if the element is in processed, we reached it with a value
        # that is minimal (including arriving here), so storing the heat loss is not needed
        if (row, col, row_dir, col_dir, steps) in processed:
            # continue skipped this current 'while queue' step
            continue
        # now we process
        processed.add((row, col, row_dir, col_dir, steps))
        # option 1: we are allowed to move in the same direction if we haven't moved max times in that direction yet
        if steps < max_in_direction:
            # determine new row and column
            new_row = row + row_dir
            new_col = col + col_dir
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                # add next place in that direction to queue
                heappush(
                    queue,
                    (heat_loss + grid[new_col][new_row], new_row, new_col, row_dir, col_dir, steps + 1)
                )
        # option 2: turning, so check all directions, but not in the same direction as we face now, or backwards
        # because that makes no sense
        # processing works the same as above, but only if we have moved enough in that direction to allow turning
        if steps >= min_in_direction:
            for (new_row_dir, new_col_dir) in [x for x in [(0, 1), (1, 0), (0, -1), (-1, 0)] if
                                               x != (row_dir, col_dir) and x != (-row_dir, -col_dir)]:
                # determine new row and column
                new_row = row + new_row_dir
                new_col = col + new_col_dir
                if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                    # add next place in the new direction to queue
                    heappush(
                        queue,
                        (heat_loss + grid[new_col][new_row], new_row, new_col, new_row_dir, new_col_dir, 1)
                    )


def part_1(filename: str) -> int:
    grid = [list(map(int, [*x])) for x in open(filename).read().splitlines()]
    return reach_end(grid, 3, 0)


def part_2(filename: str) -> int:
    grid = [list(map(int, [*x])) for x in open(filename).read().splitlines()]
    return reach_end(grid, 10, 4)
