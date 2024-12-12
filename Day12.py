from typing import List
from collections import defaultdict
import numpy as np

from utils import read_file


class Map:
    def __init__(self, data: List[str]):
        self.grid = [[ele for ele in line] for line in data]
        self.max_x, self.max_y = len(data) - 1, len(data[0]) - 1
        self.region_map = np.zeros((len(data), len(data[0])), dtype=int)
        self.regions = {}
        self.region_num = 0
        self.start_of_region = None
        self.letter = None

    def assign_regions(self):
        unassigned_coords = [[int(coord[0]), int(coord[1])] for coord in np.argwhere(self.region_map == 0)]
        while len(unassigned_coords) > 0:
            # Get a new value to start with
            self.start_of_region = unassigned_coords[0]
            self.letter = self.grid[self.start_of_region[0]][self.start_of_region[1]]
            self.region_num += 1
            self.regions[self.region_num] = {'letter': self.letter, 'perimeter': 0, 'area': 0}
            self.region_map[tuple(self.start_of_region)] = self.region_num
            # Expand region around this coordinate
            self.expand_region(self.start_of_region)
            unassigned_coords = [[int(coord[0]), int(coord[1])] for coord in np.argwhere(self.region_map == 0)]

    def expand_region(self, pos: List[int]):
        # search to the east
        if pos[1] < self.max_y and self.grid[pos[0]][pos[1] + 1] == self.letter:
            new_pos = tuple([pos[0], pos[1] + 1])
            if self.region_map[new_pos] == 0:
                self.region_map[new_pos] = self.region_num
                self.expand_region(list(new_pos))
        # search to the south
        if pos[0] < self.max_x and self.grid[pos[0]+1][pos[1]] == self.letter:
            new_pos = tuple([pos[0]+1, pos[1]])
            if self.region_map[new_pos] == 0:
                self.region_map[new_pos] = self.region_num
                self.expand_region(list(new_pos))
        # search to the west
        if pos[0] > 0 and self.grid[pos[0]][pos[1]-1] == self.letter:
            new_pos = tuple([pos[0], pos[1]-1])
            if self.region_map[new_pos] == 0:
                self.region_map[new_pos] = self.region_num
                self.expand_region(list(new_pos))
        # search to the north
        if pos[1] > self.max_y and self.grid[pos[0]-1][pos[1]] == self.letter:
            new_pos = tuple([pos[0]-1, pos[1]])
            if self.region_map[new_pos] == 0:
                self.region_map[new_pos] = self.region_num
                self.expand_region(list(new_pos))

    def calc_perimeter(self):
        for region in self.regions.keys():
            perimeter = 0
            area = 0
            for i in range(self.max_x + 1):
                for j in range(self.max_y + 1):
                    if self.region_map[(i, j)] == region:
                        area += 1
                        # Check above
                        if i == 0 or self.region_map[i - 1][j] != region:
                            perimeter += 1
                        # Check below
                        if i == self.max_x or self.region_map[i + 1][j] != region:
                            perimeter += 1
                        # Check to the right
                        if j == self.max_y or self.region_map[i][j + 1] != region:
                            perimeter += 1
                        # Check to the left
                        if j == 0 or self.region_map[i][j - 1] != region:
                            perimeter += 1
            self.regions[region]['perimeter'] = perimeter
            self.regions[region]['area'] = area


if __name__ == '__main__':
    filename = 'input/test3.txt'
    data = read_file(filename)

    map = Map(data)
    map.assign_regions()
    map.calc_perimeter()
    print(f"The answer to part 1 is {sum([region['perimeter'] * region['area'] for region in map.regions.values()])}")
    #
    # stones = Stones(data)
    # stones.blink(75)
    # print(f"The answer to part 2 is {stones.num_stones}")
