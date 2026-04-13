import pandas as pd

S1 = pd.Series([10, 20, 30], index=["apple", "banana", "cherry"]) 
S2 = pd.Series([5, 15, 25], index=["apple", "banana", "cherry"])
print(S1+S2)
print("sum of s1 and s2",sum(S1+S2))
