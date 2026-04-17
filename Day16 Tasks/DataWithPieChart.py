import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
scores = np.array([40, 60, 80, 30, 90]) 
print(scores)

#Categorize into pass and fail
pass_count=np.sum(scores > 50)
fail_count=np.sum(scores <= 50)

#Count using NumPy/Pandas 
print("the passing students are :\n",pass_count)
print("the failed students are :\n",fail_count)

#prepare data for pie chart
labels=["Pass","Fail"]
counts=[pass_count,fail_count]
colors=['red','green']

#Plot pie chart for Pass vs Fail 
plt.pie(counts,labels=labels,colors=colors, autopct='%1.1f%%',   
shadow=True, startangle=90) 
plt.title('Pie Chart')
plt.legend()
plt.show()
