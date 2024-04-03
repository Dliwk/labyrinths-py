"""Main windowing module, defines the global surface."""

import abc
import sys
from abc import abstractmethod

import pygame


class Widget(abc.ABC):
    def __init__(self, parent: "Widget | None", width: int, height: int, x: int, y: int) -> None:
        self.surface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.coordinates = (x, y)
        self.children: list[Widget] = []

        self.parent = parent
        if self.parent:
            # noinspection PyUnresolvedReferences
            self.parent.children.append(self)

        self.hidden = False

    @abstractmethod
    def render(self) -> None: ...

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def on_keydown(self, key: int) -> None:
        pass

    def on_keyup(self, key: int) -> None:
        pass

    def on_keydown_propagate(self, key: int) -> None:
        self.on_keydown(key)
        for child in self.children:
            child.on_keydown_propagate(key)

    def on_keyup_propagate(self, key: int) -> None:
        self.on_keyup(key)
        for child in self.children:
            child.on_keyup_propagate(key)

    def render_self_and_children(self, surface: pygame.Surface, real_coords: tuple[int, int]) -> None:
        if self.hidden:
            return
        self.surface.fill((0, 0, 0))
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

    def on_mouse_left_click(self) -> None:
        pass

    def on_mouse_click_check(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            for child in reversed(self.children):
                if child.on_mouse_click_check(x - child.coordinates[0], y - child.coordinates[1]):
                    break
            else:
                self.on_mouse_left_click()
                return True
        return False


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

    def on_mouse_left_click(self, x: int, y: int) -> None:
        self.root_widget.on_mouse_click_check(x, y)

    def run(self) -> None:
        """Run the event loop."""
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.KEYDOWN:
                        self.root_widget.on_keydown_propagate(event.key)
                    case pygame.KEYUP:
                        self.root_widget.on_keyup_propagate(event.key)
                    case pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.on_mouse_left_click(*event.pos)
            self.render()
            pygame.display.flip()
