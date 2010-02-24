'''
Created on Feb 23, 2010

@author: Bryan
'''
import pyglet
from pyglet.window import key

class KeyboardAgent:
    def __init__(self, keyboard_state):
        self.keyboard_state = keyboard_state
        pass
    def update(self, entity):
        for x in entity.shapes:
            if self.keyboard_state[key.RIGHT]:
                x.body.apply_impulse((100,0))
        pass
        