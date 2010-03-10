import pyglet
pyglet.options['audio'] = ('openal', 'silent') #this needs to be set before importing pyglet.media
PROJ_HOME_RELATIVE = '..'

#need to get resource loading working
class SoundRenderer:
    def __init__(self):
        self.soundpaths = ['sound']

    def do_action(self, action_string):
        raise NotImplemented
        
class BallSoundRenderer(SoundRenderer):
    def __init__(self):
        SoundRenderer.__init__(self)
        self.soundpaths.append('sound/ball')
        self.loader = pyglet.resource.Loader(path=self.soundpaths, script_home=PROJ_HOME_RELATIVE)
        #load up all sounds, probably faster than loading a la carte
        self.jump_sound = self.loader.media('sega.wav', streaming=False)

    #use a string, possibly later a message object or dict or whatever to specify action
    def do_action(self, action_string):
        if action_string == 'jump':
            self.jump_sound.play()

        
