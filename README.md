<<<<<<< HEAD
# 📊 Multi-Brand Marketing Campaign Performance Analysis & Prediction

## 📌 Project Overview

This project focuses on analyzing and predicting the performance of marketing campaigns across multiple beauty brands including Nykaa, Purplle, and Tira.

The system combines Data Analytics, Machine Learning, and Interactive Dashboarding to generate business insights, evaluate campaign effectiveness, predict future campaign revenue, and classify campaign profitability.

The project follows a complete end-to-end Data Science workflow including data preprocessing, feature engineering, exploratory data analysis, machine learning model development, model evaluation, and deployment using Streamlit.

---

## 🚀 Technologies Used

* Python
* Pandas
* NumPy
* Scikit-Learn
* Matplotlib
* Seaborn
* Streamlit
* Pickle

---

## 📊 Key Features

### Data Analytics

* Multi-Brand Campaign Analysis
* Data Cleaning & Preprocessing
* Missing Value Handling
* Duplicate Removal
* Exploratory Data Analysis (EDA)

### Feature Engineering

* ROI Calculation
* Profit Flag Creation
* Marketing Channel Encoding
* Label Encoding for Categorical Variables

### Machine Learning

#### Revenue Prediction

* Random Forest Regressor
* Revenue Forecasting

#### Profitability Prediction

* Random Forest Classifier
* Profit / Loss Classification

### Dashboard Features

* Brand Filters
* Campaign Filters
* KPI Metrics
* Revenue Analysis
* ROI Analysis
* Correlation Heatmap
* Business Insights
* SQL-style Analytical Reports
* Instant Campaign Prediction

---

## 📁 Project Structure

```bash
Marketing_Campaign_project
│
├── Data/
│
├── notebooks/
│   └── marketing_analysis.ipynb
│
├── models/
│   ├── reg_model.pkl
│   ├── clf_model.pkl
│   ├── reg_columns.pkl
│   ├── clf_columns.pkl
│   ├── mlb_encoder.pkl
│   └── label_encoders.pkl
│
├── app.py
├── requirements.txt
├── README.md
├── Marketing Campaign Presentation.pptx
└── Marketing Campaign Performance Prediction.pdf
```

---

## 🤖 Machine Learning Workflow

### Data Collection

* Load multiple campaign datasets
* Merge datasets into a unified dataframe

### Data Preprocessing

* Handle missing values
* Remove duplicates
* Transform categorical features

### Feature Engineering

* ROI Calculation
* Profit Flag Generation

### Model Building

#### Regression Model

* Random Forest Regressor
* Revenue Prediction

#### Classification Model

* Random Forest Classifier
* Profitability Prediction

### Model Evaluation

#### Regression Metrics

* MAE
* MSE
* RMSE
* R² Score

#### Classification Metrics

* Accuracy
* Precision
* Recall
* Confusion Matrix
* Classification Report

---

## 📈 Dashboard Components

### KPI Section

* Total Campaigns
* Total Revenue
* Average ROI
* Total Conversions

### Visual Analytics

* ROI Distribution
* Campaign Type Analysis
* Brand Revenue Analysis
* Correlation Heatmap

### Business Insights

* Top Performing Brand
* Best Campaign Type
* Highest ROI Campaign

### Prediction Module

Predict:

* Expected Revenue
* Estimated Profit
* Campaign Profitability Status

using user-provided campaign inputs.

---

## ⚡ Performance Optimization

To improve dashboard performance:

* Trained models are saved as Pickle Files
* Dashboard loads pre-trained models instantly
* No model retraining occurs during dashboard execution

This significantly reduces loading time and improves user experience.

---

## ▶️ How to Run

### Step 1

Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2

Run the Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 🎯 Business Outcomes

* Identified high-performing marketing channels
* Evaluated campaign profitability
* Predicted future campaign revenue
* Generated actionable business insights
* Built an interactive analytics dashboard

---

## 👨‍💻 Author

Thaheer



---

## 🌟 Conclusion

This project demonstrates a complete end-to-end Marketing Analytics and Machine Learning solution that transforms raw campaign data into actionable business insights through predictive modeling and interactive visualization.
=======
📊 Multi-Brand Marketing Campaign Performance Analysis and Prediction

📌 Project Overview

This project focuses on analyzing and predicting the performance of multi-brand marketing campaigns using Python, Machine Learning, and Streamlit.

The raw campaign datasets are cleaned, transformed, and analyzed to generate meaningful business insights. Machine learning techniques are used to predict campaign performance, while an interactive Streamlit dashboard provides visual analytics and reporting.

The system helps understand campaign effectiveness, ROI trends, customer engagement, and marketing channel performance.



🚀 Tech Stack

- Python (Pandas, NumPy) – Data cleaning & preprocessing
- Scikit-learn – Machine Learning model building
- Matplotlib & Seaborn – Data visualization
- Streamlit – Interactive dashboard development

---

 📊 Key Features

✔ Multi-CSV Dataset Integration  
✔ Data Cleaning & Preprocessing  
✔ Missing Value Handling  
✔ Feature Engineering (ROI & Profit Flag)  
✔ Machine Learning Prediction Model  
✔ Model Evaluation Metrics  
✔ Exploratory Data Analysis (EDA)  
✔ Interactive Streamlit Dashboard  
✔ Feature Importance Analysis  
✔ Marketing Performance Visualization  

---

📁 Project Structure

```bash
📦 Marketing_Campaign_project
 ┣ 📂 Data/
 ┃ ┣ nykaa_campaign_data_with_nulls.csv
 ┃ ┣ purplle_campaign_data_with_nulls.csv
 ┃ ┗ other campaign datasets
 ┣ 📄 app.py
 ┣ 📄 db.py
 ┣ 📄 requirements.txt
 ┣ 📄 README.md
 ┣ 📄 Marketing Campaign Presentation.pptx
 ┗ 📄 Marketing Campaign Performance Prediction.docx.pdf
⚙️ How to Run the Project
1️⃣ Install Dependencies
pip install -r requirements.txt
2️⃣ Run Machine Learning Pipeline
python app.py
3️⃣ Launch Streamlit Dashboard
streamlit run db.py
🤖 Machine Learning Workflow
🔹 Data Processing
CSV file loading
Dataset merging
Duplicate removal
Missing value handling
🔹 Feature Engineering
ROI Calculation
Profit Flag Generation
🔹 Machine Learning
Random Forest Regressor
Train-Test Split
Prediction Model
🔹 Model Evaluation
Mean Absolute Error (MAE)
Mean Squared Error (MSE)
R² Score
📊 Exploratory Data Analysis

The project includes visual analysis for:

📈 ROI Distribution
📊 Campaign Type Analysis
📢 Channel Used Analysis
⭐ Feature Importance Visualization

📈 Dashboard Features

The Streamlit dashboard provides:

✔ Dataset Preview
✔ Interactive Graphs
✔ ROI Visualization
✔ Campaign Analytics
✔ Channel Performance Analysis
✔ Summary Statistics

🔥 Key Insights

📊 Revenue and Acquisition Cost are the most influential campaign features
📈 ROI analysis helps identify high-performing campaigns
📢 Marketing channel analysis reveals engagement trends
⭐ Feature importance highlights business-driving factors
📉 Campaign performance varies across customer segments

🎯 Project Outcome

✔ Cleaned and processed campaign datasets
✔ Built an end-to-end machine learning pipeline
✔ Generated analytical insights using EDA
✔ Created an interactive Streamlit dashboard
✔ Developed a complete marketing analytics application

📌 Future Enhancements
SQL database integration
Advanced ML algorithms
Real-time campaign tracking
Interactive dashboard filters
Cloud deployment using Streamlit Cloud
👨‍💻 Presented By

Thaheer

🌟 Conclusion

This project demonstrates a complete end-to-end marketing analytics workflow including preprocessing, machine learning, data visualization, feature engineering, and dashboard development using Python and Streamlit.
>>>>>>> 785510a0f3a9894c28f693aff6eb44e98ce1737a
