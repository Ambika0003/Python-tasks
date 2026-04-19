import numpy as np
import pandas as pd

while True:
    try:
        x = input("Enter log: ")
        if x == "exit":
            break
        with open("log.txt", "a") as f:
            f.write(x + "\n")
    except:
        print("Error")
print("Done")