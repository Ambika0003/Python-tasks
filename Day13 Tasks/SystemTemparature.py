import numpy as np

temps = np.array([28, 32, 35, 31, 29, 40, 38])
print(temps)

new_temp=temps[temps>30]
print(new_temp)

indices=np.where(temps>30)
print(indices)
