from typing import List
import operator
from utils import read_file

OPS = {'AND': operator.and_, 'OR': operator.or_, 'XOR': operator.xor}


class Device:
    def __init__(self, data: List[str]):
        index = data.index('')
        self.gates = self.get_gates(data[index+1:])
        self.wires = self.get_wires(data[:index])
        self.max_z = max([int(w[1:]) for w in self.gates.keys() if w.startswith('z')])
        self.swaps = []

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

    def get_wires(self, data: List[str]):
        wires = {w: None for w in self.gates.keys()}
        for line in data:
            pts = line.replace(' ', '').split(':')
            wires[pts[0]] = int(pts[1])
        return wires

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

    def fix_gates(self):
        # Thanks to _garden_gnome_ whose post helped me understand how an adder works
        x, y = self.format_wire('x', 0), self.format_wire('y', 0)

        gate_carry_prev = self.get_gate(x, "AND", y)

        for i in range(1, self.max_z):
            x, y, z = self.format_wire('x', i), self.format_wire('y', i), self.format_wire('z', i)

            still_swapping = True
            while still_swapping:
                still_swapping = False

                gate_and = self.get_gate(x, 'AND', y)
                gate_xor = self.get_gate(x, "XOR", y)
                w1, op, w2 = self.gates[z]

                if w1 == gate_carry_prev and w2 != gate_xor:
                    self.swap(w2, gate_xor)
                    still_swapping = True
                    continue
                if w2 == gate_carry_prev and w1 != gate_xor:
                    self.swap(w1, gate_xor)
                    still_swapping = True
                    continue

                gate_z = self.get_gate(gate_xor, "XOR", gate_carry_prev)
                if gate_z != z:
                    self.swap(gate_z, z)
                    still_swapping = True
                    continue

                gate_tmp = self.get_gate(gate_xor, "AND", gate_carry_prev)
                gate_carry_prev = self.get_gate(gate_tmp, "OR", gate_and)


if __name__ == '__main__':
    filename = 'input/Day24.txt'
    data = read_file(filename)

    device = Device(data)
    device.simulate()
    print(f"The answer to part 1 is {device.number('z')}.")

    device.fix_gates()
    print(f"The answer to part 2 is {','.join(sorted(device.swaps))}.")

