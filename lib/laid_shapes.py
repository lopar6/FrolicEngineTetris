from frolic.vector2 import Vector2
from frolic.game_object import GameObject
from frolic.screen import Screen
from frolic.matrix import Matrix

from lib import Grid
from lib.shape import *


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
                    screen.set(y=y, x=x, char=self.matrix[i][j])

    def check_for_collision(self, shape: Shape, returnCollisionIndex = False) -> bool:
        for i in range(len(shape.matrix)):
            for j in range(len(shape.matrix[i])):
                if shape.matrix[i][j] and self.matrix[shape.position.y + i][shape.position.x + j - 2]:
                    if returnCollisionIndex:
                        return True, i, j
                    return True
        if returnCollisionIndex:
            return False, None, None
        return False



    # it may be nice to add some sort of animation here
    def clear_lines(self) -> int:
        # find and clear lines
        _cleared_lines = []
        for i in range(1, len(self.matrix)):
            if not 0 in self.matrix[i][1:-1]:
                _cleared_lines.append(i)
                self.matrix[i] = [0 for i in self.matrix[i]]

        # lower uncleared lines
        _cleared_below = 0
        _total_lines_cleared = len(_cleared_lines)
        if len(_cleared_lines) > 0:
            for i in range(len(self.matrix) - 1, 1, -1):
                for cleared_line in _cleared_lines:
                    if cleared_line > i:
                        _cleared_below += 1
                        _cleared_lines.pop(0)
                if _cleared_below:
                    self.matrix[i + _cleared_below] = self.matrix[i].copy()
                    self.matrix[i] = [0 for val in self.matrix[i]]

        return _total_lines_cleared

    def check_for_height_limit_reached(self):
        if self.highest_piece < 2:
            return True
        return False