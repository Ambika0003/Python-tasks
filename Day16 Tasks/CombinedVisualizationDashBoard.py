import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
sales = np.array([100, 200, 150, 300]) 
products = ["A", "B", "C", "D"] 

#Create DataFrame
df=pd.DataFrame({"Sales":sales,"Product":products})
print(df)

#Plot:
fig,axes=plt.subplots(1,3,figsize=(9,3))

#line graph
axes[0].plot(df["Product"],df["Sales"],color='r')
axes[0].set_title('Line graph (trend)')
axes[0].set_xlabel('Product')
axes[0].set_ylabel('Sales')

#bar graph
axes[1].bar(df["Product"],df["Sales"],color='y')
axes[1].set_title('Bar chart (comparison) ')
axes[1].set_xlabel('Product')
axes[1].set_ylabel('Sales')

#pie chart
axes[2].pie(df["Sales"],labels=df["Product"],autopct='%1.1f%%',shadow=True,startangle=90)
axes[2].set_title('Pie chart (distribution)')
plt.legend()
plt.tight_layout()
plt.show()

