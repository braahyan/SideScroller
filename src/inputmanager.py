'''
Created on Feb 24, 2010

@author: Bryan
'''

# event_name(jump), accelerators

from pyglet.window import key

class KeyboardManager:
    def __init__(self, key_config={key.LEFT:"left", key.RIGHT:"right", key.UP:"up", key.DOWN:"down"}):
        self.key_config = key_config
        self.data = {}
    
    def translate(self, key):
        if self.key_config.has_key(key):
            return self.key_config[key]
        else:
            return False
    
    def append(self, key, data=True):
        self.data[self.translate(key)] = data
    
    def __getitem__(self, key):
        if self.data.has_key(key):
            return self.data
        else:
            return False
    
    def clear(self):
        self.data.clear()