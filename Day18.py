from typing import List
import heapq

import numpy as np

from utils import read_file


class MemorySpace:
    def __init__(self, data: List[str], max_dim: int, num_bytes: int):
        self.data = data
        self.max_dim = max_dim
        self.map = np.zeros((self.max_dim + 1, self.max_dim + 1), dtype=int)
        for line in self.data[:num_bytes]:
            byte = [int(ele) for ele in line.split(',')]
            self.map[tuple(byte)] = 1
        self.start, self.end = (0, 0), (self.max_dim, self.max_dim)
        self.nodes = self.get_nodes()
        self.unvisited = []
        self.visited = set()
        self.costs = {node: float('inf') for node in self.nodes.keys()}
        self.costs[self.start] = 0
        heapq.heappush(self.unvisited, (0, self.start))

    def reset(self, num_bytes: int):
        byte = tuple([int(ele) for ele in self.data[num_bytes-1].split(',')])
        self.map[byte] = 1
        for adj_list in self.nodes.values():
            if byte in adj_list:
                adj_list.remove(byte)
        del self.nodes[byte]
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

    def find_blocking_byte(self):
        for num_bytes in range(1025, len(self.data)):
            memory_space.reset(num_bytes)
            cost = memory_space.find_shortest_path()
            if cost == float('inf'):
                break
        return self.data[num_bytes-1]


if __name__ == '__main__':
    filename = 'input/Day18.txt'
    data = read_file(filename)

    memory_space = MemorySpace(data, 70, 1024)
    print(f"The answer to part 1 is {memory_space.find_shortest_path()}")

    print(f"The answer to part 2 is {memory_space.find_blocking_byte()}")
