import pyglet
from pyglet.window import mouse
from pyglet.window import key
import renderers
import entity
import world
import pymunk as pm
from pymunk import Vec2d
import agent
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
        
circle_renderer = renderers.CircleRenderer()
platform_renderer = renderers.PlatformRenderer()

#POOOPS!
class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()
        
        pm.init_pymunk()
        self.space = world.World()
        
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        self.mouse_shape.collision_type = COLLTYPE_MOUSE
        self.space.add(self.mouse_shape)
        self.space.add_collisionpair_func(COLLTYPE_MOUSE, COLLTYPE_DEFAULT, mouse_coll_func, ("hello", "world"))
        
        self.line_point1 = None
        self.line_point2 = None
        self.run_physics = True
        self.key = key.KeyStateHandler()
        self.push_handlers(self.key)
        self.keyboard_agent = agent.KeyboardAgent(self.key)
        self.push_handlers(self.key)
        pyglet.clock.schedule_interval(self.update, 1.0/100)
        #music = pyglet.resource.media('music.mp3')
        #music.play
        #sound = pyglet.resource.media('shot.wav', streaming=False)
        #sound.play()

    def update(self,dt):
        if self.run_physics:
            for x in range(3):
                self.space.step(dt/3.0)
            for y in self.space.entities:
                if hasattr(y, "update"):
                    y.update()

    def on_draw(self):
        self.clear()
        for x in self.space.entities:
            x.render()
        for x in self.space.static_entities:
            x.render()
        if self.line_point1 is not None and self.line_point2 is not None:
            lp1 = self.line_point1
            lp2 = self.line_point2
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (int(lp1[0]), int(lp1[1]), int(lp2[0]), int(lp2[1]))))
        
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.run_physics = not self.run_physics
    
    def on_mouse_motion(self,x,y,dx,dy):
        mouse_pos = Vec2d(x,y)
        self.mouse_body.position = mouse_pos

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            p = x, y
            ball = entity.Ball(p, 10, 10, 100, .5, agent=self.keyboard_agent,renderer = circle_renderer)
            self.space.addEntity(ball)
            print 'The left mouse button was pressed.'
        elif button == mouse.RIGHT:
            if self.line_point1 is None:
                    self.line_point1 = x,y
                    self.line_point2 = x,y
                    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if mouse.RIGHT & buttons:
            self.line_point2 = Vec2d(x,y)
        
    def on_mouse_release(self, x,y, button, modifiers):
        if button == mouse.RIGHT:
            if self.line_point1 is not None:
                line_point2 = Vec2d(x, y)
                print self.line_point1, line_point2
                platform = entity.Platform(self.line_point1, line_point2, 5, renderer=platform_renderer)
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
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
