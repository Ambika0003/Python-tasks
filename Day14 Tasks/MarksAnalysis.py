import numpy as np
import pandas as pd

arr = np.array([ [80, 90], [70, 60], [85, 95]]) 
arr1=pd.DataFrame(arr, columns=["Math", "Science"])
print(arr1)

print("add new column")
arr1['Total']=arr1['Math']+arr1['Science']
print(arr1)

h_value=arr1.loc[arr1["Total"].idxmax()]
print("he highest value of total is:\n",h_value)