

from dataclasses import dataclass
from os import path
import unittest

ROOT = "root"
ME = "humn"


@dataclass
class Effect:
    a: int
    b: int


@dataclass
class NumberMonkey:
    value: int

    def calc(self, _):
        return self.value

    def get_effect(self, _, name):
        if name == ME:
            return Effect(1, 0)
        return Effect(0, self.value)


@dataclass
class OperationMonkey():
    first: str
    operation: str
    second: str
    value: int = None
    effect: str = None

    def calc(self, data):
        if self.value is None:
            first_value = data[self.first].calc(data)
            second_value = data[self.second].calc(data)
            if self.operation == "*":
                self.value = first_value * second_value
            elif self.operation == "/":
                self.value = first_value / second_value
            elif self.operation == "+":
                self.value = first_value + second_value
            elif self.operation == "-":
                self.value = first_value - second_value
            else:
                raise Exception(f"Unknown operation {self.operation}")
        return self.value

    def get_effect(self, data, _):
        if self.effect is None:
            first = data[self.first].get_effect(data, self.first)
            second = data[self.second].get_effect(data, self.second)
            if self.operation == "+" or self.operation == "-":
                mul = 1 if self.operation == "+" else -1
                self.effect = Effect(first.a + second.a * mul, first.b + second.b * mul)
            elif self.operation == "*" or self.operation == "/":
                if first.a != 0 and second.a != 0:
                    raise Exception(f"Cant do powers")
                if self.operation == "*":
                    if first.a != 0:
                        primary = first
                        secondary = second.b
                    else:
                        primary = second
                        secondary = first.b
                    self.effect = Effect(primary.a * secondary, primary.b * secondary)
                else:
                    if second.a != 0:
                        raise Exception(f"Cant do powers")
                    self.effect = Effect(first.a / second.b, first.b / second.b)
            else:
                raise Exception(f"Unknown operation {self.operation}")
        return self.effect


def parse_monkey(line):
    name, body = line.strip().split(": ")
    body_parts = body.split(" ")
    if len(body_parts) == 1:
        return name, NumberMonkey(int(body_parts[0]))
    else:
        return name, OperationMonkey(*body_parts)


def read_file(fname):
    result = {}
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            name, monkey = parse_monkey(line)
            result[name] = monkey
    return result


def find_what_to_yell(data):
    root = data[ROOT]
    root_first = data[root.first]
    root_second = data[root.second]

    first_branch = root_first.get_effect(data, root.first)
    second_branch = root_second.get_effect(data, root.second)

    if first_branch.a != 0:
        x_branch = first_branch
        other_branch = second_branch
    else:
        other_branch = first_branch
        x_branch = second_branch
    result = (other_branch.b - x_branch.b)/x_branch.a
    return int(result)


def solve_file(fname):
    data = read_file(fname)
    p1 = int(data[ROOT].calc(data))
    p2 = find_what_to_yell(data)
    return p1, p2


class TestDay(unittest.TestCase):

    def test_parse_monkey(self):
        self.assertEqual(
            parse_monkey("root: pppw + sjmn"),
            ("root", OperationMonkey("pppw", "+", "sjmn"))
        )
        self.assertEqual(parse_monkey("dbpl: 5"), ("dbpl", NumberMonkey(5)))

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (152, 301))


if __name__ == '__main__':
    print(solve_file("input.txt"))  # 3769668716709
    unittest.main()
