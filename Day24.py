import operator
from typing import List

from utils import read_file

OPS = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}


class Device:
    def __init__(self, data: List[str]):
        self.gates = self.get_gates(data[data.index('') + 1:])
        self.wires = None
        self.max_z = max([int(w[1:]) for w in self.gates.keys() if w.startswith('z')])
        self.swaps = []
        self.x, self.y, self.z = self.format_wire('x', 0), self.format_wire('y', 0), self.format_wire('z', 0)
        self.x_and_y = self.get_gate(self.x, "AND", self.y)
        self.x_xor_y = self.get_gate(self.x, "XOR", self.y)
        # This is true because the carry bit is 0 for the 0th bit
        self.x_xor_y_and_c = 0
        self.sum = self.x_xor_y
        self.carry = self.x_and_y

    @staticmethod
    def format_wire(letter: str, i: int):
        return f"{letter}{str(i).zfill(2)}"

    @property
    def all_z_wires_are_set(self):
        return all(v is not None for k, v in self.wires.items() if k.startswith('z'))

    def get_gate(self, wire1, operator, wire2):
        for output_wire, (w1, op, w2) in self.gates.items():
            if (wire1, operator, wire2) in [(w1, op, w2), (w2, op, w1)]:
                return output_wire
        return None

    def number(self, letter: str):
        num = ''.join(str(self.wires[w]) for \
                      w in sorted([wire for wire in self.wires.keys() if wire.startswith(letter)], reverse=True))
        return int(num, 2)

    def initialize(self, data: List[str]):
        self.wires = {w: None for w in self.gates.keys()}
        for line in data:
            pts = line.replace(' ', '').split(':')
            self.wires[pts[0]] = int(pts[1])

    @staticmethod
    def get_gates(data: List[str]):
        gates = {}
        for line in data:
            pts = line.split('->')
            output = pts[1].strip()
            pts = pts[0].strip().split(' ')
            gates[output] = (pts[0], pts[1], pts[2])
        return gates

    def swap(self, wire1, wire2):
        self.gates[wire1], self.gates[wire2] = self.gates[wire2], self.gates[wire1]
        self.swaps.extend([wire1, wire2])

    def simulate(self):
        while not self.all_z_wires_are_set:
            for output, (w1, op, w2) in self.gates.items():
                if self.wires[w1] is not None and self.wires[w2] is not None:
                    self.wires[output] = OPS[op](self.wires[w1], self.wires[w2])

    def update_state(self, carry_prev: str):
        self.x_and_y = self.get_gate(self.x, 'AND', self.y)
        self.x_xor_y = self.get_gate(self.x, "XOR", self.y)
        self.x_xor_y_and_c = self.get_gate(self.x_xor_y, "AND", carry_prev)
        self.sum = self.get_gate(self.x_xor_y, "XOR", carry_prev)
        self.carry = self.get_gate(self.x_xor_y_and_c, "OR", self.x_and_y)

    def fix_gates(self):

        for i in range(1, self.max_z):
            carry_prev = self.carry
            self.x, self.y, self.z = self.format_wire('x', i), self.format_wire('y', i), self.format_wire('z', i)
            self.update_state(carry_prev)
            w1, op, w2 = self.gates[self.z]

            if op == 'XOR':
                if (w1, w2) in ((carry_prev, self.x_xor_y), (self.x_xor_y, carry_prev)):
                    pass
                elif w1 == carry_prev or w2 == carry_prev:
                    if w1 == carry_prev:
                        self.swap(w2, self.x_xor_y)
                        self.update_state(carry_prev)
                    elif w2 == carry_prev:
                        self.swap(w1, self.x_xor_y)
                        self.update_state(carry_prev)
                    else:
                        print(f"Can't fix bit {i}");
                        exit()
            else:
                if (w1, w2) in ((carry_prev, self.x_xor_y), (self.x_xor_y, carry_prev),
                                (self.x, self.y), (self.y, self.x),
                                (self.x_xor_y_and_c, self.x_and_y), (self.x_and_y, self.x_xor_y_and_c)):
                    self.swap(self.sum, self.z)
                    self.update_state(carry_prev)
                else:
                    print(f"Can't fix bit {i}");
                    exit()


if __name__ == '__main__':
    filename = 'input/Day24.txt'
    data = read_file(filename)

    device = Device(data)
    device.initialize(data[:data.index("")])
    device.simulate()
    print(f"The answer to part 1 is {device.number('z')}.")

    device.fix_gates()
    print(f"The answer to part 2 is {','.join(sorted(device.swaps))}.")

    device.initialize(data[:data.index("")])
    device.simulate()
    print(f"{device.number('x')} + {device.number('y')} ?= {device.number('z')}")
    print(f"{device.number('x') + device.number('y')}")
