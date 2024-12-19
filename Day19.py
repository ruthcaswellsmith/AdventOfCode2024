from typing import List
from functools import lru_cache

from utils import read_file


class Onsen:
    def __init__(self, towels: str, patterns: List[str]):
        self.towels = [t.strip() for t in towels.split(',')]
        self.patterns = {p: 0 for p in patterns}

    @property
    def answer_pt1(self):
        return sum([v > 0 for v in self.patterns.values()])

    @property
    def answer_pt2(self):
        return sum(self.patterns.values())

    def evaluate(self):
        for p in self.patterns.keys():
            self.patterns[p] = self.find_pattern(p[:])

    @lru_cache(maxsize=None)
    def find_pattern(self, p: str):
        if not p:
            return 1

        matches = 0
        for ind in range(1, len(p) + 1):
            for t in self.towels:
                if p[:ind] == t:
                    matches += self.find_pattern(p[ind:])

        return matches


if __name__ == '__main__':
    filename = 'input/Day19.txt'
    data = read_file(filename)

    onsen = Onsen(data[0], data[2:])
    onsen.evaluate()
    print(f"The answer to part 1 is {onsen.answer_pt1}")

    print(f"The answer to part 2 is {onsen.answer_pt2}")
