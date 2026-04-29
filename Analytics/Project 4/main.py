# ==========================================================================================================
# 📊 Project Title: House Sales Data Analysis (kc_house_data.csv)
# Analyze house sales dataset using Pandas, NumPy, and Matplotlib
# ==========================================================================================================
 
 
# ==========================================================================================================
# 📦 Import Required Libraries
# ==========================================================================================================
import pandas as pd              # For data handling
import numpy as np               # For numerical operations
import matplotlib.pyplot as plt  # For visualization
 
 
# ==========================================================================================================
# 🟢 SCENARIO 1: Data Loading & Basic Cleaning
# ==========================================================================================================
# Tasks:
# 1. Load dataset using Pandas
# 2. Display first 5 rows and column names
# 3. Check missing values in bedrooms, bathrooms, sqft_living, price
# 4. Fill missing values:
#    - bedrooms → mode
#    - bathrooms → mean
#    - sqft_living → mean
#    - price → mean
# 5. Convert columns to numeric if required
# ==========================================================================================================
 
# Load dataset
df = pd.read_csv(r"C:\Users\Windows\Downloads\kc_house_data.csv")
 
# Display first 5 rows
print("First 5 rows:")
print(df.head())
print("------------------------------------------------------------")
 
# Display column names
print("Column names:")
print(df.columns)
print("------------------------------------------------------------")
 
# Check missing values
print("Missing values BEFORE cleaning:")
print(df[["bedrooms", "bathrooms", "sqft_living", "price"]].isnull().sum())
print("------------------------------------------------------------")
 
# Convert columns to numeric (invalid values become NaN)
df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")
df["bathrooms"] = pd.to_numeric(df["bathrooms"], errors="coerce")
df["sqft_living"] = pd.to_numeric(df["sqft_living"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
 
# Fill missing values
df["bedrooms"].fillna(df["bedrooms"].mode()[0], inplace=True)   # mode
df["bathrooms"].fillna(df["bathrooms"].mean(), inplace=True)    # mean
df["sqft_living"].fillna(df["sqft_living"].mean(), inplace=True) # mean
df["price"].fillna(df["price"].mean(), inplace=True)            # mean
 
# Check missing values after cleaning
print("Missing values AFTER cleaning:")
print(df[["bedrooms", "bathrooms", "sqft_living", "price"]].isnull().sum())
print("------------------------------------------------------------")
 
 
# ==========================================================================================================
# 🔵 SCENARIO 2: Line Graph + Save
# ==========================================================================================================
# Tasks:
# 1. Select id and price columns
# 2. Take first 10 rows
# 3. Convert price to NumPy array
# 4. Plot line graph (X = index, Y = price)
# 5. Add title, labels
# 6. Save graph as "house_prices_line.png"
# ==========================================================================================================
 
# Select required columns
subset = df[["id", "price"]]
 
# Take first 10 rows
subset_10 = subset.head(10)
 
# Convert price column to NumPy array
price_array = subset_10["price"].to_numpy()
 
# Create X-axis (0 to 9)
x_index = np.arange(len(price_array))
 
# Plot line graph
plt.figure()
plt.plot(x_index, price_array, marker="o")
 
# Add title and labels
plt.title("House Prices (First 10 Entries)")
plt.xlabel("Index (0-9)")
plt.ylabel("Price")
 
# Adjust layout
plt.tight_layout()
 
# Save graph
plt.savefig("house_prices_line.png")
 
# Show graph
plt.show()
 
 
# ==========================================================================================================
# 🟡 SCENARIO 3: Filtering + Bar Chart + Save
# ==========================================================================================================
# Tasks:
# 1. Filter houses where price > 1,000,000
# 2. Count number of houses per bedrooms
# 3. Select top bedroom categories
# 4. Convert to NumPy arrays
# 5. Plot bar chart
# 6. Rotate labels
# 7. Save graph as "expensive_houses_bar.png"
# ==========================================================================================================
 
# Filter expensive houses
expensive_houses = df[df["price"] > 1000000]
 
# Count houses per bedroom
bedroom_counts = expensive_houses["bedrooms"].value_counts()
 
# Select top categories (top 5)
top_bedrooms = bedroom_counts.head(5)
 
# Convert to NumPy arrays
bedrooms = top_bedrooms.index.to_numpy()
counts = top_bedrooms.values
 
# Plot bar chart
plt.figure()
plt.bar(bedrooms, counts)
 
# Add title and labels
plt.title("Expensive Houses by Bedroom Count")
plt.xlabel("Number of Bedrooms")
plt.ylabel("Number of Houses")
 
# Rotate labels for readability
plt.xticks(rotation=45)
 
# Adjust layout
plt.tight_layout()
 
# Save graph
plt.savefig("expensive_houses_bar.png")
 
# Show graph
plt.show()

 
# ==========================================================================================================
# 📊 SCENARIO 4: Pie Chart (Bedroom Distribution) + Save
# ==========================================================================================================
# Tasks:
# 1. Count number of houses by bedrooms
# 2. Select top 5 bedroom categories
# 3. Prepare labels and values
# 4. Plot a pie chart
# 5. Add percentage labels
# 6. Save graph as "bedroom_distribution.png"
# ==========================================================================================================
 
# Count number of houses for each bedroom category
bedroom_counts = df["bedrooms"].value_counts()
 
# Select top 5 bedroom categories
top_5_bedrooms = bedroom_counts.head(5)
 
# Prepare labels (bedroom numbers)
labels = top_5_bedrooms.index.to_numpy()
 
# Prepare values (counts)
values = top_5_bedrooms.values
 
# Create pie chart
plt.figure()
plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
 
# Add title
plt.title("Bedroom Distribution (Top 5 Categories)")
 
# Adjust layout
plt.tight_layout()
 
# Save graph
plt.savefig("bedroom_distribution.png")
 
# Show graph
plt.show()
 
 
# ==========================================================================================================
# 🔴 SCENARIO 5: Advanced Analysis + Multiple Graphs
# ==========================================================================================================
# Part 1: Feature Creation
# Create a new column "price_category":
# - price >= 1000000 → Luxury
# - 500000 – 999999 → Mid Range
# - < 500000 → Affordable
# ==========================================================================================================
 
df["price_category"] = np.where(
    df["price"] >= 1000000, "Luxury",
    np.where(df["price"] >= 500000, "Mid Range", "Affordable")
)
 
 
# ==========================================================================================================
# Part 2: NumPy Usage
# 1. Convert price column to NumPy array
# 2. Calculate price differences using np.diff()
# ==========================================================================================================
 
price_array = df["price"].to_numpy()
price_diff = np.diff(price_array)
 
print("Sample price differences:")
print(price_diff[:10])
print("------------------------------------------------------------")
 
 
# ==========================================================================================================
# Part 3: Visualizations
# ==========================================================================================================
 
# 📈 Line Graph
x_index = np.arange(len(price_array))
 
plt.figure()
plt.plot(x_index, price_array)
 
plt.title("Price Trend of Houses")
plt.xlabel("Index")
plt.ylabel("Price")
 
plt.tight_layout()
plt.savefig("price_trend.png")
plt.show()
 
 
# 📊 Stacked Bar Chart
category_counts = df.pivot_table(
    index="bedrooms",
    columns="price_category",
    aggfunc="size",
    fill_value=0
)
 
category_counts.plot(kind="bar", stacked=True)
 
plt.title("Price Category Distribution by Bedrooms")
plt.xlabel("Bedrooms")
plt.ylabel("Number of Houses")
 
plt.xticks(rotation=45)
plt.tight_layout()
 
plt.savefig("price_category_stacked.png")
plt.show()
 
 
# 📊 Histogram
plt.figure()
plt.hist(df["price"], bins=20)
 
plt.title("Price Distribution of Houses")
plt.xlabel("Price")
plt.ylabel("Frequency")
 
plt.tight_layout()
plt.savefig("price_histogram.png")
plt.show()
 
 
# ==========================================================================================================
# Part 5: Insights
# ==========================================================================================================
 
expensive_houses = df[df["price"] > 1000000]
bedroom_expensive = expensive_houses["bedrooms"].value_counts()
 
print("Bedroom category with most expensive houses:")
print(bedroom_expensive.idxmax())
print("------------------------------------------------------------")
 
common_category = df["price_category"].value_counts().idxmax()
 
print("Most common price category:")
print(common_category)
print("------------------------------------------------------------")
 
print("Price distribution insight:")
 
mean_price = df["price"].mean()
median_price = df["price"].median()
 
if mean_price > median_price:
    print("Right-skewed distribution (more high-value outliers)")
elif mean_price < median_price:
    print("Left-skewed distribution")
else:
    print("Approximately normal distribution")
 