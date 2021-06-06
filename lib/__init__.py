import datetime
from time import sleep
import copy

import charpy
from charpy import screen
from numpy.core.fromnumeric import shape
from pynput import keyboard

from lib.grid import Grid
from lib.shape import *
from lib.laid_shapes import LaidShapes
from lib.next_shape_box import NextShapeBox
from lib.core_game import CoreGame

class TetrisGame(charpy.Game):

    def __init__(self):
        super().__init__()
        self.deltatime : datetime.timedelta = None
        self.set_on_keydown(self.on_key_down)
        self.set_on_keyup(self.on_key_up)
        self.core_game = CoreGame()
        self.run()
    
    def draw(self):
        self.core_game.draw(self.screen)
        super().draw()

    def update(self, deltatime: datetime.timedelta):
        self.deltatime = deltatime
        self.core_game.update(deltatime)

    def on_key_down(self, key: keyboard.Key):
        self.core_game.on_key_down(key)

    def on_key_up(self, key: keyboard.Key):
        self.core_game.on_key_up(key)
