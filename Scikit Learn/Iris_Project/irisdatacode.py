# Importing required libraries
import numpy as np                  # For numerical operations
import pandas as pd                 # For handling datasets

# Loading dataset
dataset = pd.read_csv(r"C:\Users\Windows\Downloads\Iris.csv")   # Read CSV file
print(dataset.head())               # Display first 5 rows

# Selecting features (X) and target (y)
X = dataset[['SepalLengthCm','PetalLengthCm','SepalWidthCm','PetalWidthCm']].values
y = dataset['Species'].values

# Display shape of data
print('-'*80)
print(f'Shape of X is {X.shape}\nShape of y is {y.shape}')

# Splitting dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

print('-'*80)
print(f"Length of X_train: {len(X_train)}\nLength of X_test: {len(X_test)}")
print(f"Length of y_train: {len(y_train)}\nLength of y_test: {len(y_test)}")


# -----------------------------
# Feature Scaling
# -----------------------------
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

# Fit on training data and transform
'''
Different features have different ranges:

Feature	Range    Example
Sepal Length	  1–10
Petal Width	  0.1–2

👉 Problem:

Large values dominate small values
Model becomes biased

👉 Problem:

Large values dominate small values
Model becomes biased

Z=(X−Mean​)/Standard Deviation

👉 After scaling:

Mean = 0
Standard deviation = 1
'''

X_train = sc.fit_transform(X_train)

'''
This does 2 things:

fit() → learns:
Mean of each column
Standard deviation
transform() → scales data using that info
'''

# Transform test data (important: do NOT fit again)
X_test = sc.transform(X_test)

# Print few scaled values
'''
for i in range(10):
    print(X_train[i])

print('-'*80)

for i in range(10):
    print(X_test[i])'''


# ============================================================
# 1. Support Vector Machine (SVM)
# ============================================================
# SVM tries to find the best boundary (line/plane) to separate classes.
# It focuses on maximizing the margin between different classes.

from sklearn.svm import SVC
classifier = SVC()
print(classifier)

# Train model
classifier.fit(X_train, y_train)

# Predict test data
y_pred = classifier.predict(X_test)

# Evaluate accuracy
from sklearn.metrics import accuracy_score
print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 2. Logistic Regression
# ============================================================
# Logistic Regression predicts probability and classifies using a threshold.
# It works well for linearly separable data.

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 3. Naive Bayes
# ============================================================
# Naive Bayes assumes features are independent of each other.
# It uses probability to predict the most likely class.

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 4. Decision Tree Classifier
# ============================================================
# Decision Tree splits data into branches based on feature values.
# It makes decisions like a flowchart.

from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))


# ============================================================
# 5. Random Forest Classifier
# ============================================================
# Random Forest builds multiple decision trees and combines their results.
# It improves accuracy and reduces overfitting.

from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
print(classifier)

classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

print('\n'+'-'*20+'Accuracy Score on the Test set'+'-'*20)
print("{:.0%}".format(accuracy_score(y_test, y_pred)))








