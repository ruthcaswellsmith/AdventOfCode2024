from typing import List
from collections import defaultdict

from utils import read_file


class TrailMap:
    def __init__(self, data: List[str]):
        self.map = [[int(ele) if ele != '.' else -1 for ele in line] for line in data]
        self.max_rows = len(data) - 1
        self.max_cols = len(data[0]) - 1
        self.trailheads = {(row, col): {} for row in range(self.max_rows + 1)
                           for col in range(self.max_cols + 1) if
                           self.map[row][col] == 0}
        self.nines = [(row, col) for row in range(self.max_rows + 1)
                      for col in range(self.max_cols + 1) if
                      self.map[row][col] == 9]

    @property
    def trailhead_scores(self):
        return [len(trailhead.values()) for trailhead in self.trailheads.values()]

    @property
    def trailhead_ratings(self):
        return [sum(trailhead.values()) for trailhead in self.trailheads.values()]

    def evaluate_trailheads(self):
        for trailhead in self.trailheads.keys():
            for nine in self.nines:
                num_paths = self.count_paths(trailhead, nine, 9)
                if num_paths > 0:
                    self.trailheads[trailhead][nine] = num_paths

    def count_paths(self, start, end, target_len):
        visited = set()

        def dfs(row, col, curr_len):
            if (row, col) == end and curr_len == target_len:
                return 1

            visited.add((row, col))
            num_paths = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row <= self.max_rows and 0 <= new_col <= self.max_cols and \
                        (new_row, new_col) not in visited and \
                        self.map[new_row][new_col] - self.map[row][col] == 1:
                    num_paths += dfs(new_row, new_col, curr_len + 1)

            visited.remove((row, col))
            return num_paths

        return dfs(start[0], start[1], 0)


if __name__ == '__main__':
    filename = 'input/Day10.txt'
    data = read_file(filename)

    trailmap = TrailMap(data)
    trailmap.evaluate_trailheads()
    print(f"The answer to part 1 is {sum(trailmap.trailhead_scores)}")
    print(f"The answer to part 2 is {sum(trailmap.trailhead_ratings)}")
