class Tube:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        print("X {0}, Y {1}".format(self.x, self.y))

    def qua_trai(self):
        self.x -= 1

    
a = []
a.append(Tube(1, 2))
a.append(Tube(3, 4))
a.append(Tube(5, 6))

for x in a:
    x.display()

print("-----------")
for x in a:
    x.qua_trai()

for x in a:
    x.display()