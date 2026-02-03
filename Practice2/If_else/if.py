# "IF"  we want to check something we need if statement that will cheack if the condition correct or not
#Example
"""Python supports the usual logical conditions from mathematics:

Equals: a == b
Not Equals: a != b
Less than: a < b
Less than or equal to: a <= b
Greater than: a > b
Greater than or equal to: a >= b"""
a = 33
b = 200
if b > a:
  print("b is greater than a")
  """Indentation
Python relies on indentation (whitespace at the beginning of a line) to define scope in the code. Other programming languages often use curly-brackets for this purpose.

Example
If statement, without indentation (will raise an error):

a = 33
b = 200
if b > a:
print("b is greater than a") # you will get an error"""
"""Using Variables in Conditions
Boolean variables can be used directly in if statements without comparison operators.

Example
Using a boolean variable:
"""
is_logged_in = True
if is_logged_in:
  print("Welcome back!")