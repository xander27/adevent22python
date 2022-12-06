from os import path
import unittest

WINDOW_SIZE = 4

def windows(source, size):
    for i in range(len(source) - size + 1):
        begin, end = i,  i + size
        yield (begin, end, source[begin: end])

def solve(string):
    for _, end, window in windows(string, WINDOW_SIZE):
        if len(set(window)) == WINDOW_SIZE:
            return end
    raise BaseException("Start postion not found")

def read_string(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            return line

def solve_file(fname):
    string = read_string(fname)
    return solve(string)

class TestDay(unittest.TestCase):

    def test_window(self):
        source = "0123456789"
        exepcted = [
            (0,4,"0123"),
            (1,5,"1234"),
            (2,6,"2345"),
            (3,7,"3456"),
            (4,8,"4567"),
            (5,9,"5678"),
            (6,10,"6789")
        ]
        self.assertEqual(list(windows(source, WINDOW_SIZE)), exepcted)

    def test_solve(self):
        self.assertEqual(solve("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5)
        self.assertEqual(solve("nppdvjthqldpwncqszvftbrmjlhg"), 6)
        self.assertEqual(solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10)
        self.assertEqual(solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11)

if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()

