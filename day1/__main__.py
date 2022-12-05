from dataclasses import dataclass
from functools import reduce
import unittest


@dataclass
class State:
    max: int
    cur_sum: int

    def apply(self, element):
        if element is None:
            if self.cur_sum > self.max:
                return State(self.cur_sum, 0)
            else:
                return State(self.max, 0)
        else:
            return State(self.max, self.cur_sum + element)


def read_data(fname):
    with open(fname, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            if len(line) > 0:
                yield int(line)
            else:
                yield None


def solve(data):
    result = reduce(lambda s, e: s.apply(e), data, State(0, 0))
    result = result.apply(None)
    return result.max


def solve_file(fname):
    return solve(read_data(fname))


class TestDay(unittest.TestCase):

    def test_read_data(self):
        actual = list(read_data("input-test.txt"))
        self.assertEqual(
            actual,
            [1000, 2000, 3000, None, 4000, None, 5000,
                6000, None, 7000, 8000, 9000, None, 10000]
        )

    def test_solve(self):
        data = [1000, 2000, 3000, None, 4000, None, 5000,
                6000, None, 7000, 8000, 9000, None, 10000]
        self.assertEqual(solve(data), 24000)

    def test_solve_file(self):
        data = read_data("input-test.txt")
        self.assertEqual(solve(data), 24000)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
