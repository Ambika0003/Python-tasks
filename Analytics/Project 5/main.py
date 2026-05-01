# ============================================================
# 📊 Project Title: Car Data Analysis
# Analyze Car dataset using NumPy, Pandas, Matplotlib
# ============================================================
 
# ============================================================
# 📦 1. Import Required Libraries
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# ============================================================
#    Scenario 1: Data Loading & Basic Cleaning
# ============================================================
# Understand the dataset structure and prepare it for analysis.
#    Tasks:
# ● Load the dataset using Pandas.
df=pd.read_csv(r"C:\Users\Windows\Downloads\cardata.csv")
 
# ● Display:
# ○ First 5 rows
print("-------------------------------------------------------------")
print("First 5 rows:")
print(df.head())
print("-------------------------------------------------------------")
 
# ○ Last 5 rows
print("\n-------------------------------------------------------------")
print("last 5 rows:")
print(df.tail())
print("-------------------------------------------------------------")
 
# ○ Column names
print("\n-------------------------------------------------------------")
print("Column names:")
print(df.columns)
print("-------------------------------------------------------------")
 
# ○ Shape of dataset
print("-------------------------------------------------------------")
print("Shape of dataset:")
print(df.shape)
print("-------------------------------------------------------------")
 
# ● Check data types of all columns.
print("-------------------------------------------------------------")
print("data types of all columns:")
print(df.dtypes)
print("-------------------------------------------------------------")
 
# ● Check for missing values in:
# ○ Selling_Price
# ○ Present_Price
# ○ Kms_Driven
# ○ Fuel_Type
print(df[["Selling_Price","Present_Price","Kms_Driven","Fuel_Type"]].isnull().sum())
 
# ● Fill missing values:
# ○ Selling_Price → mean
# ○ Present_Price → mean
# ○ Kms_Driven → mean
# ○ Fuel_Type → mode
df["Selling_Price"]=df["Selling_Price"].fillna(df["Selling_Price"].mean(),inplace=True)
df["Present_Price"]=df["Present_Price"].fillna(df["Present_Price"].mean(),inplace=True)
df["Kms_Driven"]=df["Kms_Driven"].fillna(df["Kms_Driven"].mean(),inplace=True)
df["Fuel_Type"]=df["Fuel_Type"].fillna(df["Fuel_Type"].mode()[0],inplace=True)
 
# ● Convert numeric columns to proper numeric type if required:
# ○ Selling_Price
# ○ Present_Price
# ○ Kms_Driven
# ○ Year
df["Selling_Price"]=pd.to_numeric(df["Selling_Price"], errors="coerce")
df["Present_Price"]=pd.to_numeric(df["Present_Price"], errors="coerce")
df["Kms_Driven"]=pd.to_numeric(df["Kms_Driven"], errors="coerce")
df["Year"]=pd.to_numeric(df["Year"], errors="coerce")
 
# ● Convert Selling_Price and Kms_Driven into NumPy arrays.
# ● Use NumPy to calculate:
# ○ minimum selling price
# ○ maximum selling price
# ○ average selling price
Selling_Price_arr=df["Selling_Price"].to_numpy()
Kms_Driven_arr=df["Kms_Driven"].to_numpy()
min_selling_price=Selling_Price_arr.min()
max_selling_price=Selling_Price_arr.max()
avg_selling_price=Selling_Price_arr.mean()
print("-------------------------------------------------------------")
 
# =====================================================================
# 🚗 SCENARIO 2: Selling Price Trend (Line Graph)
# =====================================================================
# See how selling prices vary for a small sample of cars.
# Tasks:
# 2.1: Select Car_Name and Selling_Price columns
data = df[["Car_Name", "Selling_Price"]]
#print("Selected Columns:\n", data.head())
 
# 2.2: Take first 10 rows using Pandas
data_sample = data.head(10)
#print("First 10 rows:\n", data_sample)
 
# 2.3: Convert Selling_Price into NumPy array
price_array = np.array(data_sample["Selling_Price"])
print("Selling Price NumPy Array:\n", price_array)
 
# 2.4 Plot a line graph using Matplotlib:
# X-axis → row index (0–9)
# Y-axis → Selling Price
x = np.arange(0, 10) #X-axis values: [0 1 2 3 4 5 6 7 8 9]
 
#plot line Graph
plt.figure(figsize=(12,8))
plt.plot(x, price_array, marker='o')
plt.title("Selling Price Trend (First 10 Cars)")
plt.xlabel("Car Index (0–9)")
plt.ylabel("Selling Price")
plt.savefig("selling_price_trend_sample.png")
plt.tight_layout()
plt.show()
 
# =====================================================================
# 🚗 SCENARIO 3: Expensive Cars Analysis (Filtering + Bar)
# =====================================================================
# Find which fuel types are most common among expensive cars.
# �� Tasks:
# 3.1: Filter cars where Selling_Price > 10
expensive_cars = df[df["Selling_Price"] > 10]
# print("Filtered Expensive Cars:\n", expensive_cars.head())
 
# 3.2: Group the filtered data by Fuel_Type
fuel_group = expensive_cars.groupby("Fuel_Type")
 
# 3.3: Count number of cars in each fuel type
fuel_counts = fuel_group.size()
# print("Count of Expensive Cars by Fuel Type:\n", fuel_counts)
 
# 3.4: Convert fuel type labels
# counts into NumPy arrays
fuel_labels = np.array(fuel_counts.index)
fuel_values = np.array(fuel_counts.values)
# print("Fuel Type Labels:", fuel_labels)
#print("Counts:", fuel_values)
 
# 3.5: Plot a bar chart
# X-axis → Fuel Type
# Y-axis → Count of expensive cars
 
plt.figure(figsize=(12,8))
plt.bar(fuel_labels, fuel_values)
plt.title("Expensive Cars by Fuel Type (Selling Price > 10)")
plt.xlabel("Fuel Type")
plt.ylabel("Number of Expensive Cars")
plt.savefig("expensive_cars_fuel_type.png")
plt.tight_layout()
plt.show()
 
# =====================================================================
# 🚗 SCENARIO 4: Fuel Type Distribution (Pie Chart)
# =====================================================================
# Understand the overall distribution of cars by fuel type.
# �� Tasks:
# 4.1: Count the number of cars in each Fuel_Type
fuel_counts = df["Fuel_Type"].value_counts()
# print("Fuel Type Counts:\n", fuel_counts)
 
# 4.2: Select all categories (or top categories if needed)
labels = fuel_counts.index
values = fuel_counts.values
# print("Labels:", labels)
# print("Values:", values)
 
# 4.3: Convert values into a NumPy array
values_array = np.array(values)
# print("NumPy Array of Values:", values_array)
 
# 4.4: Plot a pie chart
plt.pie(values_array, labels=labels, autopct='%1.1f%%')
plt.title("Fuel Type Distribution of Cars")
plt.savefig("fuel_type_distribution.png")
plt.show()
 
# ==========================================================================================================
# 📊 SCENARIO 5: Present Price vs Selling Price (Scatter Plot)
# Check whether cars with higher present price also have higher selling price.
# ==========================================================================================================
# 👉 Tasks:
# ● Select:
#   ○ Present_Price
#   ○ Selling_Price
# ● Remove missing values if any.
# ● Take a smaller sample (for example first 50 or 100 rows) using Pandas.
# ● Convert both columns into NumPy arrays.
# ● Plot a scatter plot using Matplotlib:
#   ○ X-axis → Present_Price
#   ○ Y-axis → Selling_Price
# ● Add:
#   ○ title
#   ○ x-label
#   ○ y-label
# ● Observe whether there is a positive relationship.
# ● Save the graph.
 
# Select required columns
price_data = df[["Present_Price", "Selling_Price"]]
 
# Remove missing values
price_data = price_data.dropna()
 
# Take a smaller sample (first 100 rows)
price_sample = price_data.head(100)
 
# Convert to NumPy arrays
present_price = price_sample["Present_Price"].to_numpy()
selling_price = price_sample["Selling_Price"].to_numpy()
 
# Plot scatter plot
plt.figure(figsize=(12,6))
plt.scatter(present_price, selling_price)
plt.title("Present Price vs Selling Price")
plt.xlabel("Present Price")
plt.ylabel("Selling Price")
plt.savefig("present_vs_selling_price.png")
plt.show()
 
# ==========================================================================================================
# 📊 SCENARIO 6: Car Age Category Analysis + Bar Chart
# Create a new feature using year and compare car categories.
# ==========================================================================================================
# 👉 Tasks:
# ● Create a new column using Pandas:
#   Car Age Category
# ● Year >= 2015 → "New"
# ● 2010 to 2014 → "Medium"
# ● < 2010 → "Old"
# ● Count number of cars in each:
#   ○ Car Age Category
# ● Convert category names and counts into NumPy arrays.
# ● Plot a bar chart using Matplotlib:
#   ○ X-axis → Car Age Category
#   ○ Y-axis → Count
# ● Add title and labels.
# ● Save the graph.
 
# Create Car Age Category column
def categorize_car(year):
    if year >= 2015:
        return "New"
    elif 2010 <= year <= 2014:
        return "Medium"
    else:
        return "Old"
 
df["Car_Age_Category"] = df["Year"].apply(categorize_car)
 
# Count number of cars in each category
category_counts = df["Car_Age_Category"].value_counts()
 
# Convert to NumPy arrays
categories = category_counts.index.to_numpy()
counts = category_counts.values
 
# Plot bar chart
plt.figure(figsize=(12,6))
plt.bar(categories, counts)
plt.title("Car Age Category Distribution")
plt.xlabel("Car Age Category")
plt.ylabel("Number of Cars")
plt.savefig("car_age_category_bar_chart.png")
plt.tight_layout()
plt.show()
 
# ============================================================
#   Scenario 7: Kms Driven Distribution (Histogram)
# ============================================================
# Understand how the cars are distributed based on kilometers driven.
#   Tasks:
#● Select:
#○ Kms_Driven
#● Convert it into a NumPy array.
#● Plot a histogram using Matplotlib:
#○ X-axis → Kms Driven
#○ Y-axis → Frequency
#● Choose suitable number of bins.
#● Add:
#○ title
#○ x-label
#○ y-label
#● Save the graph.
#● Observe whether most cars have lower or higher mileage.
 
# 7.1: Select Kms_Driven column
kms = df["Kms_Driven"]
 
# 7.2: Convert it into a NumPy array
kms_array = np.array(kms)
 
# 7.3: Plot histogram
plt.figure(figsize=(12,8))
plt.hist(kms_array, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Kms Driven")
plt.xlabel("Kms Driven")
plt.ylabel("Frequency")
plt.savefig("kms_driven_histogram.png")
plt.tight_layout()
plt.show()
 
# ============================================================
#    Scenario 8: Transmission-wise Selling Price Comparison
# ============================================================
#Compare average selling price for manual vs automatic cars.
#   Tasks:
#● Group data by:
#○ Transmission
#● Calculate:
#○ average Selling_Price
#● Convert transmission labels and average prices into NumPy arrays.
#● Plot a bar chart using Matplotlib:
#○ X-axis → Transmission
#○ Y-axis → Average Selling Price
#● Add title and labels.
#● Save the graph.
 
# 8.1: Group data by Transmission
transmission_group = df.groupby("Transmission")["Selling_Price"].mean()
#print("Average Selling Price by Transmission:\n", transmission_group)
 
# 8.3: Convert to NumPy arrays
transmission_labels = np.array(transmission_group.index)
avg_prices = np.array(transmission_group.values)
 
# 8.4: Plot bar chart
plt.figure(figsize=(6,4))
plt.bar(transmission_labels, avg_prices)
plt.title("Average Selling Price by Transmission")
plt.xlabel("Transmission Type")
plt.ylabel("Average Selling Price")
plt.savefig("transmission_price_comparison.png")
plt.tight_layout()
plt.show()
 
# ============================================================
#   Scenario 9: Seller Type Analysis
# ============================================================
# Compare how many cars are sold by dealers and individuals.
#   Tasks:
#● Count number of cars by:
#○ Seller_Type
#● Convert results into NumPy arrays.
#● Plot a bar chart or pie chart using Matplotlib.
#● Add labels and title.
#● Save the graph.
#● Identify which seller type is more common.
 
# 9.1: Count number of cars by Seller_Type
seller_counts = df["Seller_Type"].value_counts()
 
# 9.2: Convert results into NumPy arrays
seller_labels = np.array(seller_counts.index)
seller_values = np.array(seller_counts.values)
 
# 9.3: Plot bar chart
plt.figure(figsize=(6,4))
plt.bar(seller_labels, seller_values)
plt.title("Seller Type Distribution")
plt.xlabel("Seller Type")
plt.ylabel("Number of Cars")
plt.savefig("seller_type_distribution.png")
plt.show()
 
# ============================================================
#   Scenario 10: Advanced Analysis + Multiple Graphs
# ============================================================
#Perform deeper analysis using Pandas, NumPy, and Matplotlib.
#   Part 1: Feature Creation
# Create a new column:
# Price Difference
# ● Price Difference = Present_Price - Selling_Price
#This shows how much value the car has depreciated.
 
df["Price_Difference"] = df["Present_Price"] - df["Selling_Price"]
#print("Price Difference :" ,df["Price_Difference"])
 
# ============================================================
#   Part 2: NumPy Usage
# Convert Selling_Price into a NumPy array.
selling_price_array = np.array(df["Selling_Price"])
 
# Use NumPy to calculate price changes between consecutive rows using:
# np.diff()
price_changes = np.diff(selling_price_array)
 
#● Convert Price Difference column into a NumPy array.
price_diff_array = np.array(df["Price_Difference"])
 
#● Find:
#○ average depreciation
#○ maximum depreciation
#○ minimum depreciation
avg_depreciation = np.mean(price_diff_array)
max_depreciation = np.max(price_diff_array)
min_depreciation = np.min(price_diff_array)
 
# Print results
print("Average Depreciation:", avg_depreciation)
print("Maximum Depreciation:", max_depreciation)
print("Minimum Depreciation:", min_depreciation)
 
# ============================================================
#   Part 3: Visualizations
#   Line Graph
# Plot Selling_Price trend for all cars.
 
# Line Graph
plt.figure(figsize=(8,5))
plt.plot(selling_price_array)
plt.title("Selling Price Trend")
plt.xlabel("Car Index")
plt.ylabel("Selling Price")
plt.savefig("selling_price_trend.png")
plt.tight_layout()
plt.show()
 
#   Bar Chart
# Show average Selling_Price by Fuel_Type.
fuel_group = df.groupby("Fuel_Type")["Selling_Price"].mean()
 
# Convert to NumPy arrays
fuel_labels = np.array(fuel_group.index)
fuel_prices = np.array(fuel_group.values)
 
# Plot bar chart
plt.figure(figsize=(6,4))
plt.bar(fuel_labels, fuel_prices)
plt.title("Average Selling Price by Fuel Type")
plt.xlabel("Fuel Type")
plt.ylabel("Average Selling Price")
plt.savefig("fuel_type_price.png")
plt.tight_layout()
plt.show()
 
#  Histogram
# Plot distribution of Selling_Price.
plt.figure(figsize=(8,5))
plt.hist(selling_price_array, bins=15, edgecolor='black')
plt.title("Selling Price Distribution")
plt.xlabel("Selling Price")
plt.ylabel("Frequency")
plt.savefig("selling_price_histogram.png")
plt.show()
 
# ============================================================
#    Part 4: Insights
 
# Which fuel type has the highest average selling price?
# Ans : Diesel fuel has the highest average selling price
print("Fuel type with highest avg price:", fuel_group.idxmax())
 
# Which transmission type has higher average selling price?
print("Insight: Transmission with highest avg price:", df.groupby("Transmission")["Selling_Price"].mean().idxmax())
# Ans: Automatic transmission has higher average selling price
 
# Are most cars concentrated in lower selling prices or higher selling prices?
# Ans: Most cars are in lower price range observed in histogram.
 
# Do older cars tend to have lower selling prices?
# Ans :yes, Older cars tend to have lower selling prices.
 
 