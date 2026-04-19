import numpy as np
import pandas as pd
import time
from functools import wraps
def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper
def stream_numeric_data(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            try:
                yield float(line.strip())
            except ValueError:
                print(f"Skipping bad data: {line.strip()}")
@time_it
def process_pipeline(filepath):
    data = np.fromiter(stream_numeric_data(filepath), dtype=float)
    if data.size == 0:
        return pd.DataFrame()
    mean_val = np.mean(data)
    std_val = np.std(data)
    results = pd.DataFrame({
        'Metric': ['Mean', 'Standard Deviation'],
        'Value': [mean_val, std_val]
    })
    return results
if __name__ == "__main__":
    with open("data.txt", "w") as f:
        f.write("10.5\n20.2\nbad_data\n30.1\n40.8\n100.0")
    df_results = process_pipeline("data.txt")
    print(df_results)