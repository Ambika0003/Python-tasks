import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Load CSV file
df=pd.read_csv(r"C:\Users\Windows\Downloads\railway_gauges 1.csv")

#Display the first 5 rows and column names. 
print("First 5 Rows:")
print(df.head())

print("\nFirst 5 columns: ")
print(df.columns)

#Find which year had the maximum installations
max=df.iloc[[df["Total"].idxmax()]]
print(max)

#plot data using bar chart
df=df.drop('Total',axis=1)
ax=df.plot(x="Year",kind="bar")
plt.xticks(rotation=70)
plt.xlabel('Year')
plt.ylabel('Total')
plt.title('Gauges:Number of railway tracks installed per year')
plt.show()