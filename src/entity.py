'''
Created on Feb 21, 2010

@author: Bryan
'''

import pymunk as pm
from pymunk import Vec2d

COLLTYPE_PLATFORM = 2

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

class Ball(ControllableEntity):
    def __init__(self, position,radius, mass = 10, inertia=100, friction = 0.99, agent=None, renderer=None):
        body = pm.Body(mass, inertia)
        body.position = position
        shape = pm.Circle(body, radius, Vec2d(0,0))
        shape.friction = friction
        ControllableEntity.__init__(self, [shape],agent=agent,renderer=renderer)
    def get_position(self):
        return self.shapes[0].body.position
    position = property(get_position)
    
class EvilCat(SimpleEntity):
    def __init__(self, position, x_length, y_length, mass = 10, inertia=100, friction = 0.99, renderer=None):
        self.poscount = 0
        body = pm.Body(mass, inertia)
        initial_bounds = [Vec2d(0, 0),
                          Vec2d(0,y_length), 
                          Vec2d(x_length,y_length), 
                          Vec2d(x_length, 0)]
        
        shape = pm.Poly(body, initial_bounds)
        body.position = position
        shape.friction = friction
        SimpleEntity.__init__(self, shape, renderer)
    def get_position(self):
        return self.shapes[0].body.position
    position = property(get_position)
    
    def update(self, world):
        pass
        #if self.poscount< 100:
            #print self.get_position()
            #print self.shapes[0].body._get_angle() #Radians!!!
            #print self.shapes[0].get_points()
            #self.poscount += 1
            
class EvilCatCircle(SimpleEntity):
    def __init__(self, position,radius, mass = 10, inertia=100, friction = 0.99, agent=None, renderer=None):
        body = pm.Body(mass, inertia)
        body.position = position
        shape = pm.Circle(body, radius, Vec2d(0,0))
        shape.friction = friction
        SimpleEntity.__init__(self, shape, renderer)
    def get_position(self):
        return self.shapes[0].body.position
    position = property(get_position)
    
    def update(self, world):
        pass
        
class Platform(SimpleEntity):
    def __init__(self, a,b, thickness=5.0, friction=0.99, renderer=None):
        body = pm.Body(pm.inf, pm.inf)
        shape= pm.Segment(body, Vec2d(a[0],a[1]), Vec2d(b[0],b[1]), thickness/2.0)
        shape.friction = friction
        shape.collision_type = COLLTYPE_PLATFORM
        SimpleEntity.__init__(self, shape, renderer)
                
class Terrain(Entity):
    #importing levels later
    def __init__(self, level_tiles, shapes=[], tile_size=30, friction=.99, renderer=None):
        shapes = []
        self.tile_size = tile_size
        self.level_tiles = level_tiles
        for tile in self.level_tiles:
            body = pm.Body(pm.inf, pm.inf)
            shape = pm.Poly(body, self.tileToVertices(tile))
            shape.friction = friction
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
