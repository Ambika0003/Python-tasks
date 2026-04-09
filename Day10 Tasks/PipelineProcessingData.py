import numpy as np

a=np.array([3,7,10,12,18,25])
print("sorted array is :\n",np.sort(a))

b=np.array_split(a,2)
print("splitting array into two parts:\n",b)

part1=np.sum(b[0])
part2=np.sum(b[1])

print("sum of first part is :\n", part1)
print("sum of second part is :\n", part2)