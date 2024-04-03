"""Main windowing module, defines the global surface."""

import abc
import sys
from abc import abstractmethod

import pygame


class Widget(abc.ABC):
    def __init__(self, parent: "Widget | None", width: int, height: int, x: int, y: int) -> None:
        self.surface = pygame.Surface((width, height))
        self.coordinates = (x, y)
        self.children: list[Widget] = []

        self.parent = parent
        if self.parent:
            # noinspection PyUnresolvedReferences
            self.parent.children.append(self)

    @abstractmethod
    def render(self) -> None: ...

    def render_self_and_children(self, surface: pygame.Surface, real_coords: tuple[int, int]) -> None:
        self.render()
        coords = (real_coords[0] + self.coordinates[0], real_coords[1] + self.coordinates[1])
        surface.blit(self.surface, coords)
        for child in self.children:
            child.render_self_and_children(surface, coords)

    def close(self):
        for child in self.children:
            child.close()
        if self.parent:
            self.parent.children.remove(self)


class RootWidget(Widget):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(None, width, height, 0, 0)

    def render(self) -> None:
        self.surface.fill((0, 0, 0))


class MainWindow:
    """Main window class."""

    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.root_widget: RootWidget = RootWidget(self.width, self.height)

    def render(self) -> None:
        """Render everything."""
        self.root_widget.render_self_and_children(self.screen, (0, 0))

    def run(self):
        """Run the event loop."""
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            self.render()
            pygame.display.flip()
