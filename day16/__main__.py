from dataclasses import dataclass
from os import path
import re
import unittest

PARSING_EXP = "Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)"


@dataclass
class Valve():
    name: str
    flow: int
    children: dict[str, int]

    def __init__(self, name, flow, *children):
        self.name = name
        self.flow = flow
        self.children = children


def parse_valve(string):
    match = re.match(PARSING_EXP, string)
    return Valve(
        match.group(1),
        int(match.group(2)),
        *list(map(lambda s: s.strip(), match.group(3).split(",")))
    )


def find_way_1(valves):
    return step_1(
        valves=valves,
        cur="AA",
        time=29,
        flow=0,
        open=set([v.name for v in valves.values() if v.flow == 0]),
        best={}
    )


def add_to_set(s, x):
    copy = s.copy()
    copy.add(x)
    return copy


@dataclass
class Option():
    name: str
    opened: str


def get_options(valves, cur, open):
    result = []
    valve = valves[cur]
    if cur not in open and valve.flow > 0:
        # new_flow = flow + valve.flow * time
        result.append(Option(cur, cur))

    for child in valve.children:
        result.append(Option(child, None))
    return result


def step_1(valves, cur, time, flow, open, best):
    if time == 0:
        return flow
    if len(open) == len(valves):
        return flow

    key = cur + ">" + ":".join(sorted(open))
    if key in best and best[key] > time:
        return -1
    best[key] = time

    m = 0
    options = get_options(valves, cur, open)
    for option in options:
        if option.name in open and len(valves[option.name].children) == 1:
            continue
        new_flow = flow 
        new_open = open
        if option.opened is not None:
            new_flow += valves[option.opened].flow * time
            new_open = open.copy()
            new_open.add(option.opened)
        result = step_1(valves, option.name, time - 1, new_flow, new_open, best)
        m = result if result > m else m

    return m

def find_way_2(valves):
    return step_2(
        valves=valves,
        cur_a="AA",
        cur_b="AA",
        pred_a="",
        pred_b="",
        time=25,
        flow=0,
        open=set([v.name for v in valves.values() if v.flow == 0]),
        best={}
    )

def test_option(valves, open, cur, path):
    if cur not in open:
        return True
    for child in valves[cur].children:
        if child in path:
            continue
        if test_option(valves, open, child, add_to_set(path, child)):
            return True
    return False

def step_2(valves, cur_a, cur_b, pred_a, pred_b, time, flow, open, best):
    if time == 0:
        return flow
    if len(open) == len(valves):
        # if time > best['all']:
        #     best['all'] = time
        return flow

    key = ":".join(sorted([cur_a, cur_b])) + ">" + ":".join(sorted(open))
    if key in best and best[key] >= time:
        # print(key)
        return -1
    best[key] = time


    options_a = get_options(valves, cur_a, open)
    options_b = get_options(valves, cur_b, open)

    m = 0
    for option_a in options_a:
        if pred_a == option_a.name: 
            continue
        valve_a = valves[option_a.name]
        if (option_a.name in open or valve_a.flow == 0) and len(valve_a.children) == 1:
            continue
        # if not test_option(valves, open, option_a.name, set(cur_a)):
        #     continue
        for option_b in options_b:
            if pred_b == option_b.name: 
                continue
            if option_a.opened is not None and option_a.opened == option_b.opened:
                continue
            valve_b = valves[option_b.name]
            if (option_b.name in open or valve_b.flow == 0) and len(valve_b.children) == 1:
                continue
            # if not test_option(valves, open, option_b.name, set(cur_b)):
            #     continue
            # print(cur_a, option_a, cur_b, option_b)
            opened = [option.opened for option in [option_a, option_b] if option.opened is not None]
            new_flow = flow 
            new_open = open.copy()
            for o in opened:
                new_flow += valves[o].flow * time
                new_open.add(o)
            result = step_2(
                valves, 
                option_a.name, 
                option_b.name, 
                cur_a,
                cur_b,
                time - 1, 
                new_flow, 
                new_open, 
                best
            )
            m = result if result > m else m

    return m



def read_valves(fname):
    result = {}
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            valve = parse_valve(line)
            result[valve.name] = valve
    return result


def solve_file(fname):
    valves = read_valves(fname)
    return find_way_2(valves)


class TestDay(unittest.TestCase):

    VAVLES = {
        "AA": Valve("AA", 0, "DD", "II", "BB"),
        "BB": Valve("BB", 13, "CC", "AA"),
        "CC": Valve("CC", 2, "DD", "BB"),
        "DD": Valve("DD", 20, "CC", "AA", "EE"),
        "EE": Valve("EE", 3, "FF", "DD"),
        "FF": Valve("FF", 0, "EE", "GG"),
        "GG": Valve("GG", 0, "FF", "HH"),
        "HH": Valve("HH", 22, "GG"),
        "II": Valve("II", 0, "AA", "JJ"),
        "JJ": Valve("JJ", 21, "II")
    }

    def test_parse_valve(self):
        input = "Valve II has flow rate=0; tunnels lead to valves AA, JJ"
        self.assertEqual(parse_valve(input), Valve("II", 0, "AA", "JJ"))

    def test_read_valves(self):
        self.assertEqual(read_valves("input-test.txt"), self.VAVLES)

    def test_find_way_1(self):
        self.assertEqual(find_way_1(self.VAVLES), 1651)

    def test_find_way_2(self):
        self.assertEqual(find_way_2(self.VAVLES), 1707)

    # def test_solve_file(self):
    #     self.assertEqual(solve_file("input-test.txt"), 1651)


if __name__ == '__main__':
    # print(solve_file("input.txt"))
    unittest.main()
