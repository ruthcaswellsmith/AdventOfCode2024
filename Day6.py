import sys
from enum import Enum
from typing import List, Tuple

import numpy as np

from utils import read_file

sys.setrecursionlimit(10_000)


class Direction(Tuple, Enum):
    NORTH = (1, (-1, 0))
    EAST = (2, (0, 1))
    SOUTH = (3, (1, 0))
    WEST = (4, (0, -1))


class Map:
    def __init__(self, data: List[str]):
        self.grid = np.array([[True if ele == '#' else False for ele in line] for line in data])
        self.max_x = len(data) - 1
        self.max_y = len(data[0]) - 1


class Guard:
    def __init__(self, data: List[str], map: Map):
        self.map = map
        self.visited = np.zeros_like(self.map.grid, dtype=int)
        for i, line in enumerate(data):
            if '^' in line:
                self.start = [i, line.index('^')]
        self.pos = self.start.copy()
        self.dir = Direction.NORTH

    @property
    def in_a_loop(self):
        last_visited_dir = self.visited[self.pos[0], self.pos[1]]
        if last_visited_dir == 0:
            return False
        if self.dir.value[0] == last_visited_dir:
            return True

    @property
    def at_edge(self):
        if self.pos[0] == 0 and self.dir == Direction.NORTH or \
                self.pos[0] == self.map.max_x and self.dir == Direction.SOUTH or \
                self.pos[1] == 0 and self.dir == Direction.WEST or \
                self.pos[1] == self.map.max_y and self.dir == Direction.EAST:
            return True
        return False

    @property
    def blocked(self):
        if self.dir == Direction.NORTH and self.map.grid[self.pos[0] - 1, self.pos[1]] or \
                self.dir == Direction.EAST and self.map.grid[self.pos[0], self.pos[1] + 1] or \
                self.dir == Direction.SOUTH and self.map.grid[self.pos[0] + 1, self.pos[1]] or \
                self.dir == Direction.WEST and self.map.grid[self.pos[0], self.pos[1] - 1]:
            return True
        return False

    def move(self):
        # Check if we are in a loop
        if self.in_a_loop:
            return
        # Mark the current spot as visited in this direction
        self.visited[self.pos[0], self.pos[1]] = self.dir.value[0]
        # Check if we are at edge
        if self.at_edge:
            # Mark current spot as different so we don't think we're in a loop
            self.visited[self.pos[0], self.pos[1]] = 5
            return
        # Check if we are blocked.  If so turn right
        if self.blocked:
            self.dir = Direction.EAST if self.dir == Direction.NORTH else \
                Direction.SOUTH if self.dir == Direction.EAST else \
                Direction.WEST if self.dir == Direction.SOUTH else \
                Direction.NORTH
        # Move to new position
        self.pos[0] += self.dir.value[1][0]
        self.pos[1] += self.dir.value[1][1]

        self.move()


if __name__ == '__main__':
    filename = 'input/Day6.txt'
    data = read_file(filename)

    guard = Guard(data, Map(data))
    guard.move()
    original_visited = guard.visited > 0

    print(f"The answer to part 1 is {np.sum(guard.visited > 0)}")

    possible_loops = 0
    # Go through and try putting an obstacle in spots along original path
    for i in range(guard.map.max_x + 1):
        for j in range(guard.map.max_y + 1):
            if original_visited[i, j] and [i, j] != guard.start:
                guard = Guard(data, Map(data))
                guard.map.grid[i, j] = True
                guard.move()
                if guard.in_a_loop:
                    print(f"found a loop {i, j}")
                    possible_loops += 1

    print(f"The answer to part 2 is {possible_loops}")
