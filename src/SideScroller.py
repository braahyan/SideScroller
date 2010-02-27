import pyglet
from pyglet.window import mouse
from pyglet.window import key
import renderers
import entity
import world
import pymunk as pm
from pymunk import Vec2d
import agent
import inputmanager

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_PLATFORM = 2
        
circle_renderer = renderers.CircleRenderer()
platform_renderer = renderers.PlatformRenderer()
tile_renderer = renderers.TileRenderer(640, 480, 30)

#POOOPS!
class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()
        
        pm.init_pymunk()
        self.space = world.World()
        
        #load level
        level = entity.Level(renderer = tile_renderer)
        self.space.addStaticEntity(level)
        
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        self.mouse_shape.sensor = True
        self.mouse_shape.collision_type = COLLTYPE_MOUSE
        self.space.add(self.mouse_shape)
        self.space.add_collisionpair_func(COLLTYPE_MOUSE, COLLTYPE_DEFAULT, mouse_coll_func, ("hello", "world"))
        
        self.line_point1 = None
        self.line_point2 = None
        self.run = True
        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)
        self.input_manager = inputmanager.KeyboardManager()
        self.keyboard_agent = agent.KeyboardAgent(self.input_manager)
        self.fps = 60
        pyglet.clock.schedule_interval(self.update, 1.0/self.fps)
        pyglet.clock.schedule_interval(self.update_keys, 1.0/self.fps)
        pyglet.clock.set_fps_limit(self.fps*2)
        self.fps_display = pyglet.clock.ClockDisplay()
        #music = pyglet.resource.media('music.mp3')
        #music.play
        #sound = pyglet.resource.media('shot.wav', streaming=False)
        #sound.play()

    def update(self,dt):
        if self.run:
            for x in range(3):
                self.space.step(dt/3.0)
            for y in self.space.entities:
                y.update(self.space)
            self.input_manager.clear()
    
    def update_keys(self,dt):
        if self.run:
            for key in [x for x in self.input_manager.key_config.keys() if self.keyboard[x]]:
                self.input_manager.append(key, True)

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
        self.fps_display.draw()
        
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.run = not self.run
    
    def on_mouse_motion(self,x,y,dx,dy):
        mouse_pos = Vec2d(x,y)
        self.mouse_body.position = mouse_pos

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            p = x, y
            ball = entity.Ball(p, 10, 10, 100, .5, agent=self.keyboard_agent,renderer = circle_renderer)
            self.space.addEntity(ball)
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
                platform = entity.Platform(self.line_point1, line_point2, 5, renderer=platform_renderer)
                self.space.addStaticEntity(platform)
                self.line_point1 = None
            
def mouse_coll_func(s1, s2, cs, normal_coef, data):
    """Simple callback that increases the radius of circles touching the mouse"""
    if s2.collision_type != COLLTYPE_MOUSE and type(s2) == pm.Circle:
        s2.radius += 0.15
    return False

if __name__ == '__main__':
    window = HelloWorldWindow()
    
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
