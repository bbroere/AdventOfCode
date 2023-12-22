# Kudos to hyper-neutrino for the way easier way of working with the ranges than I came up with!
# (https://github.com/hyper-neutrino)

def accept_part(workflows: dict, part: dict[str, int], position: str = "in") -> bool:
    # base cases
    if position == "R":
        return False
    if position == "A":
        return True
    # recursion
    rules, fallback = workflows[position]
    # process the rules in order
    for key, op, threshold, target in rules:
        # evaluate function
        if eval(f"{part[key]} {op} {threshold}"):
            return accept_part(workflows, part, target)
    # if none of the rules match, return fallback
    return accept_part(workflows, part, fallback)


def part_1(filename: str) -> int:
    p1, p2 = open(filename).read().split('\n\n')
    # keep running total
    res = 0
    # split up workflows
    workflows = {}
    for line in p1.splitlines():
        identifier, r = line[:-1].split("{")
        rules = r.split(',')
        # pop just takes the last one, as it is the default (remainder is parsed differently)
        workflows[identifier] = ([], rules.pop())
        for rule in rules:
            # key, op, threshold, target
            c, target = rule.split(':')
            key, op, threshold = (c[0], c[1], int(c[2:]))
            # add to the workflow
            workflows[identifier][0].append((key, op, threshold, target))
    # split up the parts as well
    for line in p2.splitlines():
        part = {}
        for categorie in line[1:-1].split(","):  # remove '{' and '}'
            name, value = categorie.split("=")
            part[name] = int(value)
        # check if part accepted
        if accept_part(workflows, part):
            res += sum(part.values())
    return res


def count_accepted_in_ranges(workflows: dict, ranges: dict[str, (int, int)], position: str = "in") -> int:
    # base cases
    if position == "R":
        return 0
    if position == "A":
        # ranges are accepted, so we need to multiply the lengths of all ranges to get the distinct number of solutions
        res = 1
        for lhs, rhs in ranges.values():
            res *= rhs - lhs + 1
        return res
    # recursion
    rules, fallback = workflows[position]
    # running result
    res = 0
    # process the rules in order
    for key, op, threshold, target in rules:
        lhs, rhs = ranges[key]
        # determine the parts of the ranges that are processed by this rule
        if op == "<":
            processed = (lhs, threshold - 1)
            not_processed = (threshold, rhs)
        else:
            processed = (threshold + 1, rhs)
            not_processed = (lhs, threshold)
        # now process next step for the processed part
        if processed[0] <= processed[1]:
            # construct new ranges
            c = dict(ranges)
            # As we know the processed part can continue, put that as the new range
            c[key] = processed
            res += count_accepted_in_ranges(workflows, c, target)
        if not_processed[0] <= not_processed[1]:
            # now mutate the ranges array to only keep the non-processed part
            # this way the next rule will trigger with the correct ranges
            ranges = dict(ranges)
            ranges[key] = not_processed
        else:
            # if not_processed is empty, then nothing to do anymore
            break
    # we get to this case when there were still values unprocessed by the rules, they need to go to the default
    # note that the ranges value has been updated into the not_processed parts in every step!
    else:
        res += count_accepted_in_ranges(workflows, ranges, fallback)
    # return the result
    return res


def part_2(filename: str) -> int:
    p1, p2 = open(filename).read().split('\n\n')
    # keep running total
    res = 0
    # split up workflows
    workflows = {}
    for line in p1.splitlines():
        identifier, r = line[:-1].split("{")
        rules = r.split(',')
        # pop just takes the last one, as it is the default (remainder is parsed differently)
        workflows[identifier] = ([], rules.pop())
        for rule in rules:
            # key, op, threshold, target
            c, target = rule.split(':')
            key, op, threshold = (c[0], c[1], int(c[2:]))
            # add to the workflow
            workflows[identifier][0].append((key, op, threshold, target))
    # construct a dictionary for each of the keys and pass it to the function
    return count_accepted_in_ranges(workflows, {key: (1, 4000) for key in "xmas"})
