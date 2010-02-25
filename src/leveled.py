import Tkinter, random
class Leveled:
    def __init__(self, t):
        #make a menu, don't know why menubutton needs to get created, but it does
        menuButton = Tkinter.Menubutton(t)
        menubar = Tkinter.Menu(t)
        menubar.add_command(label="Hello!", command=self.hello)
        menubar.add_command(label="Quit!", command=t.quit)
        
        t.config(menu=menubar)
        
        self.i = Tkinter.PhotoImage(file = "smilie-small.gif")
        
        self.canvas = Tkinter.Canvas(t, width=300, height=300)
        self.canvas.bind("<Double-Button-1>",self.drawSmilie)
        self.canvas.pack()
        self.drawGrid()
        self.canvas.create_text(30,0,text=" YARRRR!", anchor=Tkinter.NW)
        

    def hello(self):
        print 'Darf'
        
    def drawGrid(self):
        #hardcode gridsize/canvas size for now
        for i in range(1, 10):
            self.canvas.create_line(0, i*30, 300, i*30)
            self.canvas.create_line(i*30, 0, i*30, 300)
            
    def drawSmilie(self, event):
        ##figure out how to round a number based on where the user clicked and a given gridsize
        x = event.x
        y = event.y 
        event.widget.create_image(x, y, image = self.i, anchor=Tkinter.NW)
        print 'smilie drawn: %d, %d' % (x,y)

t = Tkinter.Tk()

# If this line is used, the program does not work
#App(t)

# If this line is used, the program works
a = Leveled(t)

t.mainloop()
