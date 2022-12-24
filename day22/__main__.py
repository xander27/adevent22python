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
CUBE_SIDE = 50
MAX_LOCAL = CUBE_SIDE - 1

# 21
# 3
# 54
# 6
SECTORS = {
    1: (0, 2),
    2: (0, 1),
    3: (1, 1),
    4: (2, 1),
    5: (2, 0),
    6: (3, 0)
}


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
    width = max(len(line) for line in lines)
    result = []
    for line in lines:
        missing_right = ' ' * (width - len(line))
        result.append(line + missing_right)
    return result


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
            return pos, angle
        pos = (pos[0] + offset[0], pos[1] + offset[1])


def in_sector(sector_id, local, angle):
    sector = SECTORS[sector_id]
    row, col = local
    row = CUBE_SIDE + row if row < 0 else row
    col = CUBE_SIDE + col if col < 0 else col
    return (sector[0] * CUBE_SIDE + row, sector[1] * CUBE_SIDE + col), angle


def wrap_p2(_, pos, angle):
    sector = (pos[0] // CUBE_SIDE, pos[1] // CUBE_SIDE)
    local = (pos[0] % CUBE_SIDE, pos[1] % CUBE_SIDE)

    if sector == SECTORS[1]:
        if angle == RIGHT:  # to 4 from right upsidedown
            return in_sector(4, (MAX_LOCAL - local[0], MAX_LOCAL), LEFT)
        if angle == DOWN:  # to 3 from right
            return in_sector(3, (local[1], MAX_LOCAL), LEFT)
        if angle == TOP:  # to 6 from bottom
            return in_sector(6, (MAX_LOCAL, local[1]), TOP)
    elif sector == SECTORS[2]:
        if angle == LEFT:  # to 5 from left upsidedown
            return in_sector(5, (MAX_LOCAL - local[0], 0), RIGHT)
        if angle == TOP:  # to 6 from left
            return in_sector(6, (local[1], 0), RIGHT)
    elif sector == SECTORS[3]:
        if angle == LEFT:  # TO 5 from top
            return in_sector(5, (0, local[0]), DOWN)
        if angle == RIGHT:  # To 1 from bottom
            return in_sector(1, (MAX_LOCAL, local[0]), TOP)
    elif sector == SECTORS[4]:
        if angle == RIGHT:  # to 1 from right upsidedown
            return in_sector(1, (MAX_LOCAL - local[0], MAX_LOCAL), LEFT)
        if angle == DOWN:  # to 6 from right
            return in_sector(6, (local[1], MAX_LOCAL), LEFT)
    elif sector == SECTORS[5]:
        if angle == TOP:  # to 3 from left
            return in_sector(3, (local[1], 0), RIGHT)
        if angle == LEFT:  # to 2 from left upsidedown
            return in_sector(2, (MAX_LOCAL - local[0], 0), RIGHT)
    elif sector == SECTORS[6]:
        if angle == RIGHT:  # to 4 from bottom
            return in_sector(4, (MAX_LOCAL, local[0]), TOP)
        if angle == DOWN:  # to 1 from top
            return in_sector(1, (0, local[1]), DOWN)
        if angle == LEFT:  # to 2 from top
            return in_sector(2, (0, local[0]), DOWN)

    raise Exception(f"Unexpected {pos} {sector}, {local}, {angle}")


def is_void(field, pos):
    if pos[0] < 0 or pos[0] >= len(field):
        return True
    if pos[1] < 0 or pos[1] >= len(field[0]):
        return True
    return field[pos[0]][pos[1]] == VOID


def move(field, pos, angle, distance, way, wrap_func):
    for _ in range(distance):
        offset = OFFSETS[angle]
        way.append((pos, angle))
        new = (pos[0] + offset[0], pos[1] + offset[1])
        new_angle = angle
        if is_void(field, new):
            new, new_angle = wrap_func(field, pos, angle)
        if field[new[0]][new[1]] == WALL:
            break
        pos, angle = new, new_angle
    return pos, angle


def find_final_pos(field, commands, wrap_func):
    pos = (0, field[0].index("."))
    angle = RIGHT
    way = []
    for command in commands:
        if command == "R":
            angle = (angle + 1) % 4
        elif command == "L":
            angle = (angle - 1) % 4
        else:
            pos, angle = move(field, pos, angle, command, way, wrap_func)
    return pos[0], pos[1], angle


def final_pos_to_code(pos_angle):
    return (pos_angle[0] + 1) * 1000 + (pos_angle[1] + 1) * 4 + pos_angle[2]


def solve(field, commands, wrap_func):
    return final_pos_to_code(find_final_pos(field, commands, wrap_func))


def read_lines(fname):
    norm_file_name = path.join(path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        return file.read().split("\n")


def solve_file(fname):
    lines = read_lines(fname)
    field, commands = parse_map(lines[:-2]), parse_commands(lines[-1])
    return (
        solve(field, commands, find_wrap),
        solve(field, commands, wrap_p2)
    )


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

    def test_find_final_pos(self):
        self.assertEqual(find_final_pos(self.MAP, self.COMMANDS, find_wrap), (5, 7, RIGHT))

    def test_solve(self):
        self.assertEqual(solve(self.MAP, self.COMMANDS, find_wrap), 6032)


if __name__ == '__main__':
    print(solve_file("input.txt"))  # (1484, 142228)
    unittest.main()
