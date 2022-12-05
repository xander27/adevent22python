from dataclasses import dataclass
from functools import reduce
from itertools import chain
from os import path
import unittest


class LimitedSortedList:
    """The first elment is the max"""

    def __init__(self, limit):
        self.limit = limit
        self.elements = []

    def append(self, element):
        inserted = False
        for i, other in enumerate(self.elements):
            if element > other:
                self.elements.insert(i, element)
                inserted = True
                break

        if inserted:
            self.elements = self.elements[0:self.limit]
        elif len(self.elements) < self.limit:
            self.elements.append(element)


@dataclass
class State:
    top3: LimitedSortedList
    cur_sum: int

    def apply(self, element):
        if element is None:
            self.top3.append(self.cur_sum)
            return State(self.top3, 0)
        return State(self.top3, self.cur_sum + element)


def read_data(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            if len(line) > 0:
                yield int(line)
            else:
                yield None


def solve(data):
    init = State(LimitedSortedList(3), 0)
    elements = chain(data, [None])
    result = reduce(lambda s, e: s.apply(e), elements, init)
    top3 = result.top3.elements
    return (top3[0], sum(top3))


def solve_file(fname):
    return solve(read_data(fname))


class TestLimitedSortedList(unittest.TestCase):

    def test_append_to_empty(self):
        self._do_test([1], 1)

    def test_apend_dsc(self):
        self._do_test([5, 4, 3], 5, 4, 3, 2, 1)

    def test_apend_asc(self):
        self._do_test([5, 4, 3], 1, 2, 3, 4, 5)

    def test_apend_random(self):
        self._do_test([10, 5, 5], 1, 5, 4, 4, 5, 3, 10, 1, 2)

    def _do_test(self, expected, *vargs):
        sample = LimitedSortedList(3)
        for x in vargs:
            sample.append(x)
        self.assertEqual(sample.elements, expected)


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
        self.assertEqual(solve(data), (24000, 45000))

    def test_solve_file(self):
        data = read_data("input-test.txt")
        self.assertEqual(solve(data), (24000, 45000))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
