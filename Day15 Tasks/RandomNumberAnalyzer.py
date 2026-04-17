import numpy as np
import random

#Use random to generate 10 numbers 
nums = [random.randint(1, 100) for i in range (10)]
print("the random numbers are :\n",nums)

#Use loop + condition to count even/odd numbers
even=[]
odd=[]

for x in nums:
    if x % 2 == 0:
        even.append(x)
    else:
        odd.append(x)

print("the even numbers are :\n",even)
print("the odd numbers are :\n", odd)

#Use set to remove duplicates
new_nums=set(nums)
print("after removing dupkicates:\n", new_nums)



