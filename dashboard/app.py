import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="AI Retail Demand Forecasting",
    layout="wide"
)

st.markdown("""
<h1 style='text-align:center;
           color:#2E86C1;
           margin-top:0px;
           margin-bottom:5px;'>
🛒 AI Retail Demand Forecasting
</h1>

<h3 style='text-align:center;
           color:gray;
           margin-top:0px;
           margin-bottom:50px;'>
AI-powered Retail Sales Forecasting using XGBoost
</h3>
""", unsafe_allow_html=True)


# ------------------------------
# File Paths
# ------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "retail_featured.csv")

# ------------------------------
# Load Model & Data
# ------------------------------
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])

# =====================================================
# KPI Cards (Paste Here)
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🏪 Total Stores", df["Store"].nunique())

with col2:
    st.metric("📦 Departments", df["Dept"].nunique())

with col3:
    st.metric(
        "💰 Total Sales",
        f"${df['Weekly_Sales'].sum():,.0f}"
    )

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.header("Select Store & Department")

store = st.sidebar.selectbox(
    "Store",
    sorted(df["Store"].unique())
)

dept = st.sidebar.selectbox(
    "Department",
    sorted(df["Dept"].unique())
)

# ------------------------------
# Filter Data
# ------------------------------
filtered = df[
    (df["Store"] == store) &
    (df["Dept"] == dept)
].sort_values("Date")

# ------------------------------
# Historical Sales
# ------------------------------
st.subheader("Historical Sales")

chart = filtered.set_index("Date")[["Weekly_Sales"]]

st.line_chart(chart)

# Monthely sales Trend

st.subheader("Monthly Sales Trend")

monthly = (
    filtered.groupby("Month")["Weekly_Sales"]
    .mean()
    .reset_index()
)

st.line_chart(monthly.set_index("Month"))

# Holiday vs Non-Holiday Sales
st.subheader("Holiday vs Non-Holiday Sales")

holiday_sales = (
    filtered.groupby("IsHoliday")["Weekly_Sales"]
    .mean()
    .reset_index()
)

holiday_sales["IsHoliday"] = holiday_sales["IsHoliday"].map({
    0: "Non-Holiday",
    1: "Holiday",
    False: "Non-Holiday",
    True: "Holiday"
})

st.bar_chart(
    holiday_sales.set_index("IsHoliday")
)

# Monthely Average Sales

st.subheader("Average Sales by Month")

month_sales = (
    filtered.groupby("Month")["Weekly_Sales"]
    .mean()
)

st.bar_chart(month_sales)

# Sales Distribution

st.subheader("Sales Distribution")

st.area_chart(filtered.set_index("Date")["Weekly_Sales"])

# Temperature vs Sales

st.subheader("Temperature vs Sales")

temp = filtered[["Temperature", "Weekly_Sales"]]
st.scatter_chart(temp)

# Markdown Impact

st.subheader("Markdown vs Sales")

markdown = filtered[
    ["MarkDown1", "Weekly_Sales"]
]

st.scatter_chart(markdown)

# ==============================
# STEP 8: Sales Insights (PASTE HERE)
# ==============================

st.subheader("Sales Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Weekly Sales",
        f"${filtered['Weekly_Sales'].mean():,.2f}"
    )

with col2:
    st.metric(
        "Maximum Weekly Sales",
        f"${filtered['Weekly_Sales'].max():,.2f}"
    )

with col3:
    st.metric(
        "Minimum Weekly Sales",
        f"${filtered['Weekly_Sales'].min():,.2f}"
    )

# Top 10 Highest Sales

st.subheader("Top 10 Highest Weekly Sales")

top_sales = filtered.nlargest(10, "Weekly_Sales")

st.dataframe(
    top_sales[["Date", "Weekly_Sales"]]
)

# Holiday Sales Pie Chart

st.subheader("Holiday Sales Distribution")

holiday = (
    filtered.groupby("IsHoliday")
    .Weekly_Sales.sum()
    .reset_index()
)

holiday["IsHoliday"] = holiday["IsHoliday"].replace(
    {0:"Non-Holiday",1:"Holiday",False:"Non-Holiday",True:"Holiday"}
)

fig = px.pie(
    holiday,
    names="IsHoliday",
    values="Weekly_Sales"
)

st.plotly_chart(fig, use_container_width=True)

# Sales by Month

st.subheader("Monthly Sales")

month_sales = (
    filtered.groupby("Month")
    .Weekly_Sales.sum()
)

st.bar_chart(month_sales)

# Download Filtered Data

csv = filtered.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_sales.csv",
    "text/csv"
)
    
# ------------------------------
# Latest Records
# ------------------------------
st.subheader("Latest Records")

st.dataframe(filtered.tail())


# ==================================
# STEP 9 (Paste Here)
# ==================================

st.subheader("Top 10 Highest Weekly Sales")

top_sales = filtered.nlargest(10, "Weekly_Sales")

st.dataframe(
    top_sales[
        [
            "Date",
            "Weekly_Sales",
            "Temperature",
            "Fuel_Price"
        ]
    ]
)


# ------------------------------
# ------------------------------
# Prediction
# ------------------------------

st.subheader("Sales Forecast")

latest = filtered.tail(1).copy()

features = [
    'Store',
    'Dept',
    'IsHoliday',
    'Temperature',
    'Fuel_Price',
    'MarkDown1',
    'MarkDown2',
    'MarkDown3',
    'MarkDown4',
    'MarkDown5',
    'CPI',
    'Unemployment',
    'Size',
    'Year',
    'Month',
    'Week',
    'Quarter',
    'Day',
    'DayOfWeek',
    'Weekend',
    'Lag_1',
    'Lag_2',
    'Rolling_Mean_4',
    'Rolling_STD_4',
    'Total_Markdown',
    'Sales_per_Size',
    'Type_B',
    'Type_C'
]

st.write("### Enter Forecast Details")

year = st.selectbox(
    "Year",
    [2012, 2013, 2014, 2015, 2016, 2017]
)

month = st.selectbox(
    "Month",
    list(range(1,13))
)

week = st.number_input(
    "Week Number",
    min_value=1,
    max_value=53,
    value=1
)

holiday = st.selectbox(
    "Holiday",
    ["No","Yes"]
)

holiday = 1 if holiday=="Yes" else 0

# Create prediction history
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Predict Sales"):

    input_data = latest[features].copy()

    input_data["Year"] = year
    input_data["Month"] = month
    input_data["Week"] = week
    input_data["IsHoliday"] = holiday

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Weekly Sales: ${prediction:,.2f}")

# Save prediction
    st.session_state.history.append({
        "Store": store,
        "Department": dept,
        "Year": year,
        "Month": month,
        "Week": week,
        "Holiday": holiday,
        "Prediction ($)": round(prediction, 2)
    })

# Show prediction history
if st.session_state.history:
    st.subheader("Prediction History")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)

if st.session_state.history:

    csv = history_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Predictions",
        data=csv,
        file_name="predictions.csv",
        mime="text/csv"
    )

# ============================================================
# PROJECT FOOTER
# ============================================================

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:20px;">

<h3 style="color:#2E86C1;">
🛒 AI Retail Demand Forecasting
</h3>

<p>
Machine Learning Dashboard using
<b>Python, Pandas, Streamlit and XGBoost</b>
</p>

<p>
Developed as a Final Year Machine Learning Project
</p>

<p>
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)