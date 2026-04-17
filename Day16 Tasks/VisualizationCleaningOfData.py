import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario
data = np.array([100, np.nan, 200, 150, np.nan, 300])

#Convert to Pandas Series 
df=pd.Series(data)
print(df)

#mean of the data 
avg=np.mean(df)
print("the mean of the data is:\n",avg)

#Replace NaN with mean 
arr1=df.fillna(avg)
print("the updated series is:\n",arr1)

#plot
fig,axes=plt.subplots(1,2,figsize=(9,3))

#Line graph of cleaned data
axes[0].plot(arr1,marker='*',color='m')
axes[0].set_title('Line graph of cleaned data')
axes[0].set_xlabel('Index')
axes[0].set_ylabel('Value')

#Bar chart of values > average
new_arr=arr1[arr1>avg]
axes[1].bar(new_arr.index,new_arr.values,color='r')
axes[1].set_title('Bar chart (values > average)')
axes[1].set_xlabel('Index')
axes[1].set_ylabel('Value')

plt.tight_layout()
plt.show()

