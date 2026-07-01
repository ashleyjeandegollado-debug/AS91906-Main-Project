class Ball():
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
    def setx(self, x):
        print("inside setx")
        if x>=0 and x<=399:
            self._x = x 
        else: 
            print("error")
            exit()
    def getx(self):
        print("inside getx")
        return self._x
    def getxr(self):
        return self._x + self._w
    def getyb(self):    
        return self._y + self._h
    x = property(getx, setx)
    xr = property(getxr)
    yb = property(getyb)

ball1 = Ball (200,200, 10, 10)
print(ball1.x)
ball1.x = 500
print(ball1.xr, ball1.yb)