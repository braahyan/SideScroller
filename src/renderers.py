'''
Created on Feb 21, 2010

@author: Bryan
'''

import primitives
import pyglet
import math

PROJ_HOME_RELATIVE = '..'

class Renderer:
    def __init__(self):
        self.imgpaths = ['img']

    def render(self):
        raise NotImplemented
        
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
        
class EvilCatRenderer(Renderer):
    def __init__(self, x, y, width, height, camera):
        Renderer.__init__(self)
        self.loader = pyglet.resource.Loader(path=self.imgpaths, script_home=PROJ_HOME_RELATIVE)
        cat_texture = self.loader.texture('evilcat.gif')
        
        #does we need these elsewhere?
        self.width = width
        self.height = height
        
        cat_texture.anchor_x = self.width/2
        cat_texture.anchor_y = self.height/2
        self.cat_sprite = pyglet.sprite.Sprite(cat_texture, x, y)
        self.camera = camera

    def render(self, entity):
        cx, cy = self.camera.offset
        width = self.camera.width
        height = self.camera.height
        top = cy
        right = cx+width
        left = cx
        bottom = cy-height
        cat_rect = entity.shapes[0]
        x,y = self.camera.translate(cat_rect.body.position[0],cat_rect.body.position[1])
        self.cat_sprite.x = x
        self.cat_sprite.y = y
        self.cat_sprite.rotation = -math.degrees(cat_rect.body._get_angle())
        self.cat_sprite.draw()

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
        for tile in tiles:
            #x,y,texture = tile
            x = tile['x']
            y = tile['y']
            texture = tile['texture']
            xp = (x-1) * tile_size
            yp = (y-1) * tile_size
            sprite = pyglet.sprite.Sprite(self.textures[texture], xp, yp, batch=self.batch)
            sprite.tile_coord = tile
            self.sprites.append(sprite)

    def render(self, entity):
        for sprite in self.sprites:
            #a,b,t = sprite.tile_coord
            a = sprite.tile_coord['x']
            b = sprite.tile_coord['y']
            t = sprite.tile_coord['texture']
            x,y = self.camera.translate((a-1)*self.tile_size, (b-1)*self.tile_size)
            sprite.x = x
            sprite.y = y
            
            if sprite.x+self.tile_size <0 or sprite.y+self.tile_size<0 or sprite.x > self.camera.width or sprite.y > self.camera.height:
                sprite.visible = False
            else:
                sprite.visible = True
        self.batch.draw()
        
class FpsRenderer(Renderer):
    def __init__(self):
        pass
        
class HudAngryRenderer(Renderer):
    def __init__(self, x, y):
        Renderer.__init__(self)
        self.imgpaths.append('img/anim')
        self.loader = pyglet.resource.Loader(path=self.imgpaths, script_home=PROJ_HOME_RELATIVE)
        self.image_list = [self.loader.image('frame1.png'),
                           self.loader.image('frame2.png'),
                           self.loader.image('frame3.png'),
                           self.loader.image('frame4.png'),
                           self.loader.image('frame5.png'),
                           self.loader.image('frame6.png'),
                           self.loader.image('frame7.png')]
        self.x = x
        self.y = y
        self.anim_speed=0.1
        
        animation = pyglet.image.Animation.from_image_sequence(self.image_list, self.anim_speed, True)
        self.sprite = pyglet.sprite.Sprite(animation, x=self.x, y=self.y)
    def render(self):
        self.sprite.draw()
