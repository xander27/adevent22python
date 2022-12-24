

from collections import defaultdict
from dataclasses import dataclass
from math import gcd
from os import path
import unittest

OFFSETS = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0),
    "+": (0, 0)
}


def is_anti_move(one, another):
    s = set([one, another])
    return s == set(["<", ">"]) or s == set(["^", "v"])


@dataclass
class BlizzardStore:
    states: list[dict[tuple[int, int], list[str]]]
    period: int

    def __init__(self, map, first_value):
        self.states = [first_value]
        self.period = lcm(map.width - 2, map.height - 2)
        for _ in range(self.period - 1):
            self.states.append(self._get_next_blizzards(map, self.states[-1]))

    def get_for_turn(self, turn):
        return self.states[turn % self.period]

    def _get_next_blizzards(self, map, current):
        result = defaultdict(list)
        for pos, chars in current.items():
            for char in chars:
                next_pos = self._get_next_blizzard_pos(pos, char, map)
                # print(char, pos, next_pos)
                result[next_pos].append(char)
        return result

    def _get_next_blizzard_pos(self, pos, char, map):
        offset = OFFSETS[char]
        candidate = (pos[0] + offset[0], pos[1] + offset[1])
        if map.is_open(candidate):
            return candidate
        if char == '>':
            return (pos[0], 1)
        if char == '<':
            return (pos[0], map.width - 2)
        if char == '^':
            return (map.height - 2, pos[1])
        if char == 'v':
            return (1, pos[1])
        raise BaseException(f"Unpexted char {char}")


@dataclass
class State:
    elfs_pos: tuple[int, int]
    blizzard_period: int

    def __init__(self, elfs_pos, blizzard_period):
        self.elfs_pos = elfs_pos
        self.blizzard_period = blizzard_period

    def __hash__(self):
        return hash((self.elfs_pos[0], self.elfs_pos[1], self.blizzard_period))


@dataclass
class Map:
    height: int
    width: int
    start_col: int
    final_col: int

    def is_open(self, pos):
        row, col = pos
        if col <= 0 or col >= self.width - 1:
            return False
        if row == 0:
            return col == self.start_col
        if row == self.height - 1:
            return col == self.final_col
        if row < 0 or row >= self.height:
            return False
        return True


def parse_map(lines):
    return Map(
        height=len(lines),
        width=len(lines[0]),
        start_col=lines[0].index("."),
        final_col=lines[-1].index("."),
    )


def parse_blizzards(lines, map):
    blizzards = defaultdict(list)
    for row, line in enumerate(lines[1:-1]):
        for col, char in enumerate(line[1:-1]):
            if char == ".":
                continue
            blizzards[(row+1, col+1)].append(char)
    # TODO nok
    return BlizzardStore(map, blizzards)


def parse_state(lines):
    return State((0, lines[0].index(".")), 0)


def solve(map, state, bs, path, memory):
    length = len(path)
    best = memory.get("best", float("+inf"))
    if state.elfs_pos == (map.height - 1, map.final_col):
        if length < best:
            memory["best"] = length
        return length

    if length > best:
        return float("+inf")

    prev = memory.get(state, False)
    if prev:
        return float("+inf")
    memory[state] = True

    next_blizzard_period = (length + 1) % bs.period
    next_blizzards = bs.states[next_blizzard_period]
    min_step = float("+inf")

    for char, offset in OFFSETS.items():
        move = (state.elfs_pos[0] + offset[0], state.elfs_pos[1] + offset[1])
        if not map.is_open(move):
            continue
        if len(next_blizzards.get(move, [])) > 0:
            continue
        result = solve(map, State(move, next_blizzard_period),
                       bs, path + char, memory)
        min_step = min(min_step, result)

    return min_step


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def solve_file(fname):
    lines = read_lines(fname)
    map = parse_map(lines)
    bs = parse_blizzards(lines, map)
    state = parse_state(lines)
    return solve(map, state, bs, "", {})


def draw_blizzards(map, blizzards):
    print("".join("#" * map.width))
    for row in range(1, map.height - 1):
        line = "#"
        for col in range(1, map.width - 1):
            directions = blizzards.get((row, col), [])
            length = len(directions)
            if length == 0:
                line += "."
            elif length == 1:
                line += directions[0]
            else:
                line += str(length)
        line += "#"
        print(line)
    print("".join("#" * map.width))


def lcm(a, b):
    return (a * b) // gcd(a, b)


class TestDay(unittest.TestCase):

    LINES = [
        "#.######",
        "#>>.<^<#",
        "#.<..<<#",
        "#>v.><>#",
        "#<^v^^>#",
        "######.#",
    ]

    MAP = Map(height=6, width=8, start_col=1, final_col=6)

    STATE = State((0, 1), 0)

    BS = BlizzardStore(
        map=MAP,
        first_value={
            (1, 1): [">"], (1, 2): [">"], (1, 4): ["<"], (1, 5): ["^"], (1, 6): ["<"],
            (2, 2): ["<"], (2, 5): ["<"], (2, 6): ["<"],
            (3, 1): [">"], (3, 2): ["v"], (3, 4): [">"], (3, 5): ["<"], (3, 6): [">"],
            (4, 1): ["<"], (4, 2): ["^"], (4, 3): ["v"], (4, 4): ["^"], (4, 5): ["^"], (4, 6): [">"]
        }
    )

    def test_parse_map(self):
        self.assertEqual(parse_map(self.LINES), self.MAP)

    def test_parse_state(self):
        self.assertEqual(parse_state(self.LINES), self.STATE)

    def test_solve(self):
        # for state in self.BS.states[:2]:
        #     draw_blizzards(self.MAP, state)
        #     # print(state)
        #     # print("=====")
        self.assertEqual(solve(self.MAP, self.STATE, self.BS, "", {}), 18)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 18)


if __name__ == '__main__':
    # print(solve_file("input.txt"))
    unittest.main()
