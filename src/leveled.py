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
        
        #need to make this a list of tuples or some such thing, so we can have texture filenames,
        #transparency, and other various tile properties, etc etc
        self.tileTexList = [Tkinter.PhotoImage(file = '%ssmilie-small.gif' % self.TEX_DIRECTORY), 
                            Tkinter.PhotoImage(file = '%sdirt.gif' % self.TEX_DIRECTORY)]
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
        self.canvas.bind("<Button-1>",self.drawTexture)
        self.canvas.bind("<Button-3>", self.switchTexture)
        self.canvas.pack()
        self.drawGrid()
        
        
        self.save_level_json = {'tiles' : []}
        
    def getTileTextures(self):
        self.tileTexList.append()
    
    def hello(self):
        print 'Darf'
        
    def drawGrid(self):
        #hardcode gridsize/canvas size for now
        for i in range(1, self.height/self.TILE_SIZE):
            self.canvas.create_line(0, i*self.TILE_SIZE, self.width, i*self.TILE_SIZE)
        for i in range(1, self.width/self.TILE_SIZE):
            self.canvas.create_line(i*self.TILE_SIZE, 0, i*self.TILE_SIZE, self.height)
            
    def drawTexture(self, event):
        x = event.x - (event.x%self.TILE_SIZE)
        y = event.y - (event.y%self.TILE_SIZE)
        imgToDraw = self.tileTexList[self.selectedTexture]
        tile_id = event.widget.create_image(x, y, image = imgToDraw, anchor=Tkinter.NW)
        self.save_level_json['tiles'].append({'x' : (x/self.TILE_SIZE)+1 , 'y' : ((self.height-y)/self.TILE_SIZE)})
        print self.save_level_json
        print 'texture drawn: %d, %d' % (x,y)
    
    def loadTexture(self):
        try:
            filename = tkFileDialog.askopenfilename()
            texture = Tkinter.PhotoImage(file = filename)
            self.tileTexList.append(texture)
            tkMessageBox.showinfo('Huzzah!', 'File Loaded.')
        except IOError:
            tkMessageBox.showerror('Ohnoes!', 'File Loading Failed!')
            
    def switchTexture(self, event):
        print 'length of texture list: %d' % len(self.tileTexList)
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
        #need to do a rendering loop, go through the dicts assigning tile textures
        #use the default for now
        print loaded_json
        return loaded_json
        
# If this line is used, the program does not work
#App(t)

# If this line is used, the program works
a = Leveled()

a.t.mainloop()
