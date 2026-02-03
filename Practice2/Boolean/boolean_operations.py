"""Most Values are True
Almost any value is evaluated to True if it has some sort of content.

Any string is True, except empty strings.

Any number is True, except 0.

Any list, tuple, set, and dictionary are True, except empty ones.

Example
The following will return True:"""

bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])
"""Some Values are False
In fact, there are not many values that evaluate to False, except empty values, such as (), [], {}, "", the number 0, and the value None. And of course the value False evaluates to False.

#Example
The following will return False:"""

bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})
#Also we can use boolaen values in functions
#Example
def myFunction() :
  return True

print(myFunction())


def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")
#And there is also three opreators for logical values 1)and 2)or 3)not
