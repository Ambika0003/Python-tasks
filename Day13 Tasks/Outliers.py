import numpy as np

values = np.array([10, 12, 15, 18, 100, 14, 13]) 
print(values)

m=np.mean(values)
print("the mean of the values is:\n", m)

sd=np.std(values)
print("the standard deviation of the values is:\n", sd)

x=values[np.abs(values-m)<=2 *sd]
print(x)

