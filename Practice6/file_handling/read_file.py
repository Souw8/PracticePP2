"""Open a File on the Server
Assume we have the following file, located in the same folder as Python:

text.txt

water is good the sky is blue you nedd to rest and lay on the ground
catch your wave with the emotioons 
max wants some sleep and he would like to finish his work web development
To open the file, use the built-in open() function.

The open() function returns a file object, which has a read() method for reading the content of the file:

ExampleGet your own Python Server"""
f = open("C:/Users/User/Desktop/text.txt") #by default in the seccond parameter we have "r" or read mode
print(f.read())




"""Example
Using the with keyword:"""

with open("text.txt") as f:
  print(f.read())
#Then you do not have to worry about closing your files, the with statement takes care of that.


"""Close Files
It is a good practice to always close the file when you are done with it.

If you are not using the with statement, you must write a close statement in order to close the file:

Example
Close the file when you are finished with it:"""

f = open("text.txt")
print(f.readline())
f.close()




"""Read Only Parts of the File
By default the read() method returns the whole text, but you can also specify how many characters you want to return:

Example
Return the 5 first characters of the file:"""

with open("demofile.txt") as f:
  print(f.read(5)) # read method parameter will be number of characters



"""Read Lines
You can return one line by using the readline() method:

Example
Read one line of the file:"""

with open("text.txt") as f:
  print(f.readline())

"""By looping through the lines of the file, you can read the whole file, line by line:

Example
Loop through the file line by line:"""

with open("demofile.txt") as f:
  for x in f:
    print(x)

