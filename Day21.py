from typing import List, Dict
from utils import read_file


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

    def get_graph_and_directions(self):
        graph, directions = {}, {}
        for button, neighbors in self.keypad.items():
            graph[button] = list(neighbors.values())
            for d, b in neighbors.items():
                directions[f"{button}-{b}"] = d
        return graph, directions

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
        self.directionals = [Keypad(DIRECTIONAL_KEYPAD) for i in range(num_robots)]
        self.code_to_buttons = {}

    @property
    def answer_pt1(self):
        return [(len(b), int(c[:-1])) for c, b in self.code_to_buttons.items()]

    def process_codes(self):
        for code in ['029A']:
            desired_path = 'A' + code
            buttons = ""
            for i in range(1, len(desired_path)):
                a_shortest_path = self.numeric.shortest_paths[(desired_path[i - 1], desired_path[i])][0]
                for j in range(1, len(a_shortest_path)):
                    buttons += self.numeric.directions[f"{a_shortest_path[j - 1]}-{a_shortest_path[j]}"]
                buttons += 'A'
            print(f"buttons {buttons}")

            for keypad in self.directionals:
                desired_path = 'A' + buttons
                buttons = ""
                for i in range(1, len(desired_path)):
                    a_shortest_path = keypad.shortest_paths[(desired_path[i - 1], desired_path[i])][0]
                    for j in range(1, len(a_shortest_path)):
                        buttons += keypad.directions[f"{a_shortest_path[j - 1]}-{a_shortest_path[j]}"]
                    buttons += 'A'
                print(f"buttons {buttons}")
            self.code_to_buttons[code] = buttons
            print(self.code_to_buttons[code])


if __name__ == '__main__':
    filename = 'input/Day21-test.txt'
    data = read_file(filename)

    door = Door(data, 2)
    door.process_codes()
    print(f"The answer to part 1 is {door.answer_pt1}.")

