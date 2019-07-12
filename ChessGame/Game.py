#I intend to use this as the main hub of everything - I will make separate pieces and board classes
#Tyler Piazza, 5/3/17

#imports
from tkinter import *
from Piece import Piece
from Vector import Vector
from PIL import Image, ImageTk
import time

print("Welcome to chess!")
root = Tk()
root.title('Chess Game:')

##This stuff sets up the graphics (lines and things)

canvas = Canvas(root,width=1000,height=600,bg='white')
canvas.pack()

switcher = False

checkLabel = Label(text="in check")

for a in range(8):
    if(switcher==True):
        switcher = False
    else:
        switcher = True

    for b in range(8):
        if(switcher==True):
            canvas.create_rectangle(100+50*a,100+50*b,150+50*a,150+50*b,fill="white")
            switcher=False
        elif(switcher == False):
            canvas.create_rectangle(100 + 50 * a, 100 + 50 * b, 150 + 50 * a, 150 + 50 * b, fill="maroon")
            switcher=True


canvas_id = canvas.create_text(10,10,anchor="nw")
canvas.itemconfig(canvas_id,text="Welcome to chess!")

canvas.insert(canvas_id,14,"")

im = Image.open('./2000px-Chess_Pieces_Sprite_svg-2.gif')#the sprite with the chess pieces

whitePiece = [] #this is to keep track of the white pieces


def cropMe(x1,y1,x2,y2,i): #note to self: you have to define methods before you use them

    croppedThing = i.crop((x1,y1,x2,y2))
    holderImage = ImageTk.PhotoImage(croppedThing)
    return(holderImage)
#end of cropImage


whitePawnPic = cropMe(250,0,300,50,im)#Note for next time: total thing has width of 300 and height of 100

#Defining the pieces, with their pictures as parameters

for a in range(8): #the pawns
    whitePiece.append( Piece("pawn",a,1,True,whitePawnPic,a) )

wRookPic = cropMe(200,0,250,50,im) #for the rooks
whitePiece.append( Piece("rook",0,0,True,wRookPic,8))
whitePiece.append( Piece("rook",7,0,True,wRookPic,9))

wKnightPic = cropMe(150,0,200,50,im) #for the knights
whitePiece.append( Piece("knight",1,0,True,wKnightPic,10))
whitePiece.append( Piece("knight",6,0,True,wKnightPic,11))

wBishopPic = cropMe(100,0,150,50,im) #for the bishop
whitePiece.append( Piece("bishop",2,0,True,wBishopPic,12))
whitePiece.append( Piece("bishop",5,0,True,wBishopPic,13))

wQueenPic = cropMe(50,0,100,50,im) #the queen
whitePiece.append( Piece("queen",3,0,True,wQueenPic,14) )

wKingPic = cropMe(0,0,50,50,im) #the king
whitePiece.append( Piece("king",4,0,True,wKingPic,15))


blackPiece = [] #for the black pieces

bPawnPic = cropMe(250,50,300,100,im)#Note for next time: total thing has width of 300 and height of 100

for a in range(8): #the pawns
    blackPiece.append( Piece("pawn",a,6,False,bPawnPic,a) )

bRookPic = cropMe(200,50,250,100,im) #for the rooks
blackPiece.append( Piece("rook",0,7,False,bRookPic,8))
blackPiece.append( Piece("rook",7,7,False,bRookPic,9))

bKnightPic = cropMe(150,50,200,100,im) #for the knights
blackPiece.append( Piece("knight",1,7,False,bKnightPic,10))
blackPiece.append( Piece("knight",6,7,False,bKnightPic,11))

bBishopPic = cropMe(100,50,150,100,im) #for the bishop
blackPiece.append( Piece("bishop",2,7,False,bBishopPic,12))
blackPiece.append( Piece("bishop",5,7,False,bBishopPic,13))

bQueenPic = cropMe(50,50,100,100,im) #the queen
blackPiece.append( Piece("queen",3,7,False,bQueenPic,14) )

bKingPic = cropMe(0,50,50,100,im) #the king
blackPiece.append( Piece("king",4,7,False,bKingPic,15))



for b in range (8): #to set up labelling
    canvas.create_text(125+50*b,525,fill="darkblue",font="Times 20 italic bold",text=str(b)+"")
    canvas.create_text(75,475-50*b,fill="darkblue",font="Times 20 italic bold",text=str(b)+"")
#canvas.update

def searchSpot(x,y,wPieces,bPieces):#this method lets me look at a spot on the board (and tells me what, if anything, is there)
    if(y<4): #look through the white pieces first, bc it is more probable to be there
        for a in wPieces:
            if a.xpos==x and a.ypos==y:
                return(a) #returns the thing itself

        for b in bPieces:
            if (b.xpos == x and b.ypos == y):
                return (b)  #returns the thing itself
    elif(y>=4):
        for b in bPieces:
            if (b.xpos == x and b.ypos == y):
                return (b)  #returns the thing itself
        for a in wPieces:
            if(a.xpos==x and a.ypos==y):
                return( a ) #returns the thing itself
    if(x<0 or x>7 or y<0 or y>7):
        return(True) #say that there is a "piece" there because this spot is outside of the boundaries
    return(False) #if it can't find any pieces, it returns false
#end of searchSpot(x,y)





whitePics = []
blackPics = []

def printPieces():#this actually displays the images on the canvas, and I save an array of each picture

    for a in range(16):
        sally = canvas.create_image(125 + 50 * whitePiece[a].xpos, 475 - 50 * whitePiece[a].ypos, image=whitePiece[a].pic)
        jimmy = canvas.create_image(125 + 50 * blackPiece[a].xpos, 475 - 50 * blackPiece[a].ypos, image=blackPiece[a].pic)
        canvas.pack()
        whitePics.append(sally)
        blackPics.append(jimmy)



#this is not to be used in recursive methods
def updatePiece(tempPiece,newX,newY):#tempPiece thinks its at old position. This moves a piece and its picture

    deltaX = newX-tempPiece.xpos
    deltaY = newY-tempPiece.ypos
    if(tempPiece.isWhite==True):

        whitePiece[tempPiece.indexVal].moveMe(newX, newY)  # update the actual position
        animateMove(tempPiece,deltaX,deltaY,whitePics)

    if(tempPiece.isWhite==False):

        blackPiece[tempPiece.indexVal].moveMe(newX, newY)  # update the actual position
        animateMove(tempPiece, deltaX, deltaY, blackPics)

#end of updatePiece

def animateMove(tempPiece,dx,dy,picArray):
    i = tempPiece.indexVal
    for a in range(50):
        canvas.move(picArray[i],dx,-dy)
        time.sleep(.005)
        #print("animating (stepwise)")
        canvas.update()



#def animateMove(tempPiece,newX,newY)

def checkIfAnythingInTheWay(iX,iY,fX,fY,wPieces,bPieces):#are there any pieces in between
    tempRange = abs(iX-fX)
    xStep,yStep=0,0
    if(tempRange==0):
        tempRange= abs(iY-fY)
    if(fX-iX>0):
        xStep=1
    elif(fX==iX):
        xStep=0
    elif(fX-iX<0):
        xStep=-1
    if(fY-iY>0):
        yStep=1
    elif(fY==iY):
        yStep=0
    elif(fY-iY<0):
        yStep=-1

    for a in range(tempRange-1):
        if( searchSpot(iX+(a+1)*xStep,iY+(a+1)*yStep,wPieces,bPieces)!=False):

            return(True)#there is something in the way

    return(False)# if nothing is in the way
#end of def checkIfAnythingInTheWay(iX,iY,fX,fY)




def checkIfLegal(jim,v,wPieces,bPieces): #to see if a move to position vector v is legal. Returns true or false
    print("checking if this move is legal:")
    jim.printSelf()
    v.printVector
    myArray=[]
    otherArray=[]
    if(jim.isWhite==True):
        myArray=wPieces
        otherArray=bPieces
    elif(jim.isWhite==False):
        myArray=bPieces
        otherArray=wPieces


    deltaVector = jim.subtractVectors(v, Vector(jim.xpos, jim.ypos))  # this is the potential "move"
    inCheck = determineIfAttacked(myArray[15].xpos,myArray[15].ypos,myArray,otherArray)



    boardInfo = moveBoardForward(jim,deltaVector,myArray,otherArray)
    if(determineIfAttacked(myArray[15].xpos,myArray[15].ypos,myArray,otherArray)==True):#if you're moving into a check
        moveBoardBackward(myArray[jim.indexVal],deltaVector,myArray,otherArray,boardInfo)
        print("Thinks the king is under attack if you move here")
        return(False)
    moveBoardBackward(myArray[jim.indexVal], deltaVector,myArray,otherArray, boardInfo)



    if(inCheck==False):

        if (jim.type == "pawn"):#for all of the special pawn-isms
            if (jim.hasMoved == False):
                doubleJump = jim.addVectors(jim.moves[0], jim.moves[0])
                if (deltaVector == doubleJump) and ( searchSpot(jim.xpos,jim.ypos+jim.moves[0].y,wPieces,bPieces)==False and searchSpot(jim.xpos,jim.ypos+(2*jim.moves[0].y),wPieces,bPieces)==False ):

                    return (True)  # if the pawn hasn't moved yet, it can move two spaces
            tempVictim = searchSpot(v.x,v.y,wPieces,bPieces)
            if(tempVictim!=False):#if there is something there
                if(tempVictim.isWhite!=jim.isWhite):#if you want to get an enemy

                    if(jim.isWhite==True):
                        if(deltaVector in [ Vector(1, 1), Vector(-1, 1) ]):
                            return (True)
                    elif(jim.isWhite==False):
                        if(deltaVector in [ Vector(1, -1), Vector(-1, -1) ]):
                            return (True)
                    if(deltaVector==jim.moves[0]): #the pawn can't take a piece directly in front of it
                        return(False)
            #now to check for en passant

            if(abs(deltaVector.x)==1 and deltaVector.y==jim.moves[0].y and searchSpot(v.x,v.y-jim.moves[0].y,wPieces,bPieces)!=False):#en passant

                timmy = searchSpot(v.x,v.y-jim.moves[0].y,wPieces,bPieces)
                #timmy.printSelf()

                if(timmy.type=="pawn" and timmy.isWhite!=jim.isWhite and timmy.justDoubleJumped==True):

                    killPiece(timmy)
                    return(True)

        if (jim.onwards == False):

            if(deltaVector in jim.moves):
                print("the move should be legal")
                return (True)

        elif (jim.onwards == True):
            if (deltaVector.x == deltaVector.y or deltaVector.x == -deltaVector.y) and (jim.type == "queen" or jim.type == "bishop"):
                if(checkIfAnythingInTheWay(jim.xpos,jim.ypos,v.x,v.y,wPieces,bPieces)==False):
                    return (True)
            elif (deltaVector.x == 0 or deltaVector.y == 0) and (jim.type == "queen" or jim.type == "rook"):
                if (checkIfAnythingInTheWay(jim.xpos, jim.ypos, v.x, v.y,wPieces,bPieces) == False):
                    return (True)

    elif(inCheck==True):
        print("YOU'RE IN CHECK")
        piecesAndMoves = generatePossibleMoves(wPieces,bPieces,True)
        possiblePieces = piecesAndMoves[0]
        possibleMoves = piecesAndMoves[1]
        for a in range(len(piecesAndMoves[0])):
            #check if your move gets you out of check
            if(jim==possiblePieces[a] and deltaVector==possibleMoves[a]):
                print("This was a legal move to get out of check")
                return(True)
        print("That was not a legal move")

    return (False)#if all else fails

#end of def checkIfLegal()

#not to be used in recursive methods
def killPiece(jim):#RIP
    jim.isAlive = False
    deltaX = jim.deathX-jim.xpos
    deltaY = jim.deathY-jim.ypos
    if (jim.isWhite == True):
        canvas.move(whitePics[jim.indexVal], 50 * deltaX, -50 * deltaY)  # for now, it moves 1,1
        whitePiece[jim.indexVal].moveMe(jim.deathX, jim.deathY)  # update the actual position
        # end of redrawPiece
    if (jim.isWhite == False):
        canvas.move(blackPics[jim.indexVal], 50 * deltaX, -50 * deltaY)  # for now, it moves 1,1
        blackPiece[jim.indexVal].moveMe(jim.deathX, jim.deathY)  # update the actual position
#end of def: killPiece(jim)

#these are the variables I use for keeping track of which piece I have just clicked
mouseIsHolding = False
tempPiece = whitePiece[0]

def checkForCastle(jim,theRook,aPiece,bPiece):
    if(jim.hasMoved==False and theRook.hasMoved==False and determineIfAttacked(4,theRook.ypos,aPiece,bPiece)==False):
        if(checkIfAnythingInTheWay(jim.xpos,jim.ypos,theRook.xpos,theRook.ypos,aPiece,bPiece)==False):
            if(theRook.xpos==0):
                if(determineIfAttacked(2,theRook.ypos,aPiece,bPiece)==False and determineIfAttacked(3,theRook.ypos,aPiece,bPiece)==False):
                    return(True)
            elif(theRook.xpos==7):
                if (determineIfAttacked(5, theRook.ypos, aPiece, bPiece) == False and determineIfAttacked(6,theRook.ypos,aPiece,bPiece)==False):
                    return (True)
                   #return(True)#yes, a castle can happen here
    return(False)#otherwise, return false


def checkSlidingMoves(jim,myMove,aPieces,bPieces):#returns a list of moves that are fine for slide-able pieces
    returnerMoves = []
    keeperBoolean = True#to continue the forloop
    currentMove = myMove
    while(keeperBoolean==True):
        #currentMove = jim.addVectors(currentMove,myMove)
        newX = jim.xpos+currentMove.x
        newY = jim.ypos+currentMove.y
        timmy = searchSpot(newX,newY,aPieces,bPieces)
        if(newX>=0 and newX<8 and newY>=0 and newY<8) and (timmy==False):
            returnerMoves.append(currentMove)
        elif(newX < 0 or newX >= 8 or newY < 0 or newY >= 8):
            keeperBoolean = False
        elif(timmy.isWhite==jim.isWhite):
            keeperBoolean = False#end the while loop
        elif(timmy.isWhite!=jim.isWhite):
            returnerMoves.append(currentMove)
            keeperBoolean = False
        currentMove = jim.addVectors(currentMove,myMove)
    #end of while loop
    return(returnerMoves)
#end of checkSlidingMoves



def generatePossibleMoves(aPieces,bPieces,careAboutCheck=True, careAboutCastle=True): #generate an array of moves and an array of pieces that correspond to those moves (so a list of two arrays)

    holderPieces = [] #store the pieces corresponding to each move (so pieces may be repeated)
    holderMoves = [] #store each move (vector) corresponding to each piece
    for myPiece in aPieces:
        if(myPiece.isAlive==True and myPiece.type!="pawn"):
            for sampleMove in myPiece.moves:
                newX = myPiece.xpos+sampleMove.x#x and y position of where the new move would be
                newY = myPiece.ypos+sampleMove.y
                if (myPiece.onwards==False) and (newX>=0 and newX<8 and newY>=0 and newY<8) and  ( searchSpot(newX,newY,aPieces,bPieces)==False or searchSpot(newX,newY,aPieces,bPieces).isWhite!=myPiece.isWhite ):
                    holderPieces.append(myPiece)#add this to your arrays
                    holderMoves.append(sampleMove)
                if(myPiece.onwards==True):#for slide-able moves
                    for move in checkSlidingMoves(myPiece,sampleMove,aPieces,bPieces):
                        holderPieces.append(myPiece)
                        holderMoves.append(move)
        elif(myPiece.isAlive==True and myPiece.type=="pawn"):#for all of the various pawn problems
            if(searchSpot(myPiece.xpos,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces)==False):

                holderPieces.append(myPiece)
                holderMoves.append(myPiece.moves[0])#add the single move
                if(myPiece.hasMoved==False and searchSpot(myPiece.xpos,myPiece.ypos+(2*myPiece.moves[0].y),aPieces,bPieces)==False and myPiece.moveNumber==0):

                    holderPieces.append(myPiece)
                    holderMoves.append(myPiece.addVectors(myPiece.moves[0], myPiece.moves[0]))  # add the double move
            for a in range(2):
                #diagonal kills
                if(searchSpot(myPiece.xpos+1-a*2,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces)!=False and searchSpot(myPiece.xpos+1-a*2,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces)!=True):# if this diagonal is ripe
                    if(searchSpot(myPiece.xpos+1-a*2,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces).isWhite!=myPiece.isWhite):
                        if(myPiece.ypos==3.5+2.5*myPiece.moves[0].y):#if your diagonal kill is a pawn promotion
                            holderPieces.append(myPiece)
                            codeVector = Vector(1-(2*a), 3)  # 3 for queen, 4 for knight <3,3> and <-3,3>
                            holderMoves.append(codeVector)

                            holderPieces.append(myPiece)
                            codeVector = Vector(1 - (2 * a), 4)  # 3 for queen, 4 for knight. <4,4> and <-4,4>
                            holderMoves.append(codeVector)
                        else:
                            holderPieces.append(myPiece)
                            sideStep = Vector(1-(a*2),0)
                            holderMoves.append(myPiece.addVectors(sideStep, myPiece.moves[0]))
                #en passant kills
                enPassantVictim = searchSpot(myPiece.xpos+1-a*2,myPiece.ypos,aPieces,bPieces)
                if(searchSpot(myPiece.xpos+1-a*2,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces)==False) and (enPassantVictim!=False) and (enPassantVictim!=True):



                    if(enPassantVictim.justDoubleJumped==True and enPassantVictim.isWhite!=myPiece.isWhite):
                        holderPieces.append(myPiece)
                        sideStep = Vector(1-(a * 2), 0) #<1,0> or <-1,0>
                        holderMoves.append(sideStep)
            #for potential pawn promotion

            if(myPiece.ypos==3.5+2.5*myPiece.moves[0].y):#6 for white, 1 for black (right before end)
                if( searchSpot(myPiece.xpos,myPiece.ypos+myPiece.moves[0].y,aPieces,bPieces)==False ):
                    holderPieces.append(myPiece)
                    codeVector = Vector(0, 3)  # 3 for queen, 4 for knight <0,3>
                    holderMoves.append(codeVector)

                    holderPieces.append(myPiece)
                    codeVector = Vector(0, 4)  # 3 for queen, 4 for knight. <0,4>
                    holderMoves.append(codeVector)

        #end of elif(myPiece.isAlive==True and myPiece.type=="pawn")



        if(myPiece.isAlive==True and myPiece.type=="king" and careAboutCastle==True):#now to check for castling
            leftRook = aPieces[8]#by the order that I assigned the pieces
            if(checkForCastle(myPiece,leftRook,aPieces,bPieces)==True):
                holderPieces.append(myPiece)
                sideStep = Vector(-2,0)
                holderMoves.append(sideStep)
            rightRook = aPieces[9]  # by the order that I assigned the pieces
            if (checkForCastle(myPiece, rightRook,aPieces,bPieces) == True):
                holderPieces.append(myPiece)
                sideStep = Vector(2, 0)
                holderMoves.append(sideStep)

    if(careAboutCheck==True):#you need limit moves
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ In check is True!")
        #you can't go forward if you will be in check
        safePieces = []
        safeMoves = []
        for a in range(len(holderPieces)):

        #sumX = holderPieces[a].xpos+holderMoves[a].x
        #sumY = holderPieces[a].ypos+holderMoves[a].y

            newInfo = moveBoardForward(holderPieces[a],holderMoves[a],aPieces,bPieces)

            if determineIfAttacked(aPieces[15].xpos,aPieces[15].ypos,aPieces,bPieces)==False:
                safePieces.append(holderPieces[a])
                safeMoves.append(holderMoves[a])

            moveBoardBackward(aPieces[holderPieces[a].indexVal],holderMoves[a],aPieces,bPieces,newInfo)

        return([safePieces,safeMoves])#if in check, only return this specific subset of moves



    return([holderPieces,holderMoves])#send the pieces and corresponding moves
#def generatePossibleMoves(aPieces,bPieces)

def printPossibleMoves(aPiece,bPiece,maybeInCheck=False):
    allWays = generatePossibleMoves(aPiece, bPiece)
    print("**********************")
    print(str(len(allWays[0])))

    for a in range(len(allWays[0])):
        allWays[0][a].printSelf()
        allWays[1][a].printVector()
#end of def printPossibleMoves(aPiece,bPiece):

def evaluateBoard(aPieces,bPieces):#this is the evaluator function, returning a number that represents how advantageous a board is for aPieces
    counter=0
    aSafety=scoreKingSafety(aPieces)
    bSafety=scoreKingSafety(bPieces)
    counter+=countMaterial(aPieces)-countMaterial(bPieces)
    counter+=(aSafety - bSafety)
    counter+=(scoreQueen(aPieces,bPieces,bSafety) - scoreQueen(bPieces,aPieces,aSafety) )
    counter+=(scoreRooks(aPieces,bPieces) - scoreRooks(bPieces,aPieces))
    counter+=(scoreKnights(aPieces,bPieces) - scoreKnights(bPieces,aPieces))
    counter+=( scorePawns(aPieces,bPieces) - scorePawns(bPieces,aPieces) )
    return(counter)
#end of evaluateBoard(aPieces,bPieces)

def countMaterial(aPieces):#very simple evaluator
    counter=0
    for a in aPieces:
        if(a.isAlive==True):
            if(a.type=="pawn"):
                counter+=1000
            if(a.type=="bishop" or a.type=="knight"):
                counter+=3000
            if(a.type=="rook"):
                counter+=5000
            if(a.type=="queen"):
                counter+=9000
            if(a.type=="king"):
                counter+=999999
    return(counter) #return the value of the pieces
#end of countMaterial(aPieces)

def scoreKingSafety(aPieces):#this method scores king safety
    safetyCounter = 0
    theKing = aPieces[15]
    if(theKing.xpos==1 or theKing.xpos==6):#first choice safety
        safetyCounter+=900
    elif(theKing.xpos==0 or theKing.xpos==2 or theKing.xpos==5 or theKing.xpos==7):#second choice safety
        safetyCounter+=500
    safetyCounter+=400*abs(3.5-theKing.ypos) #prioritize the back rows

    return(safetyCounter)
#def scoreKingSafety(aPieces):

def scoreQueen(aPieces,bPieces,otherSafety):
    scoreCounter=0
    theQueen = aPieces[14]
    if(theQueen.isAlive==True):#if not, then it doesn't count
        #centralization
        scoreCounter-=200*abs(3.5-theQueen.ypos)
        otherKing=bPieces[15]
        #now to calculate proximity to the other king (king tropism)
        distance = calculateDistance(otherKing,theQueen)
        scoreCounter-=(distance*100)
        scoreCounter-=(otherSafety)#otherSafety is the other king's safety score. The queen is more valuable when the other king is not safe
    return(scoreCounter)
#def scoreQueen(aPieces,bPieces,otherSafety):

def scoreRooks(aPieces,bPieces):
    scoreCounter=0
    otherKing=bPieces[15]
    for a in range(2):
        theRook = aPieces[8+a]
        if(theRook.isAlive==True):
            distance = calculateDistance(otherKing,theRook)#king tropism

            scoreCounter-=distance*100
            if(theRook.isWhite==True):#for if a rook is on the 7th rank
                if(theRook.ypos==7):
                    scoreCounter+=400
            elif(theRook.isWhite==False):
                if(theRook.ypos==1):
                    scoreCounter+=400
            #this tests for rook mobility
            if(searchSpot(theRook.xpos,theRook.ypos+1,aPieces,bPieces)==False):
                scoreCounter+=300
            if (searchSpot(theRook.xpos+1, theRook.ypos, aPieces, bPieces) == False):
                scoreCounter += 300
            if (searchSpot(theRook.xpos, theRook.ypos-1, aPieces, bPieces) == False):
                scoreCounter += 300
            if (searchSpot(theRook.xpos-1, theRook.ypos, aPieces, bPieces) == False):
                scoreCounter += 300


    return(scoreCounter)

#def scoreRooks(aPieces,bPieces)

def scoreKnights(aPieces,bPieces):
    scoreCounter = 0
    theKing = aPieces[15]
    samplePawn = aPieces[0]
    theMove=samplePawn.moves[0].y
    for a in range(2):#for each knight
        theKnight = aPieces[10+a]
        if(theKnight.isAlive==True):
            #king tropism
            distance = calculateDistance(theKing,theKnight)
            scoreCounter-=(distance*100)
            #outpost knight, where a knight is on the opponent's side
            pawnAttackerBoolean=False
            if((theKnight.ypos*theMove)>(3.5)*theMove and theKnight.ypos>0 and theKnight.ypos<7):#if you're on the other side
                for b in range(2):
                    theSpot=searchSpot(theKnight.xpos + 1 - 2 * b, theKnight.ypos+theMove, aPieces, bPieces)
                    if (theSpot!=False and theSpot!=True):
                        if(theSpot.type=="pawn"):
                            pawnAttackerBoolean=True
                if(pawnAttackerBoolean==False):
                    scoreCounter+=500#give a bonus for an outpost knight
            #central control
            if(theKnight.xpos>1 and theKnight.xpos<6 and theKnight.ypos>1 and theKnight.ypos<6):
                scoreCounter+=300
        #if isAlive
    return(scoreCounter)
#def scoreKnights(aPieces,bPieces)

def scorePawns(aPieces,bPieces):
    scoreCounter=0
    pawnCounter=0
    for a in range(8):
        thePawn = aPieces[a]
        if(thePawn.isAlive==True):
            #center pawn movement (get the center pawns moving)
            if(a==3 or a==4):
                if(thePawn.hasMoved==False):
                    scoreCounter-=600#penalty for central pawns that are still there
            #penalty for 8 pawns (to promote risktaking)
            pawnCounter+=1
            scoreCounter+=1000/((thePawn.moves[0].y*3.5+4)-thePawn.ypos*thePawn.moves[0].y)#give a bonus for advancing. Make it non-linear




    if(pawnCounter==8):
        scoreCounter-=900#big penalty for still having all pawns to promote risktaking

    return(scoreCounter)
#def scorePawns(aPieces,bPieces)

def calculateDistance(theKing,thePiece):
    distance = ((theKing.xpos - thePiece.xpos) ** (2) + (theKing.ypos - thePiece.ypos) ** (2)) ** (0.5)
    return(distance)
#calculateDistance

def determineIfAttacked(lookX,lookY,aPieces,bPieces):#see if you are in check

    movesAndPieces = generatePossibleMoves(bPieces,aPieces,careAboutCastle=False,careAboutCheck=False)
    possiblePieces = movesAndPieces[0]
    possibleMoves = movesAndPieces[1]

    for a in range(len(possiblePieces)):
        if(possiblePieces[a].xpos+possibleMoves[a].x==lookX) and (possiblePieces[a].ypos+possibleMoves[a].y==lookY):
            return(True)
    return(False)
#end of def determineIfInCheck(aPieces,bPieces)

def determineIfNoWayOut(aPieces,bPieces):#check for stalemate or checkmate (either way, game ends)
    movesAndPieces = generatePossibleMoves(aPieces, bPieces,careAboutCastle=False)
    possiblePieces = movesAndPieces[0]
    possibleMoves = movesAndPieces[1]
    for a in range(len(possiblePieces)):
        boardInfo = moveBoardForward(possiblePieces[a],possibleMoves[a],aPieces,bPieces)

        if(determineIfAttacked(aPieces[15].xpos,aPieces[15].ypos,aPieces,bPieces)==False):
            moveBoardBackward(aPieces[possiblePieces[a].indexVal], possibleMoves[a], aPieces, bPieces, boardInfo)
            return(False)
        moveBoardBackward(aPieces[possiblePieces[a].indexVal],possibleMoves[a],aPieces,bPieces,boardInfo)

    return(True)#if there is no hope. You are in stalemate or checkmate
#def determineIfCheckmate(aPieces,bPieces)

def determineIfMovingIntoCheck(thisPiece,thisMove,aPieces,bPieces):#true or false
    #theKing=aPieces[15]
    updateValues = moveBoardForward(thisPiece,thisMove,aPieces,bPieces)

    if(determineIfAttacked(aPieces[15].xpos,aPieces[15].ypos,aPieces,bPieces)==True):
        moveBoardBackward(thisPiece,thisMove,aPieces,bPieces,updateValues)
        return(True)
    else:
        moveBoardBackward(thisPiece,thisMove,aPieces,bPieces,updateValues)
        return(False)
#end of def determineIfMovingIntoCheck(thisPiece,thisMove,aPieces,bPieces)


def tryMovingPawnBackAndForth():
    blackPiece[0].moveMe(4,0)
    blackPiece[0].moveMe(5,0)
    blackPiece[0].moveBack(4,0)
    blackPiece[0].moveBack(2,0)

    print( blackPiece[0].hasMoved )

#end of def tryMovingPawnBackAndForth()






def moveBoardForward(thePiece,newMove,aPieces,bPieces):#this does not return anything, just changes aPieces and bPieces
    #print("moving board forward")
    if(thePiece.isWhite==aPieces[0].isWhite):#so that you refer to the right pieces
        myArray = aPieces
        otherArray = bPieces
    elif(thePiece.isWhite==bPieces[0].isWhite):
        myArray = bPieces
        otherArray = aPieces
    #so that I don't have to retype everything


    if (thePiece.type == "pawn"):  # promoting to a queen/king and en passant
        if(abs(newMove.x)==1 and newMove.y==0):#en passant
            theSpot = searchSpot(thePiece.xpos + newMove.x, thePiece.ypos, myArray,otherArray)  # something should be here

            myArray[thePiece.indexVal].moveMe(newMove.x + thePiece.xpos, thePiece.ypos+thePiece.moves[0].y)#move the original pawn
            #print(theSpot)
            otherArray[theSpot.indexVal].killMe()
            return(["en passant",theSpot])#the specific situation and the killed pawn. The move gives the necessary info on direction

        if (newMove.y==3 or newMove.y==4):#pawn promotion
            rememberMoveNumber=thePiece.moveNumber
            if(newMove.y==3):
                holderType="queen"
            elif(newMove.y==4):
                holderType="knight"

            #print("thinks it's at the edge")
            #newMove.printVector()

            if (newMove.x == 0):
                myArray[thePiece.indexVal] = Piece(holderType, thePiece.xpos, thePiece.ypos + thePiece.moves[0].y,thePiece.isWhite, thePiece.pic, thePiece.indexVal)
                return (["pawn promotion", "not kill",rememberMoveNumber])
            elif (newMove.x != 0):
                theSpot = searchSpot(thePiece.xpos+newMove.x, thePiece.ypos+thePiece.moves[0].y, myArray, otherArray)  # something should be here
                otherArray[theSpot.indexVal].killMe()
                myArray[thePiece.indexVal] = Piece(holderType, thePiece.xpos + newMove.x,thePiece.ypos + thePiece.moves[0].y, thePiece.isWhite, thePiece.pic,thePiece.indexVal)
                #print("Just moved a pawn forward to promotion (w/in move board forward method)")
                #myArray[thePiece.indexVal].printSelf()
                return(["pawn promotion","kill",theSpot,rememberMoveNumber])

                # end of stuff dealing with pawn promotion
    if(thePiece.type == "king"):#for castling
        if(abs(newMove.x)==2):
            if(newMove.x==-2):
                myArray[thePiece.indexVal].moveMe(newMove.x + thePiece.xpos, newMove.y + thePiece.ypos)
                myArray[8].moveMe(3,thePiece.ypos)
                return (["castling", "left"])
            elif(newMove.x==2):
                myArray[thePiece.indexVal].moveMe(newMove.x + thePiece.xpos, newMove.y + thePiece.ypos)
                myArray[9].moveMe(5, thePiece.ypos)
                return (["castling", "right"])

    #this is for non-specific cases of moving
    theSpot = searchSpot(thePiece.xpos+newMove.x, thePiece.ypos+newMove.y, myArray, otherArray)
    myArray[thePiece.indexVal].moveMe(newMove.x + thePiece.xpos, newMove.y + thePiece.ypos)  # move the new board piece


    if (theSpot != False and theSpot != True):
        if (theSpot.isWhite != thePiece.isWhite):


            otherArray[theSpot.indexVal].killMe()
            return (["kill", theSpot])
    return (["not kill"])

#end of def moveBoardForward(thePiece,newMove,aPieces,bPieces)


def moveBoardBackward(thePiece,newMove,aPieces,bPieces,info):#move stuff back
    #print("moving board backward")
    if (thePiece.isWhite == aPieces[0].isWhite):  # so that you refer to the right pieces
        myArray = aPieces
        otherArray = bPieces
    elif (thePiece.isWhite == bPieces[0].isWhite):
        myArray = bPieces
        otherArray = aPieces

    if(info[0]!="pawn promotion" and info[0]!="en passant"):

        myArray[thePiece.indexVal].moveBack(thePiece.xpos - newMove.x, thePiece.ypos - newMove.y)


    if (info[0] == "kill"):
        otherArray[info[1].indexVal].moveBack(info[1].perishX, info[1].perishY)
    if( info[0] == "pawn promotion"):
        #myArray[thePiece.indexVal]=Piece("pawn",myArray[thePiece.indexVal].xpos,myArray[thePiece.indexVal].ypos,myArray[thePiece.indexVal].isWhite,thePiece.pic,thePiece.indexVal)#turn it back into a pawn

        myArray[thePiece.indexVal].type="pawn"
        myArray[thePiece.indexVal].moves = []
        if(thePiece.isWhite==True):
            myArray[thePiece.indexVal].moves = [Vector(0,1)]
        elif(thePiece.isWhite==False):
            myArray[thePiece.indexVal].moves = [Vector(0, -1)]

        myArray[thePiece.indexVal].hasMoved=True

        #newMove.printVector()
        #print("Here's where it is sending the pawn to: "+str(thePiece.xpos-newMove.x)+","+str(thePiece.ypos-myArray[thePiece.indexVal].moves[0].y) )
        myArray[thePiece.indexVal].moveBack(thePiece.xpos-newMove.x,thePiece.ypos-myArray[thePiece.indexVal].moves[0].y)

        #myArray[thePiece.indexVal].moveBack(thePiece.xpos,thePiece.ypos)

        if(info[1] == "kill"):#promoted AND killed a piece
            otherArray[info[2].indexVal].moveBack(info[2].perishX, info[2].perishY)
            myArray[thePiece.indexVal].moveNumber=info[3]
        else:
            myArray[thePiece.indexVal].moveNumber = info[2]

    if( info[0]=="castling"):

        if(info[1]=="left"):
            #myArray[thePiece.indexVal].moveBack(4, thePiece.ypos)#move the king back
            myArray[8].moveBack(0,myArray[8].ypos)
        if(info[1]=="right"):
            #myArray[thePiece.indexVal].moveBack(4, thePiece.ypos)  # move the king back
            myArray[9].moveBack(7, myArray[8].ypos)

    if( info[0]=="en passant"):
        myArray[thePiece.indexVal].moveBack(thePiece.xpos - newMove.x, thePiece.ypos - thePiece.moves[0].y)
        otherArray[info[1].indexVal].moveBack(info[1].perishX, info[1].perishY)
        otherArray[info[1].indexVal].justDoubleJumped=True


#end of def moveBoardBackward(thePiece,newMove,aPieces,bPieces,info)

def alphaBetaMinimax(currentDepth,totalDepth,aPieces,bPieces,alpha,beta,isMaximizer):#alpha is minimum, beta is maximum. If alpha>beta, do not continue

    if(currentDepth==totalDepth):#just return the value of the board
        return(evaluateBoard(aPieces,bPieces))

    elif(currentDepth<totalDepth):
        if(isMaximizer==True):#looking for the largest value I can attain
            possiblePiecesAndMoves = generatePossibleMoves(aPieces, bPieces,determineIfAttacked(aPieces[15].xpos, aPieces[15].ypos,aPieces,bPieces))  # this should check for in-check
            possiblePieces = possiblePiecesAndMoves[0]
            possibleMoves = possiblePiecesAndMoves[1]

            currentBest = -9999999999999#to initialize a value for the node, the worst case scenario
            topMoveChoice=0
            for a in range(len(possiblePiecesAndMoves[0])):

                updateValues = moveBoardForward(aPieces[possiblePieces[a].indexVal], possibleMoves[a], aPieces, bPieces)



                if(currentBest<beta):#as long as the desired range is still possible. currentBest is effectively alpha here
                    currentValue = alphaBetaMinimax(currentDepth + 1, totalDepth, aPieces, bPieces,currentBest,beta,False)

                    if (currentValue > currentBest):
                        currentBest = currentValue  # keep track of the top value
                        topMoveChoice = a #keep track of which move


                moveBoardBackward(aPieces[possiblePieces[a].indexVal], possibleMoves[a], aPieces, bPieces, updateValues)



                if(currentBest>=beta):#the value that the maximizer would pick is higher than what the minimizer can pick from his options (so this thread is pointless)
                    break #end this for loop
            if(currentDepth>0):
                return(currentBest)#what you would pick as the maximizer. Note that this currentBest may be larger than beta, so this may be an illogical move
            elif(currentDepth==0):

                #return ([possiblePieces[topMoveChoice], possibleMoves[topMoveChoice]])
                return ([aPieces[possiblePieces[topMoveChoice].indexVal], possibleMoves[topMoveChoice]])

        elif(isMaximizer==False):#looking for the smallest possible value I can attain
            possiblePiecesAndMoves = generatePossibleMoves(bPieces, aPieces,determineIfAttacked(bPieces[15].xpos, bPieces[15].ypos,bPieces,aPieces))  # this should check for in-check
            possiblePieces = possiblePiecesAndMoves[0]
            possibleMoves = possiblePiecesAndMoves[1]

            currentBest = 9999999999999  # to initialize a value for the node, the worst case scenario

            for a in range(len(possiblePiecesAndMoves[0])):
            #for a in range(1):

                updateValues = moveBoardForward(bPieces[possiblePieces[a].indexVal], possibleMoves[a], bPieces, aPieces)

                if(currentBest>alpha):#if what you would pick is still acceptable to the maximizer
                    currentValue = alphaBetaMinimax(currentDepth + 1, totalDepth, aPieces, bPieces, alpha, currentBest, True)

                if (currentValue < currentBest):#if what you have is even smaller
                    currentBest = currentValue  # keep track of the top value
                    #I don't care about which move because this is the minimzer, who is never at currentDepth==0

                moveBoardBackward(bPieces[possiblePieces[a].indexVal], possibleMoves[a], bPieces, aPieces, updateValues)

                if(currentBest<=alpha):#if what you would choose as the minimizer is smaller than what the maximizer wants
                    break #end the for loop
            #end of for a
            return(currentBest)#return back the value that the minimzer would choose (it's possible that this is an irrelevant value, considering that the maximizer may ignore it)

#end of def alphaBetaMinimax(currentDepth,totalDepth,aPieces,bPieces,alpha,beta,isMaximizer)







def minimax(currentDepth,totalDepth,aPieces,bPieces):

    #print("Beginning: "+str(currentDepth))
    #if(aPieces[0].isWhite==False):
        #print(aPieces[0].hasMoved)
    #elif(bPieces[0].isWhite==False):
        #print(bPieces[0].hasMoved)


    if(currentDepth==totalDepth):#if you're at the end of the stage
        #multiplier=-1

        return( -evaluateBoard(aPieces,bPieces) )
    elif(currentDepth<totalDepth):
        #possiblePiecesAndMoves = generatePossibleMoves(aPieces,bPieces, determineIfAttacked(aPieces[15].xpos,aPieces[15].ypos,aPieces,bPieces) )#this should check for in-check
        possiblePiecesAndMoves = generatePossibleMoves(aPieces, bPieces,determineIfAttacked(aPieces[15].xpos,aPieces[15].ypos,aPieces,bPieces))  # this should check for in-check

        possiblePieces = possiblePiecesAndMoves[0]
        possibleMoves = possiblePiecesAndMoves[1]
        topEvaluation = -10000000
        topMoveChoice = 0
        for a in range(len(possiblePiecesAndMoves[0])):

            updateValues = moveBoardForward(possiblePieces[a],possibleMoves[a],aPieces,bPieces)

            currentValue = minimax(currentDepth+1,totalDepth,bPieces,aPieces)

            if(currentValue>topEvaluation):
                topEvaluation=currentValue#keep track of the top value
                topMoveChoice=a

            moveBoardBackward(aPieces[possiblePieces[a].indexVal],possibleMoves[a],aPieces,bPieces,updateValues)


        if(currentDepth>0):
            return(-1*topEvaluation)#send the chosen value, multiplied by -1
        elif(currentDepth==0):
            return([ possiblePieces[topMoveChoice] , possibleMoves[topMoveChoice] ])
#end of def minimax(currentDepth,totalDepth,aPieces,bPieces)

def debugForwardAndBackwards(aPieces,bPieces):
    print("Beginning of debug method")
    possiblePiecesAndMoves = generatePossibleMoves(aPieces, bPieces)
    possiblePieces = possiblePiecesAndMoves[0]
    possibleMoves = possiblePiecesAndMoves[1]

    for a in range(len(possiblePiecesAndMoves[0])):

        if(possiblePieces[a].indexVal==0):
            #print("in debug method, before moving")
            #print(aPieces[0].hasMoved)
            pass

        updateValues = moveBoardForward(possiblePieces[a], possibleMoves[a], aPieces, bPieces)

        if (possiblePieces[a].indexVal == 0 and updateValues[0]=="en passant"):
            #print("just moved board forward, it's an en passant:")

            updateValues[1].printSelf()


            pass


        moveBoardBackward(aPieces[possiblePieces[a].indexVal], possibleMoves[a], aPieces, bPieces, updateValues)

        if (possiblePieces[a].indexVal == 0):
            #print("in debug method, after moving backwards: has it moved?")
            #print(aPieces[0].hasMoved)
            pass


#end of def debugForwardAndBackwards(aPieces,bPieces)

def debugPawnPromotionSetUp(aPieces,bPieces):#this sets up a situation where the AI SHOULD move a pawn forward and promote it
    for a in range(16):
        if(a!=0 and a!=15 and a!=8):
            killPiece(aPieces[a])
            killPiece(bPieces[a])
    killPiece(bPieces[0])
    updatePiece(aPieces[0],0,2)
    killPiece(aPieces[8])
    #updatePiece(bPieces[8],0,0)
    #killPiece(bPieces[8])
    updatePiece(bPieces[8],1,0)
    updatePiece(aPieces[15],7,7)
    updatePiece(bPieces[15],7,0)

#end of def debugPawnPromotionSetUp(aPieces,bPieces)

def debugCheckmate(aPieces,bPieces):

    #rook, knight, bishop
    #rook is 8,9, knight is 10,11, bishop is 12,13
    killPiece(aPieces[7])
    killPiece(aPieces[5])
    killPiece(aPieces[14])
    killPiece(aPieces[11])
    killPiece(aPieces[13])

    killPiece(bPieces[11])
    killPiece(bPieces[13])


    updatePiece(aPieces[15],7,1)
    updatePiece(aPieces[8],1,0)
    updatePiece(aPieces[0],0,3)
    updatePiece(aPieces[1],1,2)
    updatePiece(aPieces[9],5,0)
    updatePiece(aPieces[4],4,3)
    updatePiece(aPieces[10],3,4)
    updatePiece(aPieces[6],6,2)

    updatePiece(bPieces[14],5,1)
    updatePiece(bPieces[3],3,5)
    updatePiece(bPieces[4],4,4)
    updatePiece(bPieces[10],2,5)
    updatePiece(bPieces[8],3,7)
    updatePiece(bPieces[12],4,6)

    #updatePiece()

#end of def debugCheckmate(aPieces,bPieces)

def tryAndFixPawnPromotionBackAndForth():
    print("setting up a situation to go back and forth with the pawn promotion")
    debugPawnPromotionSetUp(blackPiece,whitePiece)

    blackPiece[0].printSelf()

    firstValues = moveBoardForward(blackPiece[0],Vector(0,-1),blackPiece,whitePiece)

    blackPiece[0].printSelf()

    secondValues = moveBoardForward(blackPiece[0], Vector(0, 3), blackPiece, whitePiece)

    blackPiece[0].printSelf()

    moveBoardBackward(blackPiece[0], Vector(0, 3), blackPiece, whitePiece, secondValues)

    blackPiece[0].printSelf()

    moveBoardBackward(blackPiece[0], Vector(0,-1), blackPiece, whitePiece, firstValues)

    blackPiece[0].printSelf()
#end of def tryAndFixPawnPromotionBackAndForth()







def AIMove(isWhite,forNow=True):

    if(forNow==False):
        return 0




    global myText
    global canvas
    if (determineIfAttacked(blackPiece[15].xpos, blackPiece[15].ypos, blackPiece, whitePiece) == True):
        print("ENEMY IS IN CHECK")
        canvas.itemconfigure(myText, text="ENEMY IS IN CHECK")

        # myText = canvas.create_text(600, 300, text="In Check")
        if (determineIfNoWayOut(blackPiece, whitePiece) == True):
            canvas.itemconfigure(myText, text="Checkmate for enemy! You win!")
            return(0)
    else:
        if (determineIfNoWayOut(blackPiece, whitePiece) == True):
            print("Stalemate!")
            canvas.itemconfigure(myText, text="Stalemate!")
            # myText = canvas.create_text(600, 300, text="Checkmate!")
            return(0)


    if(isWhite==False):
        myArray = blackPiece
        otherArray=whitePiece
    elif(isWhite==True):

        myArray = whitePiece
        otherArray=blackPiece

    #piecesAndMoves = minimax(0, 3, blackPiece, whitePiece)
    piecesAndMoves = alphaBetaMinimax(0,3,myArray,otherArray,-9999999999999,9999999999999,True)



    

    thePiece = piecesAndMoves[0]
    theMove = piecesAndMoves[1]

    print("Here is what the AI chooses to do:")
    thePiece.printSelf()
    theMove.printVector()

    possibleTarget = searchSpot(thePiece.xpos + theMove.x, thePiece.ypos + theMove.y, whitePiece, blackPiece)

    if (possibleTarget != False and possibleTarget != True):#in an en passant, I kill the piece here
        killPiece(possibleTarget)
    #thePiece.printSelf()
    #theMove.printVector()
    if(thePiece.type=="king" and abs(theMove.x)==2):#castling
        updatePiece(thePiece, thePiece.xpos + theMove.x, thePiece.ypos + theMove.y)
        if(theMove.x==-2):
            updatePiece(myArray[8],3,myArray[8].ypos)
        elif(theMove.x==2):
            updatePiece(myArray[9], 5, myArray[9].ypos)
    elif(thePiece.type=="pawn" and theMove.y==0):#en passant
        #theSpot = searchSpot(thePiece.xpos+theMove.x,thePiece.ypos,myArray,otherArray)
        #killPiece(theSpot)#assume that theSpot is an enemy piece -- I've already killed this piece up above!
        updatePiece(thePiece, thePiece.xpos + theMove.x, thePiece.ypos + thePiece.moves[0].y)
    elif(thePiece.type=="pawn" and theMove.y>=3):#pawn promotion
        if(theMove.y==3):
            typeString = "queen"
            if(thePiece.isWhite==True):
                tempPic = wQueenPic
            else:
                tempPic=bQueenPic
        elif(theMove.y==4):
            typeString="knight"
            if (thePiece.isWhite == True):
                tempPic = wKnightPic
            else:
                tempPic = bKnightPic

        if(theMove.x==0):#non kill
            updatePiece(thePiece, thePiece.xpos, thePiece.ypos + thePiece.moves[0].y)
            print("########should change picture, no kill required")
            myArray[thePiece.indexVal] = Piece(typeString,thePiece.xpos, thePiece.ypos,thePiece.isWhite,tempPic,thePiece.indexVal)
            if(thePiece.isWhite==True):
                canvas.move(whitePics[thePiece.indexVal], -500, -1000)
                whitePics[thePiece.indexVal] = canvas.create_image(125 + 50 * whitePiece[thePiece.indexVal].xpos,
                                                                    475 - 50 * whitePiece[thePiece.indexVal].ypos,
                                                                    image=tempPic)
            else:
                canvas.move(blackPics[thePiece.indexVal], -500, -1000)
                blackPics[thePiece.indexVal] = canvas.create_image(125 + 50 * blackPiece[thePiece.indexVal].xpos,
                                                                   475 - 50 * blackPiece[thePiece.indexVal].ypos,
                                                                   image=tempPic)
        elif(theMove.x!=0):
            theSpot = searchSpot(thePiece.xpos+theMove.x, thePiece.ypos + thePiece.moves[0].y,myArray,otherArray)
            killPiece(theSpot)
            updatePiece(thePiece, thePiece.xpos+theMove.x, thePiece.ypos + thePiece.moves[0].y)

            myArray[thePiece.indexVal] = Piece(typeString, thePiece.xpos, thePiece.ypos,thePiece.isWhite, tempPic, thePiece.indexVal)
            if (thePiece.isWhite == True):
                canvas.move(whitePics[thePiece.indexVal], -500, -1000)
                whitePics[thePiece.indexVal] = canvas.create_image(125 + 50 * whitePiece[thePiece.indexVal].xpos,
                                                                   475 - 50 * whitePiece[thePiece.indexVal].ypos,
                                                                   image=tempPic)
            else:
                canvas.move(blackPics[thePiece.indexVal], -500, -1000)
                blackPics[thePiece.indexVal] = canvas.create_image(125 + 50 * blackPiece[thePiece.indexVal].xpos,
                                                                   475 - 50 * blackPiece[thePiece.indexVal].ypos,
                                                                   image=tempPic)

    else:#for regular situations
        updatePiece(thePiece, thePiece.xpos + theMove.x, thePiece.ypos + theMove.y)



#end of def AIMove(isWhite)




def on_click(event):
    print("         ")
    print("*********click*********")
    global mouseIsHolding
    global tempPiece
    xVal = int( round((event.x-125)/50,0) )#returns 0 through 7 (or not if it is not clicking on the right part of screen)
    yVal = int( round( (475-event.y)/50 ) )

    if(xVal>8):

        pass



    if(xVal>=0 and xVal<8 and yVal>=0 and yVal<8):#if it is on the board

        jim = searchSpot(xVal,yVal,whitePiece,blackPiece)

        if(jim==False):

            if(mouseIsHolding==True and tempPiece.type=="pawn" and tempPiece.ypos==3.5+2.5*tempPiece.moves[0].y and yVal==3.5+3.5*tempPiece.moves[0].y and tempPiece.xpos==xVal):
                #print("HELLO THERE, I SHOULD BE PROMOTED")

                mouseIsHolding = False
                #updatePiece(tempPiece, xVal, yVal)
                pieceChoice = input("Which piece would you like to be promoted to?")
                if pieceChoice in ['q','queen','Q']:
                    typeString="queen"
                    if(tempPiece.isWhite==True):
                        newPic = wQueenPic
                    elif(tempPiece.isWhite==False):
                        newPic = bQueenPic
                if pieceChoice in ['r','rook','R']:
                    typeString = "rook"
                    if (tempPiece.isWhite == True):
                        newPic = wRookPic
                    elif (tempPiece.isWhite == False):
                        newPic = bRookPic
                if pieceChoice in ['k','n','K','N','knight']:
                    typeString="knight"
                    if (tempPiece.isWhite == True):
                        newPic = wKnightPic
                    elif (tempPiece.isWhite == False):
                        newPic = bKnightPic

                if pieceChoice in ['bishop','b','B']:
                    typeString="bishop"
                    if (tempPiece.isWhite == True):
                        newPic = wBishopPic
                    elif (tempPiece.isWhite == False):
                        newPic = bBishopPic

                if(tempPiece.isWhite==True):
                    whitePiece[tempPiece.indexVal]=Piece(typeString,tempPiece.xpos,tempPiece.ypos,tempPiece.isWhite,newPic,tempPiece.indexVal)
                    canvas.move(whitePics[tempPiece.indexVal], -500, -1000)
                    whitePics[tempPiece.indexVal]=canvas.create_image(125 + 50 * tempPiece.xpos, 475 - 50 * tempPiece.ypos, image=newPic)
                    updatePiece(whitePiece[tempPiece.indexVal], xVal, yVal)
                elif(tempPiece.isWhite==False):
                    blackPiece[tempPiece.indexVal] = Piece(typeString, tempPiece.xpos, tempPiece.ypos, tempPiece.isWhite, newPic, tempPiece.indexVal)
                    canvas.move(blackPics[tempPiece.indexVal], -500, -1000)
                    blackPics[tempPiece.indexVal] = canvas.create_image(125 + 50 * tempPiece.xpos, 475 - 50 * tempPiece.ypos, image=newPic)
                    updatePiece(blackPiece[tempPiece.indexVal], xVal, yVal)
                #updatePiece(tempPiece,xVal,yVal)
                    #canvas.create_image(125 + 50 * whitePiece[a].xpos, 475 - 50 * whitePiece[a].ypos, image=whitePiece[a].pic)
                    #blackPiece.append( Piece("queen",3,7,False,bQueenPic,14) )
                AIMove(False)

            elif(checkIfLegal(tempPiece,Vector(xVal,yVal),whitePiece,blackPiece)==True and mouseIsHolding==True):#for legal moves

                mouseIsHolding = False

                updatePiece(tempPiece, xVal, yVal)
                AIMove(False)

        elif(jim!=False and mouseIsHolding==False):#if a piece is there
            #jim.printSelf()
            mouseIsHolding=True
            tempPiece = jim
        elif(jim!=False and mouseIsHolding==True and jim.isWhite!=tempPiece.isWhite):#enemy team is there and I am depositing a piece on top

            if (tempPiece.type == "pawn" and tempPiece.ypos == 3.5 + 2.5 * tempPiece.moves[0].y and yVal == 3.5 + 3.5 * tempPiece.moves[0].y and abs(tempPiece.xpos-jim.xpos)==1):#for pawn promotion diagonally
                killPiece(jim)
                print("HELLO THERE, I SHOULD BE PROMOTED")
                mouseIsHolding = False
                updatePiece(tempPiece, xVal, yVal)
                pieceChoice = input("Which piece would you like to be promoted to? ")
                if pieceChoice in ['q', 'queen', 'Q']:
                    typeString = "queen"
                    if (tempPiece.isWhite == True):
                        newPic = wQueenPic
                    elif (tempPiece.isWhite == False):
                        newPic = bQueenPic
                if pieceChoice in ['r', 'rook', 'R']:
                    typeString = "rook"
                    if (tempPiece.isWhite == True):
                        newPic = wRookPic
                    elif (tempPiece.isWhite == False):
                        newPic = bRookPic
                if pieceChoice in ['k', 'n', 'K', 'N', 'knight']:
                    typeString = "knight"
                    if (tempPiece.isWhite == True):
                        newPic = wKnightPic
                    elif (tempPiece.isWhite == False):
                        newPic = bKnightPic

                if pieceChoice in ['bishop', 'b', 'B']:
                    typeString = "bishop"
                    if (tempPiece.isWhite == True):
                        newPic = wBishopPic
                    elif (tempPiece.isWhite == False):
                        newPic = bBishopPic

                if (tempPiece.isWhite == True):
                    whitePiece[tempPiece.indexVal] = Piece(typeString, whitePiece[tempPiece.indexVal].xpos, whitePiece[tempPiece.indexVal].ypos,
                                                           tempPiece.isWhite, newPic, tempPiece.indexVal)
                    canvas.move(whitePics[tempPiece.indexVal], -500, -1000)
                    whitePics[tempPiece.indexVal] = canvas.create_image(125 + 50 * whitePiece[tempPiece.indexVal].xpos,
                                                                        475 - 50 * whitePiece[tempPiece.indexVal].ypos, image=newPic)
                elif (tempPiece.isWhite == False):
                    blackPiece[tempPiece.indexVal] = Piece(typeString, blackPiece[tempPiece.indexVal].xpos, blackPiece[tempPiece.indexVal].ypos,
                                                           tempPiece.isWhite, newPic, tempPiece.indexVal)
                    canvas.move(blackPics[tempPiece.indexVal], -500, -1000)
                    blackPics[tempPiece.indexVal] = canvas.create_image(125 + 50 * blackPiece[tempPiece.indexVal].xpos,
                                                                        475 - 50 * blackPiece[tempPiece.indexVal].ypos, image=newPic)


            elif (checkIfLegal(tempPiece, Vector(xVal, yVal),whitePiece,blackPiece)==True):
                print("moving piece")
                mouseIsHolding = False
                updatePiece(tempPiece, xVal, yVal)
                killPiece(jim)
                AIMove(False)

        elif(jim!=False and mouseIsHolding==True and jim==tempPiece):
            mouseIsHolding = False
        elif (jim != False and mouseIsHolding == True and jim.isWhite == tempPiece.isWhite and jim.type == "rook" and tempPiece.type=="king" and jim.hasMoved==False and tempPiece.hasMoved==False):
            if( checkForCastle(tempPiece,jim,whitePiece,blackPiece)==True ):#in this case, tempPiece is the king and jim is the rook
                if (jim.xpos < tempPiece.xpos):#if you move the king left
                    updatePiece(tempPiece, 2, tempPiece.ypos)
                    updatePiece(jim, 3, jim.ypos)
                    AIMove(False)
                elif (jim.xpos > tempPiece.xpos):#if you move the king right
                    updatePiece(tempPiece, 6, tempPiece.ypos)
                    updatePiece(jim, 5, jim.ypos)
                    AIMove(False)

        elif(jim!=False and mouseIsHolding==True and jim.isWhite==tempPiece.isWhite):
            tempPiece = jim #reassign the tempPiece
        #for castling
    elif(xVal>8):
        mouseIsHolding=False

    #printPossibleMoves(blackPiece,whitePiece,False)



    if(determineIfAttacked(whitePiece[15].xpos,whitePiece[15].ypos,whitePiece,blackPiece)==True):
        print("IN CHECK")
        canvas.itemconfigure(myText, text="IN CHECK")
        printPossibleMoves(whitePiece, blackPiece)
        #myText = canvas.create_text(600, 300, text="In Check")
        if(determineIfNoWayOut(whitePiece,blackPiece)==True):
            canvas.itemconfigure(myText, text="Checkmate!")
    else:
        if (determineIfNoWayOut(whitePiece, blackPiece) == True):
            print("Stalemate!")
            canvas.itemconfigure(myText, text="Stalemate!")
            #myText = canvas.create_text(600, 300, text="Checkmate!")
        else:
            canvas.itemconfigure(myText, text="")



        #canvas.itemconfigure(myText,text="clicked")








#end of def on_click(event)




myText = canvas.create_text(700,300,text="not in check")
canvas.create_text(700,10,text="Instructions:")
canvas.create_text(700,25,text="You play as the white pieces. Click on a piece and click on its destination. Black will move next")
canvas.create_text(700,40,text="To castle, click on the king and then click on your rook (if you are able to castle)")
canvas.create_text(700,55,text="To en passant, click on your pawn and then click on its destination")
canvas.create_text(700,70,text="To unclick a piece, click on the white screen to the right of the board")
canvas.create_text(650,85,text="To promote a pawn, click back to the page with the programming on it and type q for queen at the bottom")


#restartButton.bind("<ButtonPress-1>",on_restart)


canvas.bind("<ButtonPress-1>",on_click)#so it always listens for clicks!




printPieces()




root.mainloop()#this actually sets the image up. Put this the end



