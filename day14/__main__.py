
from dataclasses import dataclass
from os import path
import unittest

START = (500, 0)

@dataclass
class Map():
    data: list[list[str]]
    max_x: int
    max_y: int

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.data = []
        for _ in range(max_x + 1):
            self.data.append(['.'] * (max_y+1))

    def __getitem__(self, key):
        return self.data[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.data[key[0]][key[1]] = value

    def draw(self, offset):
        for r in range(self.max_y):
            for c in range(offset, self.max_x):
                print(self.data[c][r], end="")
            print()

def simulate_sand_falling(map):
    i = 0
    while True:
        if simulate_sand_path(map):
            return i
        i+=1

def simulate_sand_path(map):
    point = START
    while True:   
        if point is None:
            return False
        if point[1] == map.max_y:
            return True
        point = similate_sand_move(map, point[0], point[1])


def similate_sand_move(map, x, y):
    if map[x, y + 1]  == '.':
        return x, y + 1
    if x > 0 and map[x - 1, y + 1]  == '.':
        return x - 1, y + 1
    if x < map.max_x and map[x + 1, y + 1]  == '.':
        return x + 1, y + 1
    map[x, y] = 'O'
    return None

def read_commands(fname):
    result = []
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            command = line.split("->")
            way = []
            for point in command:
                parts = point.split(",")
                way.append((int(parts[0].strip()), int(parts[1].strip())))
            result.append(way)
    return result


def init_empty_map(commands):
    max_x = 0
    max_y = 0
    for command in commands:
        for point in command:
            if point[0] > max_x:
                max_x = point[0]
            if point[1] > max_y:
                max_y = point[1]
    return Map(max_x, max_y + 2)


def draw_line(map, p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        begin, end = (y1, y2) if y2 > y1 else (y2, y1)
        for y in range(begin, end+1):
            map[x1, y] = '#'
    elif y1 == y2:
        begin, end = (x1, x2) if x2 > x1 else (x2, x1)
        for x in range(begin, end+1):
            map[x,y1] = '#'
    else:
        raise BaseException(f"Invalid line {p1}->{p2}")


def apply_commands(map, commands):
    for command in commands:
        for p1, p2 in zip(command, command[1:]):
            draw_line(map, p1, p2)


def init_map(commands):
    map = init_empty_map(commands)
    apply_commands(map, commands)
    return map


def score_file(fname):
    commands = read_commands(fname)
    map = init_map(commands)
    return simulate_sand_falling(map)


class TestDay(unittest.TestCase):

    COMMANDS = [
        [(498, 4), (498, 6), (496, 6)],
        [(503, 4), (502, 4), (502, 9), (494, 9)]
    ]

    def test_read_commands(self):
        self.assertEqual(read_commands("input-test.txt"), self.COMMANDS)

    def test_simulate_sand(self):
        map = init_map(self.COMMANDS)
        self.assertEqual(simulate_sand_falling(map), 24)


if __name__ == '__main__':
    print(score_file("input.txt"))
    unittest.main()
