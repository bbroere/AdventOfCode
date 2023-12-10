def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # running result
    res = 0
    # loop over all lines as history
    for history in lines:
        # start tree by splitting current history
        tree: list[list[int]] = [(list(map(lambda t: int(t), history.split())))]
        # loop while not all zeros
        while not len(list(filter(lambda t: t != 0, tree[-1]))) == 0:
            # add new layer by calculating the difference
            tree.append([tree[-1][i + 1] - tree[-1][i] for i in range(len(tree[-1]) - 1)])
        # add 0 to bottom layer
        tree[-1].append(0)
        # be a fortune teller
        for i in range(len(tree) - 2, -1, -1):
            tree[i].append(tree[i][-1] + tree[i + 1][-1])
        # add to running result
        res += tree[0][-1]
    return res


# Same as part one except just swap the array as operation is symmetric
def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # running result
    res = 0
    # loop over all lines as history
    for history in lines:
        # start tree by splitting current history
        tree: list[list[int]] = [(list(map(lambda t: int(t), list(history.split())[::-1])))]  # only difference with p1
        # loop while not all zeros
        while not len(list(filter(lambda t: t != 0, tree[-1]))) == 0:
            # add new layer by calculating the difference
            tree.append([tree[-1][i + 1] - tree[-1][i] for i in range(len(tree[-1]) - 1)])
        # add 0 to bottom layer
        tree[-1].append(0)
        # be a fortune teller
        for i in range(len(tree) - 2, -1, -1):
            tree[i].append(tree[i][-1] + tree[i + 1][-1])
        # add to running result
        res += tree[0][-1]
    return res
