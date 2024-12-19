from typing import List
import heapq

import numpy as np

from utils import read_file

SPACE_SIZE = 70
MAX_BYTES_PT1 = 1024


class MemorySpace:
    def __init__(self, data: List[str], max_dim: int, max_bytes: int):
        self.bytes = [[int(ele) for ele in line.split(',')] for line in data]
        self.max_dim = max_dim
        self.max_bytes = max_bytes
        self.map = np.zeros((self.max_dim + 1, self.max_dim + 1), dtype=int)
        for byte in self.bytes[:self.max_bytes]:
            self.map[tuple(byte)] = 1
        self.start, self.end = (0, 0), (self.max_dim, self.max_dim)
        self.nodes = self.get_nodes()
        self.unvisited = []
        self.visited = set()
        self.costs = {node: float('inf') for node in self.nodes.keys()}
        self.costs[self.start] = 0
        heapq.heappush(self.unvisited, (0, self.start))

    def get_nodes(self):
        nodes = {}
        for row in range(self.max_dim + 1):
            for col in range(self.max_dim + 1):
                if self.map[(row, col)] != 1:
                    adj_list = []
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_pos = (row + dx, col + dy)
                        if 0 <= new_pos[0] <= self.max_dim and 0 <= new_pos[1] <= self.max_dim and \
                                self.map[new_pos] != 1:
                            adj_list.append(new_pos)
                    nodes[(row, col)] = adj_list

        return nodes

    def find_shortest_path(self):
        while self.unvisited:
            current_cost, current_node = heapq.heappop(self.unvisited)

            if self.end in self.visited:
                break

            if current_node not in self.visited:
                self.visited.add(current_node)

                neighbors = [n for n in self.nodes[current_node] if n not in self.visited]
                for n in neighbors:
                    cost = 1
                    new_cost = current_cost + cost
                    if new_cost <= self.costs[n]:
                        self.costs[n] = new_cost
                        heapq.heappush(self.unvisited, (new_cost, n))

        return self.costs[self.end]


if __name__ == '__main__':
    filename = 'input/Day18.txt'
    data = read_file(filename)

    memory_space = MemorySpace(data, SPACE_SIZE, MAX_BYTES_PT1)
    print(f"The answer to part 1 is {memory_space.find_shortest_path()}")

    low, high = MAX_BYTES_PT1 + 1, len(data) + 1
    while low < high:
        mid = (low + high) // 2
        memory_space = MemorySpace(data, SPACE_SIZE, mid)
        if memory_space.find_shortest_path() == float('inf'):
            high = mid
        else:
            low = mid + 1
    print(f"The answer to part 2 is {memory_space.bytes[low - 1]}")
