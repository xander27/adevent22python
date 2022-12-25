from os import path
from enum import Enum
import unittest


class Outcome(Enum):
    WIN = ("Z", 6)
    DRAW = ("Y", 3)
    LOSE = ("X", 0)

    def __init__(self, code, points):
        super().__init__()
        self.code = code
        self.points = points

    @staticmethod
    def from_code(code):
        for outcome in Outcome:
            if outcome.code == code:
                return outcome
        raise Exception(f"Unknown code {code}")


class Shape(Enum):
    """
    Rock       A   X   1
    Paper      B   Y   2
    Scissors   C   Z   3
    """
    ROCK = ('A', 'X', 'Z', 1)
    PAPER = ('B', 'Y', 'X', 2)
    SCISSORS = ('C', 'Z', 'Y', 3)

    def __init__(self, opponent_code, my_code, defeats_code, score):
        self.opponent_code = opponent_code
        self.my_code = my_code
        self.defeats_code = defeats_code
        self.score = score

    @staticmethod
    def from_my_code(code):
        for shape in Shape:
            if shape.my_code == code:
                return shape
        raise Exception(f"Unknown my code {code}")

    @staticmethod
    def from_opponent_code(code):
        for shape in Shape:
            if shape.opponent_code == code:
                return shape
        raise Exception(f"Unknown opponent code {code}")

    def get_outcome(self, opponent_shape):
        if self == opponent_shape:
            return Outcome.DRAW
        if self.defeats_code == opponent_shape.my_code:
            return Outcome.WIN
        return Outcome.LOSE


def get_shape_from_opponent_code_and_outcome(opponent_shape, outcome):
    for shape in Shape:
        if shape.get_outcome(opponent_shape) == outcome:
            return shape
    raise Exception("Unexpected state")


def score_pair_part1(opponent_code, my_code):
    my_shape = Shape.from_my_code(my_code)
    opponent_shape = Shape.from_opponent_code(opponent_code)
    outcome = my_shape.get_outcome(opponent_shape)
    return my_shape.score + outcome.points


def score_pair_part2(opponent_code, outcome_code):
    opponent_shape = Shape.from_opponent_code(opponent_code)
    outcome = Outcome.from_code(outcome_code)
    my_shape = get_shape_from_opponent_code_and_outcome(
        opponent_shape, outcome)
    return my_shape.score + outcome.points


def score_part1(list_of_pairs):
    return sum(score_pair_part1(*p) for p in list_of_pairs)


def score_part2(list_of_pairs):
    return sum(score_pair_part2(*p) for p in list_of_pairs)


def read_paris(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for s in file:
            yield [s[0], s[2]]


def score_file(fname):
    pairs = list(read_paris(fname))
    return score_part1(pairs), score_part2(pairs)


class TestDay(unittest.TestCase):

    def test_shape_from_code_ok(self):
        self.assertEqual(Shape.ROCK, Shape.from_my_code("X"))
        self.assertEqual(Shape.PAPER, Shape.from_my_code("Y"))
        self.assertEqual(Shape.SCISSORS, Shape.from_my_code("Z"))

    def test_shape_from_code_unknown(self):
        with self.assertRaises(BaseException):
            Shape.from_my_code("A")

    def test_get_outcome(self):
        self.assertEqual(Shape.ROCK.get_outcome(Shape.ROCK), Outcome.DRAW)
        self.assertEqual(Shape.ROCK.get_outcome(Shape.PAPER), Outcome.LOSE)
        self.assertEqual(Shape.ROCK.get_outcome(Shape.SCISSORS), Outcome.WIN)

        self.assertEqual(Shape.PAPER.get_outcome(Shape.ROCK), Outcome.WIN)
        self.assertEqual(Shape.PAPER.get_outcome(Shape.PAPER), Outcome.DRAW)
        self.assertEqual(Shape.PAPER.get_outcome(
            Shape.SCISSORS), Outcome.LOSE)

        self.assertEqual(Shape.SCISSORS.get_outcome(Shape.ROCK), Outcome.LOSE)
        self.assertEqual(Shape.SCISSORS.get_outcome(Shape.PAPER), Outcome.WIN)
        self.assertEqual(Shape.SCISSORS.get_outcome(
            Shape.SCISSORS), Outcome.DRAW)

    def test_score_pair_part1(self):
        self.assertEqual(score_pair_part1("A", "Y"), 8)
        self.assertEqual(score_pair_part1("B", "X"), 1)
        self.assertEqual(score_pair_part1("C", "Z"), 6)

    def test_score_pair_part2(self):
        self.assertEqual(score_pair_part2("A", "Y"), 4)
        self.assertEqual(score_pair_part2("B", "X"), 1)
        self.assertEqual(score_pair_part2("C", "Z"), 7)

    def test_score_list_pairs_part1(self):
        given = [["A", "Y"], ["B", "X"], ["C", "Z"]]
        self.assertEqual(score_part1(given), 15)

    def test_score_list_pairs_part2(self):
        given = [["A", "Y"], ["B", "X"], ["C", "Z"]]
        self.assertEqual(score_part2(given), 12)

    def test_read_paris(self):
        expected = [["A", "Y"], ["B", "X"], ["C", "Z"]]
        actual = list(read_paris("input-test.txt"))
        self.assertEqual(actual, expected)

    def test_score_file(self):
        self.assertEqual(score_file("input-test.txt"), (15, 12))


if __name__ == '__main__':
    print(score_file("input.txt"))
    print("=====")
    unittest.main()
