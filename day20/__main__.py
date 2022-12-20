

from os import path
import unittest


def read_numbers(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return list(map(int, file.read().split("\n")))

def positions_to_list(positions):
    result = [0] * len(positions)
    print(len(positions), max(positions.values()))
    for n, p in positions.items():
        result[p] = n
    return result

def reoder(numbers):
    length = len(numbers)
    positions = { n: i for i, n in enumerate(numbers) }
    print(positions_to_list(positions))
    for number in numbers:
        if number == 0: 
            continue
        cur_pos = positions[number]
        new_pos = cur_pos + number
        if number < 0:
            new_pos -= 1
        if new_pos > length:
            new_pos += 1
        new_pos = new_pos % length
        if new_pos > cur_pos:
            positions = { n: p - 1 if p > cur_pos and p <= new_pos else p for n, p in positions.items() }
        else:
            positions = { n: p + 1 if p < cur_pos and p >= new_pos else p for n, p in positions.items() }
        positions[number] = new_pos
        # print(positions_to_list(positions))
        # print(list(enumerate(positions_to_list(positions))))
    return positions_to_list(positions), positions
    
def solve(numbers):
    reordered, positions = reoder(numbers)
    p0 = positions[0]
    positions = [ (i * 1000 + p0) % len(positions) for i in range(1, 4) ]
    return sum(reordered[p] for p in positions)

def solve_file(fname):
    numbers = read_numbers(fname)
    return solve(numbers)

class TestDay(unittest.TestCase):

    NUMBERS = [1, 2, -3, 3, -2, 0, 4]

    def test_reorder(self):
        self.assertSequenceEqual(reoder(self.NUMBERS)[0], [1, 2, -3, 4, 0, 3, -2])

    def test_sovlve(self):
        self.assertEqual(solve(self.NUMBERS), 3)
    
if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()


[1, 2, -3, 3, -2, 0, 4] # 1, 2, -3, 3, -2, 0, 4 +
[2, 1, -3, 3, -2, 0, 4] # 2, 1, -3, 3, -2, 0, 4 # 1 moves between 2 and -3: +
[1, -3, 2, 3, -2, 0, 4] # 1, -3, 2, 3, -2, 0, 4 # 2 moves between -3 and 3: +
[1, 2, 3, -2, -3, 0, 4] # 1, 2, 3, -2, -3, 0, 4 # -3 moves between -2 and 0 + 
[1, 2, -2, -3, 0, 3, 4] # 1, 2, -2, -3, 0, 3, 4 # 3 moves between 0 and 4:
[1, 2, -3, 0, 3, 4, -2] # 1, 2, -3, 0, 3, 4, -2 # -2 moves between 4 and 1:
[1, 2, 4, -3, 0, 3, -2] # 4 moves between -3 and 0:









# 0 does not move:
# 1, 2, -3, 0, 3, 4, -2


# 1, 2, -3, 4, 0, 3, -2