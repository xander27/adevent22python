from dataclasses import dataclass
from os import path
import re
import unittest

PARSING_EXP = "Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)"


@dataclass
class Valve():
    name: str
    flow: int
    children: dict[str,int]

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

def find_way(valves):
    not_broken = 0
    for valve in valves.values():
        if valve.flow > 0:
            not_broken += 1
    return step(
        valves = valves,
        cur = valves["AA"],
        time = 29,
        flow = 0,
        open = set(),
        not_broken=not_broken,
        shortest=dict(),
        path = []
    )


def step(valves, cur, time, flow, open, not_broken, shortest, path):
    if time == 0:
        return flow
    if len(open) == not_broken:
        return flow

    key = cur.name + ">" + ":".join(sorted(open))
    if key in shortest and shortest[key] > time:
        return -1
    shortest[key] = time

    m = 0
    if cur.name not in open and cur.flow > 0:
        new_open = open.copy()
        new_open.add(cur.name)
        new_path = path.copy()
        new_path.append((cur.name, time))
        new_flow = flow + cur.flow * time
        result = step(valves, cur, time - 1, new_flow, new_open, not_broken, shortest, new_path)
        if result > m: 
            m = result

    for child_name in cur.children:
        child = valves[child_name]
        result = step(valves, child, time-1, flow, open, not_broken, shortest, path)
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
    return find_way(valves)


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

    def test_find_way(self):
        self.assertEqual(find_way(self.VAVLES), 1651)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 1651)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()