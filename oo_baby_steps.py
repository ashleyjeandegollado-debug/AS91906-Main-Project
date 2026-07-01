#classes
class Fruit():
    _my_type=""
    def __init__(self, the_name):
        self._name = the_name
        Fruit.my_type = "I'm a fruit"
        self._size = 2

    def show(self):
        print(Fruit.my_type)
        print(self._name)

my_fruit = Fruit("Apple")
my_fruit.show()
my_fruit2 = Fruit("Pear")
my_fruit2.show()
my_fruit._size = 3
Fruit._my_type = "blah"
my_fruit.show()
my_fruit2.show()

class Banana(Fruit):
    def __init__(self, length):
        self._length = length
        super().__init__("Banana")
    def show(self):
        print(self._length)
        super().show()

my_fruit3 = Banana(20)
my_fruit3.show()
