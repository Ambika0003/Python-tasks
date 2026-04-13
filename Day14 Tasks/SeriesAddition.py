import numpy as np
import pandas as pd

S1 = pd.Series([10, 20, 30], index=["a", "b", "c"]) 
S2 = pd.Series([5, 15, 25], index=["b", "c", "d"]) 
sum=S1+S2
print("The sum of two series are:\n",sum)

#"a" and "d" it shows NaN because a is not in S2 and d is not in S1 

f_result=sum.where(sum.notna(),0)
print(f_result)


