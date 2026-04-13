import numpy as np

nums = np.random.randint(1, 100, 10)
print("the random numbers are :\n",nums)

filtered_value=nums[nums % 5 == 0]
print("values that are divisible by 5 are :\n", filtered_value)

print("the result of sorted nums are:\n",np.sort(filtered_value))