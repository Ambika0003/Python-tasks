import numpy as np
import pandas as pd

S = pd.Series([5, 10, 15]) 
sum=np.add(S, 5)
print("the updated series is:\n", sum)