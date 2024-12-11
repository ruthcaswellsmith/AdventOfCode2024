from typing import List
from collections import defaultdict
from utils import read_file


class Stones:
    def __init__(self, data: List[str]):
        self.counts = defaultdict(int)
        for x in data[0].split():
            self.counts[x] = 1
        self.num_blinks = 0

    @property
    def num_stones(self):
        return sum(self.counts.values())

    def blink(self, max_blinks: int):
        for i in range(max_blinks):
            new_counts = defaultdict(int)
            for num, count in self.counts.items():
                num_digits = len(num)
                if num == '0':
                    new_counts['1'] += count
                elif num_digits % 2 == 0:
                    new_counts[str(int(num[:num_digits // 2]))] += count
                    new_counts[str(int(num[num_digits // 2:]))] += count
                else:
                    new_counts[str(2024 * int(num))] += count
            self.counts = new_counts


if __name__ == '__main__':
    filename = 'input/Day11.txt'
    data = read_file(filename)

    stones = Stones(data)
    stones.blink(25)
    print(f"The answer to part 1 is {stones.num_stones}")

    stones = Stones(data)
    stones.blink(75)
    print(f"The answer to part 2 is {stones.num_stones}")
