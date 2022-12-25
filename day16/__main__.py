from dataclasses import dataclass
from os import path
import re
import unittest

PARSING_EXP = "Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)"


@dataclass
class Valve:
    name: str
    flow: int
    children: dict[str, int]


def parse_valve(string):
    match = re.match(PARSING_EXP, string)
    return Valve(
        match.group(1),
        int(match.group(2)),
        {s.strip(): 1 for s in match.group(3).split(",")}
    )


def find_way(valves, time):
    not_broken = 0
    for valve in valves.values():
        if valve.flow > 0:
            not_broken += 1
    return step(
        valves=valves,
        cur="AA",
        time=time - 1,
        flow=0,
        opened=set(),
        not_broken=not_broken,
        shortest=dict()
    )


def step(valves, cur, time, flow, opened, not_broken, shortest):
    if time == 0:
        return flow
    if len(opened) == not_broken:
        return flow

    key = cur + ">" + ":".join(sorted(opened))
    if key in shortest and shortest[key] > time:
        return -1
    shortest[key] = time

    m = 0
    valve = valves[cur]
    if cur not in opened and valve.flow > 0:
        new_open = opened.copy()
        new_open.add(cur)
        new_flow = flow + valve.flow * time
        result = step(valves, cur, time - 1, new_flow, new_open, not_broken, shortest)
        if result > m:
            m = result

    for child in valve.children:
        result = step(valves, child, time - 1, flow, opened, not_broken, shortest)
        if result > m:
            m = result

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
    return find_way(valves, 30)


class TestDay(unittest.TestCase):
    VALVES = {
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

    def test_parse_valve(self):
        text = "Valve II has flow rate=0; tunnels lead to valves AA, JJ"
        self.assertEqual(parse_valve(text), Valve("II", 0, {"AA": 1, "JJ": 1}))

    def test_read_valves(self):
        self.assertEqual(read_valves("input-test.txt"), self.VALVES)

    def test_find_way(self):
        self.assertEqual(find_way(self.VALVES, 30), 1651)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 1651)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
