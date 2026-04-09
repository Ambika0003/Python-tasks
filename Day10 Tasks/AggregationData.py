import numpy as np

branch_A=np.array([[10,20],[30,40]])
branch_B=np.array([[5,15],[25,35]])
add=branch_A +branch_B
total_d=np.sum(add)

print("combined natrix:\n", add)
print("total employees across all departments ;\n", total_d)