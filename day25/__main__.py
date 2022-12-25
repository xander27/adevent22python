import unittest
from dataclasses import dataclass
from os import path

DIGIT_MAPPING = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
INVERSE_MAPPING = {2: "2", 1: "1", 0: "0", -1: "-", -2: "="}


@dataclass
class SnafuNumber:
    digits: [int]

    @staticmethod
    def parse(string):
        return SnafuNumber([DIGIT_MAPPING[c] for c in string[::-1]])

    def __add__(self, other):
        result_digits = []

        a, b = self.digits.copy(), other.digits.copy()
        while len(a) < len(b):
            a.append(0)
        while len(b) < len(a):
            b.append(0)
        carry = 0
        for x, y in zip(a, b):
            s = x + y + carry
            if -2 <= s <= 2:
                cur = s
                carry = 0
            elif s > 2:
                cur = s - 5
                carry = 1
            else:
                cur = s + 5
                carry = -1

            result_digits.append(cur)

        if carry != 0:
            result_digits.append(carry)
        result = SnafuNumber(result_digits)
        if self.to_normal() + other.to_normal() != result.to_normal():
            raise Exception(f"{self.to_normal()} + {other.to_normal()} = {result.to_normal()}")
        return result

    def __str__(self):
        return "".join(INVERSE_MAPPING[d] for d in self.digits[::-1])

    def __repr__(self):
        return f"Snafu:{str(self)}"

    def to_normal(self):
        powers = get_powers(50)
        return sum(power * digit for power, digit in zip(powers, self.digits))


def get_powers(num):
    result = []
    cur = 1
    for i in range(num):
        result.append(cur)
        cur *= 5
    return result


def to_normal(powers, string):
    return sum(power * DIGIT_MAPPING[digit] for power, digit in zip(powers, string[::-1]))


def solve_file(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    total = SnafuNumber.parse("0")
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file.read().split("\n"):
            total = total + SnafuNumber.parse(line)
    return str(total)


class TestDay(unittest.TestCase):
    POWERS = get_powers(30)

    def test_add(self):
        # 3 + 4 = 7
        self.assertEqual(SnafuNumber.parse("1=") + SnafuNumber.parse("1-"), SnafuNumber.parse("12"))
        # 33 + 4 = 37
        self.assertEqual(SnafuNumber.parse("12=") + SnafuNumber.parse("1-"), SnafuNumber.parse("122"))

    def test_to_normal(self):
        self.assertEqual(SnafuNumber.parse("1=-0-2").to_normal(), 1747)
        self.assertEqual(SnafuNumber.parse("12111").to_normal(), 906)
        self.assertEqual(SnafuNumber.parse("2=0=").to_normal(), 198)
        self.assertEqual(SnafuNumber.parse("21").to_normal(), 11)
        self.assertEqual(SnafuNumber.parse("2=01").to_normal(), 201)
        self.assertEqual(SnafuNumber.parse("111").to_normal(), 31)
        self.assertEqual(SnafuNumber.parse("20012").to_normal(), 1257)
        self.assertEqual(SnafuNumber.parse("112").to_normal(), 32)
        self.assertEqual(SnafuNumber.parse("1=-1=").to_normal(), 353)
        self.assertEqual(SnafuNumber.parse("1-12").to_normal(), 107)
        self.assertEqual(SnafuNumber.parse("12").to_normal(), 7)
        self.assertEqual(SnafuNumber.parse("1=").to_normal(), 3)
        self.assertEqual(SnafuNumber.parse("122").to_normal(), 37)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), "2=-1=0")


if __name__ == '__main__':
    print(solve_file("input.txt"))  # 2=222-2---22=1=--1-2
    unittest.main()
