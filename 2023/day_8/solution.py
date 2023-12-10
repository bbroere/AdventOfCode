import math
import re


def part_1(filename: str) -> int:
    # split input
    instructions, *nodes = re.sub('\n+', '\n', open(filename, "r").read()).splitlines()
    # create nodes
    nodes = list(map(lambda t: (t[:3], t[7:10], t[12:15]), nodes))
    # running results
    current = "AAA"
    steps = 0
    # now take steps while not at ZZZ
    while current != "ZZZ":
        # current node
        node = list(filter(lambda t: t[0] == current, nodes))[0]
        if instructions[steps % len(instructions)] == "L":
            current = node[1]
        else:
            current = node[2]
        # increment
        steps += 1
    return steps


# Same solution as pt 1 would not terminate within a week probably, so going for cycles
def part_2(filename: str) -> int:
    # split input
    instructions, *nodes = re.sub('\n+', '\n', open(filename, "r").read()).splitlines()
    # create nodes
    nodes = list(map(lambda t: (t[:3], t[7:10], t[12:15]), nodes))
    # determine all starting nodes
    starting_nodes = map(lambda t: t[0], list(filter(lambda t: t[0][2] == "A", nodes)))
    # keep running least common multiple of all path lengths
    running_path_length = None
    # loop over all starting nodes
    for starting_node in starting_nodes:
        # this will be the first endpoint of all the paths
        initial_endpoint = None
        # Current nof hops
        current = 0
        # seems iffy, but we need to continue until we complete a cycle, the best way to do that is to break when
        # the end was reached
        while True:
            # now, while the starting point does not end in Z, determine next starting point
            # note; also checking for current == 0 as per re-setting of the initial endpoint
            while not starting_node[2] == "Z" or current == 0:
                # determine instruction
                current_instruction = instructions[current % len(instructions)]
                # determine node
                node = list(filter(lambda t: t[0] == starting_node, nodes))[0]
                # and hop
                if current_instruction == "L":
                    starting_node = node[1]
                else:
                    starting_node = node[2]
                # and increment
                current += 1

            # first detect cycle; is the current starting point the same as the initial one, then we have the
            # length of the cycle
            if starting_node == initial_endpoint:
                # done with cycle, we have the length of the cycle
                # now determine the least common multiple between this length and the existing one
                if running_path_length is None:
                    running_path_length = current
                else:
                    running_path_length = math.lcm(current, running_path_length)
                # break from the while True
                break

            # now if we did not detect a cycle and this is the first path, save the new starting point to detect
            # we're done
            if initial_endpoint is None:
                initial_endpoint = starting_node
                # we forget the current number of steps as we don't care as the cycle is not necessarily complete
                current = 0

    # no post-processing needed!
    return running_path_length
