
from dataclasses import dataclass
from os import path
import unittest

BASE_ORD = ord('a')
START_CHAR = 'E'
END_CHAR = 'S'
MAX_HEIGHT = ord('z') - BASE_ORD


@dataclass
class MapGraph():
    heights: list[list[int]]
    start: tuple[int, int]
    ends: set[tuple[int, int]]
    rows: int
    cols: int

    def __init__(self, heights, start, ends):
        self.heights = heights
        self.start = start
        self.ends = ends
        self.rows = len(heights)
        self.cols = len(heights[0])


    def can_go(self, from_point, to_point):
        from_height = self.heights[from_point[0]][from_point[1]]
        to_height = self.heights[to_point[0]][to_point[1]]
        return to_height >= from_height - 1


def parse_map_graph(lines, many_ends):
    heights = []
    start = None
    ends = set()

    for i, line in enumerate(lines):
        heights_line = []
        for j, char in enumerate(line):
            if char == START_CHAR:
                heights_line.append(MAX_HEIGHT)
                start = (i, j)
            elif char == END_CHAR:
                heights_line.append(0)
                ends.add((i, j))
            else:
                height = ord(char) - BASE_ORD
                heights_line.append(height)
                if many_ends and height == 0:
                    ends.add((i, j))
        heights.append(heights_line)

    return MapGraph(heights, start, ends)

def find_way(graph):
    init_distance = graph.rows * graph.cols + 1
    distance = []
    complete = []
    for _ in range(graph.rows):
        distance.append([init_distance] * graph.cols)
        complete.append([False] * graph.cols)

    distance[graph.start[0]][graph.start[1]] = 0
    
    todo = set([graph.start])

    while len(todo) > 0:
        pointer = pop_next(todo, distance, init_distance)
        cur_dist = distance[pointer[0]][pointer[1]]
        to_go = find_points_to_go(pointer, graph, complete, distance)
        for other in to_go:
            if distance[other[0]][other[1]] > cur_dist + 1:
                distance[other[0]][other[1]] = cur_dist + 1
        complete[pointer[0]][pointer[1]] = True
        todo.update(to_go)

    return min(distance[e[0]][e[1]] for e in graph.ends)

def pop_next(todo, distance, init_distance):
    min_distance = init_distance
    result = None
    for point in todo:
        value = distance[point[0]][point[1]]
        if value < min_distance:
            min_distance = value
            result = point
    todo.remove(result)
    return result


def find_points_to_go(pointer, graph, complete, distance):
    result = []
    for (i, j) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        candidate = (pointer[0] + i, pointer[1] + j)
        if candidate[0] < 0 or candidate[0] >= graph.rows:
            continue
        if candidate[1] < 0 or candidate[1] >= graph.cols:
            continue
        if complete[candidate[0]][candidate[1]]:
            continue
        if not graph.can_go(pointer, candidate):
            continue
        result.append(candidate)
    result.sort(key = lambda p: distance[p[0]][p[1]])
    return result


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line.rstrip()

def solve_file(fname):
    lines = list(read_lines(fname))
    return (find_way(parse_map_graph(lines, False)), find_way(parse_map_graph(lines, True)))

class TestDay(unittest.TestCase):

    MAP_GRAPH_ONE_END = MapGraph(
        heights=[
            [0, 0, 1, 16, 15, 14, 13, 12],
            [0, 1, 2, 17, 24, 23, 23, 11],
            [0, 2, 2, 18, 25, 25, 23, 10],
            [0, 2, 2, 19, 20, 21, 22, 9],
            [0, 1, 3, 4, 5, 6, 7, 8]
        ],
        start=(2, 5),
        ends=set([(0,0)])
    )

    MAP_GRAPH_MANY_ENDS = MapGraph(
        heights=[
            [0, 0, 1, 16, 15, 14, 13, 12],
            [0, 1, 2, 17, 24, 23, 23, 11],
            [0, 2, 2, 18, 25, 25, 23, 10],
            [0, 2, 2, 19, 20, 21, 22, 9],
            [0, 1, 3, 4, 5, 6, 7, 8]
        ],
        start=(2, 5),
        ends=set([(0,0), (0,1), (1,0), (2,0), (3,0), (4, 0)])
    )

    def test_parse_map_graph(self):
        lines = [
            "Sabqponm",
            "abcryxxl",
            "accszExk",
            "acctuvwj",
            "abdefghi"
        ]
        self.assertEqual(parse_map_graph(lines, False), self.MAP_GRAPH_ONE_END)
        self.assertEqual(parse_map_graph(lines, True), self.MAP_GRAPH_MANY_ENDS)

    def test_find_way(self):
        self.assertEqual(find_way(self.MAP_GRAPH_ONE_END), 31)
        self.assertEqual(find_way(self.MAP_GRAPH_MANY_ENDS), 29)

if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()