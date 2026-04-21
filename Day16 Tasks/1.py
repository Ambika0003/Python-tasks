import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# Load dataset from CSV file
df = pd.read_csv(r"C:\Users\Windows\Downloads\railway_gauges 1.csv")
 
# Display first 5 rows to understand data structure
print(df.head())
 
# Display column names
print(df.columns)
 
# Check for missing (NaN) values in each column
print(df.isnull().sum())
 
# Replace all missing values with 0
df.fillna(0, inplace=True)
 
# List of columns that should contain numeric values
gauge_cols = ['Broad Gauge', 'Metre Gauge', 'Narrow Gauge', 'Total']
 
# Convert these columns to numeric (in case they are read as strings)
# If any value cannot be converted, it becomes NaN and then replaced with 0
df[gauge_cols] = df[gauge_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
 
# Extract Year and Total columns for plotting
year = df["Year"]
total = df["Total"]
 
# Create line graph to show trend of total railway tracks over years
plt.figure(figsize=(12,6))
 
# Plot Year vs Total
plt.plot(year, total, marker='o')
 
# Rotate x-axis labels so all years are visible clearly
plt.xticks(rotation=75)
 
# Add labels and title
plt.xlabel("Year")
plt.ylabel("Total Tracks")
plt.title("Total Railway Tracks Over Years")
 
# Display the graph
plt.show()
 