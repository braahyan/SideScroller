'''
Created on Feb 28, 2010

@author: Bryan
'''
#Ion's Superific QuadTree! Static for now.  
  
LEAF_MAX = 1  
  
class Rect:  
    def __init__( self, x, y, width, height):  
        self.x = x  
        self.y = y  
        self.width = width  
        self.height = height  
  
        self.right = self.x + self.width  
        self.bottom = self.y + self.height  
  
        self.centerx = self.x + (self.width/2)  
        self.centery = self.y + (self.height/2)  
        
    def testIntersect( self, other ):  
        self.right = self.x + self.width  
        self.bottom = self.y + self.height  
  
        if self.right < other.x: return False        
        if self.x > other.right: return False  
        if self.y > other.bottom: return False  
        if self.bottom < other.y: return False               
        return True             
    
    def testContains( self, other ):        
        self.right = self.x + self.width        
        self.bottom = self.y + self.height              
        if other.right > self.right: return False  
        if other.x < self.x: return False  
        if other.y < self.y: return False        
        if other.bottom > self.bottom: return False  
        return True  
    
    def colliderect( self, rect ): #pygame compatibility  
        return self.testIntersect( rect )  
    
    def contains( self, rect ): #pygame compatibility  
        return self.testContains( rect )  
    
    def getTuple( self ):  
        return (self.x, self.y, self.width, self.height)  
  
class QuadTree:  
    def __init__( self, x, y, width, height ):  
        self.rect = Rect( x, y, width, height )  
        self.oblist = []  
  
        self.subnode = []  
    def addObject( self, ob ):  
        self.oblist.append( ob )
        if len( self.oblist ) > LEAF_MAX:  
            halfwidth = self.rect.width/2  
            halfheight = self.rect.height/2  
  
            if len( self.subnode ) == 0:  
                self.subnode.append( QuadTree( self.rect.x            , self.rect.y,               halfwidth, halfheight) ) # upper left  
                self.subnode.append( QuadTree( self.rect.x + halfwidth, self.rect.y,               halfwidth, halfheight) ) #upper right  
                self.subnode.append( QuadTree( self.rect.x            , self.rect.y + halfheight,  halfwidth, halfheight) ) # lower left  
                self.subnode.append( QuadTree( self.rect.x + halfwidth, self.rect.y + halfheight,  halfwidth, halfheight) ) #lower right  
  
            kill = []  
            for ob in self.oblist:  
                for sub in self.subnode:  
                    if sub.rect.contains( ob.rect ): #object is contained in that node  
                        sub.addObject( ob )  
                        kill.append( ob )  
                        break  
            for ob in kill:  
                self.oblist.remove( ob )  

    def getInBounds( self, rect ):  
        total = []  
        for ob in self.oblist:  
            total.append( ob )  
        for sub in self.subnode:  
            if rect.colliderect( sub.rect ):  
                total += sub.getInBounds( rect )  
        return total
  
    def getAll( self ):  
        total = []  
        for ob in self.oblist:  
            total.append( ob )  
        for sub in self.subnode:  
            total += sub.getAll( )  
        return total  