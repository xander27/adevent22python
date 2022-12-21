

from dataclasses import dataclass
from os import path
import unittest


@dataclass
class NumberMonkey():
    value: int

    def calc(self, data):
        return self.value


@dataclass
class OperationMonkey():
    first: str
    operation: str
    second: str
    value: int = None

    def calc(self, data):
        if self.value is None:
            first_value = data[self.first].calc(data)
            second_value = data[self.second].calc(data)
            if self.operation == "*":
                self.value = first_value * second_value
            elif self.operation == "/":
                self.value = first_value // second_value
            elif self.operation == "+":
                self.value = first_value + second_value
            elif self.operation == "-":
                self.value = first_value - second_value
            else:
                raise BaseException(f"Unknown operation {self.operation}")
        return self.value


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

def solve_file(fname):
    data = read_file(fname)
    return data["root"].calc(data)

class TestDay(unittest.TestCase):

    def test_parse_monkey(self):
        self.assertEqual(
            parse_monkey("root: pppw + sjmn"),
            ("root", OperationMonkey("pppw", "+", "sjmn"))
        )
        self.assertEqual(parse_monkey("dbpl: 5"), ("dbpl", NumberMonkey(5)))

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 152)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
