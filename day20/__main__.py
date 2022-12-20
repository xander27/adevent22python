

from os import path
import unittest

VALUE = 1

KEY = 811589153

def read_numbers(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return list(map(int, file.read().split("\n")))

def reoder(numbers, times):
    length = len(numbers)
    original_by_index = list(enumerate(numbers))
    result = original_by_index.copy()
    for _ in range(times):
        for original_pair in original_by_index:
            current_pos = result.index(original_pair)
            new_pos = (current_pos + original_pair[VALUE]) % (length - 1)
            if new_pos == 0:
                new_pos = length
            del result[current_pos]
            result.insert(new_pos, original_pair)
    return list(map(lambda p: p[VALUE], result))
    
def solve(numbers, mult, times):
    numbers = list(map(lambda x: x * mult, numbers))
    numbers = reoder(numbers, times)
    p0 = -1
    for i, n in enumerate(numbers):
        if n == 0:
            p0 = i
            break
    positions = [ (i * 1000 + p0) % len(numbers) for i in range(1, 4) ]
    return sum(numbers[p] for p in positions)

def solve_file(fname):
    numbers = read_numbers(fname)
    return (solve(numbers, 1, 1), solve(numbers, KEY, 10))

class TestDay(unittest.TestCase):

    NUMBERS = [1, 2, -3, 3, -2, 0, 4]

    def test_reorder(self):
        self.assertSequenceEqual(reoder(self.NUMBERS, 1), [1, 2, -3, 4, 0, 3, -2])

    def test_sovlve(self):
        self.assertEqual(solve(self.NUMBERS, 1, 1), 3)
        self.assertEqual(solve(self.NUMBERS, KEY, 10), 1623178306)
    
if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()