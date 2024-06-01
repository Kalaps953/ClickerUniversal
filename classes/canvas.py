from __future__ import annotations
from .objects import Pos
import pygame as pg
import copy


class Menu:
    def __init__(self, pos: Pos, size: Pos, background: pg.Surface | list[int, int, int] | None = [200, 200, 200], buttons: list[Button] = [], planes: list[Plane] = [], submenus: list[Menu] = []):
        self.pos = pos
        self.size = size
        self.background = background
        self.buttons = buttons
        self.planes = planes
        self.submenus = submenus

    def draw(self, display: pg.Surface):
        if isinstance(self.background, list):
            display.fill(self.background, (self.pos.list(), self.size.list()))
        elif isinstance(self.background, pg.Surface):
            display.blit(self.background, self.pos.list())

        for i in self.buttons:
            i.draw(display)
        for i in self.submenus:
            i.draw(display)
        for i in self.planes:
            i.draw(display)

    def update(self, event: pg.event.Event):
        for i in self.buttons:
            i.update(event)
        for i in self.submenus:
            i.update(event)


class Plane:
    def __init__(self, pos: Pos, surface: pg.Surface):
        self.pos = pos
        self.surface = surface

    def draw(self, display: pg.Surface):
        display.blit(self.surface, self.pos.list())


class Button:
    def __init__(self, pos: Pos, size: Pos, normalColor: list[int, int, int], onHoverColor: list[int, int, int], onPressColor: list[int, int, int], onPressEvent: dict = []):
        self.pos = pos
        self.size = size
        self._rect = pg.Rect(pos.list(), size.list())
        self.normalColor = normalColor
        self.onHoverColor = onHoverColor
        self.onPressColor = onPressColor
        self.onPressEvent = onPressEvent
        self.isHovered = False
        self.isPressed = False

    def draw(self, display: pg.Surface):
        if self.isPressed:
            display.fill(self.onPressColor, (self.pos.list(), self.size.list()))
        elif self.isHovered:
            display.fill(self.onHoverColor, (self.pos.list(), self.size.list()))
        else:
            display.fill(self.normalColor, (self.pos.list(), self.size.list()))

    def update(self, event: pg.event.Event):
        if event.type == pg.MOUSEMOTION:
            if self._rect.collidepoint(event.pos):
                self.isHovered = True
            else:
                self.isHovered = False
                self.isPressed = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self.isPressed = True
        if event.type == pg.MOUSEBUTTONUP:
            self.isPressed = False
        if self.isPressed:
            for i in self.onPressEvent.keys():
                i(self.onPressEvent[i])


class Text(Plane):
    def __init__(self, pos: Pos, text: str, font: pg.font.Font, fontColor: list[int, int, int], antialias: bool | int, backgroundColor: list[int, int, int] | None = None, isCenteredX: bool = False, isCenteredY: bool = False):
        self.pos = pos
        self.prevText = text
        self.text = text
        self.font = font
        self.fontColor = fontColor
        self.antialias = antialias
        self.backgroundColor = backgroundColor
        self.isCenteredX = isCenteredX
        self.isCenteredY = isCenteredY
        super().__init__(pos, self.font.render(self.text, self.antialias, self.fontColor, self.backgroundColor))

    def draw(self, display: pg.Surface):
        if self.prevText != self.text:
            self.surface = self.font.render(self.text, self.antialias, self.fontColor, self.backgroundColor)
        pos = copy.copy(self.pos)
        if self.isCenteredX:
            pos.x -= self.surface.get_width() / 2
        if self.isCenteredY:
            pos.y -= self.surface.get_height() / 2
        display.blit(self.surface, pos.list())
