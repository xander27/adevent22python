from os import path
import unittest

WINDOW_1 = 4
WINDOW_2 = 14


def windows(source, size):
    for i in range(len(source) - size + 1):
        begin, end = i, i + size
        yield begin, end, source[begin: end]


def solve(string, window_size):
    for _, end, window in windows(string, window_size):
        if len(set(window)) == window_size:
            return end
    raise Exception("Start position not found")


def read_string(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().strip()


def solve_file(fname, window_size):
    string = read_string(fname)
    return solve(string, window_size)


class TestDay(unittest.TestCase):

    def test_window(self):
        source = "0123456789"
        expected = [
            (0, 4, "0123"),
            (1, 5, "1234"),
            (2, 6, "2345"),
            (3, 7, "3456"),
            (4, 8, "4567"),
            (5, 9, "5678"),
            (6, 10, "6789")
        ]
        self.assertEqual(list(windows(source, WINDOW_1)), expected)

    def test_solve(self):
        self.assertEqual(solve("bvwbjplbgvbhsrlpgdmjqwftvncz", WINDOW_1), 5)
        self.assertEqual(solve("nppdvjthqldpwncqszvftbrmjlhg", WINDOW_1), 6)
        self.assertEqual(solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", WINDOW_1), 10)
        self.assertEqual(solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", WINDOW_1), 11)

        self.assertEqual(solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb", WINDOW_2), 19)
        self.assertEqual(solve("bvwbjplbgvbhsrlpgdmjqwftvncz", WINDOW_2), 23)
        self.assertEqual(solve("nppdvjthqldpwncqszvftbrmjlhg", WINDOW_2), 23)
        self.assertEqual(solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", WINDOW_2), 29)
        self.assertEqual(solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", WINDOW_2), 26)


if __name__ == '__main__':
    print(solve_file("input.txt", WINDOW_1))
    print(solve_file("input.txt", WINDOW_2))
    print("=====")
    unittest.main()
