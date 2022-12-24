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


def is_anti_move(one, another):
    s = {one, another}
    return s == {"<", ">"} or s == {"^", "v"}


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
                # print(char, pos, next_pos)
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


def parse_blizzards(lines, field):
    blizzards = defaultdict(list)
    for row, line in enumerate(lines[1:-1]):
        for col, char in enumerate(line[1:-1]):
            if char == ".":
                continue
            blizzards[(row + 1, col + 1)].append(char)
    return BlizzardStore(field, blizzards)


def parse_state(lines):
    return State((0, lines[0].index(".")), 0)


def solve(field, state, bs):
    best = float("+inf")
    visited = {}
    stack = [(state, "")]

    while len(stack) > 0:
        state, way = stack.pop()
        length = len(way)

        if length >= best:
            continue

        if state.elfs_pos == (field.height - 1, field.final_col):
            best = min(length, best)
            continue

        prev_visit = visited.get(state, float("+inf"))
        if prev_visit <= length:
            continue
        visited[state] = length

        next_blizzard_period = (length + 1) % bs.period
        next_blizzards = bs.states[next_blizzard_period]

        for char, offset in OFFSETS.items():
            move = (state.elfs_pos[0] + offset[0],
                    state.elfs_pos[1] + offset[1])
            if not field.is_open(move):
                continue
            if len(next_blizzards.get(move, [])) > 0:
                continue
            new_state = State(move, next_blizzard_period)
            stack.append((new_state, way + char))

    return best


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def solve_file(fname):
    lines = read_lines(fname)
    field = parse_map(lines)
    bs = parse_blizzards(lines, field)
    state = parse_state(lines)
    return solve(field, state, bs)


def draw(field, blizzards, pos=None):
    lines = ["".join("#" * field.width)]
    for row in range(1, field.height - 1):
        line = "#"
        for col in range(1, field.width - 1):
            directions = blizzards.get((row, col), [])
            length = len(directions)
            if length == 0:
                line += "."
            elif length == 1:
                line += directions[0]
            else:
                line += str(length)
        line += "#"
        lines.append(line)
    lines.append("".join("#" * field.width))
    if pos is not None:
        lines[pos[0]] = "".join("E" if i == pos[1] else c for i, c in enumerate(lines[pos[0]]))
    print("\n".join(lines))


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
        field=MAP,
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
        # for state in self.BS.states:
        #     draw_blizzards(self.MAP, state)
        #     print()
        self.assertEqual(solve(self.MAP, self.STATE, self.BS), 18)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 18)


if __name__ == '__main__':
    print(solve_file("input.txt"))  # < 71409
    unittest.main()
