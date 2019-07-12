#Tyler Piazza, 5,3,1
#These are two dimensional vectors, meant to store x and y values together (so the order of the elements matters)
#This could be used for moves or for position (which is a "move" relative to {0,0})


class Vector(object):
    def __init__(self,a,b):
        self.x = a
        self.y = b


    def printVector(self):
        print("{"+str(self.x)+","+str(self.y)+"}")#just print it out for the world to see

    def __eq__(self,other):
        return self.__dict__ == other.__dict__
    #this lets you quickly check equality between vectors









