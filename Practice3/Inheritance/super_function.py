#Use the super() Function
#Python also has a super() function that will make the child class inherit all the methods and properties from its parent:

#Example
#class Student(Person):
  #def __init__(self, fname, lname):
    #super().__init__(fname, lname)"""
#By using the super() function, you do not have to use the name of the parent element, it will automatically inherit the methods and properties from its parent.

#Add Properties
#Example
#Add a property called graduationyear to the Student class:

#class Student(Persons):
  #def __init__(self, fname, lname):
    #super().__init__(fname, lname)
    #self.graduationyear = 2019
#In the example below, the year 2019 should be a variable, and passed into the Student class when creating student objects. To do so, add another parameter in the __init__() function:

#Example
#Add a year parameter, and pass the correct year when creating objects