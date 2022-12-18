
from os import path
import unittest


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


def count_out_surface(points):
    return 6 * len(points) - count_connections(points)


def is_surrounded(p, sum_matrices, maxs):
    for d in range(3):
        mp = [maxs[d] if i == d else p[i] for i in range(3)]
        value = sum_matrices[d][p[0]][p[1]][p[2]]
        max_value = sum_matrices[d][mp[0]][mp[1]][mp[2]]
        if value == 0 or value >= max_value:
            return False

    return True


def get_neighbors(p):
    return (
        (p[0] + 1, p[1], p[2]),
        (p[0] - 1, p[1], p[2]),
        (p[0], p[1] + 1, p[2]),
        (p[0], p[1] - 1, p[2]),
        (p[0], p[1], p[2] + 1),
        (p[0], p[1], p[2] - 1),
    )

def visit(start, marked, points, maxs):
    stack = [start]
    while len(stack) > 0:
        cur = stack.pop()
        invalid = False
        for d in range(3):
            if cur[d] < 0 or cur[d] > maxs[d]:
                invalid = True
                break
        if invalid or cur in points or cur in marked:
            continue
        marked.add(cur)
        stack.extend(get_neighbors(cur))


def get_surrounded_3(points, maxs):
    marked = set()
    visit((0,0,0), marked, points, maxs)
    result = []
    for i in range(maxs[0] + 1):
        for j in range(maxs[1] + 1):
            for k in range(maxs[2] + 1):
                p = (i, j, k)
                if p in marked or p in points:
                    continue
                result.append(p)
    return result


def get_surrounded_2(points, maxs):
    surrounded = set()
    for i in range(maxs[0] + 1):
        for j in range(maxs[1] + 1):
            for k in range(maxs[2] + 1):
                p = (i, j, k)
                if p in points:
                    continue
                found = 0
                for neighbor in get_neighbors(p):
                    if neighbor in points or neighbor in surrounded:
                        found += 1
                if found == 6:
                    surrounded.add(p)
                if find(p, points, surrounded, maxs, set()):
                    surrounded.add(p)
    return surrounded


def find(cur, points, surrounded, maxs, visitied):
    if cur == (0, 0, 0):
        return False
    if cur in surrounded:
        return True
    for d in range(3):
        if cur[d] < 0 or cur[d] > maxs[d]:
            return None
    if cur in points or cur in visitied:
        return None
    visitied.add(cur)
    # for neighbor in get_neighbors(cur):
    #     r = find(neighbor, points, surrounded, maxs, visitied):
    #     if r is not None:
    #         return r
    return None


def create_empty_matrix(maxs):
    d0 = []
    for i in range(maxs[0] + 1):
        d1 = []
        d0.append(d1)
        for j in range(maxs[1] + 1):
            d2 = []
            d1.append(d2)
            for k in range(maxs[2] + 1):
                d2.append(0)
    return d0


def get_maxs(points):
    return [max(p[i] for p in points) for i in range(3)]


def create_sum_matricies(points, maxs):

    matricies = [
        create_empty_matrix(maxs),
        create_empty_matrix(maxs),
        create_empty_matrix(maxs)
    ]

    for p in points:
        for x in range(p[0], maxs[0]+1):
            matricies[0][x][p[1]][p[2]] = matricies[0][x][p[1]][p[2]] + 1
        for x in range(p[1], maxs[1]+1):
            matricies[1][p[0]][x][p[2]] = matricies[1][p[0]][x][p[2]] + 1
        for x in range(p[2], maxs[2]+1):
            matricies[2][p[0]][p[1]][x] = matricies[2][p[0]][p[1]][x] + 1

    return matricies


def count_in_surface(points):
    maxs = get_maxs(points)
    matrices = create_sum_matricies(points, maxs)
    surrounded_points = []
    for i in range(maxs[0] + 1):
        for j in range(maxs[1] + 1):
            for k in range(maxs[2] + 1):
                point = (i, j, k)
                if point in points:
                    continue
                if is_surrounded(point, matrices, maxs):
                    surrounded_points.append(point)
    return count_out_surface(surrounded_points)

def count_in_surface2(points):
    maxs = get_maxs(points)
    surrounded = get_surrounded_3(points, maxs)
    return count_out_surface(surrounded)


def solve_file(fname):
    points = read_points(fname)
    out_surface = count_out_surface(points)
    in_surface = count_in_surface2(points)
    return (out_surface, out_surface - in_surface)


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

    def test_create_sum_matrix(self):
        expected = [
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        ]
        actual = create_empty_matrix([2, 3, 4])
        self.assertEqual(actual, expected)

    def test_issurouneded(self):
        maxs = get_maxs(self.POINTS)
        m = create_sum_matricies(self.POINTS, maxs)
        for i in range(maxs[0]+1):
            for j in range(maxs[1]+1):
                for k in range(maxs[2]+1):
                    point = (i, j, k)
                    if point in self.POINTS:
                        continue
                    expected = point == (2, 2, 5)
                    self.assertEqual(is_surrounded(point, m, maxs), expected)

    def test_is_surrounded2(self):
        maxs = get_maxs(self.POINTS)
        actual = get_surrounded_3(self.POINTS, maxs)
        self.assertEqual(actual, [(2, 2, 5)])


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
