from collections import deque


def result_for_position(lines: list[str], pos_and_dir: (int, int, (int, int))) -> int:
    # keep track of hoe many times a beam has passed through a point
    result = [["." for c in line] for line in lines]
    # keep list of processed coordinates
    processed = set()
    # keep track of all beam ends (out left, in right)
    queue = deque([pos_and_dir])
    # for _ in range(2):
    while queue:
        # get head of queue
        i, j, d = queue.popleft()
        # as long as the coordinates are in the grid, make a step
        while 0 <= i < len(lines[0]) and 0 <= j < len(lines):
            # start by adding to the processed list
            processed.add((i, j, d))
            # set value to seen in result
            result[j][i] = "#"
            # check the item in the grid
            item = lines[j][i]
            # just move along
            if item == '.':
                j += d[1]
                i += d[0]
            # move up and add up to queue if needed
            elif item == '|':
                d1 = (0, min(1, d[1] + 1))  # up
                d2 = (0, max(-1, d[1] - 1))  # down
                if d1[1] != 0 and d2[1] != 0:
                    queue.append((i + d2[0], j + d2[1], d2))
                    i += d1[0]
                    j += d1[1]
                    d = d1
                elif d1[1] != 0:
                    i += d1[0]
                    j += d1[1]
                    d = d1
                else:
                    i += d2[0]
                    j += d2[1]
                    d = d2
            # move left and add right to queue if needed
            elif item == '-':
                d1 = (min(1, d[0] + 1), 0)  # left
                d2 = (max(-1, d[0] - 1), 0)  # right
                if d1[0] != 0 and d2[0] != 0:
                    queue.append((i + d2[0], j + d2[1], d2))
                    i += d1[0]
                    j += d1[1]
                    d = d1
                elif d1[0] != 0:
                    i += d1[0]
                    j += d1[1]
                    d = d1
                else:
                    i += d2[0]
                    j += d2[1]
                    d = d2
            elif item == '/':
                # (1, 0) -> (0, -1)
                # (-1, 0) -> (0, 1)
                # (0, 1) -> (-1, 0)
                # (0, -1) -> (0, 1)
                d_new = (-d[1], -d[0])
                i += d_new[0]
                j += d_new[1]
                d = d_new
            elif item == '\\':
                # (1, 0) -> (0, 1)
                # (-1, 0) -> (0, -1)
                # (0, 1) -> (1, 0)
                # (0, -1) -> (0, -1)
                d_new = (d[1], d[0])
                i += d_new[0]
                j += d_new[1]
                d = d_new
            # if the next step is processed,  done for this branch
            if (i, j, d) in processed:
                break
    # probably faster to use the set of processed, but oh well
    return sum([sum([1 if c == '#' else 0 for c in r]) for r in result])


def part_1(filename: str) -> int:
    return result_for_position(open(filename).read().splitlines(), (0, 0, (1, 0)))


# just do the same as for part 1 but now loop over outside and return max
def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # for each of the outside borders
    results = [
        *[result_for_position(lines, (i, 0, (0, 1))) for i in range(len(lines[0]))],
        *[result_for_position(lines, (i, len(lines) - 1, (0, -1))) for i in range(len(lines[0]))],
        *[result_for_position(lines, (0, i, (1, 0))) for i in range(len(lines))],
        *[result_for_position(lines, (len(lines[0]) - 1, i, (-1, 0))) for i in range(len(lines))],
    ]
    # return max
    return max(results)
