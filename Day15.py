from typing import List, Tuple
import itertools

import numpy as np

from utils import read_file

MOVES = {'<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0)}
CHARS = {'O': 0, '#': 8, '.': -1, '@': 4}
CHARS2 = {'O': [1, 2], '#': [8, 8], '.': [-1, -1], '@': [4, -1]}


class Warehouse:
    def __init__(self, grid: List[str]):
        self.grid = np.array(
            [[CHARS[ele] for ele in line] for line in grid],
            dtype=int
        )
        self.max_x, self.max_y = len(grid) - 1, len(grid[0]) - 1
        self.robot = [
            int(np.where(self.grid == CHARS['@'])[0][0]),
            int(np.where(self.grid == CHARS['@'])[1][0])
        ]

    @property
    def box_coords(self):
        box_coords = 100 * np.where(self.grid == CHARS['O'])[0] + np.where(self.grid == CHARS['O'])[1]
        return box_coords

    def extract_array(self, move: str):
        row, col = self.robot
        if move == '>':
            return self.grid[row, col + 1:]
        elif move == '<':
            return self.grid[row, :col][::-1]
        elif move == 'v':
            return self.grid[row + 1:, col]
        else:
            return self.grid[:row, col][::-1]

    def push_boxes(self, move: str):
        ahead = self.extract_array(move)

        # Look up to the first wall
        before_wall = ahead[:np.where(ahead == CHARS['#'])[0][0]]
        space_ahead = np.where(before_wall == CHARS['.'])
        if space_ahead[0].size > 0:
            # transpose the portion of the array up to and inc first space
            ahead[:space_ahead[0][0] + 1] = ahead[:space_ahead[0][0] + 1][::-1]

    def move_robot(self, moves: str):
        while moves:
            move = moves[0]
            new_pos = (self.robot[0] + MOVES[move][0], self.robot[1] + MOVES[move][1])
            if self.grid[new_pos] == CHARS['O']:
                self.push_boxes(move)

            if self.grid[new_pos] == CHARS['.']:
                self.grid[tuple(self.robot)] = CHARS['.']
                self.robot = list(new_pos)
                self.grid[new_pos] = CHARS['@']

            moves = moves[1:]


class Warehouse2:
    def __init__(self, grid: List[str]):
        self.grid = np.array(
            [list(itertools.chain.from_iterable([CHARS2[ele] for ele in line])) for line in grid],
            dtype=int
        )
        self.max_x, self.max_y = len(grid) - 1, len(grid[0]) - 1
        self.robot = [
            int(np.where(self.grid == CHARS['@'])[0][0]),
            int(np.where(self.grid == CHARS['@'])[1][0])
        ]

    @property
    def box_coords(self):
        box_coords = 100 * np.where(self.grid == CHARS2['O'][0])[0] + np.where(self.grid == CHARS2['O'][0])[1]
        return box_coords

    def extract_array(self, move: str):
        row, col = self.robot
        if move == '>':
            return self.grid[row, col + 1:]
        elif move == '<':
            return self.grid[row, :col][::-1]
        elif move == 'v':
            return self.grid[row + 1:, col]
        else:
            return self.grid[:row, col][::-1]

    def push_right_or_left(self, move: str):
        ahead = self.extract_array(move)
        wall = np.where(ahead == CHARS['#'])[0][0]
        before_wall = ahead[:wall]
        wall_on = ahead[wall:]
        space_ahead = np.where(before_wall == CHARS['.'])
        if space_ahead[0].size > 0:
            # move the space to the beginning
            free_space = space_ahead[0][0]
            ahead[:] = np.concatenate(([-1], before_wall[:free_space], before_wall[free_space+1:], wall_on))

    def can_push_up_or_down(self, pos: Tuple[int, int], move: str, partner_checked: bool):
        can_push = True
        while can_push:
            dr, dc = MOVES[move]
            new_pos = (pos[0] + dr, pos[1] + dc)
            if self.grid[new_pos] in CHARS2['#']:
                return False
            elif self.grid[new_pos] in CHARS2['O']:
                can_push = self.can_push_up_or_down(new_pos, move, False)
            else:
                pass

            if can_push and not partner_checked:
                # check other side of box
                if self.grid[pos] == CHARS2['O'][0]:
                    can_push = self.can_push_up_or_down((pos[0], pos[1] + 1), move, True)
                else:
                    can_push = self.can_push_up_or_down((pos[0], pos[1] - 1), move, True)

            return can_push

    def push_up_or_down(self, pos: Tuple[int, int], move: str, partner_moved: bool):
        dr, dc = MOVES[move]
        new_pos = (pos[0] + dr, pos[1] + dc)
        if self.grid[new_pos] in CHARS2['O']:
            self.push_up_or_down(new_pos, move, False)
        if not partner_moved:
            if self.grid[pos] == CHARS2['O'][0]:
                self.push_up_or_down((pos[0], pos[1] + 1), move, True)
            else:
                self.push_up_or_down((pos[0], pos[1] - 1), move, True)

        self.grid[new_pos] = self.grid[pos]
        self.grid[pos] = CHARS2["."][0]

    def move_robot(self, moves: str):
        while moves:
            move = moves[0]
            new_pos = (self.robot[0] + MOVES[move][0], self.robot[1] + MOVES[move][1])
            if self.grid[new_pos] in CHARS2['O']:
                if move in ['<', '>']:
                    self.push_right_or_left(move)
                else:
                    can_push = self.can_push_up_or_down(new_pos, move, False)
                    if can_push:
                        self.push_up_or_down(new_pos, move, False)

            if self.grid[new_pos] == CHARS2['.'][0]:
                self.grid[tuple(self.robot)] = CHARS2['.'][0]
                self.robot = list(new_pos)
                self.grid[new_pos] = CHARS2['@'][0]

            moves = moves[1:]


if __name__ == '__main__':
    filename = 'input/Day15.txt'
    data = read_file(filename)
    index = data.index('')

    warehouse = Warehouse(data[:index])
    warehouse.move_robot("".join(data[index+1:]))
    print(f"The answer to part 1 is {np.sum(warehouse.box_coords)}")

    warehouse = Warehouse2(data[:index])
    warehouse.move_robot("".join(data[index+1:]))
    print(f"The answer to part 2 is {np.sum(warehouse.box_coords)}")
