import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    layout="wide"
)

st.title("📊 Marketing Campaign Performance Dashboard")

# ==============================
# LOAD DATA
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

# ==============================
# DATA CLEANING
# ==============================

df = df.drop_duplicates()
df = df.fillna(0)

# ==============================
# DATA PREVIEW
# ==============================

st.subheader("📁 Dataset Preview")

st.dataframe(df.head())

# ==============================
# BASIC INFO
# ==============================

st.subheader("📌 Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

# ==============================
# ROI DISTRIBUTION
# ==============================

if "ROI" in df.columns:

    st.subheader("📈 ROI Distribution")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.histplot(df["ROI"], bins=30, ax=ax)

    ax.set_title("ROI Distribution")

    st.pyplot(fig)

# ==============================
# CAMPAIGN TYPE COUNT
# ==============================

if "Campaign_Type" in df.columns:

    st.subheader("📊 Campaign Type Count")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(x=df["Campaign_Type"], ax=ax)

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ==============================
# CHANNEL USED ANALYSIS
# ==============================

if "Channel_Used" in df.columns:

    st.subheader("📢 Channel Used Analysis")

    fig, ax = plt.subplots(figsize=(8,5))

    sns.countplot(x=df["Channel_Used"], ax=ax)

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ==============================
# SUMMARY STATISTICS
# ==============================

st.subheader("📋 Summary Statistics")

st.dataframe(df.describe())

st.success("✅ Dashboard Loaded Successfully!")