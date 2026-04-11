import numpy as np

arr=np.array([10,20,30,40])
x=arr.copy()
arr[1]=25
print(arr)
print(x)

y=arr.view()
arr[2]=7
print(arr)
print(y)
