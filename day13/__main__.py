from os import path
import unittest
import json


def parse_pocket(string):
    return json.loads(string)

def is_valid(a, b):
    result = is_valid_step(a, b)
    return result is None or result


def is_valid_step(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return None
        return a < b

    if isinstance(a, int):
        a = [a]
    elif isinstance(b, int):
        b = [b]

    for x, y in zip(a, b):
        result = is_valid_step(x, y)
        if result == True:
            return True
        if result == False:
            return False
    return is_valid_step(len(a), len(b))


def solve(pairs):
    total = 0
    for i, pair in enumerate(pairs):
        if is_valid(*pair):
            total = total + i + 1
    return total


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line.rstrip()


def read_pairs(fname):
    pred = None
    for line in read_lines(fname):
        line = line.strip()
        if len(line) == 0:
            continue
        pocket = parse_pocket(line)
        if pred is None:
            pred = pocket
        else:
            yield (pred, pocket)
            pred = None


def solve_file(fname):
    pairs = read_pairs(fname)
    return solve(pairs)


class TestDay(unittest.TestCase):

    def test_parse_pocket(self):
        self.assertEqual(
            parse_pocket("[1,[2,[3,[4,[5,6,0]]]],8,9]"),
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        )

    def test_valid(self):
        self.assertTrue(is_valid([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]))
        self.assertTrue(is_valid([[1], [2, 3, 4]], [[1], 4]))
        self.assertFalse(is_valid([9], [[8, 7, 6]]))
        self.assertTrue(is_valid([[4, 4], 4, 4], [[4, 4], 4, 4, 4]))
        self.assertFalse(is_valid([7, 7, 7, 7], [7, 7, 7]))
        self.assertTrue(is_valid([], [3]))
        self.assertFalse(is_valid([[[]]], [[]]))
        self.assertFalse(
            is_valid(
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
            )
        )
        self.assertTrue(
            [[5], [1, [[0]]], [], [3, [[9, 1], [3, 4, 10], 8, 3], 6]],
            [[], [[6, 8], 4]]
        )

    def test_solve(self):
        pairs = [
            ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
            ([[1], [2, 3, 4]], [[1], 4]),
            ([9], [[8, 7, 6]]),
            ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
            ([7, 7, 7, 7], [7, 7, 7]),
            ([], [3]),
            ([[[]]], [[]]),
            (
                [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
            )
        ]
        self.assertEqual(solve(pairs), 13)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 13)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    # unittest.main()
