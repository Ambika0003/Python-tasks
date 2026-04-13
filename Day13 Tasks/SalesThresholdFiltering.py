import numpy as np

sales = np.array([12000, 18000, 9000, 22000, 15000, 30000]) 
print(sales)

avg=np.mean(sales)
print(avg)

filtered_array=sales[sales>avg]
print(filtered_array)

