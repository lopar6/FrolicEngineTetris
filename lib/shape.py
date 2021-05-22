import numpy
from charpy.vector2 import Vector2
from charpy.game_object import GameObject
from charpy.matrix import Matrix


class Shape(GameObject):

    char = '▣'
    shape_name = 'Shape'

    def __init__(self, matrix: Matrix):
        super().__init__()
        self.matrix = matrix
        # We only need to re-build this parallel matrix when the object is
        # created or rotated so this is a cache of that parallel matrix
        self.char_matrix = self._char_matrix()

    def __str__(self):
        return self.shape_name

    def rotate(self, clockwize: bool):
        self.matrix = self.matrix.rotated(clockwize=clockwize)
        # Cache this for future drawing, only need to rebuild the char version when it changes
        self.char_matrix = self._char_matrix()


    def _char_matrix(self) -> Matrix:
        """
        Converts the matrix of 1s and 0s to a matrix of char and None
        """
        return Matrix([
            [
                self.char if element == 1 else None
                for element in row
            ]
            for row in self.matrix.clone()
        ])


class Square(Shape):
    shape_name = 'Square'
    def __init__(self):
        matrix = Matrix([
            [1, 1],
            [1, 1],
        ])
        super().__init__(matrix)


class Line(Shape):
    char = '▤'
    shape_name = 'Line'
    def __init__(self):
        matrix = Matrix([
            [1],
            [1],
            [1],
            [1],
        ])
        super().__init__(matrix)


class ForwardsL(Shape):
    char = '▢'
    shape_name = 'ForwardsL'
    def __init__(self):
        matrix = Matrix([
            [1, 0],
            [1, 0],
            [1, 1],
        ])
        super().__init__(matrix)


class BackwardsL(Shape):
    char = '□'
    shape_name = 'BackwardsL'
    def __init__(self):
        matrix = Matrix([
            [0, 1],
            [0, 1],
            [1, 1],
        ])
        super().__init__(matrix)


class ForwardsZ(Shape):
    char = '▧'
    shapeName = 'ForwardsZ'
    def __init__(self):
        matrix = Matrix([
            [1, 1, 0],
            [0, 1, 1],
        ])
        super().__init__(matrix)


class BackwardsZ(Shape):
    char = '▨'
    shape_name = 'BackwardsZ'
    def __init__(self):
        matrix = Matrix([
            [0, 1, 1],
            [1, 1, 0],
        ])
        super().__init__(matrix)


class TShape(Shape):
    char = '▦'
    shape_name = 'TShape'
    def __init__(self):
        matrix = Matrix([
            [0, 1, 0],
            [1, 1, 1],
        ])
        super().__init__(matrix)
