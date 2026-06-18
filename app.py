<<<<<<< HEAD
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pickle

# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide"
)

st.title("📊 Marketing Campaign Performance Dashboard")

# =========================================
# LOAD PICKLE FILES — instant, no retraining
# =========================================

@st.cache_resource
def load_models():
    with open("notebooks/models/reg_model.pkl", "rb") as f:
        reg_model = pickle.load(f)
    with open("notebooks/models/clf_model.pkl", "rb") as f:
        clf_model = pickle.load(f)
    with open("notebooks/models/reg_columns.pkl", "rb") as f:
        reg_columns = pickle.load(f)
    with open("notebooks/models/clf_columns.pkl", "rb") as f:
        clf_columns = pickle.load(f)
    with open("notebooks/models/mlb_encoder.pkl", "rb") as f:
        mlb = pickle.load(f)
    with open("notebooks/models/label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)

    return reg_model, clf_model, reg_columns, clf_columns, mlb, label_encoders


if not os.path.exists("notebooks/models/reg_model.pkl"):
    st.error("❌ Model files not found! Please run notebook first.")
    st.stop()

reg_model, clf_model, reg_columns, clf_columns, mlb, label_encoders = load_models()
st.success("✅ Models Loaded Instantly from Pickle Files!")

# =========================================
# LOAD RAW DATA (for EDA & Dashboard only)
# =========================================

@st.cache_data
def load_data():
    data_path = "Data"
    all_data = []

    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            df_temp = pd.read_csv(os.path.join(data_path, file))
            df_temp["source_file"] = file

            if "nykaa" in file.lower():
                df_temp["Brand"] = "Nykaa"
            elif "purplle" in file.lower():
                df_temp["Brand"] = "Purplle"
            elif "tira" in file.lower():
                df_temp["Brand"] = "Tira"
            else:
                df_temp["Brand"] = "Unknown"

            all_data.append(df_temp)

    df = pd.concat(all_data, ignore_index=True)

    df.drop_duplicates(inplace=True)

    for col in df.columns:
        if df[col].dtype == "object" or str(df[col].dtype) == "string":
            df[col] = df[col].fillna("Unknown")
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")

    df["ROI"] = (df["Revenue"] - df["Acquisition_Cost"]) / (df["Acquisition_Cost"] + 1)
    df["Profit_Flag"] = np.where(df["ROI"] > 0, 1, 0)

    return df


df = load_data()

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.header("📌 Filter Options")

brand_filter = st.sidebar.selectbox(
    "Select Brand",
    ["All"] + list(df["Brand"].unique())
)

campaign_list = sorted([
    x for x in df["Campaign_Type"].astype(str).unique().tolist()
    if x not in ["0", "Unknown"]
])

campaign_filter = st.sidebar.selectbox(
    "Select Campaign Type",
    ["All"] + campaign_list
)

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if campaign_filter != "All":
    filtered_df = filtered_df[filtered_df["Campaign_Type"].astype(str) == campaign_filter]

# =========================================
# KPI METRICS
# =========================================

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Campaigns", filtered_df.shape[0])
with col2:
    st.metric("Total Revenue", f"₹{round(filtered_df['Revenue'].sum(), 2):,}")
with col3:
    st.metric("Average ROI", round(filtered_df["ROI"].mean(), 2))
with col4:
    st.metric("Total Conversions", int(filtered_df["Conversions"].sum()))

# =========================================
# DATA PREVIEW
# =========================================

st.subheader("📁 Dataset Preview")
st.dataframe(filtered_df.head())

# =========================================
# EDA CHARTS
# =========================================

st.subheader("📊 ROI Distribution")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df["ROI"], bins=30, ax=ax)
st.pyplot(fig)
plt.close()

st.subheader("📢 Campaign Type Analysis")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(x=filtered_df["Campaign_Type"], ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close()

st.subheader("💰 Brand-wise Revenue")
brand_revenue = filtered_df.groupby("Brand")["Revenue"].sum().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=brand_revenue, x="Brand", y="Revenue", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)
plt.close()

st.subheader("🔥 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(filtered_df.corr(numeric_only=True), cmap="coolwarm", ax=ax)
st.pyplot(fig)
plt.close()

# =========================================
# SQL ANALYSIS SECTION
# =========================================

st.subheader("🗄 SQL & MySQL Analysis")

with st.expander("1️⃣ Brand-wise Total Revenue"):
    q1 = filtered_df.groupby("Brand")["Revenue"].sum().reset_index()
    st.dataframe(q1)

with st.expander("2️⃣ Campaign Type Average Revenue"):
    q2 = filtered_df.groupby("Campaign_Type")["Revenue"].mean().reset_index()
    q2 = q2.sort_values(by="Revenue", ascending=False)
    st.dataframe(q2)

with st.expander("3️⃣ Top 10 Campaigns by ROI"):
    q3 = filtered_df[["Campaign_ID", "ROI"]].sort_values(by="ROI", ascending=False).head(10)
    st.dataframe(q3)

with st.expander("4️⃣ Channel-wise Total Conversions"):
    q4 = filtered_df.groupby("Channel_Used")["Conversions"].sum().reset_index()
    st.dataframe(q4)

with st.expander("5️⃣ Profit vs Loss Campaign Count"):
    q5 = filtered_df.groupby("Profit_Flag").size().reset_index(name="Count")
    q5["Profit_Flag"] = q5["Profit_Flag"].map({0: "Loss", 1: "Profit"})
    st.dataframe(q5)

with st.expander("⭐ Top Important Features"):
    importance_df = pd.DataFrame({
        "Feature": reg_columns,
        "Importance": reg_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    st.dataframe(importance_df.head(10))

# =========================================
# BUSINESS INSIGHTS
# =========================================

st.subheader("📌 Business Insights")

best_brand = brand_revenue.sort_values(by="Revenue", ascending=False).iloc[0]["Brand"]
st.success(f"🏆 Top Performing Brand: {best_brand}")

best_campaign = filtered_df.groupby("Campaign_Type")["Revenue"].mean().idxmax()
st.info(f"📢 Best Campaign Type: {best_campaign}")

best_roi = round(filtered_df["ROI"].max(), 2)
st.warning(f"💰 Highest ROI Observed: {best_roi}")

# =========================================
# PREDICTION SECTION
# =========================================

st.subheader("⚡ Instant Campaign Prediction")

col_a, col_b = st.columns(2)

with col_a:
    input_impressions = st.number_input("Impressions", min_value=0, value=50000)
    input_clicks = st.number_input("Clicks", min_value=0, value=5000)
    input_leads = st.number_input("Leads", min_value=0, value=2000)

with col_b:
    input_conversions = st.number_input("Conversions", min_value=0, value=1000)
    input_cost = st.number_input("Acquisition Cost (₹)", min_value=0.0, value=200.0)
    input_duration = st.number_input("Duration (days)", min_value=1, value=15)

input_engagement = st.slider("Engagement Score", 0.0, 100.0, 10.0)

selected_channels = st.multiselect(
    "Select Channels Used",
    options=list(mlb.classes_),
    default=["YouTube", "Instagram"]
)

if st.button("⚡ Predict Now"):

    if not selected_channels:
        st.warning("Please select at least one channel.")
    else:
        input_data = pd.DataFrame({
            "Impressions": [input_impressions],
            "Clicks": [input_clicks],
            "Leads": [input_leads],
            "Conversions": [input_conversions],
            "Acquisition_Cost": [input_cost],
            "Duration": [input_duration],
            "Engagement_Score": [input_engagement],
        })

        ch_encoded = pd.DataFrame(
            mlb.transform([selected_channels]),
            columns=mlb.classes_
        )

        input_data = pd.concat([input_data, ch_encoded], axis=1)

        for col in reg_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        input_reg = input_data[reg_columns]

        for col in clf_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        input_clf = input_data[clf_columns]

        predicted_revenue = reg_model.predict(input_reg)[0]
        estimated_profit = predicted_revenue - input_cost
        predicted_status = clf_model.predict(input_clf)[0]

        st.markdown("---")
        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("💰 Predicted Revenue", f"₹{round(predicted_revenue, 2):,}")
        with r2:
            st.metric("📉 Estimated Profit", f"₹{round(estimated_profit, 2):,}")
        with r3:
            if predicted_status == 1 and estimated_profit > 0:
                st.success("✅ Campaign Status: PROFITABLE")
            else:
                st.error("❌ Campaign Status: LOSS")

st.success("🎯 Dashboard Running Successfully!")
=======
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
>>>>>>> 785510a0f3a9894c28f693aff6eb44e98ce1737a
