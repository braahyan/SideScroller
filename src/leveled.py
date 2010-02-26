import Tkinter
import tkFileDialog
import tkMessageBox
import random
import math

class Leveled:
    def __init__(self):
        self.t = Tkinter.Tk()
        
        #make a menu, don't know why menubutton needs to get created, but it does
        menuButton = Tkinter.Menubutton(self.t)
        menubar = Tkinter.Menu(self.t)
        menubar.add_command(label="Save", command=self.save)
        menubar.add_command(label="Quit!", command=self.t.quit)
        self.t.config(menu=menubar)

        self.canvas = Tkinter.Canvas(self.t, width=300, height=300)
        self.canvas.bind("<Double-Button-1>",self.drawSmilie)
        self.canvas.pack()
        self.drawGrid()
        
        self.i = Tkinter.PhotoImage(file = "smilie-small.gif")
        self.tiles = []
        
    def hello(self):
        print 'Darf'
        
    def drawGrid(self):
        #hardcode gridsize/canvas size for now
        for i in range(1, 10):
            self.canvas.create_line(0, i*30, 300, i*30)
            self.canvas.create_line(i*30, 0, i*30, 300)
            
    def drawSmilie(self, event):
        ##figure out how to round a number based on where the user clicked and a given gridsize
        x = event.x - (event.x%30)
        y = event.y - (event.y%30)
        tile_id = event.widget.create_image(x, y, image = self.i, anchor=Tkinter.NW)
        self.tiles.append(tile_id)
        print 'smilie drawn: %d, %d' % (x,y)

    def save(self):
        #actual json library later, also add things like texture name
        save_json = '{ "tiles" : \n'
        for tile in self.tiles:     
            tile_coords = self.canvas.coords(tile)
            tile_json = '    {\n     "%s" : "%d"\n     "%s" : "%d"\n    }\n' % ('x',tile_coords[0],'y',tile_coords[1]) 
            save_json = '%s%s' % (save_json, tile_json)
        save_json = '%s}\n' % save_json
        
        try:
            filename = tkFileDialog.asksaveasfilename()
            file = open(filename, 'w')
            file.write(save_json)
            tkMessageBox.showinfo('Huzzah!', 'Saved File.')
        except:
            tkMessageBox.showerror('Ohnoes!', 'Save Failed!')
        print save_json    
        print "exported"



# If this line is used, the program does not work
#App(t)

# If this line is used, the program works
a = Leveled()

a.t.mainloop()
