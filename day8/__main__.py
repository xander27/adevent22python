from os import path
import unittest


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return [list(map(int, line.rstrip())) for line in file]


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


def count_visible_from_outside(forest):
    rows = len(forest)
    cols = len(forest[0])
    bool_map = init_bool_map_by_size(rows, cols)

    for row, bool_row in zip(forest, bool_map):
        fill_bool_row(row, bool_row, 0, 1, cols, 1)
        fill_bool_row(row, bool_row, cols - 1, cols - 2, -1, -1)

    for col in range(0, cols):
        fill_bool_col(forest, bool_map, col, 0, 1, rows, 1)
        fill_bool_col(forest, bool_map, col, rows - 1, rows - 2, -1, -1)

    return count_bool_map(bool_map)


def count_bool_map(bool_map):
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


def score_tree(forest, rows, cols,  row_index, col_index):
    """There a lot of room for optimisation"""
    row = forest[row_index]
    cur_val = row[col_index]
    rows = len(forest)
    cols = len(row)

    score = score_tree_in_row(row, cur_val, col_index + 1, cols, 1)
    score = score * score_tree_in_row(row, cur_val, col_index - 1, -1, -1)
    score = score * \
        score_tree_in_col(forest, col_index, cur_val, row_index + 1, rows, 1)
    score = score * \
        score_tree_in_col(forest, col_index, cur_val, row_index - 1, -1, -1)

    return score


def score_tree_in_row(row, cur_val, begin, end, delta):
    for i, col_index in enumerate(range(begin, end, delta)):
        val = row[col_index]
        if val >= cur_val:
            return i + 1
    else:
        return i + 1


def score_tree_in_col(forest, col_index, cur_val, begin, end, delta):
    for i, row_index in enumerate(range(begin, end, delta)):
        val = forest[row_index][col_index]
        if val >= cur_val:
            return i + 1
    else:
        return i + 1


def max_score_tree(forest):
    rows = len(forest)
    cols = len(forest[0])
    return max((score_tree(forest, rows, cols, r, c) for c in range(1, cols-1) for r in range(1, rows-1)))


def solve_file(fname):
    forest = read_lines(fname)
    return (count_visible_from_outside(forest), max_score_tree(forest))


class TestDay(unittest.TestCase):

    FOREST = [
        "30373",
        "25512",
        "65332",
        "33549",
        "35390",
    ]

    def test_count_visible_from_outside(self):
        self.assertEqual(count_visible_from_outside(self.FOREST), 21)

    def test_score_tree(self):
        self.assertEqual(score_tree(self.FOREST, 5, 5, 1, 2), 4)
        self.assertEqual(score_tree(self.FOREST, 5, 5, 3, 2), 8)

    def test_max_score_tree(self):
        self.assertEqual(max_score_tree(self.FOREST), 8)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
