from enum import Enum
from typing import List, Tuple

from utils import read_file


class Direction(Tuple, Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


class Guard:
    def __init__(self, data: List[str]):
        self.grid = data.copy()
        self.max_x, self.max_y = len(data) - 1, len(data[0]) - 1
        self.visited = set()
        for i, line in enumerate(data):
            if '^' in line:
                self.start = (i, line.index('^'))
        self.pos = list(self.start)
        self.dir = Direction.NORTH

    @property
    def in_a_loop(self):
        if (tuple(self.pos), self.dir.value) in self.visited:
            return True
        return False

    @property
    def at_edge(self):
        if self.pos[0] == 0 and self.dir == Direction.NORTH or \
                self.pos[0] == self.max_x and self.dir == Direction.SOUTH or \
                self.pos[1] == 0 and self.dir == Direction.WEST or \
                self.pos[1] == self.max_y and self.dir == Direction.EAST:
            return True
        return False

    @property
    def blocked(self):
        if self.grid[self.pos[0] + self.dir.value[0]][self.pos[1] + self.dir.value[1]] == '#':
            return True
        return False

    def update_pos(self):
        self.pos[0] += self.dir.value[0]
        self.pos[1] += self.dir.value[1]

    def move(self):
        while True:
            if self.in_a_loop:
                break

            # Mark the current spot as visited in this direction
            self.visited.add((tuple(self.pos), self.dir.value))

            if self.at_edge:
                self.update_pos()
                break

            if self.blocked:
                self.dir = Direction.EAST if self.dir == Direction.NORTH else \
                    Direction.SOUTH if self.dir == Direction.EAST else \
                    Direction.WEST if self.dir == Direction.SOUTH else \
                    Direction.NORTH
            else:
                self.update_pos()


if __name__ == '__main__':
    filename = 'input/Day6.txt'
    data = read_file(filename)

    guard = Guard(data)
    guard.move()
    original_visited = {pos for pos, direction in guard.visited}
    print(f"The answer to part 1 is {len(original_visited)}")

    possible_loops = 0
    # Try putting a single obstacle in each spot on the original path
    for loc in original_visited:
        if loc != guard.start:
            guard = Guard(data)
            line = guard.grid[loc[0]]
            guard.grid[loc[0]] = line[:loc[1]] + '#' + line[loc[1]+1:]
            guard.move()
            if guard.in_a_loop:
                print(f"found a loop {loc}")
                possible_loops += 1
    print(f"The answer to part 2 is {possible_loops}")