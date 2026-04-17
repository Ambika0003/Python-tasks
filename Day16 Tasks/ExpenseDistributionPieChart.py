import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Monthly expenses
expenses = np.array([500, 300, 200]) 
labels = ["Food", "Rent", "Travel"] 

#Create a pie chart
plt.pie(expenses,labels=labels, autopct='%1.1f%%',   
shadow=True, startangle=90)   
plt.axis('equal') 
plt.title('Pie Chart')

#Show percentage distribution
plt.show()