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

class ControllableEntity(Entity):
    def __init__(self,shapes=[], joints=[], agent=None, renderer=None):
        self.agent = agent
        Entity.__init__(self, shapes, joints, renderer)
    def update(self, world):
        self.agent.update(self, world)
        pass

class Ball(ControllableEntity):
    def __init__(self, position,radius, mass = 10, inertia=100, friction = 0.5, agent=None, renderer=None):
        body = pm.Body(mass, inertia)
        body.position = position
        shape = pm.Circle(body, radius, Vec2d(0,0))
        shape.friction = friction
        ControllableEntity.__init__(self, [shape],agent=agent,renderer=renderer)
        
class Platform(SimpleEntity):
    def __init__(self, a,b, thickness=5.0, friction=0.99, renderer=None):
        body = pm.Body(pm.inf, pm.inf)
        shape= pm.Segment(body, Vec2d(a[0],a[1]), Vec2d(b[0],b[1]), thickness/2.0)
        shape.friction = friction
        SimpleEntity.__init__(self, shape, renderer)
                
class Level(Entity):
    #importing levels later
    def __init__(self, shapes=[], tile_size=30, renderer=None):
        shapes = []
        self.tile_size = tile_size
        self.level_tiles = [(1,1),(2,1),(3,1),(4,1),(5,1), (7,1)] #lolz 5 tile level
        for tile in self.level_tiles:
            body = pm.Body(pm.inf, pm.inf)
            shape = pm.Poly(body, self.tileToVertices(tile))
            shapes.append(shape)
        Entity.__init__(self, shapes, [], renderer)
    
    def tileToQuad(self, indexTuple):
        x = indexTuple[0] * self.tile_size
        y = indexTuple[1] * self.tile_size
        x-=self.tile_size
        y-=self.tile_size
        return (x, y, 
                x+self.tile_size,y,
                x+self.tile_size, y+self.tile_size,
                x, y+self.tile_size
                )
    def tileToVertices(self, indexTuple):
        x = indexTuple[0] * self.tile_size
        y = indexTuple[1] * self.tile_size
        x-=self.tile_size
        y-=self.tile_size
        return [(x, y), 
                (x+self.tile_size,y),
                (x+self.tile_size, y+self.tile_size),
                (x, y+self.tile_size)                
                ]
