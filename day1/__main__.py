import unittest


def read_data(fname):
    with open(fname) as file:
        for s in file:
            s = s.rstrip()
            if len(s) > 0:
                yield int(s)
            else:
                yield None


def solve(data):
    max = 0
    cur_sum = 0
    for x in data:
        if x == None:
            if cur_sum > max:
                max = cur_sum
            cur_sum = 0
        else:
            cur_sum = cur_sum + x
    return max


def solve_file(fname):
    return solve(read_data(fname))


class TestDay(unittest.TestCase):

    def test_read_data(self):
        actual = list(read_data("input-test.txt"))
        self.assertEqual(
            actual,
            [1000, 2000, 3000, None, 4000, None, 5000,
                6000, None, 7000, 8000, 9000, None, 10000]
        )

    def test_solve(self):
        data = [1000, 2000, 3000, None, 4000, None, 5000,
                6000, None, 7000, 8000, 9000, None, 10000]
        self.assertEqual(solve(data), 24000)


    def test_solve_file(self):
        data = read_data("input-test.txt")
        self.assertEqual(solve(data), 24000)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
