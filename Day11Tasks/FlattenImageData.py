import numpy as np

image=np.array([[1,2,3],[4,5,6]])
print(image)

new_image=image.reshape(-1)
print("the flatten array is:\n",new_image)
