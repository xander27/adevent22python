
from dataclasses import dataclass
from os import path
import unittest


@dataclass
class Monkey():
    items: set[int]
    operation: str
    operation_arg: int
    divider: int
    true_path: int
    false_path: int


def remove_prefix(string, prefix):
    string = string.strip()
    if not string.startswith(prefix):
        raise BaseException(f"{string} is not started with {prefix}")
    return string[len(prefix):]


def parse_monkey(lines):
    items_str = remove_prefix(lines[1], "Starting items: ")
    items = set(map(int, items_str.split(", ")))

    operation_str = remove_prefix(lines[2], "Operation: new = old ")
    if operation_str == "* old":
        operation = "**"
        operation_arg = 2
    elif operation_str.startswith("*"):
        operation = "*"
        operation_arg = int(operation_str.split(" ")[1])
    elif operation_str.startswith("+"):
        operation = "+"
        operation_arg = int(operation_str.split(" ")[1])
    else:
        raise BaseException("Can not parse operation {lines[2]}")

    divider = int(remove_prefix(lines[3], "Test: divisible by "))
    true_path = int(remove_prefix(lines[4], "If true: throw to monkey "))
    false_path = int(remove_prefix(lines[5], "If false: throw to monkey "))
    return Monkey(items, operation, operation_arg, divider, true_path, false_path)


def parse_monkeys(lines):
    return [parse_monkey(lines[i: i + 6]) for i in range(0, len(lines), 7)]


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def read_monkeys(fname):
    lines = list(read_lines(fname))
    return parse_monkeys(lines)


class TestDay(unittest.TestCase):

    def test_read_monkeys(self):
        expected = [
            Monkey(set([79, 98]), "*", 19, 23, 2, 3),
            Monkey(set([54, 65, 75, 74]), "+", 6, 19, 2, 0),
            Monkey(set([79, 60, 97]), "**", 2, 13, 1, 3),
            Monkey(set([74]), "+", 3, 17, 0, 1),
        ]
        self.assertSequenceEqual(read_monkeys("input-test.txt"), expected)


if __name__ == '__main__':
    unittest.main()
