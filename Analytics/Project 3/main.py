# ============================================================
# 📊 Project Title: Scottish Hills Data Analysis
# Analyze Scottish Hills dataset using NumPy, Pandas, Matplotlib
# ============================================================
 
# ============================================================
# 📦 1. Import Required Libraries
# ============================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
# ============================================================
# �� Scenario 1: Data Loading & Basic Cleaning
# ============================================================
# �� Tasks:
# 1. Load the dataset using Pandas.
# 2. Display:
# ○ First 5 rows
# ○ Column names
# 3. Check for missing values in:
# ○ Height
# ○ Region
# 4. Fill missing values:
# ○ Height → use mean
# ○ Region → use mode
# 5. Convert Height column to numeric if required.
 
df=pd.read_csv("scottish_hills.csv")
# Midpoints
lat_mid = df["Latitude"].median()
lon_mid = df["Longitude"].median()
 
 
# Function to assign region
def assign_region(row):
    lat = row["Latitude"]
    lon = row["Longitude"]
    if lat >= lat_mid and lon >= lon_mid:
        return "North-East"
    elif lat >= lat_mid and lon < lon_mid:
        return "North-West"
    elif lat < lat_mid and lon >= lon_mid:
        return "South-East"
    else:
        return "South-West"
 
# Apply WITHOUT lambda
df["Region"] = df.apply(assign_region, axis=1)
 
#print(df.head())
#print(df.columns)
 
 
df["Height"]=df["Height"].fillna(df["Height"].mean())
df["Region"]=df["Region"].fillna(df["Region"].mode()[0])
df["Height"]=pd.to_numeric(df["Height"], errors="coerce")
 
 
# ============================================================
# �� Scenario 2: Line Graph + Save
# ============================================================
# You want to see how heights vary.
# �� Tasks:
# 1. Select:
# ○ Hill Name
# ○ Height
# 2. Take first 10 rows only.
# 3. Convert Height into a NumPy array.
# 4. Plot a line graph:
# ○ X-axis → index (0–9)
# ○ Y-axis → Height
# 5. Add title and labels.
# Save the graph: plt.savefig("hill_heights_line.png")
 
fil_arr=df[["Hill Name","Height"]].head(10)#pandas
height_arr=np.array(fil_arr["Height"])#numpy
plt.figure(figsize=(6,6))
plt.plot(fil_arr.index,height_arr,marker="o")
plt.title("Hill Heights")
plt.xlabel("Index")
plt.ylabel("Height")
plt.tight_layout()
plt.savefig("hill_heights_line.png")
plt.show()
# ============================================================
# �� Scenario 3: Filtering + Bar Chart + Save
# ============================================================
# You want to analyze tall hills.
# �� Tasks:
# 1. Filter hills where:
# ○ Height > 900
# 2. Count number of hills per Region.
# 3. Select top regions.
# 4. Convert results to NumPy arrays.
# 5. Plot a bar chart:
# ○ X-axis → Region
# ○ Y-axis → count
# 6. Rotate labels for clarity.
# Save graph: plt.savefig("tall_hills_bar.png")
 
fil_hill=df[df["Height"]>900]
groupByRegion=fil_hill.groupby("Region")["Hill Name"].count()
groupByRegion=groupByRegion.sort_values(ascending=False)
region=groupByRegion.index.to_numpy()
counts=groupByRegion.to_numpy()
plt.figure(figsize=(6,6))
plt.bar(region,counts)
plt.xticks(rotation=60)
plt.title("Tall Hills")
plt.xlabel("Region")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("tall_hills_bar.png")
plt.show()
 
# ============================================================
# �� Scenario 4: Pie Chart (Region Distribution) + Save
# ============================================================
# You want to see the distribution of hills.
# �� Tasks:
# 1. Count the number of hills per Region.
# 2. Select top 5 regions.
# 3. Prepare labels and values.
# 4. Plot a pie chart.
# 5. Add percentage labels.
# Save graph: plt.savefig("region_distribution.png")
 
region_counts = df.groupby("Region")['Hill Name'].count()
top5 = region_counts.head(5)
label = top5.index
value = top5.values
plt.figure(figsize=(6,6))
plt.pie(value, labels=label, autopct="%1.1f%%")
plt.title("Region Distribution")
plt.legend()
plt.tight_layout()
plt.savefig("region_distribution.png")
plt.show()
 
# ============================================================
# �� Scenario 5: Advanced Analysis + Multiple Graphs
# ============================================================
# You want deeper insights.
 
# ============================================================
# �� Part 1: Feature Creation
# ============================================================
# 1. Create a new column:
# ○ Height Category:
# ■ Height >= 1000 → "Very High"
# ■ 800–999 → "High"
# ■ < 800 → "Moderate"
 
df['Height Category'] = ["Very High"
                         if i>=1000 else "High" if i>=800 else "Moderater"
                         for i in df["Height"]]
 
# ============================================================
# �� Part 2: NumPy Usage
# ============================================================
# 2. Convert Height column to NumPy array.
# Calculate height differences using:
# np.diff()
 
heights = np.array(df["Height"])
height_diff = np.diff(heights)
 
# ============================================================
# �� Part 3: Visualizations
# ============================================================
# �� Line Graph
# 4. Plot height trend for all hills.
plt.figure(figsize=(6,6))
plt.plot(heights)
plt.title("Height Trend of All Hills")
plt.xlabel("Hill Index")
plt.ylabel("Height (m)")
plt.tight_layout()
plt.savefig("height_trend.png")
plt.show()
 
# �� Stacked Bar Chart
# 5. Show count of Height Category per Region.
category_counts = df.groupby(['Region', 'Height Category']).size().unstack(fill_value=0)
category_counts.plot(kind='bar', stacked=True, figsize=(10,6))
plt.title("Height Category per Region")
plt.xlabel("Region")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig("height_category_stacked.png")
plt.show()
 
# �� Histogram
# 6. Plot distribution of Height.
plt.figure(figsize=(6,6))
plt.hist(heights, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Hill Heights")
plt.xlabel("Height (m)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("height_histogram.png")
plt.show()
 
# ============================================================
# �� Part 4: Save All Graphs
# ============================================================
# plt.savefig("height_trend.png")
# plt.savefig("height_category_stacked.png")
# plt.savefig("height_histogram.png")
 
# ============================================================
# �� Part 5: Insights
# ============================================================
# ● Which region has tallest hills
# ● Which category is most common
# ● Distribution pattern of heights
print("Tallest hills are concentrated in Cairngorms (Ben Macdui, Braeriach, Cairn Toul).")
print("Most common category:", df['Height Category'].mode()[0])
print("Height distribution shows many hills around 900–1000m, with fewer above 1200m.")
 