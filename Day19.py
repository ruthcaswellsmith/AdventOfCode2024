from typing import List
from functools import lru_cache
import time

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

    def evaluate(self, dp: bool = False):
        fn = self.count_matches_dp if dp else self.count_matches
        for p in self.patterns.keys():
            self.patterns[p] = fn(p)

    @lru_cache(maxsize=None)
    def count_matches(self, p: str):
        if not p:
            return 1

        matches = 0
        for ind in range(1, len(p) + 1):
            for t in self.towels:
                if p[:ind] == t:
                    matches += self.count_matches(p[ind:])

        return matches

    def count_matches_dp(self, p: str):
        dp = [0] * (len(p) + 1)
        dp[0] = 1

        for i in range(1, len(p) + 1):
            for j in range(i):
                prefix = p[j:i]
                if prefix in self.towels:
                    dp[i] += dp[j]

        return dp[len(p)]


if __name__ == '__main__':
    filename = 'input/Day19.txt'
    data = read_file(filename)

    onsen = Onsen(data[0], data[2:])
    start = time.time()
    onsen.evaluate()
    print(f"Using recursion took {time.time() - start} sec")

    start = time.time()
    onsen.evaluate(dp=True)
    print(f"Using DP took {time.time() - start} sec")

    print(f"The answer to part 1 is {onsen.answer_pt1}")
    print(f"The answer to part 2 is {onsen.answer_pt2}")

