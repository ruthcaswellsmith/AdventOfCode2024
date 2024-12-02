from utils import read_file
from typing import List


class Report:
    def __init__(self, data: List[int]):
        self.data = data

    @property
    def is_increasing(self):
        return sorted(self.data[:]) == self.data

    @property
    def is_decreasing(self):
        return sorted(self.data[:], reverse=True) == self.data

    @property
    def has_safe_diffs(self):
        diffs = [abs(self.data[i] - self.data[i+1]) for i in range(len(self.data) - 1)]
        if min(diffs) < 1 or max(diffs) > 3:
            return False
        return True

    @property
    def is_safe(self):
        if not (self.is_decreasing or self.is_increasing):
            return False
        if not self.has_safe_diffs:
            return False
        return True

    @property
    def can_be_made_safe(self):
        if self.is_safe:
            return True
        for i in range(len(self.data)):
            new_report = Report(self.data[:i] + self.data[i+1:])
            if new_report.is_safe:
                return True
        return False


if __name__ == '__main__':
    filename = 'input/Day2.txt'
    data = read_file(filename)

    reports = [Report([int(ele) for ele in line.split()]) for line in data]

    print(f"The answer to part 1 is {sum([ele.is_safe for ele in reports])}")

    print(f"The answer to part 2 is {sum([ele.is_safe or ele.can_be_made_safe for ele in reports])}")
