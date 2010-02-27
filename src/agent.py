'''
Created on Feb 23, 2010

@author: Bryan
'''
import math
class KeyboardAgent:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        pass
    def update(self, entity, world):
        max_x_velocity = 100
        sprint_multiplier = 1
        if self.input_manager["sprint"]:
            sprint_multiplier = 2
        for x in entity.shapes:
            moving = False
            if self.input_manager["right"]:
                x.body.apply_impulse((1000*sprint_multiplier,0))
                moving = True
            if self.input_manager["left"]:
                x.body.apply_impulse((-1000*sprint_multiplier,0))
                moving = True
            if not moving:
                if math.fabs(x.body.velocity.x) <5:
                    x.body.velocity.x = 0
                else:
                    x.body.velocity.x = int(x.body.velocity.x + (-cmp(x.body.velocity.x, 0) * (max_x_velocity/20)))
            if math.fabs(x.body.velocity.x) > max_x_velocity * sprint_multiplier:
                x.body.velocity.x = cmp(x.body.velocity.x, 0) * (max_x_velocity * sprint_multiplier)