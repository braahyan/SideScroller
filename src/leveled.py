import Tkinter
import tkFileDialog
import tkMessageBox
import random
import math
import json

class Leveled:
    def __init__(self):
    
        self.TILE_SIZE = 30
        self.TEX_DIRECTORY = '../img/'
        self.tkWindow = Tkinter.Tk()
        
        #this is a dict so we can have texture filenames,
        #transparency, and other various tile properties, etc etc
        #might want to abstract this out to an object eventually
        smilie_tile = {
                       'filename' : 'smilie-small.gif', 
                       'texture_object' : Tkinter.PhotoImage(file = '%ssmilie-small.gif' % self.TEX_DIRECTORY)
                      }
        dirt_tile = {
                     'filename' : 'dirt.gif', 
                     'texture_object' : Tkinter.PhotoImage(file = '%sdirt.gif' % self.TEX_DIRECTORY)
                    }
        self.tileTexList = [dirt_tile, smilie_tile]
        self.gridCanvasIds = []
        self.selectedTexture = 0
        
        #need to make this into a real drop down menu eventually
        menuButton = Tkinter.Menubutton(self.tkWindow)
        menubar = Tkinter.Menu(self.tkWindow)
        menubar.add_command(label="New Level", command=self.newLevel)
        menubar.add_command(label="Save Level", command=self.saveLevel)
        menubar.add_command(label="Load Level", command=self.loadLevel)
        menubar.add_command(label="Load Texture", command=self.loadTexture)
        menubar.add_command(label="Quit!", command=self.tkWindow.quit)
        self.tkWindow.config(menu=menubar)
        
        self.width = 640
        self.height = 480
        
        self.canvas = Tkinter.Canvas(self.tkWindow, width=self.width, height=self.height)
        self.canvas.bind("<Button-1>",self.drawTileEvent)
        self.canvas.bind("<Button-3>", self.switchTexture)
        self.canvas.pack()
        self.drawGrid()
        
        self.save_level_json = {'tiles' : []}
        
    def canvasCoordToJson(self, x, y):
        '''Converts Tkinter Canvas coordinates to Json coordinates.'''
        return ((x/self.TILE_SIZE)+1, (self.height-y)/self.TILE_SIZE)
    
    def jsonCoordToCanvas(self, x, y):
        '''Converts Json coordinates to Tkinter Canvas coordinates.'''
        return ((x*self.TILE_SIZE)-1, self.height-(y*self.TILE_SIZE))
        
    def drawGrid(self):
        '''Draws a grid over the canvas based on what your specified tile size is.'''
        for i in range(1, self.height/self.TILE_SIZE):
            canvas_id = self.canvas.create_line(0, i*self.TILE_SIZE, self.width, i*self.TILE_SIZE)
            self.gridCanvasIds.append(canvas_id)
            
        for i in range(1, self.width/self.TILE_SIZE):
            canvas_id = self.canvas.create_line(i*self.TILE_SIZE, 0, i*self.TILE_SIZE, self.height)
            self.gridCanvasIds.append(canvas_id)
            
    def drawTileEvent(self, event):
        '''Event triggered when the mouse is clicked in the canvas'''
        x = event.x 
        y = event.y 
        texture = self.tileTexList[self.selectedTexture]
        tile_object = {'x' : x, 'y' : y, 'texture' : texture}
        self.drawTile(tile_object)
        
        
        
    def drawTile(self, tile):
        '''Draws a tile given a dict like
        {'x' : int, 'y' : int, 'texture' : smilie_tile, 'colltype' : int}
           Returns True if tile is overwriting another, False otherwise'''
        x = tile['x'] - (tile['x']%self.TILE_SIZE)
        y = tile['y'] - (tile['y']%self.TILE_SIZE)
        texture_name = tile['texture']['filename']
        texture = tile['texture']['texture_object']
        self.canvas.create_image(x, y, image = texture, anchor=Tkinter.NW)
     
        #check for duplicate tiles to replace in the json record
        (tile['x'],tile['y']) = self.canvasCoordToJson(x,y) # woo, destructive to original object
        
        for json_tile in self.save_level_json['tiles']:
            if json_tile['x'] == tile['x'] and json_tile['y'] == tile['y']:
                print json_tile
                json_tile['texture'] = tile['texture']['filename']
                #json_tile = tile doesn't work here... maybe a reference/value issue?
                print 'replaced tile: ', `json_tile`
                return True
        
        #if no duplicates, append
        self.save_level_json['tiles'].append({'x' : tile['x'], 
                                              'y' : tile['y'],
                                              'texture' : texture_name,
                                              'colltype' : 0})
        print 'did not replace tile'
        return False
    
    def loadTexture(self):
        '''Loads a texture into the available texture list'''
        try:
            filename = tkFileDialog.askopenfilename()
            no_path_filename = filename.rsplit('/')[1]
            texture = {'filename' : no_path_filename, 'texture_object' : Tkinter.PhotoImage(file = filename)}
            self.tileTexList.append(texture)
            tkMessageBox.showinfo('Huzzah!', 'File Loaded.')
        except IOError:
            tkMessageBox.showerror('Ohnoes!', 'File Loading Failed!')
            
    def switchTexture(self, event):
        '''Cycles through the available texture list'''
        self.selectedTexture = (self.selectedTexture + 1) % len(self.tileTexList)
        print 'selected tex #: %d' % self.selectedTexture
    
    def newLevel(self):
        [self.canvas.delete(canvas_id) for canvas_id in self.canvas.find_all() if canvas_id not in self.gridCanvasIds]
        self.save_level_json = {'tiles' : []}   
    
    def saveLevel(self):
        '''Exports the level to a json formatted file'''        
        json_level = json.dumps(self.save_level_json)
        
        try:
            filename = tkFileDialog.asksaveasfilename()
            level_file = open(filename, 'w')
            level_file.write(json_level)
            level_file.close()
            tkMessageBox.showinfo('Huzzah!', 'Saved File.')
        except IOError:
            tkMessageBox.showerror('Ohnoes!', 'Save Failed!')
        
        #should get logging for this kind of stuff
        print json_level   
        print "exported"

    def loadLevel(self):
        '''Imports the level from the json exported via saveLevel'''
        try:
            filename = tkFileDialog.askopenfilename()
            saved_file = open(filename, 'r')
            saved_file_string = saved_file.read()
            tkMessageBox.showinfo('Huzzah!', 'Level Loaded.')
        except IOError:
            tkMessageBox.showerror('Ohnoes!', 'Level Loading Failed!')
            
        loaded_json = json.loads(saved_file_string)
        tile_list = loaded_json['tiles']
        for json_tile in tile_list:
            (x, y) = self.jsonCoordToCanvas(json_tile['x'], json_tile['y'])
            texture_name = json_tile['texture']
            texture_object = self.tileTexList[0] # default value in case tile isn't found
            for tile_texture in self.tileTexList:
                if tile_texture['filename'] == texture_name:
                    texture_object = tile_texture
            tile = {'x' : x, 'y' : y, 'texture' : texture_object}
            self.drawTile(tile)
            
        save_level_json = loaded_json
        print loaded_json
        print 'loaded'
        
app = Leveled()

app.tkWindow.mainloop()
