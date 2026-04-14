import numpy as np
import pandas as pd

arr = np.array([ 
[100, 200], 
[150, 250], 
[80, 120], 
[300, 400] 
]) 
arr=pd.DataFrame(arr,columns=["Sales","Profit"])
print(arr)
filtred_array=arr[arr["Sales"]>100]
print(filtred_array)

avg=filtred_array["Profit"].mean()
print("average Profit of filtered rows is:\n",avg)