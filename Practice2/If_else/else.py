"""The Else Keyword
The else keyword catches anything which isn't caught by the preceding conditions.

The else statement is executed when the if condition (and any elif conditions) evaluate to False."""
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
#we can use other patterns like only if and else without elif
#Example
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
