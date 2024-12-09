from typing import List
from itertools import groupby

from utils import read_file, Part


class DiskMap:
    def __init__(self, data: List[str]):
        self.map = data[0]
        self.expanded = []
        self.compacted = []
        self.id = 0

    @staticmethod
    def num_free_spaces(input_list: List[str], reverse=False):
        input_copy = input_list.copy()
        if reverse:
            input_copy.reverse()
        count = 0
        for item in input_copy:
            if item == '.':
                count += 1
            else:
                break
        return count

    @staticmethod
    def num_digits(input_list: List[str], reverse=False):
        input_copy = input_list.copy()
        if reverse:
            input_copy.reverse()
        count = 0
        for item in input_copy:
            if item.isdigit():
                count += 1
            else:
                break
        return count

    @staticmethod
    def count_free_spaces(input_list: List[str]):
        # only search to the left of the occurrence of file
        counts, indices = [], []
        current_index = 0
        for key, group in groupby(input_list):
            group_len = len(list(group))
            if key == ".":
                counts.append(group_len)
                indices.append(current_index)
            current_index += group_len
        return counts, indices

    def expand(self):
        working = self.map[:]
        while True:
            for i in range(int(working[0])):
                self.expanded.append(str(self.id))
            self.id += 1
            if len(working) < 2:
                break
            for i in range(int(working[1])):
                self.expanded.append('.')
            working = working[2:]

    def compact(self, part: Part):
        if part == Part.PT1:
            self.compact_part1()
        else:
            self.compact_part2()

    def compact_part1(self):
        working = self.expanded.copy()
        while '.' in working:
            print(len(working))
            # put beginning in compacted string
            first_dot = working.index('.')
            self.compacted += working[:first_dot]
            working = working[first_dot:]
            # fill free spaces as much as we can
            free_spaces_at_beg = self.num_free_spaces(working)
            numbers_at_end = self.num_digits(working, reverse=True)
            for i in range(min(free_spaces_at_beg, numbers_at_end)):
                # move numbers
                self.compacted.append(working[-1])
                working = working[:-1]
                working = working[1:]
            # Remove trailing free spaces
            free_spaces_at_end = self.num_free_spaces(working, reverse=True)
            if free_spaces_at_end > 0:
                working = working[:-free_spaces_at_end]

        self.compacted += working

    def compact_part2(self):
        id = (len(self.map) - 1) // 2
        self.compacted = self.expanded.copy()
        for id in range(id, 0, -1):
            # See if we can move this file
            file_len = int(self.map[id * 2])
            file = [str(id)] * file_len
            for file_index, ele in enumerate(self.compacted):
                if ele == str(id):
                    break

            counts, indices = self.count_free_spaces(self.compacted[:file_index])
            for i, count in enumerate(counts):
                if count >= file_len:
                    # move this file
                    # replace the file with free spaces
                    for j in range(len(self.compacted) - file_len + 1):
                        if self.compacted[j:j + file_len] == file:
                            self.compacted[j:j + file_len] = ['.'] * file_len
                    self.compacted = self.compacted[:indices[i]] + file + \
                        self.compacted[indices[i] + file_len:]
                    break

    def get_checksum(self):
        checksum = 0
        for i in range(len(self.compacted)):
            if self.compacted[i] != '.':
                checksum += i * int(self.compacted[i])
        return checksum


if __name__ == '__main__':
    filename = 'input/Day9.txt'
    data = read_file(filename)

    diskmap = DiskMap(data)
    diskmap.expand()
    diskmap.compact(Part.PT1)
    print(f"The answer to part 1 is {diskmap.get_checksum()}")

    diskmap = DiskMap(data)
    diskmap.expand()
    diskmap.compact(Part.PT2)
    print(f"The answer to part 2 is {diskmap.get_checksum()}")

