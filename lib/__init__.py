import datetime
import random
from typing import Tuple
from charpy import screen
import numpy

import charpy
from numpy.core.fromnumeric import shape
from pynput import keyboard

from lib.grid import Grid
from lib.shape import *
from lib.laid_shapes import LaidShapes

class TetrisGame(charpy.Game):

    def __init__(self):
        _grid_height = 16    # used to initalize both grid and laid_shapes
        _grid_rows = 13
        super().__init__()
        self.grid = Grid(_grid_height, _grid_rows)
        self.grid.position.x += 2
        self.start_shape_position : Vector2 = None
        self.deltatime : datetime.timedelta = None
        self.start_shape_position: Vector2 = self.grid.position.clone()
        self.start_shape_position.x += int(self.grid.size.x/2) - 2
        self.start_shape_position.y += 1
        self.time_since_shape_lowered = self.time_played = 1
        self.shape : Shape = self.get_next_shape()
        self.laid_shapes = LaidShapes(self.grid, _grid_height, _grid_rows)
        self.set_on_keydown(self.on_key_down)
        self.game_loop()

    def get_next_shape(self) -> Shape:
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
        shape = _ShapeClass()
        shape.position = self.start_shape_position.clone()
        return shape


    def on_key_down(self, key):
        
        if key == keyboard.Key.esc:
            self.end_game()
            return

        key_character = None
        try:
            key_character = key.char
        except:
            pass

        if key_character == 'w':
            self.shape.matrix = self.shape.matrix.rotated(clockwize=True)
            return
        if key_character == 'e':
            self.shape.matrix = self.shape.matrix.rotated(clockwize=False)
            return

        spos = self.shape.position
        gpos = self.grid.position
        ssize = self.shape.size
        gsize = self.grid.size

        if key_character == 'a':
            if spos.x > gpos.x + 1: 
                self.shape.move('left', self.grid)

            if self.laid_shapes.check_for_collision(self.shape):
                self.shape.move('right', self.grid)
            return

        if key_character == 'd':
            if spos.x < gpos.x + gsize.x - ssize.x - 1 :
                self.shape.move('right', self.grid)

            elif self.laid_shapes.check_for_collision(self.shape):
                self.shape.move('right', self.grid)
            return

        if key_character == 's':
            if spos.y < gpos.y + gsize.y - ssize.y - 2 :
                self.shape.move('down', self.grid)
                
            if self.laid_shapes.check_for_collision(self.shape):
                self.shape.has_collided = True
                self.shape.move('up', self.grid)
            return


    def lower_shape(self):
        spos = self.shape.position
        gpos = self.grid.position
        sheight = self.shape.size.y
        gheight = self.grid.size.y
        if spos.y < gpos.y + gheight - sheight - 1 :
            self.shape.move('down', self.grid)
            if self.laid_shapes.check_for_collision(self.shape):
                self.shape.move('up', self.grid)
                self.shape.has_collided = True
        else:
            self.shape.has_collided = True


    def update(self, deltatime):
        self.deltatime = deltatime
        self.time_since_shape_lowered += deltatime.microseconds
        self.time_played += deltatime.microseconds
        lower_rate = 750000
        if self.time_since_shape_lowered > lower_rate:
            self.time_since_shape_lowered = 0
            self.lower_shape()
            if self.shape.has_collided:
                self.laid_shapes.add_shape(self.shape, self.grid)
                self.shape = self.get_next_shape()
                self.laid_shapes.clear_lines()


    def draw(self):
        if self.grid:
            self.draw_grid()
        self.draw_instructions()
        if self.laid_shapes:
            self.laid_shapes.draw_laid_shapes(self.grid, self.screen)
        if self.shape:
            self.shape.draw(self.screen)
        self.draw_info()
        super().draw()



    def draw_grid(self):
        pos = self.grid.position
        matrix = self.grid.matrix
        for i in range(0, len(matrix)):
            row = matrix[i]
            for j in range(0, len(row)):
                char = row[j]
                x = j + pos.x
                y = i + pos.y
                try:
                    self.screen.set(y=y, x=x, value=char)
                except IndexError:
                    print("Your terminal window is too small\nPlease resize the window and restart the game")
                    self.end_game()


    def draw_instructions(self):
        y = self.grid.position.y + self.grid.size.y


    #  add score and next piece
    def draw_info(self):
        left_offset = self.grid.position.x + self.grid.size.x + 2
        info = []
        if self.deltatime.microseconds:
            fps = str(int(1000000 / self.deltatime.microseconds))
            info.append(f'FPS:            {fps}                    ')
        for i in range(0, len(info)):
            self.screen.set(y=i+1, x=left_offset, value=info[i])
    