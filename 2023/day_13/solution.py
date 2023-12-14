# Kudos to hyper-neutrino for the python tricks (https://github.com/hyper-neutrino)

def determine_mirror_row(block: list[str], assumed_differences: int = 0) -> int:
    # don't take 0 as an empty block makes no sense
    for i in range(1, len(block)):
        # determine lines above and below split
        lines_above = block[:i][::-1]
        lines_below = block[i:]
        # now limit them to the min size of the blocks
        lines_above = lines_above[:len(lines_below)]
        lines_below = lines_below[:len(lines_above)]
        # count total differences on character basis between the 2 splits
        differences = sum(sum(0 if a == b else 1 for a, b in zip(x, y)) for x, y in zip(lines_above, lines_below))
        # if the number of differences is equal tot the amount of assumed differences, we have a match, so return index
        if differences == assumed_differences:
            return i
    # if we reach this point, no match
    return 0


def part_1(filename: str, assumed_difference: int = 0) -> int:
    # split into individual blocks
    blocks = open(filename).read().split('\n\n')
    # running total
    res = 0
    # loop over blocks
    for block in blocks:
        # determine mirror row and multiply by 100
        res += determine_mirror_row(block.splitlines(), assumed_difference) * 100
        # determine mirror col and add
        res += determine_mirror_row(list(zip(*block.splitlines())), assumed_difference)
    return res


# same as part 1 but with assumed 1 difference
def part_2(filename: str) -> int:
    return part_1(filename, 1)
