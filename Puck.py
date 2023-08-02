class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def __eq__(self, other):
        if other is None:
            return self.x == -1 and self.y == -1
    def __str__(self):
        return f"({self.x}, {self.y})"