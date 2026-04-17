import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
sales = np.array([200, 300, 250, 400, 350]) 
profit = np.array([50, 70, 60, 90, 80]) 
products = ["A", "B", "C", "D", "E"] 

#Create DataFrame
df=pd.DataFrame({"Sale":sales,"Extra":profit,"Product":products})
print(df)

#plot
fig,axes=plt.subplots(1,5,figsize=(20,5))

#Line graph → sales trend 
axes[0].plot(df["Product"],df["Sale"],color='r')
axes[0].set_title('Line graph')
axes[0].set_xlabel('Product')
axes[0].set_ylabel('Sale')

#Bar chart → product vs sales 
axes[1].bar(df["Product"],df["Sale"],color='y')
axes[1].set_title('Bar chart')
axes[1].set_xlabel('Product')
axes[1].set_ylabel('Sale')

#Pie chart → sales contribution
axes[2].pie(df["Sale"],labels=df["Product"], autopct='%1.1f%%',   
shadow=True, startangle=90) 
axes[2].set_title('Pie Chart')

#Histogram → profit distribution
axes[3].hist(df["Extra"],bins=5,color='g')
axes[3].set_title('Histogram')
axes[3].set_xlabel('Extra')
axes[3].set_ylabel('Frequency')

#Scatter plot → sales vs profit
axes[4].scatter(df.Extra, df["Sale"],color='b')
axes[4].set_title('Scatter Plot')
axes[4].set_xlabel('Extra')
axes[4].set_ylabel('Sale')

plt.tight_layout()
plt.show()