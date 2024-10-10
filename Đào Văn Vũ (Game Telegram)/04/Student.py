class Student:
    def __init__(self):
        self.name = "abc"
        self.age = 18
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print("Name {0}, Age {1}".format(self.name, self.age))

    def hoc_bai(self):
        print("{0} đang học bài".format(self.name))