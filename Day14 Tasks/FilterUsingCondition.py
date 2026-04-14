import numpy as np
import pandas as pd

arr = np.array([10, 25, 30, 15, 40])
arr=pd.Series([10, 25, 30, 15, 40])
print(arr)

filtered_array=arr[arr>20]
print("the values greater than 20 are :\n",filtered_array)