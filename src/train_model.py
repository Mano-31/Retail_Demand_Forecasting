import pandas as pd
import joblib
from xgboost import XGBRegressor


def train_model(df):

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

    X = df[features]
    y = df["Weekly_Sales"]

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, "../models/xgboost.pkl")

    print("Model saved successfully!")