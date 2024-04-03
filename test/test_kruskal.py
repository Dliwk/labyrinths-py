"""Test generators/kruskal.py"""

import pytest
from generators_common import check_maze_has_solution, check_maze_is_correctly_formed

from labyrinths.generators.kruskal import DisjointSetUnion, KruskalGenerator


@pytest.fixture
def dsu() -> DisjointSetUnion:
    return DisjointSetUnion(5)


def test_dsu_empty(dsu: DisjointSetUnion) -> None:
    assert all(dsu.find(i) == i for i in range(5))


def test_dsu_union(dsu: DisjointSetUnion) -> None:
    dsu.union(0, 1)
    assert dsu.find(0) == dsu.find(1)
    assert dsu.find(1) != dsu.find(2)
    dsu.union(2, 0)
    assert dsu.find(1) == dsu.find(2)
    dsu.union(4, 3)
    assert dsu.find(4) == dsu.find(3)
    assert dsu.find(1) != dsu.find(4)


@pytest.fixture
def gen2_4() -> KruskalGenerator:
    return KruskalGenerator(2, 4)


@pytest.fixture
def gen3_2() -> KruskalGenerator:
    return KruskalGenerator(3, 2)


@pytest.fixture
def gen1_2() -> KruskalGenerator:
    return KruskalGenerator(1, 2)


@pytest.fixture
def gen(request: pytest.FixtureRequest) -> KruskalGenerator:
    return request.getfixturevalue(request.param)


#@pytest.mark.parametrize("gen", ["gen2_4", "gen3_2", "gen1_2"], indirect=True)
#def test_kruskal_generator(gen: KruskalGenerator) -> None:
#    maze = gen.generate()
#    check_maze_is_correctly_formed(maze)


#@pytest.mark.parametrize("gen", ["gen2_4", "gen3_2", "gen1_2"], indirect=True)
#def test_kruskal_has_solution(gen: KruskalGenerator) -> None:
#    maze = gen.generate()
#    check_maze_has_solution(maze)
