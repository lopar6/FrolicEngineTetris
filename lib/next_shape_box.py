import random
import copy

from frolic.vector2 import Vector2
from frolic.game_object import GameObject
from frolic.screen import Screen
from frolic.matrix import Matrix
from frolic.matrix_border import MatrixBorder

from lib.grid import Grid
from lib.shape import *

class NextShapeBox(GameObject):

    # TODO use new Matrix.apply() 
    def __init__(self, grid: Grid):
        super().__init__()
        self.matrix : Matrix = Matrix.empty_sized(rows=4, columns=7)
        self.matrix = self.matrix.with_border(MatrixBorder(sides=MatrixBorder.SINGLE_LINE_THIN))
        self.position = Vector2(grid.position.x + grid.size.x + 1, grid.position.y)
        self.current_shape = self.get_random_shape()
        self.set_start_shape_position()


    def set_start_shape_position(self):
        _left_offset = 2
        _top_offset = 1
        self.current_shape.position = Vector2(x=(self.position.x + _left_offset), y=(self.position.y + _top_offset)) 


    def draw(self, screen: Screen):
        screen.draw_matrix(self.matrix, self.position)
        for i in range(len(self.current_shape.matrix)):
            for j in range(len(self.current_shape.matrix[i])):
                if self.current_shape.matrix[i][j]:
                    screen.set(self.current_shape.position.x + j, self.current_shape.position.y + i, self.current_shape.char)


    def get_next_shape(self) -> Shape:
        previous_shape = copy.copy(self.current_shape)
        self.current_shape = self.get_random_shape()
        self.set_start_shape_position()        
        return previous_shape
        

    def get_random_shape(self) -> Shape:
        shapes = [
            Square,
            Line,
            ForwardsL,
            BackwardsL,
            ForwardsZ,
            BackwardsZ,
            TShape,
        ]
        _ShapeClass = random.choice(shapes)
        _shape : Shape = _ShapeClass()
        return _shape
