import numpy as np
 
data =[[1, 2, 3], [4, 5], [6]]
newdata=[item for sublist in data for item in sublist]
print(newdata)

squares=[x**2 for x in newdata if x % 2 ==0]
print("the sqaures of even numbers are :\n", squares)

