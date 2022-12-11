
from dataclasses import dataclass
from os import path
import unittest

CALM_FACTOR = 3

@dataclass
class Item():
    value: int
    dividers: set[int]
    bases: set[int]

    def __init__(self, value, bases, dividers=None):
        self.bases = bases
        self.b = 1
        for base in bases:
            self.b = base * self.b
        self.value = value % self.b
        self.dividers = self._find_dividers(value) if dividers is None else dividers

    def __add__(self, other):
        return Item(self.value + other, self.bases)

    def __mul__(self, other):
        other_dividers = self._find_dividers(other)
        other_dividers.update(self.dividers)
        return Item(self.value*other, self.bases, other_dividers)

    def __pow__(self, other):
        return Item(self.value**other, self.bases, self.dividers)

    def __mod__(self, other):
        return 0 if other in self.dividers else 1

    def _find_dividers(self, value):
        dividers = set()
        while value & 1 == 0:
            value = value >> 1
            dividers.add(2)
        for base in self.bases:
            result, rem = divmod(value, base)
            if rem == 0:
                dividers.add(base)
                value = result
        return dividers


@dataclass
class Monkey():
    items: list[Item]
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

def parse_base(line):
    return int(remove_prefix(line, "Test: divisible by "))

def parse_monkey(lines, bases):
    items_str = remove_prefix(lines[1], "Starting items: ")
    items = list(map(lambda s: Item(int(s), bases), items_str.split(", ")))

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
    bases = set((parse_base(lines[i + 3]) for i in range(0, len(lines), 7)))
    monkeys = [parse_monkey(lines[i: i + 6], bases) for i in range(0, len(lines), 7)]
    return monkeys


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
        return value ** 2
    else:
        raise BaseException(f"Unkown operation {operation} for arg {arg}")


def calculate_new_value(item, operation, operation_arg, relif):
    item = apply_operation(item, operation, operation_arg)
    if relif:
        item = Item(item.value // CALM_FACTOR, item.bases)
    return item


def simulate_round(monkeys, relif):
    for monkey in monkeys:
        items = monkey.items
        monkey.inspects = monkey.inspects + len(items)
        monkey.items = []
        for item in items:
            value = calculate_new_value(
                item, monkey.operation, monkey.operation_arg, relif)
            going = monkey.true_path if value % monkey.divider == 0 else monkey.false_path
            monkeys[going].items.append(value)


def business_level(monkeys, relif, rounds_number):
    for i in range(rounds_number):
        if i % 50 == 0:
            print(f"{i}/{rounds_number}")
        simulate_round(monkeys, relif)
    all_inspects = map(lambda m: m.inspects, monkeys)
    top2 = sorted(all_inspects)[-2:]
    return top2[0] * top2[1]


def score_file(fname):
    return (
        business_level(read_monkeys(fname), True, 20),
        business_level(read_monkeys(fname), False, 10000),
    )


class TestDay(unittest.TestCase):

    BASES = set([23, 19, 17, 13])

    def _get_inital(self):
        return [
            Monkey(self._as_items(79, 98), "*", 19, 23, 2, 3),
            Monkey(self._as_items(54, 65, 75, 74), "+", 6, 19, 2, 0),
            Monkey(self._as_items(79, 60, 97), "**", 2, 13, 1, 3),
            Monkey(self._as_items(74), "+", 3, 17, 0, 1),
        ]

    def test_read_monkeys(self):
        expected = self._get_inital()
        self.assertSequenceEqual(read_monkeys("input-test.txt"), expected)

    def test_apply_operation(self):
        self.assertEqual(apply_operation(Item(5, self.BASES), "+", 2), Item(7, self.BASES))
        self.assertEqual(apply_operation(Item(5, self.BASES), "*", 3), Item(15, self.BASES))
        self.assertEqual(apply_operation(Item(5, self.BASES), "**", 2), Item(25, self.BASES))

    def test_simulate_round(self):
        monkeys = self._get_inital()
        simulate_round(monkeys, True)
        self.assertSequenceEqual(
            monkeys[0].items, self._as_items(20, 23, 27, 26))
        self.assertSequenceEqual(
            monkeys[1].items, self._as_items(2080, 25, 167, 207, 401, 1046))
        self.assertSequenceEqual(monkeys[2].items, [])
        self.assertSequenceEqual(monkeys[3].items, [])

    def _as_items(self, *numbers):
        return list(map(lambda x: Item(x, self.BASES), numbers))

    def test_business_level(self):
        self.assertEqual(business_level(self._get_inital(), True, 20), 10605)
        self.assertEqual(business_level(self._get_inital(), False, 10000), 2713310158)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), (10605, 2713310158))


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
