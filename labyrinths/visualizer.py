"""Simple module to visualize maze using pygame"""

import sys

import pygame
from pygame import draw

from labyrinths.generators.dfs import DepthFirstSearchGenerator
from labyrinths.labyrinth import LabyrinthData, WallKind
from labyrinths.mazeloader import dump_maze

pygame.init()
pygame.font.init()


class Visualizer:
    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cellwidth = 50 if columns < 10 else 20 if columns < 60 else 10 if columns < 120 else 5
        self.cellheight = 50 if rows < 10 else 20 if rows < 40 else 10 if rows < 80 else 5
        self.cellwidth = self.cellheight = min(self.cellwidth, self.cellheight)
        self.wallwidth = 1

        self.globalwidth = self.columns * self.cellwidth + self.cellwidth * 2
        self.globalheight = self.rows * self.cellheight + self.cellheight * 2
        self.globalscreen = pygame.display.set_mode(
            (self.globalwidth, self.globalheight)
        )
        self.globalscreen.fill('white')
        self.screen = self.globalscreen.subsurface(
            pygame.Rect(self.cellwidth, self.cellheight, self.columns * self.cellwidth, self.rows * self.cellheight))

        self.font = pygame.font.Font(None, self.cellheight)

        self.current_maze: LabyrinthData | None = None

    def draw_maze(self, maze: LabyrinthData) -> None:
        self.current_maze = maze

        for i in range(maze.columns):
            for j in range(maze.rows):
                x, y = i * self.cellwidth, (maze.rows - j - 1) * self.cellheight
                dx, dy = self.cellwidth, self.cellheight
                draw.rect(
                    self.screen,
                    'white',
                    pygame.Rect(x, y, dx, dy),
                    0,
                )
                celldata = maze.field[i][j]
                if celldata.left is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        'black',
                        pygame.Rect(x, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.right is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        'black',
                        pygame.Rect(x + dx - self.wallwidth, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.up is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        'black',
                        pygame.Rect(x, y, dx, self.wallwidth),
                        0,
                    )
                if celldata.down is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        'black',
                        pygame.Rect(x, y + dy - self.wallwidth, dx, self.wallwidth),
                        0,
                    )

    def new_maze(self) -> None:
        generator = DepthFirstSearchGenerator(self.columns, self.rows)
        algoname = 'Depth First Search'

        maze = generator.generate()
        self.draw_maze(maze)

        self.set_algoname(algoname)

    def set_algoname(self, algoname: str) -> None:
        draw.rect(self.globalscreen, 'white',
                  pygame.Rect(0, self.globalheight - self.cellheight, self.globalwidth, self.cellheight))
        text = self.font.render(algoname, True, 'black')
        self.globalscreen.blit(text, (0, self.globalheight - self.cellheight))

    def run(self, maze: LabyrinthData | None = None):
        pygame.display.set_caption('Labyrinths')

        text = self.font.render('Mouse click to generate a maze! Press space to save to file', True, 'black')
        self.globalscreen.blit(text, (0, 0))

        if maze is not None:
            self.draw_maze(maze)
            self.set_algoname('Loaded from file')
        else:
            self.new_maze()

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.MOUSEBUTTONDOWN:
                        self.new_maze()
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            dump_maze(self.current_maze, 'maze.json.gz')

                pygame.display.flip()
