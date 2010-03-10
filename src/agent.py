'''
Created on Feb 23, 2010

@author: Bryan
'''
import math
import SoundRenderers
class KeyboardAgent:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.sound_renderer = SoundRenderers.BallSoundRenderer()

    def update(self, entity, world):
        max_x_velocity = 100
        sprint_multiplier = 1
        if self.input_manager["sprint"]:
            sprint_multiplier = 2
            
        for x in entity.shapes:
            moving = False
            total_x_impulse=0
            total_y_impulse=0
            
            if self.input_manager["right"]:
                total_x_impulse += (1000*sprint_multiplier)
                #x.body.apply_impulse((1000*sprint_multiplier,0))
                moving = True
            if self.input_manager["left"]:
                total_x_impulse += (-1000*sprint_multiplier)
                #x.body.apply_impulse((-1000*sprint_multiplier,0))
                moving = True
            if self.input_manager["jump"]:
                total_y_impulse += (1000*sprint_multiplier)    
                #x.body.apply_impulse(0,(1000*sprint_multiplier))
                moving = True
            
            x.body.apply_impulse((total_x_impulse,total_y_impulse))
                
            if not moving:
                if math.fabs(x.body.velocity.x) <5:
                    x.body.velocity.x = 0
                else:
                    x.body.velocity.x = int(x.body.velocity.x + (-cmp(x.body.velocity.x, 0) * (max_x_velocity/20)))
            if math.fabs(x.body.velocity.x) > max_x_velocity * sprint_multiplier:
                x.body.velocity.x = cmp(x.body.velocity.x, 0) * (max_x_velocity * sprint_multiplier)
        if self.input_manager["jump"]:
            #jump with sound renderer and entity
            self.sound_renderer.do_action("jump")
