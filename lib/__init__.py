import datetime
from time import sleep
import copy

import charpy
from numpy.core.fromnumeric import shape
from pynput import keyboard

from lib.grid import Grid
from lib.shape import *
from lib.laid_shapes import LaidShapes
from lib.next_shape_box import NextShapeBox

class TetrisGame(charpy.Game):

    def __init__(self):
        _grid_height = 16    # used to initalize both grid and laid_shapes
        _grid_rows = 13
        super().__init__()
        self.grid = Grid(_grid_height, _grid_rows)
        self.grid.position.x += 2
        self.deltatime : datetime.timedelta = None
        self.start_shape_position: Vector2 = self.grid.position.clone()
        self.start_shape_position.x += int(self.grid.size.x/2) - 1
        self.start_shape_position.y += 1
        self.time_since_shape_lowered = self.time_played = 1
        self.next_shape_box = NextShapeBox(self.grid)
        self.shape : Shape = self.next_shape_box.get_next_shape()
        self.shape = self.get_next_shape()
        self.laid_shapes = LaidShapes(self.grid, _grid_height, _grid_rows)
        self.score = 0
        self.time_bewtween_shape_lowerings = 0
        self.set_on_keydown(self.on_key_down)
        self.set_on_keyup(self.on_key_up)
        self.show_debug_info = True
        self.button_repeat_interval = .2
        self.up_pressed = False
        # initalized to button repeat interval so button presses execute as they are pressed
        self.time_since_up_pressed = self.button_repeat_interval
        self.down_pressed = False
        self.time_since_down_pressed = self.button_repeat_interval
        self.left_pressed = False
        self.time_since_left_pressed = self.button_repeat_interval
        self.right_pressed = False
        self.time_since_right_pressed = self.button_repeat_interval

        try:
            _high_score_file = open("high_score.txt", "r")
            self.high_score = int(_high_score_file.read())
        except:
            _high_score_file = open("high_score.txt", "w")
            self.high_score = 0
        _high_score_file.close()
        self.run()


    def get_next_shape(self) -> Shape:
        shape = self.next_shape_box.get_next_shape()
        shape.position = self.start_shape_position.clone()
        return shape


    # handles collision logic for shape rotations
    def spin_shape(self):
        _prevous_shape = copy.copy(self.shape)
        _prevous_position = _prevous_shape.position.clone()
        # line edge case
        if self.shape.__str__() == 'Line':
            # if vertical
            if self.shape.matrix.size.y > self.shape.matrix.size.x:
                self.shape.move('left', self.grid)
                self.shape.move('down', self.grid)
            else:
                self.shape.move('right', self.grid)
                self.shape.move('up', self.grid)
            if self.shape.position.x > self.grid.position.x + self.grid.size.x - 4:
                self.shape.move('left', self.grid)
            if self.shape.position.y > self.grid.position.y + self.grid.size.y - 4:
                self.shape.move('up', self.grid)

        self.shape.matrix = self.shape.matrix.rotated(clockwize=True)

        # check if shape is within grid and correct
        if self.shape.position.x < self.grid.position.x + 1: 
            self.shape.move('right', self.grid)
        elif self.shape.position.x > self.grid.position.x + self.grid.size.x - self.shape.size.x - 1 :
            self.shape.move('left', self.grid)
        elif self.shape.position.y > self.grid.position.y + self.grid.size.y - self.shape.size.y - 1 :
            self.shape.move('up', self.grid)

        # check for collion with laid_shapes
        _was_collision, _collision_location_y, _collision_location_x = self.laid_shapes.check_for_collision(self.shape, True)
        if _was_collision:
            # if collision was on the right side
            if _collision_location_x > 0:
                self.shape.move('left', self.grid)
                _reverse_moved_direction = 'left'
            else: 
                self.shape.move('right', self.grid)
                _reverse_moved_direction = 'right'

            # check if collision fixed
            _was_collision, _collision_location_y, _collision_location_x = self.laid_shapes.check_for_collision(self.shape, True)
            if _was_collision:
                self.shape.move(_reverse_moved_direction, self.grid)
                # if collsion was on bottom side
                if _collision_location_y > 0:
                    self.shape.move('up', self.grid)
                else:
                    self.shape.move('down', self.grid)

        # occasionally shapes will still not be in bounds
        if self.laid_shapes.check_for_collision(self.shape) or \
        self.shape.position.x < self.grid.position.x + 1 or \
        self.shape.position.x > self.grid.position.x + self.grid.size.x - self.shape.size.x - 1 or \
        self.shape.position.y > self.grid.position.y + self.grid.size.y - self.shape.size.y - 1 :
            self.shape = _prevous_shape
            self.shape.position = _prevous_position


    def calculate_score(self, num_lines_cleared: int):
        self.score += (num_lines_cleared * 100) * num_lines_cleared


    def on_key_down(self, key):
        if key == keyboard.Key.esc:
            self.end_game()
            return

        key_character = None
        try:
            key_character = key.char
        except:
            pass

        # when key is pressed it executes until key is lifted
        if key_character == 'w' or key == keyboard.Key.up:
            self.up_pressed = True

        if key_character == 'a' or key == keyboard.Key.left:
            self.left_pressed = True

        if key_character == 'd' or key == keyboard.Key.right:
            self.right_pressed = True 

        if key_character == 's' or key == keyboard.Key.down:
            self.down_pressed = True

        self.execute_button_presses()

    def on_key_up(self, key):
        key_character = None
        try:
            key_character = key.char
        except:
            pass

        if key_character == 'w' or key == keyboard.Key.up:
            self.up_pressed = False
            self.time_since_up_pressed = self.button_repeat_interval

        if key_character == 'a' or key == keyboard.Key.left:
            self.left_pressed = False
            self.time_since_left_pressed = self.button_repeat_interval

        if key_character == 'd' or key == keyboard.Key.right:
            self.right_pressed = False
            self.time_bewtween_right_pressed = self.button_repeat_interval

        if key_character == 's' or key == keyboard.Key.down:
            self.down_pressed = False
            self.time_since_down_pressed = self.button_repeat_interval
        
        self.execute_button_presses()

    
    def execute_button_presses(self):
        # if key is pressed, and the right amount of time has been waited, execute 
        if self.up_pressed:
            self.time_since_up_pressed += self.deltatime
            if self.time_since_up_pressed >= self.button_repeat_interval:
                self.time_since_up_pressed = 0
                self.spin_shape()

        # getting size and position explicity for updated values after spin
        spos = self.shape.position
        gpos = self.grid.position
        ssize = self.shape.size
        gsize = self.grid.size

        if self.left_pressed:
            self.time_since_left_pressed += self.deltatime
            if self.time_since_left_pressed >= self.button_repeat_interval:
                self.time_since_left_pressed = 0
                if spos.x > gpos.x + 1: 
                    self.shape.move('left', self.grid)
                    if self.laid_shapes.check_for_collision(self.shape):
                        self.shape.move('right', self.grid)            

        if self.right_pressed:
            self.time_since_right_pressed += self.deltatime
            if self.time_since_right_pressed >= self.button_repeat_interval:
                self.time_since_right_pressed = 0
                if spos.x < gpos.x + gsize.x - ssize.x - 1 :
                    self.shape.move('right', self.grid)
                    if self.laid_shapes.check_for_collision(self.shape):
                        self.shape.move('left', self.grid)
            
        if self.down_pressed:
            self.time_since_down_pressed += self.deltatime
            if self.time_since_down_pressed >= self.button_repeat_interval:
                self.time_since_down_pressed = 0
                if spos.y < gpos.y + gsize.y - ssize.y - 1 :
                    self.shape.move('down', self.grid)
                if self.laid_shapes.check_for_collision(self.shape):
                    self.shape.has_collided = True
                    self.shape.move('up', self.grid)
            

    def lower_shape(self):
        # do not lower shape while player is manually lowering shape
        if not self.down_pressed:
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
        self.time_since_shape_lowered += deltatime
        self.time_played += deltatime
        # time bettween action repeating
        self.execute_button_presses()
        # as real time increases, the game speeds up 
        self.time_bewtween_shape_lowerings = ((1 / (self.time_played + 150)) * 100)
        if self.time_since_shape_lowered > self.time_bewtween_shape_lowerings:
            self.time_since_shape_lowered = 0
            self.lower_shape()
            if self.shape.has_collided:
                self.laid_shapes.add_shape(self.shape, self.grid)
                if self.laid_shapes.check_for_height_limit_reached():
                    self.game_over()
                _num_cleared_lines = self.laid_shapes.clear_lines()
                self.calculate_score(_num_cleared_lines)
                self.shape = self.get_next_shape()

    def draw(self):
        if self.grid:
            self.draw_grid()
        if self.laid_shapes:
            self.laid_shapes.draw_laid_shapes(self.grid, self.screen)
        if self.shape:
            self.shape.draw(self.screen)
        if self.next_shape_box:
            self.next_shape_box.draw(self.screen)
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


    #  add score and next piece
    def draw_info(self):
        left_offset = self.grid.position.x + self.grid.size.x + 2
        top_offset = self.next_shape_box.position.y + self.next_shape_box.size.y
        info = []
        info.append(f'Score:')
        info.append(f'{self.score}')
        info.append('\n')
        info.append(f'High score:')
        info.append(f'{self.high_score}')
        for i in range(0, len(info)):
            self.screen.set(y=top_offset + i, x=left_offset, value=info[i])
    

    def game_over(self):    
        if self.score > self.high_score:
            _high_score_file = open("high_score.txt", "w")
            _high_score_file.write(str(self.score))
            _high_score_file.close()
        print("You got the high score!!")
        print("Thanks for playing!")
        sleep(5)
        self.end_game()