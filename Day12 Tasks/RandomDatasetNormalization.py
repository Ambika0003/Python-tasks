import numpy as np

x=np.random.rand(8)
print("the 8 random numbers are :\n", x )

x=x*100
print("numbers multiplying with 100 are :\n", x)

newdata=x[x>50]
print("the numbers greater than 50 are :\n", newdata)

filtered_values=np.sort(newdata)
print("the sorted list is:\n",filtered_values)

