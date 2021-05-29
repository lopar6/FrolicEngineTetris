import numpy
from charpy.vector2 import Vector2
from charpy.game_object import GameObject
from charpy.screen import Screen
from charpy.matrix import Matrix

from lib import Shape, Grid


class LaidShapes(GameObject):
    '''
    Pieces that have already been laid down, and are now part of the board
    '''

    def __init__(self, grid: Grid, height, width):
        self.position = grid.position
        # border offset
        # self.position.x -= 1
        self.matrix = Matrix.empty_sized(rows=height, columns=width, value=0)
        self.char = '▢'


    def __str__(self):
        return 'LaidShapes'


    def add_shape(self, shape: Shape, grid: Grid):
        for i in range(len(shape.matrix)):
            for j in range(len(shape.matrix[i])):
                if shape.matrix[i][j]:
                    self.matrix[shape.position.y + i][shape.position.x + j -2] = 1


    def draw_laid_shapes(self, grid: Grid, screen: Screen):
        offset = Vector2(
            x = grid.position.x,
            y = grid.position.y
        )
        for i in range(0, len(self.matrix)):
            row = self.matrix[i]
            for j in range(0, len(row)):
                should_draw = row[j]
                if should_draw:
                    x = j + offset.x
                    y = i + offset.y
                    screen.set(y=y, x=x, value=self.char)