# hash function according to puzzle
def hash(code: str) -> int:
    h = 0
    for c in code:
        h += ord(c)  # determines ascii value
        h *= 17
        h %= 256
    return h


def part_1(filename: str) -> int:
    return sum(hash(code) for code in open(filename).read().split(','))


def part_2(filename: str) -> int:
    codes = open(filename).read().split(',')
    # construct dict
    d: dict[int, list[(str, int)]] = dict.fromkeys(range(256), [])
    # loop over codes, unpack them and determine which box it belongs to
    for code in codes:
        # sneaky, has length 1 in case of '-' and length 2 in case of '='
        unpacked = code.split('-')[0].split('=')
        box = hash(unpacked[0])
        if len(unpacked) == 1:
            # minus, so remove
            d[box] = list(filter(lambda t: t[0] != unpacked[0], d[box]))
        else:
            # equals, check if box contains unpacked[0] and if so override, otherwise add
            existing = list(filter(lambda t: t[0] == unpacked[0], d[box]))
            if len(existing) == 0:
                d[box] = [*d[box], (unpacked[0], int(unpacked[1]))]
            else:
                d[box][d[box].index(existing[0])] = (unpacked[0], int(unpacked[1]))
    # sum according to instructions
    return sum(sum((1 + i) * (j + 1) * l[1] for j, l in enumerate(b)) for i, b in enumerate(d.values()))
