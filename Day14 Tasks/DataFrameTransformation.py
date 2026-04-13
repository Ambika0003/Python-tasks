import numpy as np
import pandas as pd

df = pd.DataFrame({ 
"Name": ["A", "B", "C", "D"], 
"Marks": [50, 80, 30, 90] 
})
print(df)

df['pass/fail']=["Pass" if m >=50 else "Fail" for m in df["Marks"]]
print(df)

print("the pass students are :\n", df[df["pass/fail"]=="Pass"])

avg=df["Marks"].mean()
print("the average of passed students is:\n",avg)


