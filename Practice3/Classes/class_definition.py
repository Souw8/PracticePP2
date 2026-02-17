"""Classes and objects are the two core concepts in object-oriented programming.

A class defines what an object should look like, and an object is created based on that class. For example:

Class	Objects
Fruit	Apple, Banana, Mango
Car	Volvo, Audi, Toyota
When you create an object from a class, it inherits all the variables and functions defined inside that class."""

"""The __init__() Method
All classes have a built-in method called __init__(), which is always executed when the class is being initiated.

The __init__() method is used to assign values to object properties, or to perform operations that are necessary when the object is being created.

ExampleGet your own Python Server
Create a class named Person, use the __init__() method to assign values for name and age:"""

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)