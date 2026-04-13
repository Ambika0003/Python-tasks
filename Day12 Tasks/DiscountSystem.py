import numpy as np
import copy

prices = [100, 200, 300, 400]
updated_price=[p* 0.9 if p > 200 else p for p in prices]
print(updated_price)