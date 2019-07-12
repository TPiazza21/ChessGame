#this is where I define all of the pieces
from Vector import Vector

class Piece(object):
    def __init__(self,whichType,x,y,whiteStatus,holderPic,i):
        self.xpos = x   #x position on the board (initially)
        self.ypos = y   #y position on the board (initially)
        self.type = whichType   #king, queen, pawn, bishop, rook, knight
        self.isWhite = whiteStatus    #is it a black or white piece
        self.pic = holderPic
        self.indexVal = i
        self.isAlive = True
        self.deathX = x+9
        self.deathY = y
        self.hasMoved = False
        self.justDoubleJumped=False
        self.firstMove=False
        self.perishX=0
        self.perishY=0
        self.moveNumber=0#how many moves has it stepped forward (at first it has gone 0 moves)




        if self.type in ["king"]:
            self.moves = [Vector(0,1), Vector(1,1), Vector(1,0), Vector(1,-1),Vector(0,-1), Vector(-1,-1), Vector(-1,0), Vector(-1,1)]
            self.onwards = False #onwards means that you can go beyond these moves (with a positive scalar)
        if self.type in ["queen"]:
            self.moves = [Vector(0,1), Vector(1,1), Vector(1,0), Vector(1,-1),Vector(0,-1), Vector(-1,-1), Vector(-1,0), Vector(-1,1)]
            self.onwards = True #so the queen can have Vector(2,2) because this is 2 * Vector(1,1)
        if self.type in ["rook"]:
            self.moves = [Vector(0,1),Vector(1,0),Vector(0,-1),Vector(-1,0)]
            self.onwards = True
        if self.type in ["bishop"]:
            self.moves = [Vector(1,1),Vector(1,-1),Vector(-1,-1),Vector(-1,1)]
            self.onwards = True
        if self.type in ["knight"]:
            self.moves = [Vector(2,1),Vector(2,-1),Vector(1,-2),Vector(-1,-2),Vector(-2,-1),Vector(-2,1),Vector(-1,2),Vector(1,2)]
            self.onwards = False
        if self.type in ["pawn"]:
            if(self.isWhite==True):
                self.moves = [Vector(0,1)]
            else: #so this is the black piece (which starts at the top)
                self.moves = [Vector(0, -1)]

            self.onwards = False


    #end of __init__

    def printAllMoves(self):
        for a in self.moves:
            a.printVector()

        #self.addVectors(self.moves[0],self.moves[2]).printVector() #add vectors and print the result
    #end of printAllMoves

    def addVectors(self, a, b): #a and b are two dimensional vectors
        xTerm = a.x+b.x
        yTerm = a.y+b.y
        newVector = Vector(xTerm,yTerm)
        #print("added them together")
        return(newVector)

    #end of add Vectors

    def printSelf(self):
        if(self.isWhite==True):
            print("White "+self.type+" at ("+str(self.xpos)+","+str(self.ypos)+")")
        elif(self.isWhite==False):
            print("Black " + self.type + " at (" + str(self.xpos) + "," + str(self.ypos) + ")")

    def moveMe(self, newX, newY):

        if (self.justDoubleJumped == True):
            self.justDoubleJumped = False

        if(abs(newY-self.ypos)==2 and self.type=="pawn"):
            self.justDoubleJumped=True

        self.xpos=newX
        self.ypos=newY

        if(self.hasMoved==False):
            self.firstMove=True
            self.hasMoved = True

        elif(self.firstMove==True):
            self.firstMove=False

        self.moveNumber = self.moveNumber+1




    def moveBack(self,newX,newY):
        deltaY = newY-self.ypos
        self.xpos = newX
        self.ypos = newY
        '''
        if(self.firstMove==True):
            self.firstMove=False
            self.hasMoved=False
        '''
        if(self.moveNumber==1):#going from 1 to 0
            self.firstMove=False
            self.hasMoved=False
        if(self.moveNumber==2):#2 to 1
            self.firstMove=True

        '''
        if (self.type == "pawn"):
            if (self.justDoubleJumped == True and self.isAlive==True):#if you just died, you still justDoubleJumped
                self.justDoubleJumped = False
        '''



        if(self.isAlive==False):
            self.isAlive=True

        self.moveNumber = self.moveNumber - 1
#end of def moveBack(self,newX,newY)


    def killMe(self):
        self.isAlive=False

        self.perishX=self.xpos
        self.perishY=self.ypos

        self.xpos=self.deathX
        self.ypos=self.deathY

        self.moveNumber = self.moveNumber + 1



    def subtractVectors(self, a,b):
        xTerm = a.x-b.x
        yTerm = a.y-b.y
        newVector = Vector(xTerm,yTerm)
        return(newVector)
    #def subtractVectors(self,a,b)







