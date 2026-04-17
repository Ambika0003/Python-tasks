import numpy as np
import pandas as pd
from matplotlib import pyplot as plt  

#A shop records monthly sales:
sales = np.array([100, 150, 200, 250, 300]) 
months = ["Jan", "Feb", "Mar", "Apr", "May"] 

#Convert data into a Pandas DataFrame 
df=pd.DataFrame({"Sale":sales,"Month":months})
print(df)

#Plot a line graph 
plt.plot(months,sales)
plt.title('Line Graph')

#Label X-axis as months and Y-axis as sales 
plt.xlabel('Months')
plt.ylabel('Sales')
plt.show()
