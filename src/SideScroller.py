import pyglet
from pyglet.window import mouse
import primitives
import pymunk as pm
from pymunk import Vec2d
import math
import re

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

class World(pm.Space):
    def __init__(self, gravity=Vec2d(0.0, -900.0)):
        pm.Space.__init__(self)
        self.gravity = gravity
    

class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()

        self.label = pyglet.text.Label('Hello, world!')
        self.image = pyglet.resource.image("ball.png")
        
        #self.circle = primitives.Circle(x=320, y=240, z=1, width=20, color=(1,1,1,1), stroke=200)
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        self.balls = []
        self.sprites = []
        
        self.line = primitives.Line( a=(1,1), b=(100,100), z=1, color=(1,1,1,1), stroke=10)
        self.lines = []
        
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        self.mouse_shape.collision_type = COLLTYPE_MOUSE
        self.space.add(self.mouse_shape)

        self.space.add_collisionpair_func(COLLTYPE_MOUSE, COLLTYPE_DEFAULT, mouse_coll_func, ("hello", "world"))
        self.line_point1 = None
        self.line_point2 = None
        self.static_lines = []
        self.run_physics = True
        pyglet.clock.schedule_interval(self.update, 1.0/100)
        #music = pyglet.resource.media('music.mp3')
        #music.play
        #sound = pyglet.resource.media('shot.wav', streaming=False)
        #sound.play()

    def update(self,dt):
        if self.run_physics:
            self.space.step(dt)
            for primi,shape in self.sprites:
                primi.x = shape.body.position[0]
                primi.y = shape.body.position[1]

    def on_draw(self):
        self.clear()
        for x in self.sprites:
            x[0].render()
        for x in self.lines:
            x.render()
        if self.line_point1 is not None and self.line_point2 is not None:
            lp1 = self.line_point1
            lp2 = self.line_point2
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(lp1.x), int(lp1.y), int(lp2.x), int(lp2.y))))
        
        
        self.label.draw()
        #self.image.blit(200,200)
        #self.circle.render()
        #pyglet.gl.glColor4f(1.0,0,0,1.0)
        
    
    def on_key_press(self, symbol, modifiers):
        print 'A key was pressed'
        
    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            p = x, y
            body = pm.Body(10, 100)
            body.position = p
            shape = pm.Circle(body, 10, Vec2d(0,0))
            shape.friction = 0.5
            self.space.add(body, shape)
            self.balls.append(shape)
            sprite = primitives.Circle(x=x, y=y, z=1, width=20, color=(1,1,1,1), stroke=200)
            self.sprites.append((sprite,shape))
            print 'The left mouse button was pressed.'
        elif button == mouse.RIGHT:
            if self.line_point1 is None:
                    self.line_point1 = Vec2d(x, y)
                    self.line_point2 = Vec2d(x,y)
                    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if mouse.RIGHT <= buttons:
            self.line_point2 = Vec2d(x,y)
        
    def on_mouse_release(self, x,y, button, modifiers):
        if button == mouse.RIGHT:
            if self.line_point1 is not None:
                line_point2 = Vec2d(x, y)
                print self.line_point1, line_point2
                body = pm.Body(pm.inf, pm.inf)
                shape= pm.Segment(body, self.line_point1, line_point2, 0.0)
                shape.friction = 0.99
                self.space.add_static(shape)
                self.static_lines.append(shape)
                line = primitives.Line( a=(self.line_point1.x,self.line_point1.y), b=(x,y), z=1, color=(1,1,1,1), stroke=10)
                self.lines.append(line)
                self.line_point1 = None
        pass
            
def mouse_coll_func(s1, s2, cs, normal_coef, data):
    """Simple callback that increases the radius of circles touching the mouse"""
    if s2.collision_type != COLLTYPE_MOUSE and type(s2) == pm.Circle:
        s2.radius += 0.15
    return False

if __name__ == '__main__':
    window = HelloWorldWindow()
    window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()