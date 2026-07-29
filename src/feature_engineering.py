import pandas as pd


def create_features(df):

    df["Date"] = pd.to_datetime(df["Date"])

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
    df["Quarter"] = df["Date"].dt.quarter
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Weekend"] = (df["DayOfWeek"] >= 5).astype(int)

    df["Lag_1"] = df.groupby(
        ["Store", "Dept"]
    )["Weekly_Sales"].shift(1)

    df["Lag_2"] = df.groupby(
        ["Store", "Dept"]
    )["Weekly_Sales"].shift(2)

    df["Rolling_Mean_4"] = (
        df.groupby(["Store", "Dept"])["Weekly_Sales"]
        .transform(lambda x: x.rolling(4).mean())
    )

    df["Rolling_STD_4"] = (
        df.groupby(["Store", "Dept"])["Weekly_Sales"]
        .transform(lambda x: x.rolling(4).std())
    )

    df["Total_Markdown"] = (
        df["MarkDown1"]
        + df["MarkDown2"]
        + df["MarkDown3"]
        + df["MarkDown4"]
        + df["MarkDown5"]
    )

    df["Sales_per_Size"] = df["Weekly_Sales"] / df["Size"]

    df = pd.get_dummies(df, columns=["Type"], drop_first=True)

    df = df.fillna(0)

    return df