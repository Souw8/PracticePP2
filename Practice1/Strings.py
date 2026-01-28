#Strings in python are surrounded by either single quotation marks, or double quotation marks.

#'hello' is the same as "hello".

#You can display a string literal with the print() function:
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)
#in this example we have multistring this can contain many line of words
#next thing we need to talk is strings as arrays
#this means that string can be represent like array 
#for example
word="hello"
print(word[0])#[] with this we take the element spoted in this index and for thi sutiation it will be "h"

for x in "banana":
  print(x) #and like arrays we can walk through all elements of string 

txt = "The best things in life are free!"
print("free" in txt) #you can check if in this sentence  we need to check word free in this senntence and output will be true


b = "Hello, World!"
print(b[2:5]) #with this  we can retrieve elements of string  with index dia.


a = "Hello, World!"
print(a.upper())
a = "Hello, World!"
print(a.lower())
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"
a = "Hello, World!"
print(a.replace("H", "J"))
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']
a = "Hello"
b = "World"
c = a + b
print(c)
age = 36
txt = f"My name is John, I am {age}"
print(txt)
txt = "We are the so-called \"Vikings\" from the north."