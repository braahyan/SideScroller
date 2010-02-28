'''
Created on Feb 21, 2010

@author: Bryan
'''

import primitives
import pyglet

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
        
class TileRenderer:
    #going to cheat here for now, should be able to get access to the window size
    def __init__(self,texture,tiles, camera, tile_size=30):
        self.texture = texture
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.camera = camera
        self.tile_size = tile_size
        for tile in tiles:
            sprite = pyglet.sprite.Sprite(self.texture, (tile[0]-1)*tile_size, (tile[1]-1)*tile_size, batch=self.batch)
            sprite.tile_coord = tile
            self.sprites.append(sprite)

    def render(self, entity):
        for sprite in self.sprites:
            a,b = sprite.tile_coord
            x,y = self.camera.translate((a-1)*self.tile_size, (b-1)*self.tile_size,)
            sprite.x = x
            sprite.y = y
        self.batch.draw()