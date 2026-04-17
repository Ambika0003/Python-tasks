import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

products = ["Pen", "Book", "Pencil"] 
sales = np.array([50, 80, 40]) 

#Create DataFrame 
df=pd.DataFrame({"Product":products,"Sale":sales})
print(df)

#Plot bar chart 
plt.bar(products,sales)

# Add labels and title 
plt.xlabel('Products')
plt.ylabel('Sales')
plt.title('Bar Graph')
plt.show()