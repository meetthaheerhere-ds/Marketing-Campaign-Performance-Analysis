import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("🚀 Marketing Campaign Project Starting...")

# ==============================
# 1. LOAD DATA
# ==============================

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
print("Shape:", df.shape)

# ==============================
# 2. DATA CLEANING
# ==============================

print("\n🧹 Cleaning Data...")

print("Missing values:\n", df.isnull().sum())

df = df.drop_duplicates()
df = df.fillna(0)

print("After cleaning shape:", df.shape)

# ==============================
# 3. FEATURE ENGINEERING
# ==============================

print("\n⚙ Feature Engineering...")

# ROI Calculation
if "Revenue" in df.columns and "Acquisition_Cost" in df.columns:
    df["ROI"] = (
        (df["Revenue"] - df["Acquisition_Cost"]) /
        (df["Acquisition_Cost"] + 1)
    )

# Profit Flag
if "Revenue" in df.columns and "Acquisition_Cost" in df.columns:
    df["Profit_Flag"] = np.where(
        df["Revenue"] > df["Acquisition_Cost"],
        1,
        0
    )

print("Feature engineering done")

# ==============================
# 4. ENCODING CATEGORICAL DATA
# ==============================

print("\n🔤 Encoding categorical columns...")

le = LabelEncoder()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = le.fit_transform(df[col].astype(str))

print("Encoding completed")

# ==============================
# 5. SPLIT DATA
# ==============================

print("\n📊 Splitting data...")

# Target Selection
if "ROI" in df.columns:
    target = "ROI"
elif "Revenue" in df.columns:
    target = "Revenue"
else:
    target = df.columns[-1]

X = df.drop(columns=[target])
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)

# ==============================
# 6. MODEL TRAINING
# ==============================

print("\n🤖 Training Model...")

model = RandomForestRegressor(
    n_estimators=20,
    random_state=42
)

model.fit(X_train, y_train)

# ==============================
# 7. PREDICTION
# ==============================

y_pred = model.predict(X_test)

# ==============================
# 8. EVALUATION
# ==============================

print("\n📈 Model Performance:")

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("MSE:", mse)
print("R2 Score:", r2)

# ==============================
# 9. FEATURE IMPORTANCE
# ==============================

print("\n⭐ Feature Importance:")

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

print(importance.head(10))

print("\n🎯 ML Project Completed Successfully!")

# ==============================
# 10. EXPLORATORY DATA ANALYSIS
# ==============================

print("\n📊 Generating EDA Graphs...")

# ------------------------------
# ROI Distribution
# ------------------------------

if "ROI" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.histplot(df["ROI"], bins=30)

    plt.title("ROI Distribution")
    plt.xlabel("ROI")
    plt.ylabel("Frequency")

    plt.show()

# ------------------------------
# Campaign Type Analysis
# ------------------------------

if "Campaign_Type" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(x=df["Campaign_Type"])

    plt.title("Campaign Type Count")

    plt.xticks(rotation=45)

    plt.show()

# ------------------------------
# Channel Used Analysis
# ------------------------------

if "Channel_Used" in df.columns:

    plt.figure(figsize=(8, 5))

    sns.countplot(x=df["Channel_Used"])

    plt.title("Channel Used Analysis")

    plt.xticks(rotation=45)

    plt.show()

# ------------------------------
# Feature Importance Graph
# ------------------------------

plt.figure(figsize=(10, 5))

sns.barplot(
    x=importance["Importance"].head(10),
    y=importance["Feature"].head(10)
)

plt.title("Top 10 Important Features")

plt.xlabel("Importance Score")
plt.ylabel("Features")

plt.show()

print("\n✅ EDA Completed Successfully!")