import numpy as np
import pandas as pd
from matplotlib import pyplot as plt  

#Marks of students:
names = ["A", "B", "C", "D"] 
marks = np.array([70, 85, 60, 90]) 

#Create a DataFrame 
df=pd.DataFrame({"Name":names, "Mark":marks})
print(df)

#Plot a bar graph
plt.bar(names,marks)
plt.title('Marks of student')

#Show student names on X-axis 
plt.xlabel('Names')
plt.ylabel('Marks')
plt.show()