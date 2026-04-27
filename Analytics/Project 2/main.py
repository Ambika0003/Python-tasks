# ============================================================
# Project Title: IGN
# Analyze ign dataset using NumPy, Pandas, Matplotlib
# ============================================================

# ============================================================
# 📦 1. Import Required Libraries
# ============================================================

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#==============================================================
#��Scenario 1: Data Loading & Preprocessing
#==============================================================
#You are given the ign.csv dataset containing game reviews. 
#��Tasks: 

#1.Load the dataset using Pandas. 
df=pd.read_csv(r"C:\Users\Windows\Downloads\ign.csv")

#2. Display: ○ First 5 rows (head()) ○ Last 5 rows (tail()) ○ Shape of dataset 
print("\n First 5 rows are:")
print(df.head())

print("\n Last 5 rows: ")
print(df.tail())

print("\n Shape of dataset is:")
print(df.shape)

#3. Remove the unnecessary column: ○ "Unnamed: 0" (index column)
df=df.drop(columns=["Unnamed:0"],errors='ignore')
print(df)

#4.Check for missing values in: ○ score, genre, platform 
print("\n missing values are:")
missing_values = df[['score', 'genre', 'platform']].isnull().sum()
print(missing_values)

#5. Handle missing values: 
# ○ Fill numeric column score with mean  
df['score']=df['score'].fillna(df['score'].mean())
print(df['score'])

#○ Fill categorical column genre with mode
df['genre']=df['genre'].fillna(df['genre'].mode()[0])
print(df['genre'])

#6. Ensure correct data types: ○ score → float ○ release_year, release_month, release_day → integer
# Convert data types
df['score'] = df['score'].astype(float)

df['release_year'] = df['release_year'].astype(int)
df['release_month'] = df['release_month'].astype(int)
df['release_day'] = df['release_day'].astype(int)

# Print data types to verify
print(df.dtypes)

#==============================================================
#��Scenario 2: Line Graph (Score Trend) + Save 
#==============================================================
#You want to analyze how game scores change over time. 
#��Tasks: 

# 1 & 2: Group by release_year and calculate average score
yearly_scores = df.groupby('release_year')['score'].mean()

# 3: Convert to NumPy arrays
years = yearly_scores.index.to_numpy()
avg_scores = yearly_scores.values

# 4: Plot line graph
plt.figure(figsize=(8, 5))
plt.plot(years, avg_scores, marker='o')

# 5: Add title and labels
plt.title("Average Game Score Over Years")
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.grid(True)

# 6: Save the graph
plt.savefig("avg_score_trend.png")
plt.show()

#==============================================================
#��Scenario 3: Filtering + Bar Chart + Save  
#==============================================================
#You want to compare top platforms. 
#��Tasks: 

# 1: Filter dataset where score > 7
high_rated = df[df['score'] > 7]
print("dataset where score is > 7:\n",high_rated)

# 2: Count number of high-rated games per platform
platform_counts = high_rated['platform'].value_counts()

# 3: Select top 10 platforms
top_platforms = platform_counts.head(10)

# 4: Convert to NumPy arrays
platform_names = top_platforms.index.to_numpy()
game_counts = top_platforms.values

# 5: Plot bar chart
plt.figure(figsize=(10, 6))
plt.bar(platform_names, game_counts)

# 6: Rotate x-axis labels
plt.xticks(rotation=45)

# Add title and labels 
plt.title("Top 10 Platforms by High-Rated Games")
plt.xlabel("Platform")
plt.ylabel("Number of Games")

# Save the graph
plt.savefig("top_platforms_bar.png")

# Show the plot
plt.show()

#==============================================================
#��Scenario 4: Aggregation + Pie Chart + Save
#==============================================================
#You want to analyze genre distribution. 
#��Tasks: 

#1.import matplotlib.pyplot as plt

# 1: Count number of games per genre
genre_counts = df['genre'].value_counts()

# 2: Select top 5 genres using pandas
top_genres = genre_counts.head(5)
print("Top 5 genres are:\n",top_genres)

# 3: Prepare labels and values
labels = top_genres.index
values = top_genres.values

# 4: Plot pie chart
plt.figure(figsize=(7, 7))
plt.pie(values, labels=labels, autopct='%1.1f%%')

# Add title
plt.title("Top 5 Game Genres Distribution")

# Save the graph
plt.savefig("genre_distribution.png")

# Show the plot
plt.show()

#==============================================================
#��Scenario 5: Advanced Analysis + Multiple Graphs
#==============================================================
#You are asked to perform a detailed analysis of review patterns. 

#��Part 1: Feature Engineering 

#1.Create a new column: ○ score_category: ■ score >= 9 → "Excellent" ■ 7 <= score < 9 → "Good" ■ < 7 → "Average" 
df['score_category'] = np.where(
    df['score'] >= 9, "Excellent",
    np.where(df['score'] >= 7, "Good", "Average")
)

# 2: Convert editors_choice (Y → 1, N → 0)
df['editors_choice'] = df['editors_choice'].map({'Y': 1, 'N': 0})
print(df['editors_choice'])

# verify changes
print(df[['score', 'score_category', 'editors_choice']].head())

#��Part 2: NumPy Analysis 
#3. Use NumPy to: ○ Calculate yearly score growth using np.diff() on average yearly scores 

# Group by year and calculate average score
yearly_scores = df.groupby('release_year')['score'].mean()

# Convert to NumPy array (sorted by year)
avg_scores = yearly_scores.values

# 3: Calculate yearly score growth using np.diff()
score_growth = np.diff(avg_scores)

# Optional: show results
print("Average Scores per Year:")
print(avg_scores)

print("\nYearly Score Growth:")
print(score_growth)

#��Part 3: Visualizations 

#4.��Line Graph 4. Plot trend of: ○ Average score per release_year 

# Group and calculate average score per year
yearly_scores = df.groupby('release_year')['score'].mean()
print(yearly_scores)

plt.figure(figsize=(8, 5))
plt.plot(yearly_scores.index, yearly_scores.values, marker='o')

plt.title("Average Score per Release Year")
plt.xlabel("Release Year")
plt.ylabel("Average Score")
plt.grid(True)

plt.savefig("score_trend.png")
plt.show()

#��Stacked Bar Chart 5. Show count of: ○ score_category per release_year 

## Count score categories per year
category_year = df.groupby(['release_year', 'score_category']).size().unstack()

# Plot stacked bar chart
category_year.plot(kind='bar', stacked=True, figsize=(10, 6))

plt.title("Score Category Distribution per Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Games")
plt.xticks(rotation=45)

plt.savefig("score_category_stacked.png")
plt.show()

#��Histogram 6. Plot distribution of: ○ score 

#plt.figure(figsize=(8, 5))

plt.hist(df['score'], bins=15, edgecolor='black')

plt.title("Distribution of Game Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")

plt.savefig("score_distribution.png")
plt.show()

#=============================================THE END======================================================




