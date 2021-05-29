import numpy

from charpy.screen import Screen
from charpy.vector2 import Vector2
from charpy.game_object import GameObject
from charpy.matrix import Matrix

from lib.grid import Grid

class Shape(GameObject):
    char = '▣'
    has_collided = False

    def __str__(self):
        return 'Shape'


    def draw(self, screen: Screen):
    # Note: Shape positions are NOT relative to the grid position
        offset = Vector2(
            x=self.position.x,
            y=self.position.y
        )
        for i in range(0, len(self.matrix)):
            row = self.matrix[i]
            for j in range(0, len(row)):
                should_draw = row[j]
                if should_draw:
                    x = j + offset.x
                    y = i + offset.y
                    screen.set(y=y, x=x, value=self.char)


    def move(self, direction: str, grid: Grid):
            spos = self.position
            gpos = grid.position
            sheight = self.size.y
            gheight = grid.size.y
            if direction == 'left':
                spos.x -= 1
            if direction == 'right':
                spos.x += 1
            if direction == 'down':   
                spos.y += 1
            if direction == 'up':
                spos.y -= 1


class Square(Shape):
    def __init__(self):
        matrix = Matrix([
            [1, 1],
            [1, 1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'Square'

class Line(Shape):
    char = '▤'
    def __init__(self):
        matrix = Matrix([
            [1],
            [1],
            [1],
            [1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'Line'


class ForwardsL(Shape):
    char = '▢'
    def __init__(self):
        matrix = Matrix([
            [1, 0],
            [1, 0],
            [1, 1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'ForwardsL'


class BackwardsL(Shape):
    char = '□'
    def __init__(self):
        matrix = Matrix([
            [0, 1],
            [0, 1],
            [1, 1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'BackwardsL'


class ForwardsZ(Shape):
    char = '▧'
    def __init__(self):
        matrix = Matrix([
            [1, 1, 0],
            [0, 1, 1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'ForwardsZ'


class BackwardsZ(Shape):
    char = '▨'
    def __init__(self):
        matrix = Matrix([
            [0, 1, 1],
            [1, 1, 0],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'BackwardsZ'


class TShape(Shape):
    char = '▦'
    def __init__(self):
        matrix = Matrix([
            [0, 1, 0],
            [1, 1, 1],
        ])
        super().__init__(matrix=matrix)

    def __str__(self):
        return 'TShape'

# todo add spin collision check