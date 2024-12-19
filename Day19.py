from typing import List
import heapq

import numpy as np

from utils import read_file


class Onsen:
    def __init__(self, towels: str, patterns: List[str]):
        self.towels = [t.strip() for t in towels.split(',')]
        self.patterns = {p: False for p in patterns}

    @property
    def answer_pt1(self):
        return sum(self.patterns.values())

    def evaluate(self):
        for p in self.patterns.keys():
            print(f"trying pattern {p}")
            self.patterns[p] = self.find_pattern(p[:])

    def find_pattern(self, p: str):
        if not p:
            return True

        found, ind = False, 0
        while not found and ind <= len(p):
            ind += 1
            for t in self.towels:
                if p[:ind] == t:
                    found = self.find_pattern(p[ind:])
                    if found:
                        break

        return True if found else False



if __name__ == '__main__':
    filename = 'input/Day19.txt'
    data = read_file(filename)

    onsen = Onsen(data[0], data[2:])
    onsen.evaluate()
    print(f"The answer to part 1 is {onsen.answer_pt1}")

