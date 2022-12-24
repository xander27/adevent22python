from collections import defaultdict
from dataclasses import dataclass
from math import gcd
from os import path
import unittest

OFFSETS = {
    "<": (0, -1),
    "^": (-1, 0),
    "+": (0, 0),
    ">": (0, 1),
    "v": (1, 0),
}


@dataclass
class BlizzardStore:
    states: list[dict[tuple[int, int], list[str]]]
    period: int

    def __init__(self, field, first_value):
        self.states = [first_value]
        self.period = lcm(field.width - 2, field.height - 2)
        for _ in range(self.period - 1):
            self.states.append(self._get_next_blizzards(field, self.states[-1]))

    def _get_next_blizzards(self, field, current):
        result = defaultdict(list)
        for pos, chars in current.items():
            for char in chars:
                next_pos = self._get_next_blizzard_pos(pos, char, field)
                result[next_pos].append(char)
        return result

    @staticmethod
    def _get_next_blizzard_pos(pos, char, field):
        offset = OFFSETS[char]
        candidate = (pos[0] + offset[0], pos[1] + offset[1])
        if field.is_open(candidate):
            return candidate
        if char == '>':
            return pos[0], 1
        if char == '<':
            return pos[0], field.width - 2
        if char == '^':
            return field.height - 2, pos[1]
        if char == 'v':
            return 1, pos[1]
        raise Exception(f"Unexpected char {char}")


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
class Field:
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


def parse_field(lines):
    return Field(
        height=len(lines),
        width=len(lines[0]),
        start_col=lines[0].index("."),
        final_col=lines[-1].index("."),
    )


def parse_blizzards(lines, field):
    blizzards = defaultdict(list)
    for row, line in enumerate(lines[1:-1]):
        for col, char in enumerate(line[1:-1]):
            if char == ".":
                continue
            blizzards[(row + 1, col + 1)].append(char)
    return BlizzardStore(field, blizzards)


def solve(field, start, finish, b_period, bs, items_order):
    offsets = OFFSETS.values() if items_order else list(OFFSETS.values())[::-1]

    best = float("+inf")
    visited = {}
    state = State(start, b_period)
    stack = [(state, 0)]

    while len(stack) > 0:
        state, length = stack.pop()

        if length >= best:
            continue

        if state.elfs_pos == finish:
            best = min(length, best)
            continue

        prev_visit = visited.get(state, float("+inf"))
        if prev_visit <= length:
            continue
        visited[state] = length

        next_blizzard_period = (state.blizzard_period + 1) % bs.period
        next_blizzards = bs.states[next_blizzard_period]

        for offset in offsets:
            move = (state.elfs_pos[0] + offset[0], state.elfs_pos[1] + offset[1])
            if not field.is_open(move):
                continue
            if len(next_blizzards.get(move, [])) > 0:
                continue
            new_state = State(move, next_blizzard_period)
            stack.append((new_state, length + 1))

    return best


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def solve_file(fname):
    lines = read_lines(fname)
    field = parse_field(lines)
    bs = parse_blizzards(lines, field)

    orig_start = (0, field.start_col)
    orig_finish = (field.height - 1, field.final_col)

    p1 = solve(field, orig_start, orig_finish, 0, bs, True)

    p2 = p1 + solve(field, orig_finish, orig_start, p1 % bs.period, bs, False)
    p2 += solve(field, orig_start, orig_finish, p2 % bs.period, bs, True)
    return p1, p2


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

    MAP = Field(height=6, width=8, start_col=1, final_col=6)

    STATE = State((0, 1), 0)

    BS = BlizzardStore(
        field=MAP,
        first_value={
            (1, 1): [">"], (1, 2): [">"], (1, 4): ["<"], (1, 5): ["^"], (1, 6): ["<"],
            (2, 2): ["<"], (2, 5): ["<"], (2, 6): ["<"],
            (3, 1): [">"], (3, 2): ["v"], (3, 4): [">"], (3, 5): ["<"], (3, 6): [">"],
            (4, 1): ["<"], (4, 2): ["^"], (4, 3): ["v"], (4, 4): ["^"], (4, 5): ["^"], (4, 6): [">"]
        }
    )

    def test_parse_map(self):
        self.assertEqual(parse_field(self.LINES), self.MAP)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (18, 54))


if __name__ == '__main__':
    print(solve_file("input.txt"))  # 288
    unittest.main()
