class Animal:
    def __init__(self, name, age=5):
       self.name = name
       self.age = age
    
    def introduce(self):
        print(self.name, self.age)
    
    def walk(self):
        print("walking") 
        

burek = Animal("Burek", 5)
azor = Animal("Azor", 3)
default = Animal("Rex")
explicite = Animal(age="4", name="Lola")
burek.introduce()
azor.introduce()
default.introduce()
explicite.introduce()