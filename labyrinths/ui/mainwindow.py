"""Main windowing module, defines the global surface."""

from __future__ import annotations

import abc
import enum
import sys
import weakref
from abc import abstractmethod
from typing import Any, Callable

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

    def toggle(self) -> None:
        self.hidden = not self.hidden

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

    def on_mouse_left_button_down(self) -> None:
        pass

    def on_mouse_left_button_up(self) -> None:
        pass

    def on_mouse_hover(self) -> None:
        pass

    def on_mouse_hover_end(self) -> None:
        pass

    def on_mouse_right_button_down(self) -> None:
        pass

    def on_mouse_right_button_up(self) -> None:
        pass

    def on_mouse_motion(self, dx: int, dy: int) -> None:
        pass

    def on_mouse_wheel(self, wheel: int) -> None:
        pass

    def get_widget_at(self, x: int, y: int) -> weakref.ref[Widget] | None:
        if self.hidden:
            return None
        if 0 <= x < self.width and 0 <= y < self.height:
            for child in reversed(self.children):
                result = child.get_widget_at(x - child.coordinates[0], y - child.coordinates[1])
                if result is not None:
                    return result
            return weakref.ref(self)
        return None


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
        self.hovered_widget: weakref.ref[Widget] | None = None

    def render(self) -> None:
        """Render everything."""
        self.root_widget.render_self_and_children(self.screen, (0, 0))

    def widget_action(self, x: int, y: int, action: Callable, *args, **kwargs) -> None:
        ref = self.root_widget.get_widget_at(x, y)
        if ref is None:
            return
        result = ref()
        if result is None:
            return
        action(result, *args, **kwargs)

    def on_mouse_hover(self, x: int, y: int) -> None:
        result = self.root_widget.get_widget_at(x, y)
        if result != self.hovered_widget:
            if self.hovered_widget is not None:
                widget = self.hovered_widget()
                if widget:
                    widget.on_mouse_hover_end()
            if result is not None:
                widget = result()
                if widget:
                    widget.on_mouse_hover()
            self.hovered_widget = result

    def on_mouse_left_button_down(self, x: int, y: int) -> None:
        self.widget_action(x, y, lambda this: this.on_mouse_left_button_down())

    def on_mouse_right_button_down(self, x: int, y: int) -> None:
        self.widget_action(x, y, lambda this: this.on_mouse_right_button_down())

    def on_mouse_left_button_up(self, x: int, y: int) -> None:
        self.widget_action(x, y, lambda this: this.on_mouse_left_button_up())

    def on_mouse_right_button_up(self, x: int, y: int) -> None:
        self.widget_action(x, y, lambda this: this.on_mouse_right_button_up())

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self.widget_action(x, y, lambda this, dx2, dy2: this.on_mouse_motion(dx2, dy2), dx, dy)

    def on_mouse_wheel(self, x: int, y: int, wheel: int) -> None:
        self.widget_action(x, y, lambda this: this.on_mouse_wheel(wheel))

    def run(self) -> None:
        """Run the event loop."""

        clock = pygame.time.Clock()

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
                            self.on_mouse_left_button_down(*event.pos)
                        elif event.button == 2:
                            self.on_mouse_right_button_down(*event.pos)
                    case pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.on_mouse_left_button_up(*event.pos)
                        elif event.button == 2:
                            self.on_mouse_right_button_up(*event.pos)
                    case pygame.MOUSEMOTION:
                        self.on_mouse_hover(*event.pos)
                        self.on_mouse_motion(*event.pos, *event.rel)
                    case pygame.MOUSEWHEEL:
                        pos: tuple[int, int] = pygame.mouse.get_pos()
                        self.on_mouse_wheel(*pos, event.y)
            self.render()
            pygame.display.flip()

            clock.tick(60)
