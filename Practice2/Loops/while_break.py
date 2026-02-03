"""The break Statement
With the break statement we can stop the loop even if the while condition is true:

Example
Exit the loop when i is 3:"""

i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1
#in conclusion we can say that if we want stop program you can add your condition and it will break 
#instantly
#example you might want see all  even numbers but if in the sequence you encounter odd it will stop
i=2
num=int(input())
while i<=num and i%2==0:
  print(i)
  i+=1
   