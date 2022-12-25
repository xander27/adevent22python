from dataclasses import dataclass
import os
import unittest


@dataclass
class File:
    name: str
    size: int

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class Dir:
    name: str
    _children: set

    def __init__(self, name, *varg) -> None:
        self.name = name
        self._children = set(varg)
        self._size = -1

    def __hash__(self) -> int:
        return hash(self.name)

    def calculate_size(self):
        if self._size < 0:
            self._size = 0
            for child in self._children:
                if isinstance(child, Dir):
                    self._size = self._size + child.calculate_size()
                else:
                    self._size = self._size + child.size
        return self._size

    def add_child(self, child):
        self._children.add(child)


@dataclass
class DirRegistry:
    dirs: dict = None

    def __getitem__(self, path):
        if self.dirs is None:
            self.dirs = {}

        path_string = "/" + "/".join(path)

        if path_string in self.dirs:
            return self.dirs[path_string]

        new_dir = Dir(path_string)
        self.dirs[path_string] = new_dir
        return new_dir


def parse(commands):
    dir_registry = DirRegistry()
    path = []
    cur_dir = dir_registry[path]

    for command in commands:
        command = command.rstrip()
        parts = command.split(" ")
        if parts[0] == "$":
            if parts[1] == "cd":
                if parts[2] == "/":
                    path = []
                elif parts[2] == "..":
                    path.pop()
                else:
                    path.append(parts[2])
            cur_dir = dir_registry[path]
        elif parts[0] == "dir":
            path.append(parts[1])
            cur_dir.add_child(dir_registry[path])
            path.pop()
        else:
            size = int(parts[0])
            file = File(parts[1], size)
            cur_dir.add_child(file)
    return dir_registry.dirs


def read_lines(fname):
    norm_file_name = os.path.join(os.path.dirname(__file__), fname)
    with open(norm_file_name, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def find_total_small(dirs):
    total_small = 0
    for cur_dir in dirs.values():
        size = cur_dir.calculate_size()
        if size <= 100000:
            total_small = total_small + size
    return total_small


def find_smallest_to_delete(dirs):
    total_space = 70000000
    free_needed = 30000000
    space_used = dirs["/"].calculate_size()
    free_now = total_space - space_used
    delete_needed = free_needed - free_now

    min_to_delete = total_space
    for cur_dir in dirs.values():
        size = cur_dir.calculate_size()
        if size < delete_needed:
            continue
        if size < min_to_delete:
            min_to_delete = size

    if min_to_delete == total_space:
        raise Exception("Can't find directory to delete")
    return min_to_delete


def solve_file(fname):
    dirs = parse(read_lines(fname))
    return find_total_small(dirs), find_smallest_to_delete(dirs)


class TestDay(unittest.TestCase):

    def test_parse(self):
        actual = parse(read_lines("input-test.txt"))
        self.assertEqual(actual["/a/e"], Dir("/a/e", File("i", 584)))

    def test_calculate_size(self):
        actual = Dir("/a", File("i", 100), Dir("/a/e", File("x", 10), File("y", 20))).calculate_size()
        self.assertEqual(actual, 130)

    def test_solve(self):
        self.assertEqual(solve_file("input-test.txt"), (95437, 24933642))


if __name__ == '__main__':
    print(solve_file("input.txt"))
    print("=====")
    unittest.main()
