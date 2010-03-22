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
import json

TILE_COLLTYPE = 0
PLAYER_COLLTYPE = 1
ENTITY_COLLTYPE = 2
RESPAWN_COLLTYPE = 3
MOUSE_COLLTYPE = 4

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
                         "smilie-small.gif":pyglet.image.load('../img/smilie-small.gif')}
        
        #load level
        #level_tiles = [{'x': x, 'y' : 1, 'texture': 'dirt.gif'} for x in range(1,30)]
        level_tiles = self.load_level('blarf')
        tile_renderer = renderers.TileRenderer(self.textures, level_tiles, camera)
        level = entity.Terrain(level_tiles=level_tiles,renderer = tile_renderer)
        self.space.addStaticEntity(level)
        
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        self.mouse_shape.sensor = True
        self.mouse_shape.collision_type = MOUSE_COLLTYPE
        self.space.add(self.mouse_shape)
        
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
        

        self.ball_spawn_point = (50, 300)
        self.ball = entity.Ball(self.ball_spawn_point, 10, 10, 100, .5, agent=self.keyboard_agent,renderer = circle_renderer)
        #self.evilcat = entity.EvilCat((evilcat_renderer.cat_sprite.x, evilcat_renderer.cat_sprite.y), 64, 64, renderer=evilcat_renderer)
        #self.evilcat = entity.EvilCatSquare((evilcat_renderer.cat_sprite.x, evilcat_renderer.cat_sprite.y), 32, renderer=evilcat_renderer)
        self.evilcat = entity.RespawnSquare((evilcat_renderer.cat_sprite.x, evilcat_renderer.cat_sprite.y), 32, renderer=evilcat_renderer)
        self.space.addEntity(self.ball)
        #self.space.addEntity(self.evilcat)
        self.space.addStaticEntity(self.evilcat)
        self.hud_manager = hud.HudManager()
        #music = pyglet.resource.media('music.mp3')
        #music.play
        self.space.add_collision_handler(PLAYER_COLLTYPE, RESPAWN_COLLTYPE, self.respawnCallBack, None, None, None, player_entity=self.ball)
    
    def respawnCallBack(self, space, arb, player_entity=None):
        player_body = player_entity.shapes[0].body
        player_body.position = self.ball_spawn_point 
        player_body._set_velocity(Vec2d(0,0))
        player_body._set_angular_velocity(0)
        player_body.reset_forces()
        return False

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

    def load_level(self, filename):
        level_file = pyglet.resource.file('level_1.lvl')
        level_str = level_file.read()
        level_json = json.loads(level_str)
        tile_list = level_json['tiles']

        #go go gadget hack in respawn points! 
        tile_list.append({'x': 1, 'y' : 0, 'texture': 'smilie-small.gif', 'colltype' : RESPAWN_COLLTYPE})
        tile_list.append({'x': 18, 'y' : 0, 'texture': 'smilie-small.gif', 'colltype' : RESPAWN_COLLTYPE})
        tile_list.append({'x': 21, 'y' : 0, 'texture': 'smilie-small.gif', 'colltype' : RESPAWN_COLLTYPE})
        return tile_list

            
def mouse_coll_func(s1, s2, cs, normal_coef, data):
    """Simple callback that increases the radius of circles touching the mouse"""
    if s2.collision_type != MOUSE_COLLTYPE and type(s2) == pm.Circle:
        s2.radius += 0.15
    return False

if __name__ == '__main__':
    window = HelloWorldWindow()
    
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()
