from collections import defaultdict
from functools import cmp_to_key

from typing import List
from utils import read_file


class Rules:
    def __init__(self, data: List[str]):
        self.before = defaultdict(list)
        for line in data:
            parts = line.split('|')
            self.before[parts[0]].append(parts[1])

    def compare(self, x: str, y: str):
        if x in self.before and y in self.before[x]:
            return -1
        if y in self.before and x in self.before[y]:
            return 1
        return 0


class Update:
    def __init__(self, line: str, rules: Rules):
        self.rules = rules
        self.pages = line.split(',')
        self.sorted = sorted(self.pages, key=cmp_to_key(self.rules.compare))

    @property
    def middle_page(self):
        return self.pages[len(self.pages)//2]

    @property
    def middle_page_sorted(self):
        return self.sorted[len(self.pages)//2]

    @property
    def correctly_ordered(self):
        return self.sorted == self.pages


if __name__ == '__main__':
    filename = 'input/Day5.txt'
    data = read_file(filename)

    empty_index = data.index('')
    rules = Rules(data[:empty_index])
    updates = [Update(line, rules) for line in data[empty_index+1:]]

    print(f"The answer to part 1 is "
          f"{sum([int(update.middle_page) for update in updates if update.correctly_ordered])}")

    print(f"The answer to part 2 is "
          f"{sum([int(update.middle_page_sorted) for update in updates if not update.correctly_ordered])}")
