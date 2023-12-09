from collections import defaultdict


def part_1(filename: str) -> int:
    lines = open(filename, "r").read().split('\n')
    # keep running total
    res = 0
    # for each card
    for card in lines:
        # split winners, draws
        winners, draws = card.split(": ")[1].strip().split(" | ")
        winners = winners.split()
        draws = draws.split()
        # determine successes
        nof_successes = len(list(filter(lambda w: draws.count(w) == 1, winners)))
        # add score to result
        if nof_successes >= 1:
            res += pow(2, nof_successes - 1)
    return res


def part_2(filename: str) -> int:
    lines = open(filename, "r").read().split('\n')
    # keep running total
    res = 0
    # keep track of card copies
    card_copies = defaultdict(lambda: 1)
    # for each card
    for i in range(len(lines)):
        # split winners, draws
        winners, draws = lines[i].split(": ")[1].strip().split(" | ")
        winners = winners.split()
        draws = draws.split()
        # determine successes
        nof_successes = len(list(filter(lambda w: draws.count(w) == 1, winners)))
        # determine own copies amount
        own_copies = card_copies[i]
        # add own copies amount of copies to each of the next nof_successes cards
        if nof_successes >= 1:
            for c in range(i + 1, i + nof_successes + 1):
                card_copies[c] += own_copies
        # add own copies to running total
        res += own_copies
    return res
