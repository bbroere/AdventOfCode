# two bricks overlap if both the x and y ranges overlap in any fashion
from collections import deque


# Kudos to hyper-neutrino for reorganizing my thoughts and removing a lot of bulk code in the process
# (https://github.com/hyper-neutrino)


def do_overlap(b1, b2) -> bool:
    overlaps_x = max(b1[0], b2[0]) <= min(b1[3], b2[3])
    overlaps_y = max(b1[1], b2[1]) <= min(b1[4], b2[4])
    return overlaps_x and overlaps_y


def part_1(filename: str):
    lines = open(filename).read().splitlines()
    # split up the bricks in arrays of 6 integers
    # keep in mind, contrary to normal coordinates, here the z index is the vertical, not the y!
    bricks = []
    for line in lines:
        bricks.append(list(map(int, line.replace('~', ',').split(','))))
    # to drop the bricks down, it is a good idea to sort them by starting z index
    # this way we know that everything a brick can be 'on top of' has already been processed
    # this makes it, so we don't need th 'drop down' all bricks multiple times
    bricks.sort(key=lambda t: t[2])
    # now 'drop the bricks' by z-layer, so in order
    # note that the minimum z-value a brick can have is 1, not 0
    for i, brick in enumerate(bricks):
        # assume it can fall down as far as it wants
        new_z = 1
        # by ordering, we now only need to check the previously processed bricks to see if it is below it and, if so
        # how far it can fall down
        for brick2 in bricks[:i]:
            if do_overlap(brick, brick2):
                # if they overlap, brick needs to be at least one higher then brick2
                new_z = max(new_z, brick2[5] + 1)
        # now set the new z value (first do the end while we still know the initial value)
        brick[5] = brick[5] + new_z - brick[2]
        brick[2] = new_z
    # re-sort as they've fallen
    bricks.sort(key=lambda t: t[2])
    # now we determine a list of parents and children of each of the bricks to see what happens when we delete a brick
    parents_of = {i: set() for i in range(len(bricks))}
    children_of = {i: set() for i in range(len(bricks))}
    # loop over all bricks and add all children and parents accordingly
    for j, above in enumerate(bricks):
        for i, below in enumerate(bricks[:j]):
            # if the two bricks overlap and one is exactly above the other, then below is parent of above and
            # above is a child of below
            if above[2] == below[5] + 1 and do_overlap(above, below):
                parents_of[j].add(i)
                children_of[i].add(j)
    # check for each brick if it can be safely removed (i.e. all children have 2 or more parents)
    res = 0
    for i in range(len(bricks)):
        if all(len(parents_of[j]) >= 2 for j in children_of[i]):
            res += 1
    # done
    return res


def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # split up the bricks in arrays of 6 integers
    # keep in mind, contrary to normal coordinates, here the z index is the vertical, not the y!
    bricks = []
    for line in lines:
        bricks.append(list(map(int, line.replace('~', ',').split(','))))
    # to drop the bricks down, it is a good idea to sort them by starting z index
    # this way we know that everything a brick can be 'on top of' has already been processed
    # this makes it, so we don't need th 'drop down' all bricks multiple times
    bricks.sort(key=lambda t: t[2])
    # now 'drop the bricks' by z-layer, so in order
    # note that the minimum z-value a brick can have is 1, not 0
    for i, brick in enumerate(bricks):
        # assume it can fall down as far as it wants
        new_z = 1
        # by ordering, we now only need to check the previously processed bricks to see if it is below it and, if so
        # how far it can fall down
        for brick2 in bricks[:i]:
            if do_overlap(brick, brick2):
                # if they overlap, brick needs to be at least one higher then brick2
                new_z = max(new_z, brick2[5] + 1)
        # now set the new z value (first do the end while we still know the initial value)
        brick[5] = brick[5] + new_z - brick[2]
        brick[2] = new_z
    # re-sort as they've fallen
    bricks.sort(key=lambda t: t[2])
    # now we determine a list of parents and children of each of the bricks to see what happens when we delete a brick
    parents_of = {i: set() for i in range(len(bricks))}
    children_of = {i: set() for i in range(len(bricks))}
    # loop over all bricks and add all children and parents accordingly
    for j, above in enumerate(bricks):
        for i, below in enumerate(bricks[:j]):
            # if the two bricks overlap and one is exactly above the other, then below is parent of above and
            # above is a child of below
            if above[2] == below[5] + 1 and do_overlap(above, below):
                parents_of[j].add(i)
                children_of[i].add(j)
    # check for each brick the length of the chain reaction it produces when removed
    res = 0
    for i in range(len(bricks)):
        # keep a queue of what needs to fall and keep track of what has fallen
        falling_queue = deque(j for j in children_of[i] if len(parents_of[j]) == 1)
        fell = set(falling_queue)
        # while there still are things that can fall, let them
        while falling_queue:
            j = falling_queue.popleft()
            # no need to check the already fallen bricks, that would be silly
            for c in (children_of[j] - fell):
                # for sets <= means subset, neat!
                if parents_of[c] <= fell:
                    falling_queue.append(c)
                    fell.add(c)
        # add the length of the chain reaction to the running result
        res += len(fell)
    return res
