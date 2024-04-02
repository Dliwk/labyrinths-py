import random
from dataclasses import dataclass
from typing import override

from labyrinths.generators.generator import LabyrinthGenerator
from labyrinths.labyrinth import LabyrinthData, WallKind


@dataclass
class Edge:
    source: (int, int)
    destination: (int, int)
    weight: float


class DisjointSetUnion:
    def __init__(self, n: int) -> None:
        self.parent = [i for i in range(n)]
        self.rank = [0 for _ in range(n)]

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            y = self.parent[x]
            self.parent[x] = self.parent[y]
            x = y
        return x

    def union(self, x: int, y: int) -> bool:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.rank[x] < self.rank[y]:
            self.parent[x] = y
        elif self.rank[x] > self.rank[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
            self.rank[y] += 1
        return True


class KruskalGenerator(LabyrinthGenerator):
    def __init__(self, columns: int, rows: int) -> None:
        super().__init__(columns, rows)

    def cell_id(self, x: int, y: int) -> int:
        return x * self.rows + y

    def cell_by_id(self, i: int) -> (int, int):
        return i // self.rows, i % self.rows

    @override
    def generate(self) -> LabyrinthData:
        edges: list[Edge] = []
        for i in range(self.columns):
            for j in range(self.rows):
                if i != self.columns - 1:
                    edges.append(Edge((i, j), (i + 1, j), random.random()))
                if j != self.rows - 1:
                    edges.append(Edge((i, j), (i, j + 1), random.random()))

        edges.sort(key=lambda e: e.weight)

        dsu = DisjointSetUnion(self.columns * self.rows)

        for edge in edges:
            if dsu.union(self.cell_id(*edge.source), self.cell_id(*edge.destination)):
                self.set_wall_at(
                    edge.source[0],
                    edge.source[1],
                    edge.destination[0] - edge.source[0],
                    edge.destination[1] - edge.source[1],
                    WallKind.EMPTY,
                )

        return self.current
