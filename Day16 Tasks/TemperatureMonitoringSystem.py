import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario:
temps = np.array([28, 30, 32, 35, 33, 31, 29]) 
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

#Create DataFrame
df=pd.DataFrame({"Temp":temps,"Day":days})
print(df)

#plot
fig,axes=plt.subplots(1,5,figsize=(20,5))

#Line graph → daily temperature trend
axes[0].plot(df["Day"],df["Temp"],color='r')
axes[0].set_title('Line graph')
axes[0].set_xlabel('Day')
axes[0].set_ylabel('Temp')

#Bar chart → day-wise temperature
axes[1].bar(df["Day"],df["Temp"],color='y')
axes[1].set_title('Bar chart')
axes[1].set_xlabel('Day')
axes[1].set_ylabel('Temp')

#Categorize into high and low temps
high_temp=np.sum(temps >30)
low_temp=np.sum(temps <= 30)

print("the high temps are :",high_temp)
print("the low temps are:",low_temp)

#prepare data for pie chart
labels=["High","Low"]
counts=[high_temp,low_temp]
colors=['m','g']

#Pie chart → proportion of high (>30) vs low temp
axes[2].pie(counts,labels=labels,colors=colors, autopct='%1.1f%%',   
shadow=True, startangle=90) 
axes[2].set_title('Pie Chart')

#Histogram → temperature frequency
axes[3].hist(df["Temp"],bins=5,color='c')
axes[3].set_title('Histogram')
axes[3].set_xlabel('Temp')
axes[3].set_ylabel('Frequency')

#Scatter plot → day index vs temperature 
axes[4].scatter(df.index, df["Temp"],color='b')
axes[4].set_title('Scatter Plot')
axes[4].set_xlabel('Index')
axes[4].set_ylabel('Temp')

plt.tight_layout()
plt.show()

