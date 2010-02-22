import pyglet
from pyglet.window import mouse
import primitives
import pymunk as pm
from pymunk import Vec2d
import cPickle

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

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
        

class Level:
    pass

class Entity:
    '''class for physics object represented by some renderer'''
    def __init__(self, shapes=[],joints=[], renderer=None):
        self.shapes = shapes
        self.joints = joints
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
    def __init__(self, a,b, thickness=5.0, renderer=None):
        body = pm.Body(pm.inf, pm.inf)
        shape= pm.Segment(body, a, b, thickness/2.0)
        shape.friction = 0.99
        SimpleEntity.__init__(self, shape, renderer)

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
        
circle_renderer = CircleRenderer()        
platform_renderer = PlatformRenderer()

class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()
        
        #self.circle = primitives.Circle(x=320, y=240, z=1, width=20, color=(1,1,1,1), stroke=200)
        pm.init_pymunk()
        self.space = World()
        
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        self.mouse_shape.collision_type = COLLTYPE_MOUSE
        self.space.add(self.mouse_shape)
        self.space.add_collisionpair_func(COLLTYPE_MOUSE, COLLTYPE_DEFAULT, mouse_coll_func, ("hello", "world"))
        
        self.line_point1 = None
        self.line_point2 = None
        self.run_physics = True
        pyglet.clock.schedule_interval(self.update, 1.0/100)
        #music = pyglet.resource.media('music.mp3')
        #music.play
        #sound = pyglet.resource.media('shot.wav', streaming=False)
        #sound.play()

    def update(self,dt):
        if self.run_physics:
            for x in range(3):
                self.space.step(dt/3.0)

    def on_draw(self):
        self.clear()
        primitives.Line( a=(1,1), b=(100,100), z=1, color=(1,1,1,1), stroke=10)
        for x in self.space.entities:
            x.render()
        for x in self.space.static_entities:
            x.render()
        if self.line_point1 is not None and self.line_point2 is not None:
            lp1 = self.line_point1
            lp2 = self.line_point2
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(lp1.x), int(lp1.y), int(lp2.x), int(lp2.y))))
        
    
    def on_key_press(self, symbol, modifiers):
        if symbol == 32:
            self.run_physics = not self.run_physics            
        print symbol
    
    def on_mouse_motion(self,x,y,dx,dy):
        mouse_pos = Vec2d(x,y)
        self.mouse_body.position = mouse_pos

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            p = x, y
            ball = Ball(p, 10, 10, 100, .5, renderer = circle_renderer)
            self.space.addEntity(ball)
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
                platform = Platform(self.line_point1, line_point2, 5, renderer=platform_renderer)
                self.space.addStaticEntity(platform)
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