
from dataclasses import dataclass
from enum import Enum, IntEnum
from os import path
import re
import unittest


class Element(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class State():
    robots: tuple[int, int, int, int]
    stash: tuple[int, int, int, int]

    def turn(self, robot_type=None, cost=None):
        if robot_type is None:
            after_work = tuple(x + self.robots[i]
                               for i, x in enumerate(self.stash))
            return State(
                tuple(r for r in self.robots),
                after_work
            )

        updated_stash = tuple(x - cost[i] for i, x in enumerate(self.stash))
        can_add = all(map(lambda x: x >= 0, updated_stash))
        if can_add:
            after_work = tuple(x + self.robots[i]
                               for i, x in enumerate(updated_stash))
            new_robots = tuple(r + 1 if i == robot_type else r for i, r in enumerate(self.robots))
            return State(new_robots, after_work)
        return None

    def __hash__(self):
        return hash((self.robots, self.stash))


ROBOTS = 0
STASH = 1

INITIAL_STATE = State((1, 0, 0, 0), (0, 0, 0, 0))


def get_best_possible(state, time):
    prog_sum = time * (time + 1) // 2
    return state.stash[Element.GEODE] * 2 + prog_sum


def visit(state, time, blueprint, memory):
    # print(state, time)
    # TODO check if better state exists for this time
    val = state.stash[Element.GEODE]
    if time <= 0:
        return val
    if val > memory['best']:
        memory['best'] = val
    elif get_best_possible(state, time) < memory['best']:
        return -1
    
    prev = memory.get(state, -1)
    if prev >= time:
        return -1
    memory[state] = time
    new_time = time-1
    options = []

    for element in range(3, -1, -1):
        new_state = state.turn(element, blueprint[element])
        if new_state is not None:
            options.append(new_state)
    if len(options) < len(Element):
        options.append(state.turn())
    result = max(visit(o, new_time, blueprint, memory) for o in options)

    return result


def score_blueprint(blueprint):
    return visit(INITIAL_STATE, 24, blueprint, {'best': 0})


def parse_cost(line, element):
    exp = f"([0-9]+) {element.name.lower()}"
    match = re.search(exp, line)
    return 0 if match is None else int(match.group(1))


def parse_blueprint(line):
    parts = line.split(".")[:len(Element)]
    return [[parse_cost(part, element) for element in Element] for part in parts]


def parse_blueprints(lines):
    return [parse_blueprint(lines[i:i+4]) for i in range(1, len(lines), 6)]


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def read_blueprints(fname):
    return [parse_blueprint(l) for l in read_lines(fname)]

def solve_file(fname):
    blueprints = [parse_blueprint(l) for l in read_lines(fname)]
    total = 0
    for i, b in enumerate(blueprints):
        print(i)
        total += score_blueprint(b) * (i+1) 
    return total

class TestDay(unittest.TestCase):

    BLUEPRINTS = [
        [
            [4, 0, 0, 0],
            [2, 0, 0, 0],
            [3, 14, 0, 0],
            [2, 0, 7, 0],
        ],
        [
            [2, 0, 0, 0],
            [3, 0, 0, 0],
            [3, 8, 0, 0],
            [3, 0, 12, 0],
        ],
    ]

    def test_parse_blueprint(self):
        lines = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
        self.assertEqual(parse_blueprint(lines), self.BLUEPRINTS[0])

    def test_read_blueprints(self):
        self.assertEqual(read_blueprints("input-test.txt"), self.BLUEPRINTS)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 33)

if __name__ == '__main__':
    print(solve_file("input.txt")) # 1150
    unittest.main()
