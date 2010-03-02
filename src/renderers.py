'''
Created on Feb 21, 2010

@author: Bryan
'''

import primitives
import pyglet
import quadtree
import SideScroller

class CircleRenderer:
    def __init__(self, camera, width=20, color=(1,1,1,1), stroke=200):
        self.primitive = primitives.Circle(x=0, y=0, z=1, width=width, color=color, stroke=stroke)
        self.camera = camera
        pass
    def render(self, entity):
        ball = entity.shapes[0]
        x,y = self.camera.translate(ball.body.position[0],ball.body.position[1])
        self.primitive.x = x 
        self.primitive.y = y
        self.primitive.width = ball.radius * 2
        self.primitive.render()

class PlatformRenderer:
    def __init__(self, camera):
        self.primitive = primitives.Line( a=(1,1), b=(100,100), z=1, color=(1,1,1,1), stroke=10)
        self.camera = camera
    def render(self, entity):
        platform = entity.shapes[0]
        a = self.camera.translate(platform.a[0],platform.a[1])
        b = self.camera.translate(platform.b[0],platform.b[1])
        self.primitive.init(a, b)
        self.primitive.width = platform.radius*2
        self.primitive.render()
        
class TileRenderer:
    #going to cheat here for now, should be able to get access to the window size
    def __init__(self,textures,tiles, camera, tile_size=30):
        self.textures = textures
        self.sprites = []
        self.camera = camera
        self.tile_size = tile_size
        self.batch = pyglet.graphics.Batch()
        self.tiles = []
        for tile in tiles:
            x,y,texture = tile
            xp = (x-1) * tile_size
            yp = (y-1) * tile_size
            sprite = pyglet.sprite.Sprite(self.textures[texture], xp, yp, batch=self.batch)
            sprite.tile_coord = tile
            t = quadtree.Rect(xp, yp, xp + tile_size, yp - tile_size)
            self.sprites.append(sprite)
            self.tiles.append(t)
        self.quad_tree = quadtree.QuadTree(items=self.tiles)

    def render(self, entity):
        cx, cy = self.camera.offset
        width = self.camera.width
        height = self.camera.height
        top = cy
        right = cx+width
        left = cx
        bottom = cy-height
        print self.quad_tree.hit(quadtree.Rect(left, top, right, bottom))
        for sprite in self.sprites:
            a,b,t = sprite.tile_coord
            x,y = self.camera.translate((a-1)*self.tile_size, (b-1)*self.tile_size,)
            sprite.x = x
            sprite.y = y
        self.batch.draw()
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
        bin = pyglet.image.atlas.TextureBin()
        images = [bin.add(image) for image in self.image_list]
        animation = pyglet.image.Animation.from_image_sequence(images, 0.1, True)
        self.sprite = pyglet.sprite.Sprite(animation, x=200, y=50)
    def render(self):
        self.sprite.draw()
        #ANIMATE STUFF
        #pyglet.resource.
        
execfile('SideScroller.py')
