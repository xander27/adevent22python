from dataclasses import dataclass
from os import path
import re
import unittest


@dataclass
class Valve:
    name: str
    flow: int
    children: dict[str, int]

    @staticmethod
    def parse(string):
        match = re.match("Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)", string)
        return Valve(
            match.group(1),
            int(match.group(2)),
            {s.strip(): 1 for s in match.group(3).split(",")}
        )


@dataclass
class State:
    opened: set[str]
    position: str

    def __hash__(self):
        return hash(self.position + ">" + ":".join(sorted(self.opened)))


def optimize_children_distance(valves):
    for k, valve in valves.items():
        for i in valves.keys():
            for j in valves.keys():
                current = valves[i].children.get(j, float("+inf"))
                new = valves[i].children.get(k, float("+inf")) + valves[k].children.get(j, float("+inf"))
                valves[i].children[j] = min(current, new)


def remove_zero_flow(valves):
    to_delete = {n for n, v in valves.items() if v.flow == 0}
    result = {}
    for name, valve in valves.items():
        if name in to_delete:
            continue
        valve.children = {c: d for c, d in valve.children.items() if d < float("+inf") and c not in to_delete}
        result[name] = valve
    return result


def optimize_valves(valves):
    optimize_children_distance(valves)
    return remove_zero_flow(valves)


def find_way(valves, time):
    start = valves["AA"]
    valves = optimize_valves(valves)
    start.children = {c: n for c, n in start.children.items() if c in valves.keys()}
    best = dict()
    return step(valves=valves, valve=start, time=time, flow=0, opened=set(), best=best), best


def step(valves, valve, time, flow, opened, best):
    if len(opened) == len(valves):
        return flow

    state = State(opened, valve.name)
    pred = best.get(state, -1)
    if pred >= flow:
        return -1
    best[state] = flow

    m = flow

    for child_name, distance in valve.children.items():
        if child_name in opened:
            continue
        child_valve = valves[child_name]
        new_time = time - distance - 1
        if new_time <= 0:
            continue
        new_flow = flow + new_time * child_valve.flow
        new_open = opened.copy()
        new_open.add(child_name)
        result = step(valves, child_valve, new_time, new_flow, new_open, best)
        m = max(result, m)

    return m


def read_valves(fname):
    result = {}
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            valve = Valve.parse(line)
            result[valve.name] = valve
    return result


def overlap(a, b):
    for x in a:
        if x in b:
            return True
    return False


def solve_1(valves):
    return find_way(valves, 30)[0]


def solve_2(valves):
    best = find_way(valves, 26)[1]
    max_p2 = 0
    items = list(best.items())
    for i, a in enumerate(items):
        for b in items[i+1:]:
            if overlap(a[0].opened, b[0].opened):
                continue
            max_p2 = max(max_p2, a[1] + b[1])
    return max_p2


def solve_file(fname):
    valves = read_valves(fname)
    return solve_1(valves), solve_2(valves)


class TestDay(unittest.TestCase):
    RAW_VALVES = {
        "AA": Valve("AA", 0, {"DD": 1, "II": 1, "BB": 1}),
        "BB": Valve("BB", 13, {"CC": 1, "AA": 1}),
        "CC": Valve("CC", 2, {"DD": 1, "BB": 1}),
        "DD": Valve("DD", 20, {"CC": 1, "AA": 1, "EE": 1}),
        "EE": Valve("EE", 3, {"FF": 1, "DD": 1}),
        "FF": Valve("FF", 0, {"EE": 1, "GG": 1}),
        "GG": Valve("GG", 0, {"FF": 1, "HH": 1}),
        "HH": Valve("HH", 22, {"GG": 1}),
        "II": Valve("II", 0, {"AA": 1, "JJ": 1}),
        "JJ": Valve("JJ", 21, {"II": 1})
    }

    OPTIMIZED_VALVES = {
        "BB": Valve("BB", 13, {'CC': 1, 'BB': 2, 'DD': 2, 'EE': 3, 'HH': 6, 'JJ': 3}),
        "CC": Valve("CC", 2, {'DD': 1, 'BB': 1, 'CC': 2, 'EE': 2, 'HH': 5, 'JJ': 4}),
        "DD": Valve("DD", 20, {'CC': 1, 'EE': 1, 'BB': 2, 'DD': 2, 'HH': 4, 'JJ': 3}),
        "EE": Valve("EE", 3, {'DD': 1, 'BB': 3, 'CC': 2, 'EE': 2, 'HH': 3, 'JJ': 4}),
        "HH": Valve("HH", 22, {'BB': 6, 'CC': 5, 'DD': 4, 'EE': 3, 'HH': 2, 'JJ': 7}),
        "JJ": Valve("JJ", 21, {'BB': 3, 'CC': 4, 'DD': 3, 'EE': 4, 'HH': 7, 'JJ': 2})
    }

    def test_parse_valve(self):
        text = "Valve II has flow rate=0; tunnels lead to valves AA, JJ"
        self.assertEqual(Valve.parse(text), Valve("II", 0, {"AA": 1, "JJ": 1}))

    def test_find_way(self):
        self.assertEqual(find_way(self.RAW_VALVES, 30)[0], 1651)

    def test_optimize_valves(self):
        self.assertDictEqual(optimize_valves(self.RAW_VALVES), self.OPTIMIZED_VALVES)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (1651, 1707))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
