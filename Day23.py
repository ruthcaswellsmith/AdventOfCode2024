from typing import List, Set
from collections import defaultdict
from utils import read_file


class NetworkMap:
    def __init__(self, data: List[str]):
        self.graph = defaultdict(set)
        self.nodes = set()
        for line in data:
            n1, n2 = line.split('-')
            self.nodes.add(n1); self.nodes.add(n2)
            self.graph[n1].add(n2); self.graph[n2].add(n1)
        self.cycles = set()
        self.maximal_cliques = set()

    @property
    def password(self):
        return ','.join(self.largest_clique)

    @property
    def largest_clique(self):
        max_size, max_clique = 0, None
        for c in self.maximal_cliques:
            if len(c) > max_size:
                max_size = len(c); max_clique = c
        return max_clique

    @property
    def cycles_with_t(self):
        return sum([any([n[0] == 't' for n in cycle]) for cycle in self.cycles if len(cycle) == 3])

    def find_cycles(self):
        for n in self.nodes:
            self.dfs(n, [], set())

    def dfs(self, node, path: List, visited: Set):
        visited.add(node)
        path.append(node)

        if len(path) > 2:
            if path[0] in self.graph[path[-1]]:
                self.cycles.add(tuple(sorted(path)))
            return

        for n in self.graph[node]:
            if n not in visited:
                self.dfs(n, path.copy(), visited.copy())

    def find_maximal_cliques(self):
        self.bk(set(), self.nodes, set())

    def bk(self, r, p, x):
        if not p and not x:
            self.maximal_cliques.add(tuple(sorted(r)))

        while p:
            n = next(iter(p))
            new_r = r.copy()
            new_r.add(n)
            self.bk(new_r, p.intersection(self.graph[n]), x.intersection(self.graph[n]))
            p.remove(n)
            x.add(n)


if __name__ == '__main__':
    filename = 'input/Day23.txt'
    data = read_file(filename)

    network_map = NetworkMap(data)
    network_map.find_cycles()
    print(f"The answer to part 1 is {network_map.cycles_with_t}.")

    network_map.find_maximal_cliques()
    print(f"The answer to part 2 is {network_map.password}.")
