"""The Elif Keyword
The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".

The elif keyword allows you to check multiple expressions for True and execute a block of code as soon as one of the conditions evaluates to True."""

a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
  #When you use elif, Python evaluates the conditions from top to bottom. As soon as it finds a condition that is true, it executes that block and skips all remaining conditions.
  