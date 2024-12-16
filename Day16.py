from typing import List
from collections import defaultdict

import numpy as np
import heapq

from utils import read_file

# Right, Down, Left, Up
DIRECTIONS = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
DIRECTIONS_TO_GO = {
    0: [0, 1, 3],
    1: [1, 0, 2],
    2: [2, 1, 3],
    3: [3, 0, 2]
}
OPPOSITE_DIRECTIONS = {0: 2, 1: 3, 2: 0, 3: 1}


class Maze:
    def __init__(self, data: List[str]):
        self.data = np.array([[c for c in line] for line in data])
        self.start = self.get_start()
        self.ends = self.get_ends()
        self.unvisited = []
        self.visited = set()
        self.all_paths = []
        self.best_tiles = set()
        self.previous = defaultdict(list)

        self.nodes, self.edge_costs = self.get_nodes()
        self.costs = {node: float('inf') for node in self.nodes.keys()}
        self.costs[self.start] = 0
        self.min_cost = float('inf')
        heapq.heappush(self.unvisited, (0, self.start))

    def get_start(self):
        result = np.where(self.data == 'S')
        return result[0][0], result[1][0], 0

    def get_ends(self):
        ends = []
        result = np.where(self.data == 'E')
        for i in range(len(result[0])):
            row, col = result[0][i], result[1][i]
            for dir_id in DIRECTIONS.keys():
                dr, dc = DIRECTIONS[OPPOSITE_DIRECTIONS[dir_id]]
                if self.data[row + dr, col + dc] != '#':
                    ends.append((row, col, dir_id))
        return ends

    def get_nodes(self):
        nodes, edge_costs = {}, {}
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] != '#':
                    for dir_id in DIRECTIONS.keys():
                        dr, dc = DIRECTIONS[OPPOSITE_DIRECTIONS[dir_id]]
                        # We can only be facing this way if we don't have a wall behind us
                        # (or we are at the start)
                        if self.data[row + dr][col + dc] != '#' or (row, col, dir_id) == self.start:
                            adj_list = []

                            for dir_to_go in DIRECTIONS_TO_GO[dir_id]:
                                dr, dc = DIRECTIONS[dir_to_go]
                                if self.data[row + dr][col + dc] != '#':
                                    adj_list.append((row + dr, col + dc, dir_to_go))
                                    edge_costs[(row, col, dir_id), (row + dr, col + dc, dir_to_go)] = 1 \
                                        if dir_to_go == dir_id else 1001
                            nodes[(row, col, dir_id)] = adj_list

        return nodes, edge_costs

    def find_shortest_path(self):
        while self.unvisited:
            current_cost, current_node = heapq.heappop(self.unvisited)

            if all([end in self.visited for end in self.ends]):
                break

            if current_node not in self.visited:
                self.visited.add(current_node)

                neighbors = [n for n in self.nodes[current_node] if n not in self.visited]
                for n in neighbors:
                    cost = self.edge_costs[(current_node, n)]
                    new_cost = current_cost + cost
                    if new_cost <= self.costs[n]:
                        self.costs[n] = new_cost
                        heapq.heappush(self.unvisited, (new_cost, n))
                        self.previous[n].append(current_node)

        self.min_cost = min([self.costs[end] for end in self.ends])

    def reconstruct_shortest_paths(self):
        def dfs(node, current_path):
            if node == self.start:
                self.all_paths.append(current_path[::-1])
                return
            for prev in self.previous[node]:
                dfs(prev, current_path + [prev])

        for end in self.ends:
            if self.costs[end] == self.min_cost:
                dfs(end, [end])

    def get_best_tiles(self):
        for path in self.all_paths:
            for node in path:
                self.best_tiles.add((node[0], node[1]))


if __name__ == '__main__':
    filename = 'input/Day16.txt'
    data = read_file(filename)

    maze = Maze(data)
    maze.find_shortest_path()
    print(f"The answer to part 1 is {maze.min_cost}")

    maze.reconstruct_shortest_paths()
    maze.get_best_tiles()
    print(f"The answer to part 2 is {len(maze.best_tiles)}")
