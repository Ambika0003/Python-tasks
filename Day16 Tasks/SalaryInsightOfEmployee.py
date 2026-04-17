import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
salaries = np.array([25000, 30000, 28000, 40000, 50000, 35000]) 
departments = ["HR", "IT", "HR", "IT", "Sales", "Sales"] 

#Convert into DataFrame
df=pd.DataFrame({"Salary":salaries,"Roles":departments})
print(df)

#plot
fig,axes=plt.subplots(1,5,figsize=(20,5))

#Line graph → salary trend 
axes[0].plot(df["Roles"],df["Salary"],color='r')
axes[0].set_title('Line graph')
axes[0].set_xlabel('Roles')
axes[0].set_ylabel('Salary')

#Bar chart → department-wise salary comparison 
axes[1].bar(df["Roles"],df["Salary"],color='y')
axes[1].set_title('Bar chart')
axes[1].set_xlabel('Roles')
axes[1].set_ylabel('Salary')

#Pie chart → department distribution 
axes[2].pie(df["Salary"],labels=df["Roles"], autopct='%1.1f%%',   
shadow=True, startangle=90) 
axes[2].set_title('Pie Chart')

#Histogram → salary distribution 
axes[3].hist(df["Salary"],bins=5,color='g')
axes[3].set_title('Histogram')
axes[3].set_xlabel('Salary')
axes[3].set_ylabel('Frequency')

#Scatter plot → index vs salary
axes[4].scatter(df.index, df["Salary"],color='b')
axes[4].set_title('Scatter Plot')
axes[4].set_xlabel('Index')
axes[4].set_ylabel('Salary')

plt.tight_layout()
plt.show()