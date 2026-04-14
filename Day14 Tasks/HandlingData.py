import numpy as np
import pandas as pd

arr = np.array([10, np.nan, 30, np.nan, 50])
arr=pd.Series(arr)
print(arr)

arr1=np.mean(arr)
print("the mean of the series is:\n",arr1)

u_series=arr.fillna(arr1)
print("the updates series is:\n",u_series)
