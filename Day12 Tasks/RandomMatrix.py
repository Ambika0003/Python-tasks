import numpy as np

matrix=np.random.randint(0,51, (3,3))
print(matrix)

newdata=matrix[matrix>25]
print(newdata)