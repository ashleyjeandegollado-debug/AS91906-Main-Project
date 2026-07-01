#Simple collision detection for a hit box

class Entity:
    def __init__(self, x, y, w, h):
        print("Entity Init")
        self._x = x
        self._y = y
        self._h = h
        self._w = w
    def get_react(self):
        return self.__x, self.__y, self.__w, self.__h
    def collide(self, x, y, w, h):
        # If there is NO collision, one (or more) of the following MUST be true
        # - left edge of A past right edge of B
        # - top edge of A below bottom edge of B 
        # - right edge of A  is before left edge of B
        # - bottom edge of A is above top edge of B
        if  x > self.__x + self.__w or \
            y > self.__y + self.__h or \
            x + w < self.__x or \
            y + h < self.__y:
            return False
        else:
            return True
    def get_x(self):
        return self.__x  

class Obstacle(Entity):
    def __init__(self, x):
        print("Obstacle Init")
        super().__init__(x, 10, 10, 10)
    def show(self):
        print(self._Entity__x)
        print(dir(self))

entity_a = Entity(10, 10, 10, 10)
entity_b = Entity(15, 15, 10, 10)
entity_c = Entity(21, 15, 10, 10)

print(entity_a.collide(*entity_b.get_rect()))
print(entity_a.collide(*entity_c.get_rect()))

obstacle_a = Obstacle(10)
obstacle_a.show()
print(obstacle_a.collide(*entity_a.get_rect()))

# Note, I am using the \ character to continue a line so that the set of conditions are more readable.
# However, because I am continuing the line, I can not comment each condition on that line, as it would actually
# in the middle of the logical expression

# also, note the * when I call the collide function.
# returning multiple values actually returns a Tuple (a, b , c, d) which will come back as a single object,
# and python will say there are 3 parameters missing.
#   The * operator unpacks the tuple into the four variables.

# It's actually a lot harder to define what IS a collision than what is not, because there's a bunch of exceptions.