from datetime import datetime

from charpy import game, vector2
from charpy.game_object import GameObject
from pynput import keyboard

from lib.shape import *

class EndScreen(GameObject):
    def __init__(self, score : int, got_high_score: bool):
        super().__init__()
        self.score = score
        if got_high_score:
            self.matrix
        self.message = []
        if got_high_score:
            self.message.append('Congrats! You got the high score!')
        else:
            self.message.append('Thanks for playing!')
        self.message.append('Your score was:')
        self.message.append(f'   {self.score}')
        self.message.append('')
        self.message.append('Press "space" to reclaim your console')
        
    
    def update(self, deltatime):
        pass


    def draw(self, screen: Screen):
        for i in range(0, len(self.message)):
            screen.draw_string(self.message[i], Vector2(x = 4, y = 2 + i))

    def on_key_down(self, key):
        if key == keyboard.Key.space:
            self.game_instance.end_game()

    
    def on_key_up(self, key):
        pass