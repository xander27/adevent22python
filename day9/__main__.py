from dataclasses import dataclass
from enum import Enum
from os import path
import unittest


class Direction(Enum):
    UP = ("U", 0, -1)
    DOWN = ("D", 0, 1)
    LEFT = ("L", -1, 0)
    RIGHT = ("R", 1, 0)

    def __init__(self, code, x_diff, y_diff):
        super().__init__()
        self.code = code
        self.diff = (x_diff, y_diff)

    @staticmethod
    def from_code(code):
        for direction in Direction:
            if direction.code == code:
                return direction
        raise BaseException(f"Unknown code {code}")


@dataclass
class Command():
    direction: Direction
    distance: int

    @staticmethod
    def parse(string):
        parts = string.split()
        return Command(Direction.from_code(parts[0]), int(parts[1]))


def read_commands(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for s in file:
            yield Command.parse(s.rstrip())


def get_next_tail_position(cur_tail, head):
    diff = (head[0] - cur_tail[0], head[1] - cur_tail[1])
    abs_diff = (abs(diff[0]), abs(diff[1]))
        

    if abs_diff[0] > 1:
        if abs_diff[1] == 0:
            return (cur_tail[0] + normalize(diff[0]), cur_tail[1])
        else:
            return (cur_tail[0] + normalize(diff[0]), cur_tail[1] + normalize(diff[1]))

    if abs_diff[1] > 1:
        if abs_diff[0] == 0:
            return (cur_tail[0], cur_tail[1]  + normalize(diff[1]))
        else:
            return (cur_tail[0] + normalize(diff[0]), cur_tail[1] + normalize(diff[1]))
    
    return cur_tail

def count_tail_positions(commands):
    positions = set()
    tail, head = (0, 0), (0, 0)
    positions.add(tail)

    for command in commands:
        diff = command.direction.diff
        for _ in range(command.distance):
            head = (head[0] + diff[0], head[1] + diff[1])
            tail = get_next_tail_position(tail, head)
            positions.add(tail)

    return len(positions)


def normalize(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def score_file(fname):
    commands = read_commands(fname)
    return count_tail_positions(commands)


class TestDay(unittest.TestCase):

    COMMANDS = [
        Command(Direction.RIGHT, 4),
        Command(Direction.UP, 4),
        Command(Direction.LEFT, 3),
        Command(Direction.DOWN, 1),
        Command(Direction.RIGHT, 4),
        Command(Direction.DOWN, 1),
        Command(Direction.LEFT, 5),
        Command(Direction.RIGHT, 2)
    ]

    def teat_count_tail_positions(self):
        self.assertEqual(count_tail_positions(self.COMMANDS), 13)

    def read_commands(self):
        self.assertSequenceEqual(
            list(read_commands("input-test.txt")), self.COMMANDS)

    def test_score_filee(self):
        self.assertEqual(score_file("input-test.txt"), 13)


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
