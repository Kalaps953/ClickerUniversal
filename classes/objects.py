from __future__ import annotations

import time

import pynput.mouse as mouse


class Pos:
    def __init__(self, x: float | int, y: float | int):
        self.x = x
        self.y = y

    def __add__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return Pos(self.x + other, self.y + other)
        if isinstance(other, Pos):
            return Pos(self.x + other.x, self.y + other.y)
        raise TypeError()

    def __sub__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return Pos(self.x - other, self.y - other)
        if isinstance(other, Pos):
            return Pos(self.x - other.x, self.y - other.y)
        raise TypeError()

    def __mul__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return Pos(self.x * other, self.y * other)
        if isinstance(other, Pos):
            return Pos(self.x * other.x, self.y * other.y)
        raise TypeError()

    def __truediv__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return Pos(self.x / other, self.y / other)
        if isinstance(other, Pos):
            return Pos(self.x / other.x, self.y / other.y)
        raise TypeError()

    def __gt__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return self.x > other and self.y > other
        if isinstance(other, Pos):
            return self.x > other.x and self.y > other.y
        raise TypeError()

    def __ge__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return self.x >= other and self.y >= other
        if isinstance(other, Pos):
            return self.x >= other.x and self.y >= other.y
        raise TypeError()

    def __lt__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return self.x < other and self.y < other
        if isinstance(other, Pos):
            return self.x < other.x and self.y < other.y
        raise TypeError()

    def __le__(self, other: float | int | Pos):
        if isinstance(other, float) or isinstance(other, int):
            return self.x <= other and self.y <= other
        if isinstance(other, Pos):
            return self.x <= other.x and self.y <= other.y
        raise TypeError()

    def __str__(self):
        return f'Pos({self.x}, {self.y})'

    def list(self):
        return [self.x, self.y]


class MouseEvent(Pos):
    def __init__(self,
                 isPress: bool = True,
                 isRelease: bool = True,
                 delayB: float = 0,
                 duration: float = 0,
                 delayA: float = 0,
                 button: mouse.Button = mouse.Button.left,
                 local: bool = True,
                 x: float = 0,
                 y: float = 0
                 ):
        self.isPress = isPress
        self.isRelease = isRelease
        self.delayB = delayB
        self.duration = duration
        self.delayA = delayA
        self.button = button
        self.local = local
        super().__init__(x, y)

    def do(self, controller: mouse.Controller):
        time.sleep(self.delayB)
        if self.local:
            controller.move(self.x, self.y)
        else:
            controller.position = self.list()
        if self.isPress:
            controller.press(self.button)
            if self.isRelease and self.duration >= 0:
                time.sleep(self.duration)
                controller.release(self.button)
        time.sleep(self.delayA)

    def pos(self):
        return Pos(self.x, self.y)