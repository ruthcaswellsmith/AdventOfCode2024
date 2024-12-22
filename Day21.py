from typing import List, Dict
from utils import read_file
from functools import lru_cache
from itertools import product


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
        self.distances, self.next = self.find_shortest_paths()
        self.shortest_paths = self.get_shortest_paths()

    @lru_cache
    def get_graph_and_directions(self):
        graph, directions = {}, {}
        for button, neighbors in self.keypad.items():
            graph[button] = list(neighbors.values())
            for d, b in neighbors.items():
                directions[f"{button}-{b}"] = d
        return graph, directions

    @lru_cache
    def find_shortest_paths(self):
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

    def reconstruct_paths(self, start, end, path=None, visited=None):
        if path is None:
            path = [start]
        if visited is None:
            visited = set()
        if path[-1] == end:
            return [path]
        paths = []
        for neighbor in self.next[path[-1]][end]:
            if neighbor not in visited:
                if neighbor not in path:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    paths.extend(self.reconstruct_paths(neighbor, end, new_path, visited.copy()))
        return paths

    @lru_cache
    def get_shortest_paths(self):
        shortest_paths = {}
        for n1 in self.graph:
            for n2 in self.graph:
                shortest_paths[(n1, n2)] = self.reconstruct_paths(n1, n2)
        return shortest_paths


class Door:
    def __init__(self, data: List[str], num_robots: int):
        self.codes = data
        self.numeric = Keypad(NUMERIC_KEYPAD)
        self.directionals = [Keypad(DIRECTIONAL_KEYPAD) for _ in range(num_robots)]
        self.code_to_buttons = {}

    @property
    def answer_pt1(self):
        answer = 0
        for code, list_of_buttons in self.code_to_buttons.items():
            shortest = min([len(b) for b in list_of_buttons])
            answer += shortest * int(code[:-1])
        return answer

    def process_codes(self):
        for code in self.codes:
            self.process_code(code)

    @lru_cache()
    def process_code(self, code: str):
        list_of_buttons = [code]
        self.code_to_buttons[code] = []
        for k_ind, keypad in enumerate([self.numeric] + self.directionals):
            next_level_buttons = []
            for buttons in list_of_buttons:
                buttons = 'A' + buttons
                new_buttons = []
                for i in range(len(buttons) - 1):
                    new_buttons.append(keypad.shortest_paths[(buttons[i], buttons[i + 1])])

                for buttons_combo in list(product(*new_buttons)):
                    buttons = ''
                    for p in buttons_combo:
                        buttons += ''.join(
                            keypad.directions[f"{p[j]}-{p[j + 1]}"]
                            for j in range(len(p) - 1)) + 'A'
                    next_level_buttons.append(buttons)
            list_of_buttons = next_level_buttons
            print(code, k_ind + 1, len(list_of_buttons))
            if k_ind == 2:
                self.code_to_buttons[code].extend(list_of_buttons)


if __name__ == '__main__':
    filename = 'input/Day21-test.txt'
    data = read_file(filename)

    door = Door(data, 2)
    door.process_codes()
    print(f"The answer to part 1 is {door.answer_pt1}.")

