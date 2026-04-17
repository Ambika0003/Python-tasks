import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Daily temperatures:
temps = np.array([28, 30, 32, 31, 29])

#Convert into Pandas Series
df=pd.Series(temps)
print(df)

#Plot a line graph 
plt.plot([28,30,32,31,29])
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

#Add title and grid 
plt.title('Line Graph')
plt.grid(True)
plt.show()