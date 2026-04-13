import pandas as pd
import numpy as np

data = pd.DataFrame({ 
"A": [10, 20, 30], 
"B": [5, 15, 25] 
}, index=["x", "y", "z"]) 

df=pd.DataFrame(data)
print(df)
print("row with index y:\n",df.loc['y'])

df=df.drop('x')
print("after deleting row x:\n",df)