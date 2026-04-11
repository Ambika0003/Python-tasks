import numpy as np
temp=np.array([28,31,35,27,40,22])

new_temp=[]

for i in temp:
    if i >30:
        new_temp.append(True)
    else:
        new_temp.append(False)
newvalue=temp[new_temp]

print(new_temp)
print(newvalue)