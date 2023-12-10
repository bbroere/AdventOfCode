def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # keep running total
    res = 0
    # loop over lines
    for line in lines:
        # get all digits
        digits = list(filter(lambda t: t.isdigit(), line))
        # smash together, convert to int and sum
        res += int(digits[0] + digits[-1])
    return res


def part_2(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # keep running total
    res = 0
    # loop over lines
    for line in lines:
        # safe replace of all words that represent numbers
        line = (line.
                replace("one", "one1one").
                replace("two", "two2two").
                replace("three", "three3three").
                replace("four", "four4four").
                replace("five", "five5five").
                replace("six", "six6six").
                replace("seven", "seven7seven").
                replace("eight", "eight8eight").
                replace("nine", "nine9nine")
                )
        # repeat pt 1
        digits = list(filter(lambda t: t.isdigit(), line))
        res += int(digits[0] + digits[-1])
    return res
