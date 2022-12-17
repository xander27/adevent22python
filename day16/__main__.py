# inspired by https://github.com/juanplopes/advent-of-code-2022/blob/main/day16.py

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


def solve_file(fname):
    valves = read_valves(fname)
    indecies, connections = {}, {}

    i = 0
    valves_with_flow = {}
    for name, valve in valves.items():
        connections[name] = {v: 1 if v in valve[1]
                             else float('+inf') for v in valves.keys()}
        if valve[0] > 0:
            valves_with_flow[name] = valve
            indecies[name] = 1 << i
            i += 1

    for k in connections:
        for i in connections:
            for j in connections:
                connections[i][j] = min(
                    connections[i][j], connections[i][k]+connections[k][j])

    def visit(cur, time, state, flow, best):
        best[state] = max(best.get(state, 0), flow)
        for next, valve in valves_with_flow.items():
            new_time = time - connections[cur][next] - 1
            new_state = indecies[next] | state
            if new_time <= 0 or new_state == state:
                continue
            new_flow = flow + new_time * valve[0]
            visit(next, new_time, new_state, new_flow, best)
        return best

    p1 = max(visit("AA", 30, 0, 0, {}).values())
    best = visit('AA', 26, 0, 0, {})
    p2 = max(v1+v2 for k1, v1 in best.items()
             for k2, v2 in best.items() if not k1 & k2)
    return p1, p2


print(solve_file("input-test.txt"))
print(solve_file("input.txt"))
