import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario: 
marks = np.array([45, 80, 60, 30, 90]) 
names = ["A", "B", "C", "D", "E"]

#Convert to DataFrame 
df=pd.DataFrame({"Name":names,"Mark":marks})
print(df)

#Filter students with marks > 50 
filtered_array=df[df["Mark"]>50]
print(filtered_array)

#Plot bar chart only for filtered students 
plt.bar(filtered_array["Name"],filtered_array["Mark"])
plt.xlabel('Names')
plt.ylabel('Marks')
plt.title('Bar Chart')
plt.show()
