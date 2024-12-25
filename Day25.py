from typing import List
from utils import read_file
import numpy as np


class Schematic:
    def __init__(self, data: List[str]):
        self.grid = np.array([[ele for ele in line] for line in data])
        self.size = self.grid.shape
        self.type = 'LOCK' if all([ele == '#' for ele in data[0]]) else 'KEY'
        if self.type == 'KEY':
            self.grid = np.rot90(self.grid, 2)
        self.counts = self.get_counts()

    def get_counts(self):
        r = range(self.size[1]) if self.type == 'LOCK' else range(self.size[1]-1, -1, -1)
        counts = [sum([ele == '#' for ele in self.grid[1:, j]]) for j in r]
        return np.array(counts, dtype=int)


class OfficeDoor:
    def __init__(self, schematics: List[Schematic]):
        self.locks = [s for s in schematics if s.type == 'LOCK']
        self.keys = [s for s in schematics if s.type == 'KEY']
        self.overlap = self.locks[0].grid.shape[0] - 1

    def try_keys_in_locks(self):
        return sum(self.key_fits(lock, key) for lock in self.locks for key in self.keys)

    def key_fits(self, lock: Schematic, key: Schematic):
        return all((lock.counts + key.counts) < self.overlap)


if __name__ == '__main__':
    filename = 'input/Day25.txt'
    data = read_file(filename)

    schematics = []
    while data:
        try:
            ind = data.index("")
            schematics.append(Schematic(data[:ind]))
            data = data[ind + 1:]
        except ValueError:
            schematics.append(Schematic(data))
            break

    door = OfficeDoor(schematics)
    print(f"The answer to part 1 is {door.try_keys_in_locks()}.")
