import pyglet
pyglet.options['audio'] = ('openal', 'silent') #this needs to be set before importing pyglet.media

#need to get resource loading working
class SoundRenderer:
    def __init__(self):
        pass
    def render(self):
        raise NotImplemented
        
class BallSoundRenderer(SoundRenderer):
    def __init__(self):
        #load up sounds, probably faster than loading a la carte
        self.jump_sound = pyglet.resource.media('sega.wav', streaming=False)

    #this might fit for passing inputmanager bindings directly in
    def do_action(self, action_string):
        if action_string == 'jump':
            self.jump_sound.play()

        
