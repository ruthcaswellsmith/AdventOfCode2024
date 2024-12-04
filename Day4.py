from enum import Enum
from typing import List, Tuple

from utils import read_file

PATTERN = 'XMAS'
X_PATTERN = 'MAS'


class Direction(Tuple, Enum):
    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    EAST = (0, 1)
    SOUTHEAST = (1, 1)
    SOUTH = (1, 0)
    SOUTHWEST = (1, -1)
    WEST = (0, -1)
    NORTHWEST = (-1, -1)


class WordSearch:
    def __init__(self, data: List[str], pattern: str, x_pattern: str):
        self.data = data
        self.rows, self.cols = len(data), len(data[0])
        self.pattern = pattern
        self.num_chars = len(pattern)
        self.x_pattern = x_pattern
        self.x_index = (len(x_pattern) - 1) // 2

    def search_pattern(self):
        patterns_found = 0
        for row in range(self.rows):
            line = data[row]
            for col in range(self.cols):
                char = line[col]
                if char == self.pattern[0]:
                    # We've found first letter of pattern
                    patterns_found += \
                        self.search_in_direction(row, col, Direction.NORTH, 0) + \
                        self.search_in_direction(row, col, Direction.NORTHEAST, 0) + \
                        self.search_in_direction(row, col, Direction.EAST, 0) + \
                        self.search_in_direction(row, col, Direction.SOUTHEAST, 0) + \
                        self.search_in_direction(row, col, Direction.SOUTH, 0) + \
                        self.search_in_direction(row, col, Direction.SOUTHWEST, 0) + \
                        self.search_in_direction(row, col, Direction.WEST, 0) + \
                        self.search_in_direction(row, col, Direction.NORTHWEST, 0)
        return patterns_found

    def search_in_direction(self, row: int, col: int, direction: Direction, char_num: int):
        row += direction.value[0]
        col += direction.value[1]
        char_num += 1
        if row == self.rows or row < 0 or col == self.cols or col < 0:
            # We're off the grid
            return 0
        if self.data[row][col] != self.pattern[char_num]:
            # This letter isn't in the pattern
            return 0
        if char_num == len(self.pattern) - 1:
            # we've found a pattern
            return 1
        # Otherwise continue to search in appropriate direction
        return self.search_in_direction(row, col, direction, char_num)

    def search_x_pattern(self):
        patterns_found = 0
        # Only search center of grid where we would have enough room for an X-pattern
        for row in range(self.x_index, self.rows - self.x_index):
            line = data[row]
            for col in range(self.x_index, self.cols - self.x_index):
                char = line[col]
                if char == self.x_pattern[self.x_index]:
                    # We've found a possible middle of an X-pattern.
                    diagonal_1, diagonal_2 = '', ''
                    for i in range(-self.x_index, self.x_index + 1):
                        diagonal_1 += self.data[row + i][col + i]
                        diagonal_2 += self.data[row + i][col - i]
                    if (diagonal_1 == self.x_pattern or diagonal_1[::-1] == self.x_pattern) and \
                            (diagonal_2 == self.x_pattern or diagonal_2[::-1] == self.x_pattern):
                        # Both diagonals spell the pattern
                        patterns_found += 1
        return patterns_found


if __name__ == '__main__':
    filename = 'input/Day4.txt'
    data = read_file(filename)

    word_search = WordSearch(data, PATTERN, X_PATTERN)

    print(f"The answer to part 1 is {word_search.search_pattern()}")

    print(f"The answer to part 2 is {word_search.search_x_pattern()}")
