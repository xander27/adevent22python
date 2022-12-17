# based on https://github.com/juanplopes/advent-of-code-2022/blob/main/day16.py

from os import path
import re

PARSING_EXP = "Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)"


def read_valves(fname):
    result = {}
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(PARSING_EXP, line)
            name = match.group(1)
            flow = int(match.group(2))
            children = set(map(lambda s: s.strip(), match.group(3).split(",")))
            result[name] = (flow, children)
    return result

def build_connections(valves):
    max_value = len(valves) + 1
    result = {}
    for name, valve in valves.items():
        result[name] = {v: 1 if v in valve[1] else max_value for v in valves}
    for k in valves.keys():
        for i in valves.keys():
            for j in valves.keys():
                result[i][j] = min(result[i][j], result[i][k]+result[k][j])
    return result

def build_indecies(names):
    return { name: 1 << i for i, name in enumerate(names) }


def visit(connections, indecies, valves_with_flow, cur, time, state, flow, best):
    best[state] = max(best.get(state, 0), flow)
    for other, valve in valves_with_flow.items():
        new_time = time - connections[cur][other] - 1
        new_state = indecies[other] | state
        if new_time <= 0 or new_state == state:
            continue
        new_flow = flow + new_time * valve[0]
        visit(connections, indecies, valves_with_flow, other, new_time, new_state, new_flow, best)
    return best

def solve_file(fname):
    valves = read_valves(fname)
    connections = build_connections(valves)
    valves_with_flow = {n: v for n, v in valves.items() if v[0] > 0}
    indecies = build_indecies(valves_with_flow.keys())

    p1 = max(visit(connections, indecies, valves_with_flow,"AA", 30, 0, 0, {}).values())
    best = visit(connections, indecies, valves_with_flow,'AA', 26, 0, 0, {})

    # find two best solutions which do not open same valves
    p2 = max(v1+v2 for k1, v1 in best.items() for k2, v2 in best.items() if not k1 & k2)
    return p1, p2


print(solve_file("input-test.txt"))
print(solve_file("input.txt"))
