import numpy as np
import copy

classes = [["Math", [30, 35]], ["Science", [25, 28]]] 
b=copy.deepcopy(classes)
print(classes)
b[0][1][0]=99
print(b)
