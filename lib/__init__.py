import datetime
import random
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

    # todo move shape logic to shape class
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

        if key == keyboard.Key.space:
            self.shape = self.get_next_shape()
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

        if key_character == 'a':
            self.move_shape('left')
            return

        if key_character == 'd':
            self.move_shape('right')
            return

        if key_character == 's':
            self.move_shape('down')
            return


    def lower_shape(self):
        spos = self.shape.position
        gpos = self.grid.position
        sheight = self.shape.size.y
        gheight = self.grid.size.y
        if spos.y < gpos.y + gheight - sheight - 1 :
            spos.y += 1
        else:
            self.laid_shapes.add_shape(self.shape, self.grid)
            self.shape = self.get_next_shape()


    def move_shape(self, direction: str):
        # Note: we have to pretend the grid is smaller than it really is to
        #       take the grid's outer box shape into account
        spos = self.shape.position
        gpos = self.grid.position
        swidth = self.shape.size.x
        gwidth = self.grid.size.x
        sheight = self.shape.size.y
        gheight = self.grid.size.y
        if direction == 'left':
            spos.x -= 1
            if spos.x < gpos.x + 1:
                spos.x = gpos.x + 1
        if direction == 'right':
            spos.x += 1
            if spos.x > gpos.x + gwidth - swidth - 1:
                spos.x = gpos.x + gwidth - swidth - 1
        if direction == 'down':   # currently causes bug where grid moves down if shape is out of bounds
            if spos.y > gpos.y + gheight - sheight - 2 :
                # gpos.y = gpos.y + gheight - sheight - 1
                pass
            else:
                spos.y += 1


    def update(self, deltatime):
        self.deltatime = deltatime
        self.time_since_shape_lowered += deltatime.microseconds
        self.time_played += deltatime.microseconds
        lower_rate = 750000
        if self.time_since_shape_lowered > lower_rate:
            self.time_since_shape_lowered = 0
            self.lower_shape()



    def draw(self):
        if self.grid:
            self.draw_grid()
        self.draw_instructions()
        if self.laid_shapes:
            self.laid_shapes.draw_laid_shapes(self.grid, self.screen)
        if self.shape:
            self.draw_shape()
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


    def draw_shape(self):
        # Note: Shape positions are NOT relative to the grid position
        matrix = self.shape.matrix
        offset = Vector2(
            x=self.shape.position.x,
            y=self.shape.position.y
        )
        for i in range(0, len(matrix)):
            row = matrix[i]
            for j in range(0, len(row)):
                should_draw = row[j]
                if should_draw:
                    x = j + offset.x
                    y = i + offset.y
                    self.screen.set(y=y, x=x, value=self.shape.char)
                # This is for testing purposes, it prints over the empty matrix
                # spots too
                # else:
                #     x = j + offset.x
                #     y = i + offset.y
                #     self.screen[y][x] = ' '

    def draw_instructions(self):
        y = self.grid.position.y + self.grid.size.y
        self.screen.set(y=y, x=0, value="Press 'w' arrow to spin shape!")


    def draw_info(self):
        left_offset = self.grid.position.x + self.grid.size.x + 2
        info = []
        if self.shape:
            info.append(f'Shape:          {self.shape}             ')
            info.append(f'Shape Position: {self.shape.position}    ')
        if self.grid:
            info.append(f'Grid Position:  {self.grid.position}     ')
        if self.deltatime.microseconds:
            fps = str(int(1000000 / self.deltatime.microseconds))
            info.append(f'FPS:            {fps}                    ')
        info.append(f'Chars redrawn:  {charpy.ConsolePrinter.replaced}    ')
        info.append(f'time: {self.time_played}')
        for i in range(0, len(info)):
            self.screen.set(y=i+1, x=left_offset, value=info[i])
