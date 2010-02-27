'''
Created on Feb 23, 2010

@author: Bryan
'''

class KeyboardAgent:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        pass
    def update(self, entity, world):
        for x in entity.shapes:
            if self.input_manager["right"]:
                x.body.apply_impulse((1000,0))
            if self.input_manager["left"]:
                x.body.apply_impulse((-1000,0))
            if self.input_manager["up"]:
                x.body.apply_impulse((0,1000))
            if self.input_manager["down"]:
                x.body.apply_impulse((0,-1000))
            