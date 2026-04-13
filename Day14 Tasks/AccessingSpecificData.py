import pandas as pd

S = pd.Series([100, 200, 300, 400], index=["A", "B", "C", "D"]) 
print("subset is :\n", S[['B','D']])
