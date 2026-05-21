import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(r"C:\Users\Windows\OneDrive\Documents\datasets\Heart.csv")

print("First 5 Rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================================
# Graph 1 : Correlation Heatmap
# ==========================================

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# ==========================================
# Graph 2 : Heart Disease Count
# ==========================================

plt.figure(figsize=(6, 4))
sns.countplot(x='target', data=df)
plt.title("Heart Disease Count")
plt.xlabel("Target")
plt.ylabel("Count")
plt.show()

# ==========================================
# Graph 3 : Age Distribution
# ==========================================

plt.figure(figsize=(6, 4))
plt.hist(df['age'], bins=10)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

# ==========================================
# Graph 4 : Cholesterol Distribution
# ==========================================

plt.figure(figsize=(6, 4))
plt.hist(df['chol'], bins=10)
plt.title("Cholesterol Distribution")
plt.xlabel("Cholesterol")
plt.ylabel("Count")
plt.show()

# ==========================================
# Features and Target
# ==========================================

X = df.drop("target", axis=1)
y = df["target"]

# ==========================================
# Train Test Split
# ==========================================

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ==========================================
# Import Metrics
# ==========================================

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# ==========================================
# Algorithm 1 : Logistic Regression
# ==========================================

from sklearn.linear_model import LogisticRegression
lr_model = LogisticRegression(max_iter=10000)
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_pred)

print("\n===== Logistic Regression =====")
print("Accuracy :", accuracy_score(y_test, lr_pred))
print("Precision:", precision_score(y_test, lr_pred))
print("Recall   :", recall_score(y_test, lr_pred))
print("F1 Score :", f1_score(y_test, lr_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, lr_pred))

# ==========================================
# Algorithm 2 : Random Forest
# ==========================================

from sklearn.ensemble import RandomForestClassifier
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)

print("\n===== Random Forest =====")
print("Accuracy :", accuracy_score(y_test, rf_pred))
print("Precision:", precision_score(y_test, rf_pred))
print("Recall   :", recall_score(y_test, rf_pred))
print("F1 Score :", f1_score(y_test, rf_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

# ==========================================
# Graph 5 : Accuracy Comparison
# ==========================================

algorithms = ['Logistic Regression', 'Random Forest']
accuracies = [lr_accuracy, rf_accuracy]
plt.figure(figsize=(6, 4))
plt.bar(algorithms, accuracies)
plt.title("Algorithm Accuracy Comparison")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.show()