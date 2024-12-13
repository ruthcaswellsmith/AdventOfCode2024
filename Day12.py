from typing import List, Tuple

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

    def on_the_grid(self, pos: Tuple[int, int]) -> bool:
        return True if 0 <= pos[0] <= self.max_x and 0 <= pos[1] <= self.max_y else False

    def assign_regions(self):
        unassigned_coords = [[int(coord[0]), int(coord[1])] for coord in np.argwhere(self.region_map == 0)]
        while len(unassigned_coords) > 0:

            self.start_of_region = unassigned_coords[0]
            self.letter = self.grid[self.start_of_region[0]][self.start_of_region[1]]
            self.region_num += 1
            self.region_map[tuple(self.start_of_region)] = self.region_num
            perimeter, corners = self.expand_region(self.start_of_region)
            area = np.count_nonzero(self.region_map == self.region_num)
            self.regions[self.region_num] = {
                'letter': self.letter,
                'perimeter': perimeter,
                'area': area,
                'sides': corners
            }
            unassigned_coords = [[int(coord[0]), int(coord[1])] for coord in np.argwhere(self.region_map == 0)]

    def expand_region(self, pos: List[int]):
        perimeter, corners = 0, 0

        # determine whether 8 neighbors match
        neighbors = {}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
            new_pos = (pos[0] + dx, pos[1] + dy)
            neighbors[(dx, dy)] = True \
                if self.on_the_grid(new_pos) and self.grid[new_pos[0]][new_pos[1]] == self.letter \
                else False

        # check for corners
        for h, v in [((0, -1), (-1, 0)), ((0, 1), (-1, 0)), ((0, 1), (1, 0)), ((0, -1), (1, 0))]:
            # if both horiz and vert neighbors do not match, we have an outer corner
            if sum([neighbors[h], neighbors[v]]) == 0:
                corners += 1
            # if both horiz and vert neighbors match and the diagonal does not match we have an inner corner
            if sum([neighbors[h], neighbors[v]]) == 2 and not neighbors[(h[0]+v[0], h[1]+v[1])]:
                corners += 1

        for i, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            new_pos = (pos[0] + dx, pos[1] + dy)
            if neighbors[(dx, dy)]:
                if self.region_map[new_pos] == 0:
                    self.region_map[new_pos] = self.region_num
                    p, c = self.expand_region(list(new_pos))
                    perimeter, corners = perimeter + p, corners + c
            else:
                perimeter += 1
        return perimeter, corners


if __name__ == '__main__':
    filename = 'input/Day12.txt'
    data = read_file(filename)

    map = Map(data)
    map.assign_regions()
    print(f"The answer to part 1 is {sum([region['perimeter'] * region['area'] for region in map.regions.values()])}")

    print(f"The answer to part 2 is {sum([region['area'] * region['sides'] for region in map.regions.values()])}")
