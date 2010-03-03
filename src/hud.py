import renderers

class HudManager:
    '''Container class for HudElements'''
    def __init__(self, elements=None):
        '''elements - dict with a string for a key, and a HudElement as a value'''
        if not elements:
            #default hud elements, maybe move entire setup to config file later
            self.elements = {}
            angry_renderer = renderers.HudAngryRenderer(320, 430)
            angry_indicator = HudElement('angry', angry_renderer)
            self.elements[angry_indicator.name] = angry_indicator
        else:
            self.elements = elements

    def add(self, name, element):
        self.elements[name] = element
    
    def hide(self, element_name):
        self.elements[element_name].is_hidden=True
        
    def show(self, element_name):
        self.elements[element_name].is_hidden=False
        
    def remove(self, hud_element_name):
        raise NotImplemented
        
    def hideAll(self):
        raise NotImplemented
        
    def render(self):
        [element.render() for element in self.elements.values()]
    
class HudElement:
    '''Element to a heads up display'''
    def __init__(self, name, renderer, is_hidden=False): 
        self.name = name
        self.renderer = renderer
        self.is_hidden = is_hidden
        
    def render(self):
        if not self.is_hidden:
            self.renderer.render()
        else:
            pass
        
        
class FpsHudElement(HudElement):
    def __init__(self, name):
        self.fps_display = pyglet.clock.ClockDisplay()

    def render(self):
        self.fps_display.draw()
