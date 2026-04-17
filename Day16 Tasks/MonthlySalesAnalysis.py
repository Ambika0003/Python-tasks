import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
sales = np.array([100, 150, 200, 180, 220, 300]) 
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] 

# Create DataFrame
df=pd.DataFrame({"Sale":sales,"Month":months})
print(df)

#plot
fig,axes=plt.subplots(1,5,figsize=(20,5))

#Line graph → sales trend 
axes[0].plot(df["Month"],df["Sale"],color='r')
axes[0].set_title('Line graph')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Sale')

#Bar chart → month-wise comparison 
axes[1].bar(df["Month"],df["Sale"],color='y')
axes[1].set_title('Bar chart')
axes[1].set_xlabel('Month')
axes[1].set_ylabel('Sale')

# Pie chart → contribution of each month
axes[2].pie(df["Sale"],labels=df["Month"], autopct='%1.1f%%',   
shadow=True, startangle=90) 
axes[2].set_title('Pie Chart')

#Histogram → frequency of sales values
axes[3].hist(df["Sale"],bins=5,color='g')
axes[3].set_title('Histogram')
axes[3].set_xlabel('Sale')
axes[3].set_ylabel('Frequency')

#Scatter plot → month index vs sale
axes[4].scatter(df.index, df["Sale"],color='b')
axes[4].set_title('Scatter Plot')
axes[4].set_xlabel('Index')
axes[4].set_ylabel('Sale')

plt.tight_layout()
plt.show()

