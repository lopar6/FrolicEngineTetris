import datetime
import random

import charpy
from pynput import keyboard

from lib.grid import Grid
from lib.shape import *

class TetrisGame(charpy.Game):

    def __init__(self):
        super().__init__()
        self.grid = Grid()
        self.grid.position.x += 2
        self.start_shape_position : Vector2 = None
        self.deltatime : datetime.timedelta = None
        self.start_shape_position: Vector2 = self.grid.position.clone()
        self.start_shape_position.x += int(self.grid.size.x/2) - 2
        self.start_shape_position.y += 1
        self.shape : Shape = self.get_next_shape()
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

        if key == keyboard.Key.space:
            self.shape = self.get_next_shape()
            return

        key_character = None
        try:
            key_character = key.char
        except:
            pass

        if key_character == 'w':
            self.shape.rotate(clockwize=True)
            return
        if key_character == 'e':
            self.shape.rotate(clockwize=False)
            return

        if key_character == 'a':
            self.move_shape('left')
            return

        if key_character == 'd':
            self.move_shape('right')
            return


    def move_shape(self, direction: str):
        # Note: we have to pretend the grid is smaller than it really is to
        #       take the grid's outer box shape into account
        spos = self.shape.position
        gpos = self.grid.position
        swidth = self.shape.size.x
        gwidth = self.grid.size.x
        if direction == 'left':
            spos.x -= 1
            if spos.x < gpos.x + 1:
                spos.x = gpos.x + 1
        if direction == 'right':
            spos.x += 1
            if spos.x > gpos.x + gwidth - swidth - 1:
                spos.x = gpos.x + gwidth - swidth - 1



    def update(self, deltatime):
        self.deltatime = deltatime


    def draw(self):
        self.screen.draw_matrix(self.grid.matrix, self.grid.position)
        self.screen.draw_matrix(self.shape.char_matrix, self.shape.position)
        self.draw_instructions()
        self.draw_info()
        super().draw()


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
        for i in range(0, len(info)):
            self.screen.set(y=i+1, x=left_offset, value=info[i])
