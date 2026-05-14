import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

print("🚀 Marketing Campaign Project Starting...")

# =====================================================
# 1. LOAD DATA
# =====================================================

data_path = "data"

files = os.listdir(data_path)

all_data = []

for file in files:

    if file.endswith(".csv"):

        df_temp = pd.read_csv(os.path.join(data_path, file))

        df_temp["source_file"] = file

        all_data.append(df_temp)

df = pd.concat(all_data, ignore_index=True)

print("\n✅ Data Loaded Successfully")
print("Dataset Shape:", df.shape)

# =====================================================
# 2. DATA CLEANING
# =====================================================

print("\n🧹 Cleaning Data...")

print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
for col in df.columns:

    if df[col].dtype == "object":

        df[col].fillna("Unknown", inplace=True)

    else:

        df[col].fillna(df[col].median(), inplace=True)

print("\n✅ Missing values handled")
print("After Cleaning Shape:", df.shape)

# =====================================================
# 3. FEATURE ENGINEERING
# =====================================================

print("\n⚙ Performing Feature Engineering...")

# ROI Calculation
if "Revenue" in df.columns and "Acquisition_Cost" in df.columns:

    df["ROI"] = (
        (df["Revenue"] - df["Acquisition_Cost"]) /
        (df["Acquisition_Cost"] + 1)
    )

# Profit Flag Creation
df["Profit_Flag"] = np.where(df["ROI"] > 0, 1, 0)

print("✅ ROI & Profit_Flag Created")

# =====================================================
# 4. ENCODING CATEGORICAL COLUMNS
# =====================================================

print("\n🔤 Encoding Categorical Columns...")

le = LabelEncoder()

for col in df.columns:

    if df[col].dtype == "object":

        df[col] = le.fit_transform(df[col].astype(str))

print("✅ Encoding Completed")

# =====================================================
# 5. REGRESSION MODEL
# =====================================================

print("\n📈 REGRESSION MODEL")

# Avoid Data Leakage
regression_drop_cols = [
    "ROI",
    "Profit_Flag"
]

X_reg = df.drop(columns=regression_drop_cols)

y_reg = df["ROI"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg,
    y_reg,
    test_size=0.2,
    random_state=42
)

# Model
reg_model = RandomForestRegressor(
    n_estimators=50,
    random_state=42
)

reg_model.fit(X_train_reg, y_train_reg)

# Prediction
y_pred_reg = reg_model.predict(X_test_reg)

# Evaluation
mae = mean_absolute_error(y_test_reg, y_pred_reg)
mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)

print("\n✅ Regression Model Performance")
print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)

# =====================================================
# 6. CLASSIFICATION MODEL
# =====================================================

print("\n📊 CLASSIFICATION MODEL")

# Avoid leakage
classification_drop_cols = [
    "Profit_Flag",
    "ROI"
]

X_clf = df.drop(columns=classification_drop_cols)

y_clf = df["Profit_Flag"]

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf,
    y_clf,
    test_size=0.2,
    random_state=42
)

# Model
clf_model = RandomForestClassifier(
    n_estimators=50,
    random_state=42
)

clf_model.fit(X_train_clf, y_train_clf)

# Prediction
y_pred_clf = clf_model.predict(X_test_clf)

# Evaluation
accuracy = accuracy_score(y_test_clf, y_pred_clf)

print("\n✅ Classification Model Performance")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test_clf, y_pred_clf))

# =====================================================
# 7. FEATURE IMPORTANCE
# =====================================================

print("\n⭐ Top Important Features")

importance = pd.DataFrame({

    "Feature": X_reg.columns,

    "Importance": reg_model.feature_importances_

}).sort_values(by="Importance", ascending=False)

print(importance.head(10))

# =====================================================
# 8. EDA VISUALIZATION
# =====================================================

print("\n📊 Generating EDA Graphs...")

# ROI Distribution
if "ROI" in df.columns:

    plt.figure(figsize=(8,5))

    sns.histplot(df["ROI"], bins=30)

    plt.title("ROI Distribution")

    plt.xlabel("ROI")

    plt.ylabel("Frequency")

# Campaign Type
if "Campaign_Type" in df.columns:

    plt.figure(figsize=(8,5))

    sns.countplot(x=df["Campaign_Type"])

    plt.title("Campaign Type Analysis")

    plt.xticks(rotation=45)

# Channel Analysis
if "Channel_Used" in df.columns:

    plt.figure(figsize=(8,5))

    sns.countplot(x=df["Channel_Used"])

    plt.title("Channel Used Analysis")

    plt.xticks(rotation=45)

# Feature Importance
plt.figure(figsize=(10,5))

sns.barplot(
    x=importance["Importance"].head(10),
    y=importance["Feature"].head(10)
)

plt.title("Top 10 Important Features")

plt.xlabel("Importance")

plt.ylabel("Features")

print("\n✅ EDA Completed Successfully!")

print("\n🎯 PROJECT COMPLETED SUCCESSFULLY!")
