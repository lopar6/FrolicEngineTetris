from datetime import datetime

from charpy import vector2
from charpy.game_object import GameObject

from lib.shape import *

class EndScreen(GameObject):
    def __init__(self):
        super().__init__()
        self.matrix = Matrix([
                                '                                    ',
                                '               end screen           ',
                                '                                    ',
                                '                                    ',
                                '                                    ',
                                '                                    ',])

    
    def update(self, deltatime):
        pass


    def draw(self, screen: Screen):
        screen.draw_matrix(self.matrix, Vector2.zero())


    def on_key_down(self, key):
        self.game_instance.start_core_game()

    
    def on_key_up(self):
        pass