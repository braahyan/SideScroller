'''
Created on Feb 21, 2010

@author: Bryan
'''
import pymunk as pm
from pymunk import Vec2d
class World(pm.Space):
    def __init__(self, gravity=(0.0, -900.0)):
        pm.Space.__init__(self)
        self.gravity = Vec2d(gravity[0],gravity[1])
        self.entities = []
        self.static_entities = []
    
    def addEntity(self, entity):
        self.entities.append(entity)
        for x in entity.shapes:
            self.add(x, x.body)
        for x in entity.joints:
            self.add(x)

    def addStaticEntity(self, entity):
        self.static_entities.append(entity)
        for x in entity.shapes:
            self.add_static(x)