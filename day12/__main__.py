
from dataclasses import dataclass
from os import path
import unittest

BASE_ORD = ord('a')
START_CHAR = 'S'
END_CHAR = 'E'
MAX_HEIGHT = ord('z') - BASE_ORD


@dataclass
class MapGraph():
    heights: list[list[int]]
    start: tuple[int, int]
    end: tuple[int, int]
    rows: int
    cols: int

    def __init__(self, heights, start, end):
        self.heights = heights
        self.start = start
        self.end = end
        self.rows = len(heights)
        self.cols = len(heights[0])


    def can_go(self, from_point, to_point):
        from_height = self.heights[from_point[0]][from_point[1]]
        to_height = self.heights[to_point[0]][to_point[1]]
        return to_height <= from_height + 1


def parse_map_graph(lines):
    heights = []
    start = None
    end = None

    for i, line in enumerate(lines):
        heights_line = []
        for j, char in enumerate(line):
            if char == START_CHAR:
                heights_line.append(0)
                start = (i, j)
            elif char == END_CHAR:
                heights_line.append(MAX_HEIGHT)
                end = (i, j)
            else:
                heights_line.append(ord(char) - BASE_ORD)
        heights.append(heights_line)

    return MapGraph(heights, start, end)

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
        if graph.end == pointer:
            for g in graph.heights:
                print(g)
            print("=====")
            for d in distance:
                print(d)
            return cur_dist
        to_go = find_points_to_go(pointer, graph, complete, distance)
        for other in to_go:
            if distance[other[0]][other[1]] > cur_dist + 1:
                distance[other[0]][other[1]] = cur_dist + 1
        complete[pointer[0]][pointer[1]] = True
        todo.update(to_go)
    
    raise BaseException("Can't find the way")

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

def read_map_graph(fname):
    return parse_map_graph(read_lines(fname))

def solve_file(fname):
    return find_way(read_map_graph(fname))

class TestDay(unittest.TestCase):

    MAP_GRAPH = MapGraph(
        heights=[
            [0, 0, 1, 16, 15, 14, 13, 12],
            [0, 1, 2, 17, 24, 23, 23, 11],
            [0, 2, 2, 18, 25, 25, 23, 10],
            [0, 2, 2, 19, 20, 21, 22, 9],
            [0, 1, 3, 4, 5, 6, 7, 8]
        ],
        start=(0, 0),
        end=(2,5)
    )

    def test_parse_map_graph(self):
        lines = [
            "Sabqponm",
            "abcryxxl",
            "accszExk",
            "acctuvwj",
            "abdefghi"
        ]
        self.assertEqual(parse_map_graph(lines), self.MAP_GRAPH)

    def test_read_map_graph(self):
        self.assertEqual(read_map_graph("input-test.txt"), self.MAP_GRAPH)

    def test_find_way(self):
        self.assertEqual(find_way(self.MAP_GRAPH), 31)

if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()