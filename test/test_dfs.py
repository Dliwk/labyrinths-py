"""Test generators/dfs.py"""

import pytest
from generators_common import check_maze_has_solution, check_maze_is_correctly_formed

from labyrinths.generators.dfs import DepthFirstSearchGenerator


@pytest.fixture
def gen2_4() -> DepthFirstSearchGenerator:
    return DepthFirstSearchGenerator(2, 4)


@pytest.fixture
def gen3_2() -> DepthFirstSearchGenerator:
    return DepthFirstSearchGenerator(3, 2)


@pytest.fixture
def gen1_2() -> DepthFirstSearchGenerator:
    return DepthFirstSearchGenerator(1, 2)


@pytest.fixture
def gen(request: pytest.FixtureRequest) -> DepthFirstSearchGenerator:
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("gen", ["gen2_4", "gen3_2", "gen1_2"], indirect=True)
def test_dfs_generator(gen: DepthFirstSearchGenerator) -> None:
    maze = gen.generate()
    check_maze_is_correctly_formed(maze)


@pytest.mark.parametrize("gen", ["gen2_4", "gen3_2", "gen1_2"], indirect=True)
def test_dfs_has_solution(gen: DepthFirstSearchGenerator) -> None:
    maze = gen.generate()
    check_maze_has_solution(maze)
