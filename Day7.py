import operator
import itertools

from utils import read_file, Part


def concatenate(a: int, b: int):
    return int(str(a) + str(b))


class Calibration:
    def __init__(self, line: str, part: Part):
        pts = line.split(':')
        self.value = int(pts[0])
        self.inputs = [int(pt) for pt in pts[1].split()]
        self.ops = [operator.add, operator.mul]
        if part == Part.PT2:
            self.ops += [concatenate]

    @property
    def result(self):
        return self.value if self.can_be_true else 0

    @property
    def can_be_true(self):
        combos = list(itertools.product(self.ops, repeat=len(self.inputs) - 1))
        for combo in combos:
            left_side = self.inputs[0]
            for pos in range(1, len(self.inputs)):
                left_side = combo[pos - 1](left_side, self.inputs[pos])
            if left_side == self.value:
                return True
        return False


if __name__ == '__main__':
    filename = 'input/Day7.txt'
    data = read_file(filename)

    calibrations = [Calibration(line, Part.PT1) for line in data]
    print(f"The answer to part 1 is {sum([c.result for c in calibrations])}")

    calibrations = [Calibration(line, Part.PT2) for line in data]
    print(f"The answer to part 2 is {sum([c.result for c in calibrations])}")
