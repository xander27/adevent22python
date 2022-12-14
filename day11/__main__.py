
from dataclasses import dataclass
from functools import reduce
from os import path
import unittest

CALM_FACTOR = 3


@dataclass
class Monkey:
    items: list[int]
    operation: str
    arg: int
    divider: int
    true_path: int
    false_path: int
    inspects: int = 0


def remove_prefix(string, prefix):
    string = string.strip()
    if not string.startswith(prefix):
        raise Exception(f"{string} is not started with {prefix}")
    return string[len(prefix):]


def parse_base(line):
    return int(remove_prefix(line, "Test: divisible by "))


def parse_monkey(lines):
    items_str = remove_prefix(lines[1], "Starting items: ")
    items = list(map(int, items_str.split(", ")))

    operation_str = remove_prefix(lines[2], "Operation: new = old ")
    if operation_str == "* old":
        operation = "**"
        arg = 2
    elif operation_str.startswith("*"):
        operation = "*"
        arg = int(operation_str.split(" ")[1])
    elif operation_str.startswith("+"):
        operation = "+"
        arg = int(operation_str.split(" ")[1])
    else:
        raise Exception("Can not parse operation {lines[2]}")

    divider = int(remove_prefix(lines[3], "Test: divisible by "))
    true_path = int(remove_prefix(lines[4], "If true: throw to monkey "))
    false_path = int(remove_prefix(lines[5], "If false: throw to monkey "))
    return Monkey(items, operation, arg, divider, true_path, false_path)


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


def apply_operation(value, operation, arg):
    if operation == "+":
        return value + arg
    if operation == "*":
        return value * arg
    if operation == "**" and arg == 2:
        return value ** 2
    raise Exception(f"Unknown operation {operation} for arg {arg}")


def calculate_new_value(item, operation, arg, calm, base):
    item = apply_operation(item, operation, arg)
    if calm:
        item = item // CALM_FACTOR
    item = item % base
    return item


def simulate_round(monkeys, calm, base):
    for monkey in monkeys:
        items = monkey.items
        monkey.inspects = monkey.inspects + len(items)
        monkey.items = []
        for item in items:
            value = calculate_new_value(item, monkey.operation, monkey.arg, calm, base)
            going = monkey.true_path if value % monkey.divider == 0 else monkey.false_path
            monkeys[going].items.append(value)


def business_level(monkeys, relif, rounds_number):
    base = get_base(monkeys)
    for i in range(rounds_number):
        if i % 50 == 0:
            print(f"{i}/{rounds_number}")
        simulate_round(monkeys, relif, base)
    all_inspects = map(lambda m: m.inspects, monkeys)
    top2 = sorted(all_inspects)[-2:]
    return top2[0] * top2[1]


def get_base(monkeys):
    return reduce(lambda a, b: a * b, map(lambda m: m.divider, monkeys))


def score_file(fname):
    return (
        business_level(read_monkeys(fname), True, 20),
        business_level(read_monkeys(fname), False, 10000),
    )


class TestDay(unittest.TestCase):

    @staticmethod
    def _get_init():
        return [
            Monkey([79, 98], "*", 19, 23, 2, 3),
            Monkey([54, 65, 75, 74], "+", 6, 19, 2, 0),
            Monkey([79, 60, 97], "**", 2, 13, 1, 3),
            Monkey([74], "+", 3, 17, 0, 1),
        ]

    def test_read_monkeys(self):
        expected = self._get_init()
        self.assertSequenceEqual(read_monkeys("input-test.txt"), expected)

    def test_apply_operation(self):
        self.assertEqual(apply_operation(5, "+", 2), 7)
        self.assertEqual(apply_operation(5, "*", 3), 15)
        self.assertEqual(apply_operation(5, "**", 2), 25)

    def test_simulate_round(self):
        monkeys = self._get_init()
        simulate_round(monkeys, True, get_base(monkeys))
        self.assertSequenceEqual(monkeys[0].items, [20, 23, 27, 26])
        self.assertSequenceEqual(
            monkeys[1].items, [2080, 25, 167, 207, 401, 1046])
        self.assertSequenceEqual(monkeys[2].items, [])
        self.assertSequenceEqual(monkeys[3].items, [])

    def test_business_level(self):
        self.assertEqual(business_level(self._get_init(), True, 20), 10605)
        self.assertEqual(business_level(
            self._get_init(), False, 10000), 2713310158)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), (10605, 2713310158))


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
