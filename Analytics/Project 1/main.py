import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#Scenario 1: Basic Data Loading & Cleaning

#Load the dataset into a Pandas DataFrame.
df=pd.read_csv(r'C:\Users\Windows\Downloads\Python Practice\Analytics\Project 1\railway_gauges.csv')
##Display the first 5 rows and column names. 
print("the first 5 rows and column of the dataset is:\n",df.head())

#Check for missing values and replace them with 0.
print("missing values are:\n",df.isnull().sum())
df.fillna(0)

#Convert all gauge columns (Broad, Metre, Narrow, Total) to numeric types.
df["Broad Gauge"]=pd.to_numeric(df["Broad Gauge"],errors="coerce")
df["Metre Gauge"]=pd.to_numeric(df["Metre Gauge"],errors="coerce")
df["Narrow Gauge"]=pd.to_numeric(df["Narrow Gauge"],errors="coerce")
df["Total"]=pd.to_numeric(df["Total"],errors="coerce")
print(df.dtypes)

#Scenario 2: Simple Visualization

#Extract Year and Total columns. 
extract=(df[["Year","Total"]])

#Plot a line graph showing Total tracks over years.
plt.plot(df["Year"],df["Total"])
#Add:Title 
plt.title("Total Tracks Over Years")
#X and Y labels 
plt.xlabel('Year')
plt.ylabel('Total')
plt.xticks(rotation=85)
plt.show()

#Identify whether the trend is increasing or decreasing. 
if df["Total"].iloc[-1]>df["Total"].iloc[0]:
    print("Trend is incresing")
else:
    print("Trend is decresing")

#Scenario 3: Filtering + Bar Chart

#convert the dataset into number because its in string form
df["new_year"]=df["Year"].str.split("-").str[0]
df["new_year"]=df["new_year"].astype(int)

#Filter the dataset for years after 2000. 
Y=df[df["new_year"]>2000]
print("the dataset for years after 2000:\n",Y)

#Select Broad Gauge, Metre Gauge, and Narrow Gauge. 
select=Y[["Broad Gauge", "Metre Gauge","Narrow Gauge"]]

#Plot a grouped bar chart comparing all three gauges.
x=np.arange(len(Y))
w=0.25
plt.bar(x,Y["Broad Gauge"],w,label="Broad")
plt.bar(x+w,Y["Metre Gauge"],w,label="Metre")
plt.bar(x+2*w,Y["Narrow Gauge"],w,label="Narrow")
plt.title('Comparison of Gauges')
#Add legend and proper labels. 
plt.xlabel('Years')
plt.ylabel('Tracks')
plt.legend()
plt.xticks(x,Y["Year"],rotation=85)
plt.show()

#Identify which gauge dominates in recent years
dominant=Y[["Broad Gauge","Metre Gauge","Narrow Gauge"]].sum().idxmax()
print("The dominant gauge in recent years is:",dominant)

#Scenario 4: Feature Engineering + Pie Chart

#. Calculate total sum of each gauge across all years. 
Total=df[["Broad Gauge","Metre Gauge","Narrow Gauge"]].sum()

#Create a new structure (Series/DataFrame) for totals.
print("the totol sum of each gauge is:\n",Total)

#Plot a pie chart showing percentage contribution.
#Add percentage labels (autopct). 
plt.pie(Total,labels=Total.index,autopct='%1.1f%%',shadow=True,startangle=90)
plt.title('Percentage Contribution')
plt.legend(loc="upper left")
plt.show()

#Interpret which gauge contributes the most. 
print("Highest Contribution gauge is: ",Total.idxmax())

#Scenario 5: Advanced Analysis + Multiple Graphs

#Convert year to numeric
new_cols=df["Year"].str.split("-").str[0].astype(int)

#Create new % columns: 
df["% Broad"]=(df["Broad Gauge"]/df["Total"])*100
df["% Metre"]=(df["Metre Gauge"]/df["Total"])*100
df["% Narrow"]=(df["Narrow Gauge"]/df["Total"])*100

#Use NumPy (np.diff) to calculate yearly growth of Total tracks.
growth=np.diff(df["Total"])
print(growth)

#Plot:  Line graph for all gauges 
plt.figure()
plt.plot(df["Year"],df["Broad Gauge"],label="Broad")
plt.plot(df["Year"],df["Metre Gauge"],label="Metre")
plt.plot(df["Year"],df["Narrow Gauge"],label="Narrow")
plt.title("Railway Gauges Trend")
plt.xlabel("Year")
plt.ylabel("Tracks")
plt.xticks(rotation=90)
plt.legend()
plt.show()

#Stacked bar chart showing composition
plt.figure()
plt.bar(df["Year"],df["Broad Gauge"],label="Broad")
plt.bar(df["Year"],df["Metre Gauge"],bottom=df["Broad Gauge"],label="Metre")
plt.bar(df["Year"],df["Narrow Gauge"],bottom=df["Broad Gauge"]+df["Metre Gauge"],label="Narrow")
plt.title("Gauge Composition")
plt.xlabel('Year')
plt.ylabel("Tracks")
plt.xticks(rotation=85)
plt.legend()
plt.show()

#Highlight: Years with highest growth 
max_growth=df["Year"].iloc[np.argmax(growth)+1]
print("Years with highest growth:", max_growth)

#Decline in any gauge 
if any(growth > 0):
    print("Decline observed in some years")
else:
    print("No Decline observed")

#Is the railway system shifting towards a single dominant gauge?
bg=df["Broad Gauge"].iloc[-1]>df["Broad Gauge"].iloc[0]
mg=df["Metre Gauge"].iloc[-1]>df["Metre Gauge"].iloc[0]
ng=df["Narrow Gauge"].iloc[-1]>df["Narrow Gauge"].iloc[0]

print(bg)
print(mg)
print(ng)

if bg and mg and ng:
    print("Conclusion: Railway system shifting towards a single dominant gauge")
else:
    print("Conculsion: No clear shift towards a single dominant gauge")








