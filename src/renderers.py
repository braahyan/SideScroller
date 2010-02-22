'''
Created on Feb 21, 2010

@author: Bryan
'''

import primitives
class CircleRenderer:
    def __init__(self, width=20, color=(1,1,1,1), stroke=200):
        self.primitive = primitives.Circle(x=0, y=0, z=1, width=width, color=color, stroke=stroke)
        pass
    def render(self, entity):
        ball = entity.shapes[0]
        self.primitive.x = ball.body.position[0]
        self.primitive.y = ball.body.position[1]
        self.primitive.width = ball.radius * 2
        self.primitive.render()

class PlatformRenderer:
    def __init__(self):
        self.primitive = primitives.Line( a=(1,1), b=(100,100), z=1, color=(1,1,1,1), stroke=10)
    def render(self, entity):
        platform = entity.shapes[0]
        self.primitive.init(platform.a, platform.b)
        self.primitive.width = platform.radius*2
        self.primitive.render()