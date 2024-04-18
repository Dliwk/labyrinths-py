"""Test maze loading and dumping."""

from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.mazeloader import dump_maze, load_maze


def test_load_dump(tmp_path) -> None:
    maze = KruskalGenerator(2, 3).generate()
    path = tmp_path / "maze.json.gz"
    dump_maze(maze, path)
    loaded = load_maze(path)
    assert loaded == maze
