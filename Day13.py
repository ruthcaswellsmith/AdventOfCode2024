from typing import List
from decimal import Decimal

from utils import read_file, Part


class ClawMachine:
    def __init__(self, data: List[str], part: Part):
        self.moves = []
        for i in range(2):
            pts = data[i].split(':')
            self.moves.append([Decimal(pt.strip().strip('X+').strip('Y+')) for pt in pts[1].split(',')])
        pts = data[2].split(':')
        self.prize = [Decimal(pt.strip().strip('X=').strip('Y=')) for pt in pts[1].split(',')]
        if part == Part.PT2:
            self.prize = [10_000_000_000_000 + prize for prize in self.prize]
        self.pushes = []

    @property
    def tokens(self):
        return 3 * self.pushes[0] + self.pushes[1] if self.pushes else 0

    def solve(self):
        num1 = self.prize[0] * self.moves[0][1] - self.prize[1] * self.moves[0][0]
        num2 = self.moves[1][0] * self.moves[0][1] - self.moves[1][1] * self.moves[0][0]
        if num1 % num2 == 0:
            b = round(num1 / num2)
            self.pushes = [
                round((self.prize[0] - b * self.moves[1][0]) / self.moves[0][0]),
                b
            ]


if __name__ == '__main__':
    filename = 'input/Day13.txt'
    data = read_file(filename)

    for i, part in enumerate(Part):
        claws = [ClawMachine(data[i:i + 3], part) for i in range(0, len(data) - 1, 4)]
        [claw.solve() for claw in claws]
        print(f"The answer to part {i+1} is {sum([claw.tokens for claw in claws])}")
