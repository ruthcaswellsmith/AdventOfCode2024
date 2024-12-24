from typing import List, Dict
from utils import read_file
from functools import lru_cache


NUMERIC_KEYPAD = {
            'A': {'<': '0', '^': '3'},
            '0': {'^': '2', '>': 'A'},
            '1': {'^': '4', '>': '2'},
            '2': {'v': '0', '<': '1', '>': '3', '^': '5'},
            '3': {'v': 'A', '<': '2', '^': '6'},
            '4': {'v': '1', '>': '5', '^': '7'},
            '5': {'v': '2', '<': '4', '>': '6', '^': '8'},
            '6': {'v': '3', '<': '5', '^': '9'},
            '7': {'v': '4', '>': '8'},
            '8': {'v': '5', '<': '7', '>': '9'},
            '9': {'v': '6', '<': '8'},
        }

DIRECTIONAL_KEYPAD = {
            'A': {'<': '^', 'v': '>'},
            '>': {'^': 'A', '<': 'v'},
            '<': {'>': 'v'},
            '^': {'>': 'A', 'v': 'v'},
            'v': {'<': '<', '^': '^', '>': '>'}
        }


class Keypad:
    def __init__(self, keypad: Dict):
        self.keypad = keypad
        self.graph, self.directions = self.get_graph_and_directions()
        self.distances, self.next = self.floyd_warshall()
        self.shortest_paths = self.get_shortest_paths()

    def get_graph_and_directions(self):
        graph, directions = {}, {}
        for button, neighbors in self.keypad.items():
            graph[button] = list(neighbors.values())
            for d, b in neighbors.items():
                directions[f"{button}{b}"] = d
        return graph, directions

    def get_shortest_paths(self):
        shortest_paths = {}
        for n1 in self.graph:
            for n2 in self.graph:
                if n1 != n2:
                    paths = self.reconstruct_paths(n1, n2, set())
                    shortest_paths[f"{n1}{n2}"] = [self.translate_path(path) for path in paths]
        return shortest_paths

    def floyd_warshall(self):
        dist = {node: {n: float('inf') for n in self.graph} for node in self.graph}
        next = {node: {n: [] for n in self.graph} for node in self.graph}
        for node in self.graph:
            dist[node][node] = 0
            for n in self.graph[node]:
                dist[node][n] = 1
                next[node][n].append(n)

        for k in self.graph:
            for i in self.graph:
                for j in self.graph:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next[i][j] = next[i][k].copy()
                    elif dist[i][j] == dist[i][k] + dist[k][j] and k != j and k != i:
                        next[i][j].extend(next[i][k])
        return dist, next

    def reconstruct_paths(self, path, end, visited):
        if path[-1] == end:
            return [path]
        paths = []
        for neighbor in self.next[path[-1]][end]:
            if neighbor not in visited:
                if neighbor not in path:
                    visited.add(neighbor)
                    paths.extend(self.reconstruct_paths(path + neighbor, end, visited.copy()))
        return paths

    def translate_path(self, path: str):
        translated_path = ''
        for pair in [(path[i:i+2]) for i in range(len(path) - 1)]:
            translated_path += self.directions[pair]
        return translated_path


class Door:
    def __init__(self, data: List[str], num_robots: int):
        self.codes = data
        self.num_robots = num_robots
        numeric = Keypad(NUMERIC_KEYPAD)
        directional = Keypad(DIRECTIONAL_KEYPAD)
        self.keypads = [numeric] + [directional] * num_robots
        self.code_to_buttons = {}
        self.min_lengths = {}

    @property
    def answer(self):
        return sum([length * int(code[:-1]) for code, length in self.min_lengths.items()])

    def find_min_lengths(self):
        for code in self.codes:
            self.min_lengths[code] = self.find_min_length(code, 0)

    @lru_cache()
    def find_min_length(self, buttons: str, level: int):
        if level == self.num_robots + 1:
            return len(buttons)

        min_length, buttons = 0, 'A' + buttons
        for pair in [buttons[i:i+2] for i in range(len(buttons) - 1)]:
            paths = self.keypads[level].shortest_paths.get(pair, "")
            min_lengths = [self.find_min_length(p + 'A', level + 1) for p in paths]
            if min_lengths:
                min_length += min(min_lengths)
            else:   # We're pushing same button twice so not traveling but it results in an A
                min_length += 1
        return min_length


if __name__ == '__main__':
    filename = 'input/Day21.txt'
    data = read_file(filename)

    door = Door(data, 2)
    door.find_min_lengths()
    print(f"The answer to part 1 is {door.answer}.")

    door = Door(data, 25)
    door.find_min_lengths()
    print(f"The answer to part 2 is {door.answer}.")
