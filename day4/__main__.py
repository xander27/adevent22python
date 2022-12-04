from dataclasses import dataclass
import unittest


@dataclass
class Range:
    begin: int
    end: int

    def __include(self, other):
        return self.begin <= other.begin and self.end >= other.end

    def include_or_included_by(self, other):
        return self.__include(other) or other.__include(self)


def read_pairs(fname):
    with open(fname) as file:
        for s in file:
            yield line_to_pair(s)


def line_to_pair(line):
    first, second = line.split(",")
    return (range_from_string(first), range_from_string(second))


def range_from_string(s):
    begin, end = map(int, s.split("-"))
    return Range(begin, end)


def score_file(fname):
    return sum(1 for p in read_pairs(fname) if p[0].include_or_included_by(p[1]))


class TestDay(unittest.TestCase):

    def test_range_from_string(self):
        self.assertEqual(range_from_string("2-4"), Range(2, 4))

    def test_line_to_pair(self):
        self.assertEqual(line_to_pair("2-4,6-8"), (Range(2, 4), Range(6, 8)))

    def test_include_or_included_by(self):
        self.assert_include_or_included_by_both_ways(
            Range(2, 4), Range(6, 8), False)
        self.assert_include_or_included_by_both_ways(
            Range(2, 7), Range(7, 9), False)
        self.assert_include_or_included_by_both_ways(
            Range(6, 6), Range(4, 6), True)
        self.assert_include_or_included_by_both_ways(
            Range(2, 8), Range(3, 7), True)

    def assert_include_or_included_by_both_ways(self, a, b, expected):
        self.assertEqual(a.include_or_included_by(b), expected)
        self.assertEqual(b.include_or_included_by(a), expected)

    def test_read_pairs(self):
        expected = [
            (Range(2, 4), Range(6, 8)),
            (Range(2, 3), Range(4, 5)),
            (Range(5, 7), Range(7, 9)),
            (Range(2, 8), Range(3, 7)),
            (Range(6, 6), Range(4, 6)),
            (Range(2, 6), Range(4, 8))
        ]
        self.assertEqual(list(read_pairs("input-test.txt")), expected)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), 2)


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
