
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


def parse_cost(line, element):
    exp = f"([0-9]+) {element.name.lower()}"
    match = re.search(exp, line)
    return 0 if match is None else int(match.group(1))


def parse_blueprint(lines):
    return tuple(tuple(parse_cost(line, element) for element in Element) for line in lines)

def parse_blueprints(lines):
    return tuple(parse_blueprint(lines[i:i+4]) for i in range(1, len(lines), 6))

def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")

def read_blueprints(fname):
    lines = read_lines(fname)
    return parse_blueprints(lines)

class TestDay(unittest.TestCase):

    BLUEPRINTS = (
        (
            (4, 0, 0, 0),
            (2, 0, 0, 0),
            (3, 14, 0, 0),
            (2, 0, 7, 0),
        ),
        (
            (2, 0, 0, 0),
            (3, 0, 0, 0),
            (3, 8, 0, 0),
            (3, 0, 12, 0),
        ),
    )

    def test_parse_blueprint(self):
        lines = [
            "Each ore robot costs 4 ore",
            "Each clay robot costs 2 ore",
            "Each obsidian robot costs 3 ore and 14 clay",
            "Each geode robot costs 2 ore and 7 obsidian"
        ]
        self.assertEqual(parse_blueprint(lines), self.BLUEPRINTS[0])

    def test_read_blueprints(self):
        self.assertEqual(read_blueprints("input-test.txt"), self.BLUEPRINTS)


if __name__ == '__main__':
    unittest.main()
