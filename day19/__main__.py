from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from functools import reduce
from os import path
import re
import unittest


class Element(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class State:
    robots: tuple[int, int, int, int]
    stash: tuple[int, int, int, int]

    MAX_RES = 100

    def turn(self, robot_type=None, cost=None):
        if robot_type is None:
            after_work = tuple(x + self.robots[i] for i, x in enumerate(self.stash))
            return State(tuple(r for r in self.robots), after_work)

        updated_stash = tuple(x - cost[i] for i, x in enumerate(self.stash))
        can_add = all(map(lambda x: x >= 0, updated_stash))
        if can_add:
            after_work = tuple(min(x + self.robots[i], self.MAX_RES)
                               for i, x in enumerate(updated_stash))
            new_robots = tuple(r + 1 if i == robot_type else r for i, r in enumerate(self.robots))
            return State(new_robots, after_work)
        return None

    def __hash__(self):
        return hash((self.robots, self.stash))

    def is_better(self, other):
        better, worse = False, False

        for a, b in zip(self.robots, other.robots):
            if a > b:
                better = True
            elif a < b:
                worse = True

        for a, b in zip(self.stash, other.stash):
            if a > b:
                better = True
            elif a < b:
                worse = True

        if better == worse:
            return None
        return better


INITIAL_STATE = State((1, 0, 0, 0), (0, 0, 0, 0))


def get_best_possible(state, time):
    prog_sum = time * (time + 1) // 2
    return state.stash[Element.GEODE] * 2 + prog_sum


def get_max_robots(blueprint):
    maxs = [0, 0, 0, 999]
    for robot in blueprint:
        for i, cost in enumerate(robot):
            if cost > maxs[i]:
                maxs[i] = cost
    return maxs


def get_options(state, blueprint, time, max_robots):
    new_state = state.turn(Element.GEODE, blueprint[Element.GEODE])
    if new_state is not None:
        return [new_state]

    options = []
    for element in range(2, -1, -1):
        if time < 2 and element < 2:
            continue
        if state.robots[element] >= max_robots[element]:
            continue
        new_state = state.turn(element, blueprint[element])
        if new_state is not None:
            options.append(new_state)
    options.append(state.turn())
    return options


def visit(state, time, blueprint, by_state, by_time, max_robots):
    val = state.stash[Element.GEODE]
    if time <= 0:
        return val
    if val > by_state['best']:
        by_state['best'] = val
    elif get_best_possible(state, time) < by_state['best']:
        return -1
    prev = by_state.get(state, -1)
    if prev >= time:
        return -1

    same_time = by_time[time]
    if state in same_time:
        return -1
    to_replace = []
    for other in same_time:
        better = state.is_better(other)
        if better is None:
            continue
        if better:
            to_replace.append(other)
        else:
            return -1
    same_time.add(state)
    for other in to_replace:
        same_time.remove(other)

    by_state[state] = time
    new_time = time - 1

    options = get_options(state, blueprint, time, max_robots)
    result = max(visit(o, new_time, blueprint, by_state, by_time, max_robots) for o in options)

    return result


def score_blueprint(blueprint, turns):
    return visit(INITIAL_STATE, turns, blueprint, {'best': 0}, defaultdict(set), get_max_robots(blueprint))


def parse_cost(line, element):
    exp = f"([0-9]+) {element.name.lower()}"
    match = re.search(exp, line)
    return 0 if match is None else int(match.group(1))


def parse_blueprint(line):
    parts = line.split(".")[:len(Element)]
    return [[parse_cost(part, element) for element in Element] for part in parts]


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def read_blueprints(fname):
    return [parse_blueprint(l) for l in read_lines(fname)]


def solve_file_p1(fname):
    blueprints = [parse_blueprint(line) for line in read_lines(fname)]
    return sum(score_blueprint(b, 24) * (i + 1) for i, b in enumerate(blueprints))


def solve_file_p2(fname):
    blueprints = [parse_blueprint(line) for line in read_lines(fname)]
    blueprints = blueprints[:3]
    return reduce(lambda a, b: a * b, (score_blueprint(b, 32) for b in blueprints))


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

    def test_is_better(self):
        this = State((1, 1, 1, 1), (1, 1, 1, 1))
        self.assertTrue(this.is_better(State((1, 1, 1, 0), (1, 1, 1, 1))))
        self.assertTrue(this.is_better(State((1, 1, 1, 1), (1, 1, 1, 0))))
        self.assertTrue(this.is_better(State((1, 1, 0, 1), (1, 1, 1, 0))))

        self.assertFalse(this.is_better(State((2, 1, 1, 1), (1, 1, 1, 1))))
        self.assertFalse(this.is_better(State((1, 1, 1, 1), (2, 1, 1, 1))))
        self.assertFalse(this.is_better(State((1, 2, 1, 1), (1, 2, 1, 1))))

        self.assertIsNone(this.is_better(State((2, 1, 1, 1), (0, 1, 1, 1))))
        self.assertIsNone(this.is_better(State((1, 1, 1, 0), (2, 1, 1, 1))))
        self.assertIsNone(this.is_better(State((1, 2, 1, 0), (1, 2, 1, 1))))

    def test_parse_blueprint(self):
        lines = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 " \
                "ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian. "
        self.assertEqual(parse_blueprint(lines), self.BLUEPRINTS[0])

    def test_read_blueprints(self):
        self.assertEqual(read_blueprints("input-test.txt"), self.BLUEPRINTS)

    def test_solve_file(self):
        self.assertEqual(solve_file_p1("input-test.txt"), 33)

    def test_get_max_robots(self):
        self.assertEqual(get_max_robots(self.BLUEPRINTS[0]), [4, 14, 7, 999])
        self.assertEqual(get_max_robots(self.BLUEPRINTS[1]), [3, 8, 12, 999])


if __name__ == '__main__':
    # print(solve_file_p1("input.txt")) # 1150
    # print(solve_file_p2("input.txt"))  # - 37367
    unittest.main()
