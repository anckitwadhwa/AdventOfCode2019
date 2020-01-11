class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __hash__(self):
        return(hash((self.x, self.y)))

    def __str__(self):
        return("("+str(self.x) + "," + str(self.y)+")")

    def __eq__(self, other):
        if isinstance(other, Point):
            return((self.x == other.x) and (self.y == other.y))

        return False
