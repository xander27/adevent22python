
from dataclasses import dataclass
from os import path
import unittest


# @dataclass
# class Point:
#     x: int
#     y: int
#     z: int
#     connected: set[tuple[int, int, int]]

#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.connected = set()

#     def possible_connections(self):
#         return set([
#             (self.x - 1, self.y, self.z),
#             (self.x + 1, self.y, self.z),
#             (self.x, self.y - 1, self.z),
#             (self.x, self.y + 1, self.z),
#             (self.x, self.y, self.z - 1),
#             (self.x, self.y, self.z + 1),
#         ])

def parse_point(string):
    coords = [int(s) for s in string.split(",")]
    return (coords[0], coords[1], coords[2])

def read_points(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return [parse_point(line.strip()) for line in file]

def is_connected(point_a, point_b):
    diff = [abs(x_a - x_b) for x_a, x_b in zip(point_a, point_b)]
    return sum(diff) == 1

def count_connections(points):
    connections = 0
    for i, point in enumerate(points):
        for other in points[i+1:]:
            if is_connected(point, other):
                connections += 2
    return connections

def solve(points):
    return 6 * len(points) - count_connections(points)

def solve_file(fname):
    points = read_points(fname)
    return solve(points)

class TestDay(unittest.TestCase):

    POINTS = [
        (2,2,2),
        (1,2,2),
        (3,2,2),
        (2,1,2),
        (2,3,2),
        (2,2,1),
        (2,2,3),
        (2,2,4),
        (2,2,6),
        (1,2,5),
        (3,2,5),
        (2,1,5),
        (2,3,5)
    ]

    def test_read_points(self):
        self.assertEqual(read_points("input-test.txt"), self.POINTS)

    def test_is_connected(self):
        self.assertTrue(is_connected((2,2,2), (1,2,2)))
        self.assertTrue(is_connected((2,2,2), (3,2,2)))
        self.assertFalse(is_connected((1,2,2), (3,2,2)))

    def count_connections(self):
        points = [(1,1,1), (2,1,1), (1,2,1), (3,3,3)]
        self.assertEqual(count_connections(points), 4)

    def test_solve(self):
        self.assertEqual(solve(self.POINTS), 64)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 64)

if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()