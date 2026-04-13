import pandas as pd

cities = {"Delhi": 2000000, "Mumbai": 3000000, "Chennai": 1500000}

city_series = pd.Series(cities, index=["Delhi", "Chennai", "Bangalore"])
print(city_series)

print(city_series.isnull())
print(city_series)
