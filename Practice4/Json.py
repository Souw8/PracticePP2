"""JSON is a syntax for storing and exchanging data.

JSON is text, written with JavaScript object notation.

JSON in Python
Python has a built-in package called json, which can be used to work with JSON data.

ExampleGet your own Python Server
Import the json module:"""

import json
#Parse JSON - Convert from JSON to Python
#If you have a JSON string, you can parse it by using the json.loads() method.

#The result will be a Python dictionary.

#Example
#Convert from JSON to Python:

import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["age"])


#Convert from Python to JSON
#If you have a Python object, you can convert it into a JSON string by using the json.dumps() method.

#Example
#Convert from Python to JSON:

import json

# a Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)


#Order the Result
#The json.dumps() method has parameters to order the keys in the result:

#Example
#Use the sort_keys parameter to specify if the result should be sorted or not:

json.dumps(x, indent=4, sort_keys=True)


#Example
#Use the separators parameter to change the default separator:

json.dumps(x, indent=4, separators=(". ", " = "))