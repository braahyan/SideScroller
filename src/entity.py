'''
Created on Feb 21, 2010

@author: Bryan
'''

import pymunk as pm
from pymunk import Vec2d
class Entity:
    '''class for physics object represented by some renderer'''
    def __init__(self, shapes=[],joints=[], renderer=None):
        self.shapes = shapes
        for x in self.shapes:
            x.entity = self
        self.joints = joints
        for x in self.joints:
            x.entity = self
        self.renderer = renderer

    def render(self):
        if self.renderer is not None:
            self.renderer.render(self)

class SimpleEntity(Entity):
    def __init__(self, shape, renderer = None):
        Entity.__init__(self, [shape], renderer=renderer)

class Ball(SimpleEntity):
    def __init__(self, position,radius, mass = 10, inertia=100, friction = 0.5, renderer=None):
        body = pm.Body(mass, inertia)
        body.position = position
        shape = pm.Circle(body, radius, Vec2d(0,0))
        shape.friction = friction
        SimpleEntity.__init__(self, shape, renderer)
        
class Platform(SimpleEntity):
    def __init__(self, a,b, thickness=5.0, friction=0.99, renderer=None):
        body = pm.Body(pm.inf, pm.inf)
        shape= pm.Segment(body, Vec2d(a[0],a[1]), Vec2d(b[0],b[1]), thickness/2.0)
        shape.friction = friction
        SimpleEntity.__init__(self, shape, renderer)