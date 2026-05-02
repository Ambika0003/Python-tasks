# ============================================================
# 📊 KC Housing Data - Multiple Regression Models
# ============================================================

import numpy as np
import pandas as pd

# Load dataset
dataset = pd.read_csv(r"C:\Users\Windows\Downloads\kc_house_data.csv")

# Features and target
X = dataset[['bedrooms','bathrooms','sqft_living','sqft_lot',
             'floors','condition','grade','sqft_basement',
             'yr_built','yr_renovated']].values

y = dataset['price'].values

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# ============================================================
# 📦 Models
# ============================================================

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate(name, y_test, y_pred):
    print("-" * 80)
    print(f"{name} Performance:")
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("MSE:", mean_squared_error(y_test, y_pred))
    print("R2 Score:", r2_score(y_test, y_pred))


# ============================================================
# 1️⃣ Linear Regression
# ============================================================

from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("Linear Regression", y_test, y_pred)


# ============================================================
# 2️⃣ Lasso Regression
# ============================================================

from sklearn.linear_model import Lasso

model = Lasso(alpha=1.0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("Lasso Regression", y_test, y_pred)


# ============================================================
# 3️⃣ SVR
# ============================================================

from sklearn.svm import SVR

model = SVR()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("SVR", y_test, y_pred)


# ============================================================
# 4️⃣ Decision Tree
# ============================================================

from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("Decision Tree", y_test, y_pred)


# ============================================================
# 5️⃣ Random Forest
# ============================================================

from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("Random Forest", y_test, y_pred)


# ============================================================
# 6️⃣ KNN
# ============================================================

from sklearn.neighbors import KNeighborsRegressor

model = KNeighborsRegressor(n_neighbors=5)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("KNN Regressor", y_test, y_pred)


# ============================================================
# 7️⃣ Gradient Boosting
# ============================================================

from sklearn.ensemble import GradientBoostingRegressor

model = GradientBoostingRegressor(random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
evaluate("Gradient Boosting", y_test, y_pred)