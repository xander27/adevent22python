
import inspect
from os import path
import unittest
from enum import Enum


class Figure(Enum):
    DASH = (["@@@@"])
    PLUS = (
        [
            " @ ",
            "@@@",
            " @ "
        ]
    ),
    ANGLE = (
        [
            "@@@",
            "  @",
            "  @"
        ]
    ),
    PILONE = ["@", "@", "@", "@"]
    SQUARE = (
        [
            "@@",
            "@@"
        ]
    )

    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])

    @staticmethod
    def all():
        return [f for f in Figure]


class Game():
    COLS = 7
    START_OFFSET = 3
    EMPTY_LINE = [' '] * COLS
    """Represents the game field. Coordinates [row, column]. First row is initial floor."""

    def __init__(self, wind_pattern):
        self.data = []
        self.top_poistion = 0
        self._wind_pattern = wind_pattern
        self._wind_postition = 0

    def __str__(self):
        lines = []
        for row in self.data[::-1]:
            lines.append("|" + "".join(row) + '|')
        lines.append('+' + '-' * self.COLS + '+')
        return "\n".join(lines)

    def add(self, figure):
        """Figure is array of strings"""

        figure_left = 2
        figure_bottom = self.top_poistion + self.START_OFFSET
        figure_top = figure_bottom + figure.height

        need_add = figure_top - len(self.data)
        for _ in range(need_add):
            self.data.append(self.EMPTY_LINE.copy())

        while True:
            wind = self._wind_pattern[self._wind_postition % len(self._wind_pattern)]
            self._wind_postition += 1
            offset = 1 if wind == ">" else -1
            if self._can_move(figure, figure_left, figure_bottom, offset):
                figure_left += offset
            if self._can_fall(figure, figure_left, figure_bottom):
                figure_bottom -= 1
            else:
                break
        self._add_figure(figure, figure_left, figure_bottom)
        self.top_poistion = max(
            self.top_poistion, figure_bottom + figure.height)

    def _add_figure(self, figure, left, bottom):
        for col in range(figure.width):
            data_column = left + col
            for row in range(figure.height):
                if figure.data[row][col] == ' ':
                    continue
                data_row = bottom + row
                self.data[data_row][data_column] = '#'

    def _can_move(self, figure, left, bottom, offset):
        new_left = left + offset
        if new_left < 0 or new_left + figure.width > self.COLS:
            return False
        for col in range(figure.width):
            data_column = new_left + col
            for row in range(figure.height):
                if figure.data[row][col] == ' ':
                    continue
                data_row = bottom + row
                if self.data[data_row][data_column] != ' ':
                    return False
        return True

    def _can_fall(self, figure, left, bottom):
        new_bottom = bottom - 1
        if new_bottom < 0:
            return False
        for col in range(figure.width):
            data_column = left + col
            for row in range(figure.height):
                if figure.data[row][col] == ' ':
                    continue
                data_row = new_bottom + row
                if self.data[data_row][data_column] != ' ':
                    return False
        return True

def solve(wind_pattern, turns):
    game = Game(wind_pattern)
    figures = Figure.all()
    for i in range(turns):
         game.add(figures[i % len(figures)])
    # print(game)
    return game.top_poistion

def solve_file(fname, turns):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        wind_pattern = file.read().strip()
    return solve(wind_pattern, turns)

class TestDay(unittest.TestCase):

    WIND_PATTERN = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

    def test_add_figure(self):
        expected = """
        |       |
        |       |
        |       |
        |       |
        |    ## |
        |    ## |
        |    #  |
        |  # #  |
        |  # #  |
        |#####  |
        |  ###  |
        |   #   |
        |  #### |
        +-------+"""
        expected = inspect.cleandoc(expected)
        game = Game(self.WIND_PATTERN)
        for figure in Figure:
            game.add(figure)
        self.assertEqual(str(game), expected)

    def test_solve(self):
        self.assertEqual(solve(self.WIND_PATTERN, 2022), 3068)
        # self.assertEqual(solve(self.WIND_PATTERN, 1000000000000), 1000000000000)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt", 2022), 3068)
        # self.assertEqual(solve_file("input-test.txt", 1000000000000), 1000000000000)


if __name__ == '__main__':
    print(solve_file("input.txt", 2022))
    # print(solve_file("input.txt", 1000000000000))
    unittest.main()
