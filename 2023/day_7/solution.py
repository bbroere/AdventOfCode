def part_1(filename: str) -> int:
    # read the hands and bids
    lines = open(filename).read().splitlines()
    # keep transforming array
    hands_with_score = []
    for line in lines:
        # split hand and bid
        hand, bid = line.split()
        # determine max 2 counts in a hand (set for duplications)
        counts = sorted(set(map(lambda t: ([*hand].count(t), t), [*hand])), reverse=True)
        # now check base rank
        r = ""
        if counts[0][0] == 5:
            r += "7"
        elif counts[0][0] == 4:
            r += "6"
        elif counts[0][0] == 3 and counts[1][0] == 2:
            r += "5"
        elif counts[0][0] == 3:
            r += "4"
        elif counts[0][0] == 2 and counts[1][0] == 2:
            r += "3"
        elif counts[0][0] == 2:
            r += "2"
        else:
            r += "1"
        # add card ranks
        for card in [*hand]:
            if card.isdigit():
                r += "0" + card
            elif card == "T":
                r += "10"
            elif card == "J":
                r += "11"
            elif card == "Q":
                r += "12"
            elif card == "K":
                r += "13"
            else:
                r += "14"
        # add score, hand, bid to running array
        hands_with_score.append((int(r), hand, int(bid)))
    # sort array and multiply bid by index and sum
    hands_with_score = sorted(hands_with_score)
    res = 0
    for i in range(len(hands_with_score)):
        res += (i + 1) * hands_with_score[i][2]
    return res


def part_2(filename: str) -> int:
    # read the hands and bids
    lines = open(filename).read().splitlines()
    # keep transforming array
    hands_with_score = []
    for line in lines:
        # split hand and bid
        hand, bid = line.split()
        # determine max 2 counts in a hand (set for duplications)
        counts = sorted(set(map(lambda t: ([*hand].count(t), t), [*hand])), reverse=True)
        j_counts = [*hand].count("J")
        # now check base rank
        r = ""
        if (
                counts[0][0] == 5 or  # includes JJJJJ
                counts[0][0] == 4 and j_counts == 1 or
                counts[0][0] == 3 and j_counts == 2 or
                counts[1][0] == 2 and j_counts == 3 or
                counts[1][0] == 1 and j_counts == 4
        ):
            r += "7"
        elif (
                counts[0][0] == 4 or  # includes JJJJ
                counts[0][0] == 3 and j_counts == 1 or
                counts[1][0] == 2 and j_counts == 2 or  # needing 2 pairs essentially
                counts[1][0] == 1 and j_counts == 3
        ):
            r += "6"
        elif (
                counts[0][0] == 3 and counts[1][0] == 2 or
                counts[0][0] == 2 and counts[1][0] == 2 and j_counts == 1  # like JQQKK
        ):
            r += "5"
        elif (
                counts[0][0] == 3 or
                counts[0][0] == 2 and j_counts == 1 or  # like JQQKT, essentially one pair and 3 singles, including J
                counts[0][0] == 2 and j_counts == 2  # like JJQKT, essentially one pair of Js and a single
        ):
            r += "4"
        elif counts[0][0] == 2 and counts[1][0] == 2:
            r += "3"
        elif (
                counts[0][0] == 2 or
                counts[0][0] == 1 and j_counts == 1  # 5 different cards, including J
        ):
            r += "2"
        else:
            r += "1"
        # add card ranks
        for card in [*hand]:
            if card.isdigit():
                r += "0" + card
            elif card == "T":
                r += "10"
            elif card == "J":
                r += "01"  # change from part 1
            elif card == "Q":
                r += "12"
            elif card == "K":
                r += "13"
            else:
                r += "14"
        # add score, hand, bid to running array
        hands_with_score.append((int(r), hand, int(bid)))
    # sort array and multiply bid by index and sum
    hands_with_score = sorted(hands_with_score)
    res = 0
    for i in range(len(hands_with_score)):
        res += (i + 1) * hands_with_score[i][2]
    return res
