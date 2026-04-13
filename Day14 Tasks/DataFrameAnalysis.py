import pandas as pd
import numpy as np

data = pd.DataFrame({ 
"Name": ["A", "B", "C"], 
"Math": [80, 70, 60], 
"Science": [90, 60, 70] 
})
df=pd.DataFrame(data)
print(df)

print("add new column")
data['Total']=data['Math']+data['Science']
print(data)
 
marks=data.loc[data["Total"].idxmax()]
print("the highest marks of the student is :\n", marks)


