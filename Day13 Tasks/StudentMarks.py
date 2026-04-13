import numpy as np

marks = np.array([ 
[70, 80, 90], 
[60, 75, 85], 
[50, 65, 70], 
[90, 95, 85], 
[40, 55, 60] 
])
print(marks)

total=np.sum(marks, axis=1)
print("the total marks of each student is :\n",total)

avg=np.mean(total)
print("the average is:\n", avg)

class_avg=total[total>avg]
print(" total marks above the class average:\n",class_avg)