from os import path
import unittest


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line.rstrip()


def init_bool_map_by_size(rows, cols):
    result = []
    result.append([True] * cols)
    for _ in range(rows - 2):
        line = []
        line.append(True)
        line.extend([False] * (cols-2))
        line.append(True)
        result.append(line)
    result.append([True] * cols)
    return result


def solve(forest):
    rows = len(forest)
    cols = len(forest[0])
    bool_map = init_bool_map_by_size(rows, cols)

    for row, bool_row in zip(forest, bool_map):
        fill_bool_row(row, bool_row, 0, 1, cols, 1)
        fill_bool_row(row, bool_row, cols - 1, cols - 2, -1, -1)

    for col in range(0, cols):
        fill_bool_col(forest, bool_map, col, 0, 1, rows, 1)
        fill_bool_col(forest, bool_map, col, rows - 1, rows - 2, -1, -1)

    return sum((sum(row) for row in bool_map))


def fill_bool_row(row, bool_row, first_pos, begin, end, delta):
    max_h = row[first_pos]
    for i in range(begin, end, delta):
        cur = row[i]
        if cur > max_h:
            max_h = cur
            bool_row[i] = True


def fill_bool_col(forest, bool_map, col, first_pos, begin, end, delta):
    max_h = forest[first_pos][col]
    for i in range(begin, end, delta):
        cur = forest[i][col]
        if cur > max_h:
            max_h = cur
            bool_map[i][col] = True


def solve_file(fname):
    forest = list(read_lines(fname))
    return solve(forest)


class TestDay(unittest.TestCase):

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 21)

if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()