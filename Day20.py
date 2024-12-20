from typing import List
import heapq
import numpy as np

from collections import defaultdict

from utils import read_file


class RaceTrack:
    def __init__(self, data: List[str]):
        self.grid = np.array([[ele for ele in list] for list in data])
        self.max_row, self.max_col = len(data), len(data[0])
        self.start = tuple(np.argwhere(self.grid == 'S')[0])
        self.end = tuple(np.argwhere(self.grid == 'E')[0])
        for pos in [self.start, self.end]:
            self.grid[pos] = "."
        self.nodes = self.get_nodes()
        self.predecessors = {node: [] for node in self.nodes}
        self.unvisited = []
        self.visited = set()
        self.costs = {node: float('inf') for node in self.nodes.keys()}
        self.costs[self.start] = 0
        heapq.heappush(self.unvisited, (0, self.start))
        self.shortest_path = {}
        self.cheats = {}

    def manhattan(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_nodes(self):
        nodes = {}
        for row in range(1, self.max_row - 1):
            for col in range(1, self.max_col - 1):
                if self.grid[(row, col)] != '#':
                    adj_list = []
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        new_pos = (row + dx, col + dy)
                        if self.grid[new_pos] != '#':
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
                    new_cost = current_cost + 1
                    if new_cost < self.costs[n]:
                        self.costs[n] = new_cost
                        self.nodes[current_node] = n
                        self.predecessors[n] = [current_node]
                        heapq.heappush(self.unvisited, (new_cost, n))
                    elif new_cost == self.costs[n]:
                        self.predecessors[n].append([current_node])

        return self.costs[self.end]

    def reconstruct_shortest_path(self):
        current, path = self.end, []
        for i in range(self.find_shortest_path()):
            path.append(current)
            current = self.predecessors[current][0]
        path.append(self.start)
        path.reverse()

        for i, coords in enumerate(path):
            self.shortest_path[coords] = i

    def determine_cheats(self, max_cheat: int):
        for n1 in self.shortest_path.keys():
            # get all nodes on the shortest path within the manhattan distance
            for dx in range(-max_cheat, max_cheat + 1):
                for dy in range(-(max_cheat - abs(dx)), max_cheat - abs(dx) + 1):
                    n2 = (n1[0] + dx, n1[1] + dy)
                    if n1 != n2 and n2 in self.shortest_path and (n2, n1) not in self.cheats:
                        d = self.manhattan(n1, n2)
                        saving = abs(self.shortest_path[n1] - self.shortest_path[n2]) - d
                        if saving > 0:
                            self.cheats[(n1, n2)] = saving

    def count_cheats(self, min_savings: int):
        savings_counts = defaultdict(int)
        for value in self.cheats.values():
            savings_counts[value] += 1

        return sum([count for saving, count in savings_counts.items() if saving >= min_savings])


if __name__ == '__main__':
    filename = 'input/Day20.txt'
    data = read_file(filename)

    race_track = RaceTrack(data)

    race_track.reconstruct_shortest_path()
    race_track.determine_cheats(2)
    print(f"The answer to part 1 is {race_track.count_cheats(100)}.")

    race_track.cheats = {}
    race_track.determine_cheats(20)
    print(f"The answer to part 2 is {race_track.count_cheats(100)}.")

