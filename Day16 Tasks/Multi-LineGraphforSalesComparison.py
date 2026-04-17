import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario:
data = { 
"Month": ["Jan", "Feb", "Mar"], 
"Store_A": [100, 150, 200], 
"Store_B": [90, 140, 210] 
} 

#Create DataFrame 
df=pd.DataFrame(data)
print(df)

# Plot two line graphs on same plot 
plt.figure(figsize=(9,3))  
plt.subplot(121)   
plt.plot(df['Month'],df['Store_A'],label="Store_A")
plt.title('Store A')
#Add legend 
plt.legend()

plt.subplot(122)
plt.plot(df['Month'],df['Store_B'],label="Store_B")
plt.title('Store B')
plt.legend()

plt.suptitle('Sales Comparison')
plt.show()