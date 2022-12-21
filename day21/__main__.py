

from dataclasses import dataclass
from os import path
import unittest

ROOT = "root"
ME = "humn"


@dataclass
class Fraction:
    top: int
    bottom: int

    def __init__(self, top, bottom):
        if top % bottom == 0:
            self.top = top // bottom
            self.bottom = 1
        else:
            self.top = top
            self.bottom = bottom

    def __add__(self, other):
        return Fraction(self.top * other.bottom + self.bottom * other.top, self.bottom * other.bottom)

    def __sub__(self, other):
        return Fraction(self.top * other.bottom - self.bottom * other.top, self.bottom * other.bottom)

    def __mul__(self, other):
        if isinstance(other, int):
            return Fraction(self.top * other, self.bottom)
        return Fraction(self.top * other.top, self.bottom * other.bottom)

    def __truediv__(self, other):
        return Fraction(self.top * other.bottom, self.bottom * other.top)

    def as_int(self):
        return self.top // self.bottom


@dataclass
class Effect:
    a: int
    b: int


@dataclass
class NumberMonkey():
    value: int

    def calc(self, data):
        return Fraction(self.value, 1)

    def get_effect(self, data, name):
        if name == ME:
            return Effect(Fraction(1, 1), Fraction(0, 1))
        return Effect(Fraction(0, 1), Fraction(self.value, 1))


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
                raise BaseException(f"Unknown operation {self.operation}")
        return self.value

    def get_effect(self, data, name):
        if self.effect is None:
            first = data[self.first].get_effect(data, self.first)
            second = data[self.second].get_effect(data, self.second)
            if self.operation == "+" or self.operation == "-":
                mul = 1 if self.operation == "+" else -1
                self.effect = Effect(first.a + second.a * mul, first.b + second.b * mul)
            elif self.operation == "*" or self.operation == "/":
                if first.a.top != 0 and second.a.top != 0:
                    raise BaseException(f"Cant do powers")
                if self.operation == "*":
                    if first.a.top != 0:
                        primary = first
                        secondary = second.b
                    else:
                        primary = second
                        secondary = first.b
                    self.effect = Effect(primary.a * secondary, primary.b * secondary)
                else:
                    if second.a.top != 0:
                        raise BaseException(f"Cant do powers")
                    self.effect = Effect(first.a / second.b, first.b / second.b)
            else:
                raise BaseException(f"Unknown operation {self.operation}")
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
    print(x_branch, other_branch)
    result = (other_branch.b - x_branch.b)/x_branch.a
    return result.as_int()


def solve_file(fname):
    data = read_file(fname)
    p1 = data[ROOT].calc(data).as_int()
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
    print(solve_file("input.txt")) # 3769668716709
    unittest.main()
