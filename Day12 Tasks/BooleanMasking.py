import numpy as np

salary=np.array([25000, 40000, 15000, 50000, 30000])
print(salary)

x=salary[salary>30000]
print(x)

employee=np.sum(salary>30000)
print(employee)