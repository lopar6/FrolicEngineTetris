from charpy.matrix_border import MatrixBorder
from charpy.vector2 import Vector2
from charpy.game_object import GameObject
from charpy.matrix import Matrix

class Grid(GameObject):
    # The matrix will look something like this, but its size
    # is set by the gridsize handed in to the constructor
    # ╔═══╗
    # ║°°°║
    # ║°°°║
    # ║°°°║
    # ╚═══╝

    def __init__(self, height, width):
        self.empty_char = '.' # '°'
        self.position = Vector2(x=5, y=0)
        matrix = Matrix.empty_sized(rows=height, columns=width, value='.')
        matrix = matrix.with_border(MatrixBorder(sides=MatrixBorder.DOUBLE_LINE))
        super().__init__(matrix=matrix)
