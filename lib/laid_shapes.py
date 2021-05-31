import numpy
import copy
import colorama

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
        # making this grid the exact same size as the main grid makes it easier to work with
        self.position = grid.position.clone()
        # currenly this value only increase, and never goes down when lines clear
        # highest Piece is actually the lowest value for y
        self.highest_piece = height
        # border offset
        self.matrix = Matrix.empty_sized(rows=height, columns=width, value=0)
        self.char = '▢'


    def __str__(self):
        return 'LaidShapes'


    def add_shape(self, shape: Shape, grid: Grid):
        for i in range(len(shape.matrix)):
            for j in range(len(shape.matrix[i])):
                if shape.matrix[i][j]:
                    # not sure why, but x axis is 2 off!
                    self.matrix[shape.position.y + i][shape.position.x + j -2] = shape.char
                    # update highest piece
                    if shape.position.y < self.highest_piece:
                        self.highest_piece = shape.position.y

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
                    screen.set(y=y, x=x, value=self.matrix[i][j])

    def check_for_collision(self, shape: Shape) -> bool:
        for i in range(len(shape.matrix)):
            for j in range(len(shape.matrix[i])):
                if shape.matrix[i][j] and self.matrix[shape.position.y + i][shape.position.x + j - 2]:
                    return True
        return False

    # it may be nice to add some sort of animation here
    def clear_lines(self) -> int:
        # find and clear lines
        cleared_lines = []
        for i in range(1, len(self.matrix)):
            if not 0 in self.matrix[i][1:-2]:
                cleared_lines.append(i)
                self.matrix[i] = [0 for i in self.matrix[i]]

        # lower uncleared lines
        cleared_below = 0
        if len(cleared_lines) > 0:
            for i in range(len(self.matrix) - 1, 1, -1):
                for cleared_line in cleared_lines:
                    if cleared_line > i:
                        cleared_below += 1
                        cleared_lines.pop(0)
                if cleared_below:
                    self.matrix[i + cleared_below] = self.matrix[i].copy()
                    self.matrix[i] = [0 for val in self.matrix[i]]

        return len(cleared_lines)

    def check_for_height_limit_reached(self):
        if self.highest_piece < 2:
            return True
        return False