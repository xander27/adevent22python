
from os import path
import unittest


def parse_point(string):
    coords = [int(s) for s in string.split(",")]
    return coords[0], coords[1], coords[2]


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


def count_out_surface(points):
    return 6 * len(points) - count_connections(points)


def get_neighbors(point):
    return (
        (point[0] + 1, point[1], point[2]),
        (point[0] - 1, point[1], point[2]),
        (point[0], point[1] + 1, point[2]),
        (point[0], point[1] - 1, point[2]),
        (point[0], point[1], point[2] + 1),
        (point[0], point[1], point[2] - 1),
    )


def visit(start, marked, points, maxs):
    stack = [start]
    while len(stack) > 0:
        cur = stack.pop()
        invalid = False
        for dems in range(3):
            if cur[dems] < 0 or cur[dems] > maxs[dems]:
                invalid = True
                break
        if invalid or cur in points or cur in marked:
            continue
        marked.add(cur)
        stack.extend(get_neighbors(cur))


def get_surrounded(points):
    maxs = [max(p[i] for p in points) for i in range(3)]
    marked = set()
    visit((0, 0, 0), marked, points, maxs)
    result = []
    for i in range(maxs[0] + 1):
        for j in range(maxs[1] + 1):
            for k in range(maxs[2] + 1):
                p = (i, j, k)
                if p in marked or p in points:
                    continue
                result.append(p)
    return result


def count_in_surface(points):
    surrounded = get_surrounded(points)
    return count_out_surface(surrounded)


def solve_file(fname):
    points = read_points(fname)
    out_surface = count_out_surface(points)
    in_surface = count_in_surface(points)
    return out_surface, out_surface - in_surface


class TestDay(unittest.TestCase):

    POINTS = [
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5)
    ]

    def test_read_points(self):
        self.assertEqual(read_points("input-test.txt"), self.POINTS)

    def test_is_connected(self):
        self.assertTrue(is_connected((2, 2, 2), (1, 2, 2)))
        self.assertTrue(is_connected((2, 2, 2), (3, 2, 2)))
        self.assertFalse(is_connected((1, 2, 2), (3, 2, 2)))

    def count_connections(self):
        points = [(1, 1, 1), (2, 1, 1), (1, 2, 1), (3, 3, 3)]
        self.assertEqual(count_connections(points), 4)

    def test_count_out_surface(self):
        self.assertEqual(count_out_surface(self.POINTS), 64)

    def test_count_in_surface(self):
        self.assertEqual(count_in_surface(self.POINTS), 6)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), (64, 58))

    def test_is_surrounded(self):
        actual = get_surrounded(self.POINTS)
        self.assertEqual(actual, [(2, 2, 5)])


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
