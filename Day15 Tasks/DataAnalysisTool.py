import numpy as np
import pandas as pd
#Generate marks using NumPy 
marks=np.random.randint(0,100,10)
students=["Ambi","Bala","Cherry","Don","Eva","Faf","Gagan","Henry","Ishu","Jack"]

#Convert into Pandas DataFram
df=pd.DataFrame({"Student":students,
                 "Marks":marks})
print("Students details:\n ",df)

#Use conditions to filter passing students
filtred_array=df[df["Marks"]>=50]
print("the passing students are :\n", filtred_array)

#Calculate mean using math/NumPy 
avg=np.mean(df["Marks"])
print("average of the marks is:\n ",avg)

#Using loop to print results 
print("\nFinal Results:")
for index, row in df.iterrows():
    status = "Pass" if row["Marks"] >= 50 else "Fail"
    print(row["Student"], "-", row["Marks"], "-", status)



