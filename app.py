import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pickle

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide"
)

st.title("📊 Marketing Campaign Performance Dashboard")

# =========================================
# LOAD MODELS
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
    st.error("❌ Model files not found! Run notebook first.")
    st.stop()

reg_model, clf_model, reg_columns, clf_columns, mlb, label_encoders = load_models()
st.success("✅ Models Loaded Successfully!")

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    data_path = "Data"
    all_data = []

    if not os.path.exists(data_path):
        st.error("❌ Data folder not found!")
        return pd.DataFrame()

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

    if len(all_data) == 0:
        return pd.DataFrame()

    df = pd.concat(all_data, ignore_index=True)
    df.drop_duplicates(inplace=True)

    # SAFE missing value handling (FIXED ERROR HERE)
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")

    # Feature engineering
    if "Revenue" in df.columns and "Acquisition_Cost" in df.columns:
        df["ROI"] = (df["Revenue"] - df["Acquisition_Cost"]) / (df["Acquisition_Cost"] + 1)
        df["Profit_Flag"] = np.where(df["ROI"] > 0, 1, 0)

    return df


df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# =========================================
# SIDEBAR FILTERS
# =========================================
st.sidebar.header("📌 Filters")

brand_filter = st.sidebar.selectbox(
    "Select Brand",
    ["All"] + list(df["Brand"].dropna().unique())
)

campaign_list = sorted(df["Campaign_Type"].dropna().astype(str).unique())
campaign_filter = st.sidebar.selectbox(
    "Select Campaign Type",
    ["All"] + list(campaign_list)
)

filtered_df = df.copy()

if brand_filter != "All":
    filtered_df = filtered_df[filtered_df["Brand"] == brand_filter]

if campaign_filter != "All":
    filtered_df = filtered_df[filtered_df["Campaign_Type"].astype(str) == campaign_filter]

# =========================================
# KPI SECTION (SAFE)
# =========================================
st.subheader("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Campaigns", len(filtered_df))

with col2:
    st.metric("Total Revenue", f"₹{filtered_df['Revenue'].sum():,.2f}" if "Revenue" in filtered_df else "0")

with col3:
    st.metric("Average ROI", round(filtered_df["ROI"].mean(), 2) if "ROI" in filtered_df else 0)

with col4:
    st.metric("Total Conversions", int(filtered_df["Conversions"].sum()) if "Conversions" in filtered_df else 0)

# =========================================
# DATA PREVIEW
# =========================================
st.subheader("📁 Dataset Preview")
st.dataframe(filtered_df.head())

# =========================================
# CHARTS (SAFE)
# =========================================
if "ROI" in filtered_df:

    st.subheader("📊 ROI Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["ROI"], bins=30, ax=ax)
    st.pyplot(fig)

if "Campaign_Type" in filtered_df:

    st.subheader("📢 Campaign Type Analysis")
    fig, ax = plt.subplots()
    sns.countplot(x=filtered_df["Campaign_Type"], ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

if "Brand" in filtered_df and "Revenue" in filtered_df:

    st.subheader("💰 Brand-wise Revenue")
    brand_revenue = filtered_df.groupby("Brand")["Revenue"].sum().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=brand_revenue, x="Brand", y="Revenue", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# =========================================
# FIXED ERROR SECTION (IMPORTANT)
# =========================================
st.subheader("📌 Insights")

if "Brand" in filtered_df and "Revenue" in filtered_df and len(filtered_df) > 0:
    brand_revenue = filtered_df.groupby("Brand")["Revenue"].sum().reset_index()

    if len(brand_revenue) > 0:
        best_brand = brand_revenue.sort_values("Revenue", ascending=False).iloc[0]["Brand"]
        st.success(f"🏆 Top Brand: {best_brand}")
    else:
        st.warning("No brand data available")

if "Campaign_Type" in filtered_df:
    best_campaign = filtered_df.groupby("Campaign_Type")["Revenue"].mean().idxmax()
    st.info(f"📢 Best Campaign Type: {best_campaign}")

if "ROI" in filtered_df:
    st.warning(f"💰 Highest ROI: {filtered_df['ROI'].max():.2f}")

# =========================================
# PREDICTION SECTION (SAFE)
# =========================================
st.subheader("⚡ Prediction")

input_impressions = st.number_input("Impressions", 0, value=50000)
input_clicks = st.number_input("Clicks", 0, value=5000)
input_leads = st.number_input("Leads", 0, value=2000)
input_conversions = st.number_input("Conversions", 0, value=1000)
input_cost = st.number_input("Cost", 0.0, value=200.0)
input_duration = st.number_input("Duration", 1, value=15)
input_engagement = st.slider("Engagement Score", 0.0, 100.0, 10.0)

selected_channels = st.multiselect(
    "Channels",
    options=list(mlb.classes_) if mlb else [],
    default=["YouTube", "Instagram"] if mlb else []
)

if st.button("Predict"):

    if len(selected_channels) == 0:
        st.warning("Select at least one channel")
        st.stop()

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
        if col not in input_data:
            input_data[col] = 0
    input_reg = input_data[reg_columns]

    for col in clf_columns:
        if col not in input_data:
            input_data[col] = 0
    input_clf = input_data[clf_columns]

    predicted_revenue = reg_model.predict(input_reg)[0]
    estimated_profit = predicted_revenue - input_cost
    predicted_status = clf_model.predict(input_clf)[0]

    st.metric("Predicted Revenue", f"₹{predicted_revenue:,.2f}")
    st.metric("Estimated Profit", f"₹{estimated_profit:,.2f}")

    if predicted_status == 1 and estimated_profit > 0:
        st.success("PROFITABLE CAMPAIGN")
    else:
        st.error("LOSS CAMPAIGN")

st.success("🎯 Dashboard Running Successfully!")