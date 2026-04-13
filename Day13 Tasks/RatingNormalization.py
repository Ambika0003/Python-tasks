import numpy as np

r = np.array([2, 3, 4, 5, 1]) 

n=(r-np.min(r))/(np.max(r)-np.min(r))
print(n)

