from typing import List
from collections import defaultdict
from utils import read_file
import numpy as np


class Buyer:
    def __init__(self, data: str, repetitions: int):
        self.repetitions = repetitions
        self.secret_nums = self.generate_secret_numbers(int(data))
        self.prices = self.secret_nums % 10
        self.diffs = np.diff(self.prices)

    @staticmethod
    def get_secret_number(num):
        num = (64 * num ^ num) % 16777216
        num = (num // 32 ^ num) % 16777216
        num = (num * 2048 ^ num) % 16777216
        return num

    def generate_secret_numbers(self, start: int):
        secret_nums = np.zeros(self.repetitions + 1, dtype=int)
        secret_nums[0] = (start)

        for j in range(self.repetitions):
            secret_nums[j + 1] = (self.get_secret_number(secret_nums[j]))
        return secret_nums


class Market:
    def __init__(self, buyers: List[Buyer]):
        self.buyers = buyers
        self.sequences = defaultdict(int)

    def inspect_sequences(self):
        for b in self.buyers:
            seen = set()
            for i in range(b.repetitions - 3):
                seq = tuple(b.diffs[i:i+4])
                if seq not in seen:
                    self.sequences[seq] += b.prices[i+4]
                    seen.add(seq)


if __name__ == '__main__':
    filename = 'input/Day22.txt'
    data = read_file(filename)

    market = Market([Buyer(line, 2000) for line in data])
    print(f"The answer to part 1 is {sum([b.secret_nums[-1] for b in market.buyers])}.")

    market.inspect_sequences()
    print(f"The answer to part 2 is {max(market.sequences.values())}.")

