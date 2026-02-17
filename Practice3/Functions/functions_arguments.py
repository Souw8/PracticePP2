def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")
#Argument it is a vlaue that we input into our function
# in this case it is fname
"""From a function's perspective:

A parameter is the variable listed inside the parentheses in the function definition.

An argument is the actual value that is sent to the function when it is called."""
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")
# Also we can take default values for argument if argument wasn given
#in the 19 line we doont have argument therefore it will print Hello friend
#Positional-Only Arguments
#You can specify that a function can have ONLY positional arguments.

#To specify positional-only arguments, add , / after the arguments:

#Example
def my_function(name, /):
  print("Hello", name)

my_function("Emil")
#Without the , / you are actually allowed to use keyword arguments even if the function expects positional arguments:

#Example
def my_function(name):
  print("Hello", name)

my_function(name = "Emil")
#With , /, you will get an error if you try to use keyword arguments:

#Example
def my_function(name, /):
  print("Hello", name)

my_function(name = "Emil")
#Keyword-Only Arguments
#To specify that a function can have only keyword arguments, add *, before the arguments:

#Example
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil")
#Without *,, you are allowed to use positional arguments even if the function expects keyword arguments:

#Example
def my_function(name):
  print("Hello", name)

my_function("Emil")
#With *,, you will get an error if you try to use positional arguments:

#Example
def my_function(*, name):
  print("Hello", name)

my_function("Emil")
#Combining Positional-Only and Keyword-Only
#You can combine both argument types in the same function.

#Arguments before / are positional-only, and arguments after * are keyword-only:

#Example
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)