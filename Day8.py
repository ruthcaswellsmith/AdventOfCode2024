from typing import List

from utils import read_file, Part


class Grid:
    def __init__(self, data: List[str]):
        self.data = data
        self.max_x, self.max_y = len(data) - 1, len(data[0]) - 1
        self.lines = {}
        self.antinodes = set()

    def on_the_grid(self, row: int, col: int):
        return False if row < 0 or row > self.max_x or col < 0 or col > self.max_y else True

    def find_lines(self):
        for i, line1 in enumerate(self.data):
            for j, ele1 in enumerate(line1):
                if ele1 != '.':
                    if ele1 not in self.lines:
                        self.lines[ele1] = []
                    for k, line2 in enumerate(self.data):
                        for l, ele2 in enumerate(line2):
                            # Check this space is further along and we match
                            if (k > i or k == i and l > j) and self.data[k][l] == ele1:
                                self.lines[ele1].append(((i, j), (k, l)))

    def find_antinodes(self, part: Part):
        self.find_lines()
        for ele, pairs in self.lines.items():
            for ((i, j), (k, l)) in pairs:
                dx, dy = k - i, l - j
                if part == Part.PT1:
                    if self.on_the_grid(i - dx, j - dy):
                        self.antinodes.add((i - dx, j - dy))
                    if self.on_the_grid(k + dx, l + dy):
                        self.antinodes.add((k + dx, l + dy))
                else:
                    # Start at (i, j) and work backwards
                    new_x, new_y = i - dx, j - dy
                    self.antinodes.add((i, j))
                    while self.on_the_grid(new_x, new_y):
                        self.antinodes.add((new_x, new_y))
                        new_x -= dx
                        new_y -= dy
                    # Start at (k, l) and work forwards
                    new_x, new_y = k + dx, l + dy
                    self.antinodes.add((k, l))
                    while self.on_the_grid(new_x, new_y):
                        self.antinodes.add((new_x, new_y))
                        new_x += dx
                        new_y += dy


if __name__ == '__main__':
    filename = 'input/Day8.txt'
    data = read_file(filename)

    grid = Grid(data)
    grid.find_antinodes(Part.PT1)
    print(f"The answer to part 1 is {len(grid.antinodes)}")

    grid = Grid(data)
    grid.find_antinodes(Part.PT2)
    print(f"The answer to part 2 is {len(grid.antinodes)}")

