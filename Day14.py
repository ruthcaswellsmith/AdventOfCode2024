from typing import List

import numpy as np

from utils import read_file, Part

MAX_X = 101
MAX_Y = 103


class Robot:
    def __init__(self, data: str):
        pts = data.split()
        self.pos = [int(ele) for ele in pts[0].strip('p=').split(',')]
        self.v = [int(ele) for ele in pts[1].strip('v=').split(',')]


class Floor:
    def __init__(self, robots: List[Robot]):
        self.robots = robots
        self.grid = np.zeros((MAX_X, MAX_Y), dtype=int)
        self.x_var_min, self.y_var_min = 10_000, 10_000

    def move(self, num_secs, part: Part):
        if part == part.PT1:
            for r in robots:
                r.pos = [
                    (r.pos[0] + r.v[0] * num_secs) % MAX_X,
                    (r.pos[1] + r.v[1] * num_secs) % MAX_Y,
                ]
                self.grid[r.pos[0], r.pos[1]] += 1

        else:
            for sec in range(1, num_secs + 1):
                locs = np.array([
                    [(r.pos[0] + r.v[0] * sec) % MAX_X,
                     (r.pos[1] + r.v[1] * sec) % MAX_Y]
                    for r in robots])

                x_var, y_var = np.var(locs[:, 0]), np.var(locs[:, 1])
                # Note that these variances will repeat ever MAX_X and MAX_Y secs,
                # respectively
                self.x_var_min = x_var if x_var < self.x_var_min else self.x_var_min
                self.y_var_min = y_var if y_var < self.x_var_min else self.y_var_min

                if sec > 1 and x_var == self.x_var_min and y_var == self.y_var_min:
                    # If this is true we have hit the min variance for both x and y
                    # at the same time, i.e. robots are highly clustered together
                    return sec

    def robots_per_quadrant(self):
        x_index, y_index = (MAX_X - 1) // 2, (MAX_Y - 1) // 2
        return [
            np.sum(self.grid[:x_index, :y_index]),
            np.sum(self.grid[x_index + 1:, :y_index]),
            np.sum(self.grid[:x_index:, y_index + 1:]),
            np.sum(self.grid[x_index + 1:, y_index + 1:])
        ]


if __name__ == '__main__':
    filename = 'input/Day14.txt'
    data = read_file(filename)

    robots = [Robot(line) for line in data]
    floor = Floor(robots)
    floor.move(100, Part.PT1)
    print(f"The answer to part 1 is {np.prod(floor.robots_per_quadrant())}")

    robots = [Robot(line) for line in data]
    floor = Floor(robots)
    print(f"The answer to part 2 is {floor.move(10_000, Part.PT2)}")
