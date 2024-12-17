from typing import List
from collections import defaultdict

from utils import read_file


class Device:
    def __init__(self, registers: List[str], program: str):
        self.registers = defaultdict(int)
        self.registers = {
            key[-1]: int(value.strip())
            for key, value in (line.split(':') for line in registers)
        }
        self.program = [int(ele) for ele in program.split(":")[1].strip().split(',')]
        self.inst_ptr = 0
        self.output = []
        self.combo_map = {i: i for i in range(4)}
        self.combo_map[7] = None

        self.opcodes = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }

    @property
    def answer_pt1(self):
        return ','.join([str(ele) for ele in device.output])

    def reset(self, a=0, b=0, c=0):
        self.registers['A'] = a
        self.registers['B'] = b
        self.registers['C'] = c
        self.inst_ptr = 0
        self.output = []

    def adv(self, operand: int):
        self.registers['A'] = int(self.registers['A'] / 2 ** self.combo_map[operand])
        self.inst_ptr += 2

    def bxl(self, operand: int):
        self.registers['B'] = self.registers['B'] ^ operand
        self.inst_ptr += 2

    def bst(self, operand: int):
        self.registers['B'] = self.combo_map[operand] % 8
        self.inst_ptr += 2

    def jnz(self, operand: int):
        if self.registers['A'] > 0:
            self.inst_ptr = operand
        else:
            self.inst_ptr += 2

    def bxc(self, operand: int):
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        self.inst_ptr += 2

    def out(self, operand: int):
        self.inst_ptr += 2
        return self.combo_map[operand] % 8

    def bdv(self, operand: int):
        self.registers['B'] = int(self.registers['A'] / 2 ** self.combo_map[operand])
        self.inst_ptr += 2

    def cdv(self, operand: int):
        self.registers['C'] = int(self.registers['A'] / 2 ** self.combo_map[operand])
        self.inst_ptr += 2

    def run_program(self):
        while self.inst_ptr < len(self.program):
            op = self.program[self.inst_ptr+1]
            if op in range(4, 7):
                self.combo_map[op] = self.registers['ABC'[op - 4]]

            result = self.opcodes[self.program[self.inst_ptr]](op)
            if result or result == 0:
                self.output.append(result)

    def find_quine(self):
        def inner_search(a, sig_digit):
            if sig_digit > len(self.program):
                return a

            for i in range(8):
                # this shifts a to the left 3 bits, then adds i to the octal
                # representation then converts it all back to decimal.
                new_a = int((oct(a) + str(i))[2:], 8)
                self.reset(a=new_a)
                self.run_program()
                if self.output[-sig_digit:] == self.program[-sig_digit:]:
                    result = inner_search(new_a, sig_digit + 1)
                    if result:
                        return result

            return None

        return inner_search(0, 1)


if __name__ == '__main__':
    filename = 'input/Day17.txt'
    data = read_file(filename)
    index = data.index('')

    device = Device(data[:index], data[index+1:][0])
    device.run_program()
    print(f"The answer to part 1 is {device.answer_pt1}")

    print(f"The answer to Part 2 is {device.find_quine()}")


