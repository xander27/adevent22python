from os import path
import unittest
import json


def parse_pocket(string):
    return json.loads(string)

def in_order(a, b):
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


def valid_positions_score(data):
    total = 0
    for i in range(len(data)//2):
        if in_order(data[i*2], data[i*2+1]):
            total = total + i + 1
    return total


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line.rstrip()


def read_data(fname):
    data = []
    for line in read_lines(fname):
        line = line.strip()
        if len(line) == 0:
            continue
        pocket = parse_pocket(line)
        data.append(pocket)
    return data

def find_decoder_key(data):
    first = [[2]]
    second = [[6]]
    index_first = 1
    index_second = 2
    for item in data:
        if in_order(item, first):
            index_first = index_first + 1
            index_second = index_second + 1
        elif in_order(item, second):
            index_second = index_second + 1
    return index_first * index_second


def solve_file(fname):
    data = read_data(fname)
    return valid_positions_score(data), find_decoder_key(data)


class TestDay(unittest.TestCase):

    DATA = [
           [1, 1, 3, 1, 1], [1, 1, 5, 1, 1],
           [[1], [2, 3, 4]], [[1], 4],
           [9], [[8, 7, 6]],
           [[4, 4], 4, 4], [[4, 4], 4, 4, 4],
           [7, 7, 7, 7], [7, 7, 7],
           [], [3],
           [[[]]], [[]],
           
              [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
              [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
           
        ]

    def test_parse_pocket(self):
        self.assertEqual(
            parse_pocket("[1,[2,[3,[4,[5,6,0]]]],8,9]"),
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        )

    def test_in_order(self):
        self.assertTrue(in_order(*self.DATA[0:2]))
        self.assertTrue(in_order(*self.DATA[2:4]))
        self.assertFalse(in_order(*self.DATA[4:6]))
        self.assertTrue(in_order(*self.DATA[6:8]))
        self.assertFalse(in_order(*self.DATA[8:10]))
        self.assertTrue(in_order(*self.DATA[10:12]))
        self.assertFalse(in_order(*self.DATA[12:14]))
        self.assertFalse(in_order(*self.DATA[14:16]))

    def valid_positions_score(self):
        self.assertEqual(valid_positions_score(self.DATA), 13)

    def test_find_decoder_key(self):
        self.assertEqual(find_decoder_key(self.DATA), 140)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (13, 140))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
