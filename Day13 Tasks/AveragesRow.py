import numpy as np

data = np.arange(1, 13)
print(data)

new_data=data.reshape(3,4)
print(" 3×4 matrix is :\n", new_data)

avg=np.mean(new_data,axis=1)
print("the average of each row is :\n", avg)