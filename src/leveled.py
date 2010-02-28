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
        self.t = Tkinter.Tk()
        
        #this is a dict so we can have texture filenames,
        #transparency, and other various tile properties, etc etc
        smilie_tile = {'filename' : 'smilie-small.gif', 
                       'texture_object' : Tkinter.PhotoImage(file = '%ssmilie-small.gif' % self.TEX_DIRECTORY)}
        dirt_tile = {'filename' : 'dirt.gif', 'texture_object' : 
                     Tkinter.PhotoImage(file = '%sdirt.gif' % self.TEX_DIRECTORY)}
        self.tileTexList = [dirt_tile, smilie_tile]
        self.selectedTexture = 0
        
        #make a menu, don't know why menubutton needs to get created, but it does
        menuButton = Tkinter.Menubutton(self.t)
        menubar = Tkinter.Menu(self.t)
        menubar.add_command(label="Save Level", command=self.saveLevel)
        menubar.add_command(label="Load Level", command=self.loadLevel)
        menubar.add_command(label="Load Texture", command=self.loadTexture)
        menubar.add_command(label="Quit!", command=self.t.quit)
        self.t.config(menu=menubar)
        self.width = 640
        self.height = 480
        self.canvas = Tkinter.Canvas(self.t, width=self.width, height=self.height)
        self.canvas.bind("<Button-1>",self.drawTileEvent)
        self.canvas.bind("<Button-3>", self.switchTexture)
        self.canvas.pack()
        self.drawGrid()
        
        
        self.save_level_json = {'tiles' : []}
        
    def getTileTextures(self):
        self.tileTexList.append()
    
    def hello(self):
        print 'Darf'
        
    def drawGrid(self):
        for i in range(1, self.height/self.TILE_SIZE):
            self.canvas.create_line(0, i*self.TILE_SIZE, self.width, i*self.TILE_SIZE)
        for i in range(1, self.width/self.TILE_SIZE):
            self.canvas.create_line(i*self.TILE_SIZE, 0, i*self.TILE_SIZE, self.height)
            
    def drawTileEvent(self, event):
        x = event.x 
        y = event.y 
        texture = self.tileTexList[self.selectedTexture]
        tile_object = {'x' : x, 'y' : y, 'texture' : texture}
        self.drawTile(tile_object)
        
        
        
    def drawTile(self, tile):
        x = tile['x'] - (tile['x']%self.TILE_SIZE)
        y = tile['y'] - (tile['y']%self.TILE_SIZE)
        texture_name = tile['texture']['filename']
        texture = tile['texture']['texture_object']
        self.canvas.create_image(x, y, image = texture, anchor=Tkinter.NW)
        self.save_level_json['tiles'].append({'x' : (x/self.TILE_SIZE)+1 , 
                                              'y' : (self.height-y)/self.TILE_SIZE,
                                              'texture' : texture_name})
    
    def loadTexture(self):
        try:
            filename = tkFileDialog.askopenfilename()
            #no_path_filename? crappy name if i ever heard one...
            no_path_filename = filename.rsplit('/')[1]
            texture = {'filename' : no_path_filename, 'texture_object' : Tkinter.PhotoImage(file = filename)}
            self.tileTexList.append(texture)
            tkMessageBox.showinfo('Huzzah!', 'File Loaded.')
        except IOError:
            tkMessageBox.showerror('Ohnoes!', 'File Loading Failed!')
            
    def switchTexture(self, event):
        self.selectedTexture = (self.selectedTexture + 1) % len(self.tileTexList)
        print 'selected tex #: %d' % self.selectedTexture
    
    def saveLevel(self):        
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
            x = (json_tile['x'] * self.TILE_SIZE) - 1
            y = self.height - (json_tile['y'] * self.TILE_SIZE)
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
        
        
# If this line is used, the program does not work
#App(t)

# If this line is used, the program works
a = Leveled()

a.t.mainloop()
