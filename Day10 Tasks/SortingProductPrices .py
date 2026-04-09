import numpy as np

price=[499,299,799,199,599]
price_arr=np.array(price)
print(price_arr)

sort_price=np.sort(price_arr)
print("sorted array:", sort_price)