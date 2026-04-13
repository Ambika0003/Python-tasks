import numpy as np

data = np.array([1, 2, 2, 3, 1, 4, 2, 3]) 
print(data)

values=np.unique(data)
print(values)

values, count=np.unique(data, return_counts=True)
print(count)