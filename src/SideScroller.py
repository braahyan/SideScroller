import pyglet
from pyglet.window import mouse
from pyglet.window import key
import renderers
import entity
import world
import pymunk as pm
from pymunk import Vec2d
import agent
from camera import Camera
import inputmanager
import hud

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_PLATFORM = 2

camera = Camera(640, 480,offset=(-30,0))
circle_renderer = renderers.CircleRenderer(camera)
evilcat_renderer = renderers.EvilCatRenderer(300, 100, 64, 64, camera)
platform_renderer = renderers.PlatformRenderer(camera)

pyglet.options['audio'] = ('openal', 'silent') #this needs to be set before importing pyglet.media

#POOOPS!
class HelloWorldWindow(pyglet.window.Window):
    def __init__(self):
        super(HelloWorldWindow, self).__init__()
        
        pm.init_pymunk()
        self.space = world.World()
        self.tilebatch = pyglet.graphics.Batch()
        self.textures = {"dirt.gif":pyglet.image.load('../img/dirt.gif'),
                         "smilie.gif":pyglet.image.load('../img/smilie.gif')}
        
        #load level
        level_tiles = [(x,1,"dirt.gif") for x in range(1,30)]
        tile_renderer = renderers.TileRenderer(self.textures, level_tiles, camera)
        level = entity.Terrain(level_tiles=level_tiles,renderer = tile_renderer)
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
        self.ball = entity.Ball((20,300), 10, 10, 100, .5, agent=self.keyboard_agent,renderer = circle_renderer)
        #self.evilcat = entity.EvilCat((evilcat_renderer.cat_sprite.x, evilcat_renderer.cat_sprite.y), 64, 64, renderer=evilcat_renderer)
        self.evilcat = entity.EvilCatCircle((evilcat_renderer.cat_sprite.x, evilcat_renderer.cat_sprite.y), 32, renderer=evilcat_renderer)
        self.space.addEntity(self.ball)
        self.space.addEntity(self.evilcat)
        self.hud_manager = hud.HudManager()
        #music = pyglet.resource.media('music.mp3')
        #music.play
        #self.SEGA_sound = pyglet.resource.media('sega.wav', streaming=False)
        #self.SEGA_sound.play()

    def update(self,dt):
        if self.run:
            for x in range(0,3):
                self.space.step(dt/3)
            for y in self.space.entities:
                y.update(self.space)
            self.input_manager.clear()
            camera.update(self.ball.position[0], self.ball.position[1])
    
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
            
        self.fps_display.draw()
        self.hud_manager.render()
        
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.run = not self.run
    
    def on_mouse_motion(self,x,y,dx,dy):
        mouse_pos = Vec2d(x,y)
        self.mouse_body.position = mouse_pos

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.RIGHT:
            if self.line_point1 is None:
                    self.line_point1 = camera.reverse_translate(x,y)
                    self.line_point2 = camera.reverse_translate(x,y)
                    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if mouse.RIGHT & buttons:
            x,y = camera.reverse_translate(x,y)
            self.line_point2 = Vec2d(x,y)
        
    def on_mouse_release(self, x,y, button, modifiers):
        if button == mouse.RIGHT:
            if self.line_point1 is not None:
                x,y = camera.reverse_translate(x,y)
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
