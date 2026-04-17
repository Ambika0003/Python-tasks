import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#A school records marks of students in one subject: 
marks = np.array([45, 67, 89, 56, 72, 91, 38]) 
students = ["A", "B", "C", "D", "E", "F", "G"] 

#Convert to Pandas DataFrame
df=pd.DataFrame({"Marks":marks,"Student":students})
print(df)

#plot
fig,axes=plt.subplots(1,5,figsize=(20,5))

#Line graph → trend of marks
axes[0].plot(df["Student"],df["Marks"],color='r')
axes[0].set_title('Line graph')
axes[0].set_xlabel('Student')
axes[0].set_ylabel('Marks')

#Bar chart → student vs marks 
axes[1].bar(df["Student"],df["Marks"],color='y')
axes[1].set_title('Bar chart')
axes[1].set_xlabel('Student')
axes[1].set_ylabel('Marks')

#Categorize into pass and fail
pass_count=np.sum(marks > 50)
fail_count=np.sum(marks <= 50)

#Count using NumPy/Pandas 
print("the passing students are :\n",pass_count)
print("the failed students are :\n",fail_count)

#prepare data for pie chart
labels=["Pass","Fail"]
counts=[pass_count,fail_count]
colors=['c','m']

#Pie chart → Pass (>50) vs Fail 
axes[2].pie(counts,labels=labels,colors=colors, autopct='%1.1f%%',   
shadow=True, startangle=90) 
axes[2].set_title('Pie Chart')

#Histogram → distribution of marks 
axes[3].hist(df["Marks"],bins=5,color='g')
axes[3].set_title('Histogram')
axes[3].set_xlabel('Student')
axes[3].set_ylabel('Frequency')

#Scatter plot → index vs marks 
axes[4].scatter(df.index, df["Marks"],color='b')
axes[4].set_title('Scatter Plot')
axes[4].set_xlabel('Index')
axes[4].set_ylabel('Marks')

plt.tight_layout()
plt.show()


