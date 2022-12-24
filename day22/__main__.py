from os import path
import unittest

SPACE = '.'
WALL = '#'
VOID = ' '
OFFSETS = ((0, 1), (1, 0), (0, -1), (-1, 0))
ARROWS = ['>', 'V', '<', '^']

RIGHT = 0
DOWN = 1
LEFT = 2
TOP = 3


def parse_commands(line):
    result = []
    buffer = ''
    for char in line:
        if char == 'R' or char == 'L':
            if len(buffer) > 0:
                result.append(int(buffer))
                buffer = ''
            result.append(char)
        else:
            buffer += char
    if len(buffer) > 0:
        result.append(int(buffer))
    return result


def parse_map(lines):
    width = max(len(l) for l in lines)
    result = []
    for line in lines:
        missing_right = ' ' * (width - len(line))
        result.append(line + missing_right)
    return result


def find_start_col(field):
    for i, col in enumerate(field[0]):
        if col == '.':
            return i
    raise Exception("Start position not found")


def find_wrap(field, pos, angle):
    if angle == RIGHT:
        pos = (pos[0], 0)
    elif angle == LEFT:
        pos = (pos[0], len(field[0]) - 1)
    elif angle == DOWN:
        pos = (0, pos[1])
    else:
        pos = (len(field) - 1, pos[1])

    offset = OFFSETS[angle]
    while pos:
        if field[pos[0]][pos[1]] != VOID:
            return pos
        pos = (pos[0] + offset[0], pos[1] + offset[1])


def draw(field, way):
    tmp = []
    for line in field:
        tmp.append([c for c in line])
    for point in way:
        tmp[point[0][0]][point[0][1]] = ARROWS[point[1]]
    print("----------")
    for line in tmp:
        print("".join(line))
    print("----------")


def is_void(map, pos):
    if pos[0] < 0 or pos[0] >= len(map):
        return True
    if pos[1] < 0 or pos[1] >= len(map[0]):
        return True
    return map[pos[0]][pos[1]] == VOID


def move(field, pos, angle, distance, way):
    offset = OFFSETS[angle]
    for _ in range(distance):
        way.append((pos, angle))
        new = (pos[0] + offset[0], pos[1] + offset[1])
        if is_void(field, new):
            new = find_wrap(field, pos, angle)
        if field[new[0]][new[1]] == WALL:
            break
        pos = new
    return pos


def find_final_pos(field, commands):
    pos = (0, find_start_col(field))
    angle = RIGHT
    way = []
    for command in commands:
        if command == "R":
            angle = (angle + 1) % 4
        elif command == "L":
            angle = (angle - 1) % 4
        else:
            pos = move(field, pos, angle, command, way)
    # draw(map, path)
    return pos[0], pos[1], angle


def final_pos_to_code(pos_angle):
    return (pos_angle[0] + 1) * 1000 + (pos_angle[1] + 1) * 4 + pos_angle[2]


def solve(field, commands):
    return final_pos_to_code(find_final_pos(field, commands))


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def solve_file(fname):
    lines = read_lines(fname)
    field, commands = parse_map(lines[:-2]), parse_commands(lines[-1])
    return solve(field, commands)


class TestDay(unittest.TestCase):
    COMMANDS = [10, "R", 5, "L", 5, "R", 10, "L", 4, "R", 5, "L", 5]

    MAP = [
        "        ...#    ",
        "        .#..    ",
        "        #...    ",
        "        ....    ",
        "...#.......#    ",
        "........#...    ",
        "..#....#....    ",
        "..........#.    ",
        "        ...#....",
        "        .....#..",
        "        .#......",
        "        ......#.",
    ]

    def test_parse_commands(self):
        self.assertEqual(parse_commands("10R5L5R10L4R5L5"), self.COMMANDS)

    def test_parse_map(self):
        raw_input = [
            "        ...#",
            "        .#..",
            "        #...",
            "        ....",
            "...#.......#",
            "........#...",
            "..#....#....",
            "..........#.",
            "        ...#....",
            "        .....#..",
            "        .#......",
            "        ......#.",
        ]
        self.assertEqual(parse_map(raw_input), self.MAP)

    def test_find_start_col(self):
        self.assertEqual(find_start_col(self.MAP), 8)

    def test_find_final_pos(self):
        self.assertEqual(find_final_pos(
            self.MAP, self.COMMANDS), (5, 7, RIGHT))

    def test_solve(self):
        self.assertEqual(solve(self.MAP, self.COMMANDS), 6032)

    def test_solve_file(self):
        self.assertEqual(solve_file("input-test.txt"), 6032)


if __name__ == '__main__':
    print(solve_file("input.txt"))
    unittest.main()
