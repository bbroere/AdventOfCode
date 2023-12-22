import math
from collections import deque


# Kudos to hyper-neutrino for the assumption ideas of part 2 (https://github.com/hyper-neutrino)

class Module:
    name: str
    type: str
    outputs: list[str]
    state: str  # not applicable for all types
    memory: dict[str, str]  # not applicable for all types, will be (target -> last signal)

    def __init__(self, line: str):
        l, r = line.split(" -> ")
        self.memory = dict()
        self.state = "off"
        self.type = ""
        if l == "broadcaster" or l == "rx":
            self.name = l
        else:
            self.type = l[0]
            self.name = l[1:]
        self.outputs = r.split(", ")


# queue is src, tgt, signal
def perform_button_press_and_count_signals(modules: dict[str, Module]) -> (int, int):
    # setup and initialize queue
    counters: dict[str, int] = {"L": 0, "H": 0}
    # we start in broadcaster
    signals = deque([("", "broadcaster", "L")])
    # process signals
    while signals:
        # get signal (from left)
        source, target, pulse = signals.popleft()
        # update counter
        counters[pulse] += 1
        # if we reach output, just go on
        if target not in modules.keys():
            continue
        # get module
        module = modules[target]
        # process signal
        if module.type == "%" and pulse == "L":  # flip flop module
            # flip state
            module.state = "on" if module.state == "off" else "off"
            # queue other signals (right)
            send_signal = "L" if module.state == "off" else "H"
            for output in module.outputs:
                signals.append((module.name, output, send_signal))
        elif module.type == "&":  # conjunction module
            # set memory state
            module.memory[source] = pulse
            # determine signal and queue (right)
            send_signal = "H" if "L" in module.memory.values() else "L"
            for output in module.outputs:
                signals.append((module.name, output, send_signal))
        elif module.name == "broadcaster":  # broadcaster
            for output in module.outputs:
                signals.append((module.name, output, pulse))
        # for part 2
        elif module.name == "rx":
            module.state = "on" if pulse == "L" else "off"
    return counters["L"], counters["H"]


def part_1(filename: str) -> int:
    modules = {}
    for line in open(filename).read().splitlines():
        m = Module(line)
        modules[m.name] = m
    # set memory
    for module in modules.values():
        if module.type == "&":
            for key in list(filter(lambda t: module.name in t.outputs, modules.values())):
                module.memory[key.name] = "L"
    l, h = 0, 0
    for i in range(1000):
        r_l, r_h = perform_button_press_and_count_signals(modules)
        l += r_l
        h += r_h
    return l * h


# queue is src, tgt, signal
def perform_button_press_until_rx(modules: dict[str, Module]) -> int:
    # find out what is/are the sources of rx, hard assumption: 1 module only
    # nice notation where this throws an error if there are more sources
    (src,) = [module for module in modules.values() if "rx" in module.outputs]
    # assume that source is a conjunction module
    assert src.type == "&"
    # now, this only returns low if all of its inputs were high
    # as a working assumption, assume that every one of the modules that feeds into source returns L every press,
    # except on a specified interval
    # so set up a dictionary keeping track of the sources of source and their on-off pattern
    cycles = {}
    # also keep track of how many times we've seen the inputs if source
    time_seen = {module.name: 0 for module in modules.values() if src.name in module.outputs}
    # running result
    res = 0
    while True:
        res += 1  # button pressed
        # we start in broadcaster
        signals = deque([("", "broadcaster", "L")])
        # process signals
        while signals:
            # get signal (from left)
            source, target, pulse = signals.popleft()
            # if we reach output, just go on
            if target not in modules.keys():
                continue
            # get module
            module = modules[target]
            # check if this is the src module and the signal it sends is high
            if module.name == src.name and pulse == 'H':
                # we've seen it one more time
                time_seen[source] += 1
                # this also means we found its cycle length
                if source not in cycles:
                    cycles[source] = res  # equal to number of presses until now
                # now do sanity check that the current number of presses is a multiple of the found cycle
                else:
                    assert res % cycles[source] == 0
                # now also check if we've seen everyone at least once and return the least common multiple of all cycles
                if all([t if t > 0 else None for t in time_seen.values()]):
                    return math.lcm(*cycles.values())
            # process signal
            if module.type == "%" and pulse == "L":  # flip flop module
                # flip state
                module.state = "on" if module.state == "off" else "off"
                # queue other signals (right)
                send_signal = "L" if module.state == "off" else "H"
                for output in module.outputs:
                    signals.append((module.name, output, send_signal))
            elif module.type == "&":  # conjunction module
                # set memory state
                module.memory[source] = pulse
                # determine signal and queue (right)
                send_signal = "H" if "L" in module.memory.values() else "L"
                for output in module.outputs:
                    signals.append((module.name, output, send_signal))
            elif module.name == "broadcaster":  # broadcaster
                for output in module.outputs:
                    signals.append((module.name, output, pulse))
            # for part 2
            elif module.name == "rx":
                module.state = "on" if pulse == "L" else "off"


def part_2(filename: str) -> int:
    modules = {}
    for line in open(filename).read().splitlines():
        m = Module(line)
        modules[m.name] = m
    # set memory
    for module in modules.values():
        if module.type == "&":
            for key in list(filter(lambda t: module.name in t.outputs, modules.values())):
                module.memory[key.name] = "L"
    return perform_button_press_until_rx(modules)
