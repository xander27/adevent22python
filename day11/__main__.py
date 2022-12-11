
from dataclasses import dataclass
from os import path
import unittest

CALM_FACTOR = 3
ROUNDS_NUMBER = 20

@dataclass
class Monkey():
    items: list[int]
    operation: str
    operation_arg: int
    divider: int
    true_path: int
    false_path: int 
    inspects: int = 0


def remove_prefix(string, prefix):
    string = string.strip()
    if not string.startswith(prefix):
        raise BaseException(f"{string} is not started with {prefix}")
    return string[len(prefix):]


def parse_monkey(lines):
    items_str = remove_prefix(lines[1], "Starting items: ")
    items = list(map(int, items_str.split(", ")))

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


def apply_operation(value, operation, arg):
    if operation == "+":
        return value + arg
    elif operation == "*":
        return value * arg
    elif operation == "**" and arg == 2:
        return value * value
    else:
        raise BaseException(f"Unkown operation {operation} for arg {arg}")


def calculate_new_value(value, operation, operation_arg):
    return apply_operation(value, operation, operation_arg) // CALM_FACTOR


def simulate_round(monkeys):
    for monkey in monkeys:
        items = monkey.items
        monkey.inspects = monkey.inspects + len(items)
        monkey.items = []
        for item in items:
            value = calculate_new_value(item, monkey.operation, monkey.operation_arg)  
            going = monkey.true_path if value % monkey.divider == 0 else monkey.false_path
            monkeys[going].items.append(value)

def business_level(monkeys):
    for _ in range(ROUNDS_NUMBER):
        simulate_round(monkeys)
    all_inspects = map(lambda m: m.inspects, monkeys)
    top2 = sorted(all_inspects)[-2:]
    return top2[0] * top2[1]

def score_file(fname):
    monkeys = read_monkeys(fname)
    return business_level(monkeys)


class TestDay(unittest.TestCase):

    def _get_inital_monkeys(self):
        return [
            Monkey([79, 98], "*", 19, 23, 2, 3),
            Monkey([54, 65, 75, 74], "+", 6, 19, 2, 0),
            Monkey([79, 60, 97], "**", 2, 13, 1, 3),
            Monkey([74], "+", 3, 17, 0, 1),
        ]

    def test_read_monkeys(self):
        expected = self._get_inital_monkeys()
        self.assertSequenceEqual(read_monkeys("input-test.txt"), expected)

    def test_apply_operation(self):
        self.assertEqual(apply_operation(5, "+", 2), 7)
        self.assertEqual(apply_operation(5, "*", 3), 15)
        self.assertEqual(apply_operation(5, "**", 2), 25)

    def test_simulate_round(self):
        monkeys = self._get_inital_monkeys()
        simulate_round(monkeys)
        self.assertSequenceEqual(monkeys[0].items, [20, 23, 27, 26])
        self.assertSequenceEqual(monkeys[1].items, [2080, 25, 167, 207, 401, 1046])
        self.assertSequenceEqual(monkeys[2].items, [])
        self.assertSequenceEqual(monkeys[3].items, [])

    def test_business_level(self):
        self.assertEqual(business_level(self._get_inital_monkeys()), 10605)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), 10605)


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
