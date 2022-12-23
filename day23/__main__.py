from collections import defaultdict
from enum import Enum
from os import path
import unittest


class Direction(Enum):
    N = ((-1, 0), ((-1, -1), (-1, 0), (-1, 1)))
    S = ((1, 0), ((1, -1), (1, 0), (1, 1)))
    W = ((0, -1), ((-1, -1), (0, -1), (1, -1)))
    E = ((0, 1), ((-1, 1), (0, 1), (1, 1)))

    def __init__(self, move_offset, check_offsets):
        super().__init__()
        self.move_offset = move_offset
        self.check_offsets = check_offsets

    @staticmethod
    def all():
        return [Direction.N, Direction.S, Direction.W, Direction.E]


def read_map(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    map = set()
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            for j, char in enumerate(line):
                if char == "#":
                    map.add((i, j))
    return map


def get_directions(round):
    length = len(Direction)
    return [Direction.all()[(i + round) % length] for i in range(length)]


def get_new_pos(map, pos, directions):
    canidate = None
    found = False
    for direction in directions:
        if canidate is not None and found:
            break
        to_check = [(pos[0] + off[0], pos[1] + off[1])
                    for off in direction.check_offsets]
        if any(c in map for c in to_check):
            found = True
        elif canidate is None:
            canidate = (pos[0] + direction.move_offset[0],
                        pos[1] + direction.move_offset[1])
    if not found or canidate is None:
        return pos
    return canidate

def get_bounds(map):
    min_row, min_col = float("+inf"), float("+inf")
    max_row, max_col = float("-inf"), float("-inf")

    for pos in map:
        min_row = min(pos[0], min_row)
        min_col = min(pos[1], min_col)
        max_row = max(pos[0], max_row)
        max_col = max(pos[1], max_col)
    
    return min_row, max_row, min_col, max_col

def score_map(map):
    min_row, max_row, min_col, max_col = get_bounds(map)
    size = (max_row - min_row + 1) * (max_col - min_col + 1)
    return size - len(map)


def draw(map):
    min_row, max_row, min_col, max_col = get_bounds(map)
    print("----")
    for row in range(min_row, max_row + 1):
        line = ""
        for col in range(min_col, max_col + 1):
            line += "#" if (row, col) in map else "."
        print(line)
    print("----")

def do_steps(map, max_round):
    round = 0
    while max_round is None or round < max_round:
        new_positions = defaultdict(set)  # new pos -> set of prev pos
        directions = get_directions(round)
        for pos in map:
            new_pos = get_new_pos(map, pos, directions)
            new_positions[new_pos].add(pos)

        new_map = set()
        for new_pos, old in new_positions.items():
            if len(old) == 1:
                new_map.add(new_pos)
            else:
                new_map.update(old)
        round += 1
        if new_map == map:
            return map, round
        map = new_map
    return map, max_round 

def solve_file(fname):
    map = read_map(fname)
    return  (
        score_map(do_steps(map, 10)[0]),
        do_steps(map, None)[1]
    )


class TestDay(unittest.TestCase):

    def test_get_directions(self):
        self.assertEqual(
            get_directions(0),
            [Direction.N, Direction.S, Direction.W, Direction.E]
        )
        self.assertEqual(
            get_directions(1),
            [Direction.S, Direction.W, Direction.E, Direction.N]
        )
        self.assertEqual(
            get_directions(2),
            [Direction.W, Direction.E, Direction.N, Direction.S]
        )

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (110, 20))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
