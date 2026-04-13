import numpy as np
import pandas as pd

df = pd.DataFrame({ "Price": [100, 200, 300] })
df["discount"]=df["Price"]* 0.10
print(df)

df["f_price"]=df["Price"]-df["discount"]
print(df)