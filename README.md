# 🛒 AI Retail Demand Forecasting

## Overview

This project predicts weekly retail sales using Machine Learning (XGBoost).

The dashboard allows users to:

- View historical sales
- Explore interactive charts
- Enter forecast details
- Predict future weekly sales
- Download prediction results

---

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Scikit-learn
- XGBoost
- Matplotlib
- Plotly

---

## Project Structure

```
Retail_Demand_Forecasting/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── xgboost.pkl
│
├── notebooks/
│   ├── 01_Data_Loading.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_Feature_Engineering.ipynb
│   ├── 05_Model_Training.ipynb
│   ├── 06_Model_Evaluation.ipynb
│   └── 07_Feature_Importance.ipynb
│
├── images/
├── README.md
├── requirements.txt
└── Dockerfile
```

---

## Dashboard Features

- KPI Cards
- Historical Sales Chart
- Monthly Sales Chart
- Holiday Sales Chart
- Temperature vs Sales
- Top 10 Sales
- Sales Forecast
- Prediction History
- CSV Download

---

## Machine Learning Model

- XGBoost Regressor

### Performance

- R² Score: 0.9976
- MAE: 407.55
- RMSE: 1114.27

---

## Run the Project

```bash
pip install -r requirements.txt
```

```bash
streamlit run dashboard/app.py
```

---

## Author

Manogaran P