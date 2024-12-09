from typing import List
from itertools import groupby

from utils import read_file


class DiskMapPt1:
    def __init__(self, data: List[str]):
        self.map = [int(ele) for ele in data[0]]
        self.pos = 0
        self.checksum = 0
        self.id_left = 0
        self.id_right = (len(self.map) - 1) // 2

    def update_checksum(self, id: int):
        self.checksum += self.pos * id
        self.pos += 1

    def compact(self):
        for i in range(self.map[0]):
            self.update_checksum(self.id_left)
        self.map = self.map[1:]

        while len(self.map):
            while self.map[0] > 0 and self.map[-1] > 0:
                self.map[0] -= 1
                self.map[-1] -= 1
                self.update_checksum(self.id_right)
            if self.map[0] == 0:
                self.map = self.map[1:]
                self.id_left += 1
                for i in range(self.map[0]):
                    self.update_checksum(self.id_left)
                self.map = self.map[1:]
            if self.map and self.map[-1] == 0:
                self.map = self.map[:-2]
                self.id_right -= 1


class DiskMapPt2:
    def __init__(self, data: List[str]):
        self.data = data[0]
        self.max_id = (len(data[0]) - 1) // 2
        self.map = [('0', int(self.data[0]))]
        self.data = self.data[1:]
        for i in range(1, self.max_id + 1):
            self.map.append(('.', int(self.data[0])))
            self.map.append((str(i), int(self.data[1])))
            self.data = self.data[2:]

    def get_checksum(self):
        checksum = 0
        pos = 0
        for char, length in self.map:
            if char != '.':
                for i in range(length):
                    checksum += int(char) * pos
                    pos += 1
            else:
                pos += length
        return checksum

    def combine_spaces(self):
        result = []
        for char, group in groupby(self.map, key=lambda x: x[0]):
            total_length = sum(length for _, length in group)
            result.append((char, total_length))
        return result

    def compact(self):
        for i in range(self.max_id, 0, -1):
            # Find this file
            for file_pos, (file_char, file_length) in enumerate(self.map):
                if file_char == str(i):
                    break

            move_file = False
            for pos, (char, length) in enumerate(self.map):
                if pos > file_pos:
                    # we don't move the file because it's to the right
                    break

                if char == '.':
                    if length >= file_length:
                        move_file = True
                        break

            if move_file:
                self.map[pos] = (file_char, file_length)
                if length > file_length:
                    self.map = self.map[:pos+1] + [('.', length - file_length)] + self.map[pos+1:]
                    file_pos += 1
                self.map[file_pos] = ('.', file_length)
                self.map = self.combine_spaces()


if __name__ == '__main__':
    filename = 'input/Day9.txt'
    data = read_file(filename)

    diskmap = DiskMapPt1(data)
    diskmap.compact()
    print(f"The answer to part 1 is {diskmap.checksum}")

    diskmap = DiskMapPt2(data)
    diskmap.compact()
    print(f"The answer to part 2 is {diskmap.get_checksum()}")

