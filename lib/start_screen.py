from datetime import datetime

from charpy import vector2
from charpy.game_object import GameObject

from lib.shape import *

class StartScreen(GameObject):
    def __init__(self):
        super().__init__()
        self.time_since_lower = 0
        self.time_between_lowers = .05
        self.base_height = 6
        self.start_time = 0
        self.first_t = LetterT()
        self.letter_e = LetterE()
        self.second_t = LetterT()
        self.letter_r = LetterR()
        self.letter_i = LetterI()
        self.letter_s = LetterS()
        self.set_shape_positions()

    def set_shape_positions(self):
        self.first_t.position = Vector2(x = 1,  y = 0)
        self.letter_e.position  = Vector2(x = 7,  y = 0)
        self.second_t.position  = Vector2(x = 12, y = 0)
        self.letter_r.position  = Vector2(x = 18, y = 0)
        self.letter_i.position  = Vector2(x = 24, y = 0)
        self.letter_s.position  = Vector2(x = 27, y = 0)


    def lower_all_shapes(self, delatime):
        self.time_since_lower += delatime
        if self.time_since_lower > self.time_between_lowers:
            self.time_since_lower = 0
            if self.first_t.position.y < self.base_height:
                self.first_t.position.y += 1
            elif self.letter_e.position.y < self.base_height:
                self.letter_e.position.y += 1
            elif self.second_t.position.y < self.base_height:
                self.second_t.position.y += 1
            elif self.letter_r.position.y < self.base_height:
                self.letter_r.position.y += 1
            elif self.letter_i.position.y < self.base_height:
                self.letter_i.position.y += 1
            elif self.letter_s.position.y < self.base_height:
                self.letter_s.position.y += 1
                

    def update(self, deltatime):
        self.start_time += deltatime
        self.lower_all_shapes(deltatime)
        if self.start_time > 3:
            self.game_instance.start_core_game()


    def draw(self, screen: Screen):
        self.first_t.draw(screen)
        self.letter_e.draw(screen)
        self.second_t.draw(screen)
        self.letter_r.draw(screen)
        self.letter_i.draw(screen)
        self.letter_s.draw(screen)


    def on_key_down(self, key):
        self.game_instance.start_core_game()

    
    def on_key_up(self):
        pass