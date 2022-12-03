
from enum import Enum
import unittest


class Shape(Enum):
    """
    Rock       A   X   1
    Paper      B   Y   2
    Scissors   C   Z   3
    """
    ROCK = ('A', 'X', 'C', 1)
    PAPPER = ('B', 'Y', 'A', 2)
    SCISSORS = ('C', 'Z', 'B', 3)

    def __init__(self, opponent_code, my_code, wins_opponent_code, score):
        self.opponent_code = opponent_code
        self.my_code = my_code
        self.wins_opponent_code = wins_opponent_code
        self.score = score

    @staticmethod
    def from_my_code(code):
        for shape in Shape:
            if shape.my_code == code:
                return shape
        raise f"Unknown code {code}"


def score_for_outcome(opponent_code, my_shape):
    if my_shape.opponent_code == opponent_code:
        return 3
    if my_shape.wins_opponent_code == opponent_code:
        return 6
    return 0


def score_pair(opponent_code, my_code):
    my_shape = Shape.from_my_code(my_code)
    return my_shape.score + score_for_outcome(opponent_code, my_shape)


def score_pairs(list_of_pairs):
    return sum(score_pair(*p) for p in list_of_pairs)


def read_paris(fname):
    with open(fname) as file:
        for s in file:
            yield [s[0], s[2]]


def score_file(fname):
    return score_pairs(read_paris(fname))


class TestDay(unittest.TestCase):

    def test_shape_from_code_ok(self):
        self.assertEqual(Shape.ROCK, Shape.from_my_code("X"))
        self.assertEqual(Shape.PAPPER, Shape.from_my_code("Y"))
        self.assertEqual(Shape.SCISSORS, Shape.from_my_code("Z"))

    def test_shape_from_code_unkwnow(self):
        with self.assertRaises(BaseException):
            Shape.from_my_code("A")

    def test_score_for_outcome(self):
        self.assertEqual(score_for_outcome("A", Shape.ROCK), 3)
        self.assertEqual(score_for_outcome("A", Shape.PAPPER), 6)
        self.assertEqual(score_for_outcome("A", Shape.SCISSORS), 0)

        self.assertEqual(score_for_outcome("B", Shape.ROCK), 0)
        self.assertEqual(score_for_outcome("B", Shape.PAPPER), 3)
        self.assertEqual(score_for_outcome("B", Shape.SCISSORS), 6)

        self.assertEqual(score_for_outcome("C", Shape.ROCK), 6)
        self.assertEqual(score_for_outcome("C", Shape.PAPPER), 0)
        self.assertEqual(score_for_outcome("C", Shape.SCISSORS), 3)

    def test_score_pair(self):
        self.assertEqual(score_pair("A", "Y"), 8)
        self.assertEqual(score_pair("B", "X"), 1)
        self.assertEqual(score_pair("C", "Z"), 6)

    def test_score_list_pairs(self):
        given = [["A", "Y"], ["B", "X"], ["C", "Z"]]
        self.assertEqual(score_pairs(given), 15)

    def test_read_paris(self):
        expected = [["A", "Y"], ["B", "X"], ["C", "Z"]]
        actual = list(read_paris("input-test.txt"))
        self.assertEqual(actual, expected)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), 15)


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
