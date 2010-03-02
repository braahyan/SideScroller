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
    def __init__(self,texture,tiles,tile_size=30):
        self.texture = texture
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        for tile in tiles:
            self.sprites.append(pyglet.sprite.Sprite(self.texture, (tile[0]-1)*tile_size, (tile[1]-1)*tile_size, batch=self.batch))

    def render(self, entity):
        self.batch.draw()
        
class SpriteRenderer:
    #hardcodizzle
    def __init__(self):
        self.image_list = [pyglet.image.load('../img/anim/frame1.png'),
                            pyglet.image.load('../img/anim/frame2.png'),
                            pyglet.image.load('../img/anim/frame3.png'),
                            pyglet.image.load('../img/anim/frame4.png'),
                            pyglet.image.load('../img/anim/frame5.png'),
                            pyglet.image.load('../img/anim/frame6.png'),
                            pyglet.image.load('../img/anim/frame7.png')]
    def render(self)
        bin = pyglet.image.atlas.TextureBin()
        images = [bin.add(image) for image in self.image_list]
        #ANIMATE STUFF
        
        
