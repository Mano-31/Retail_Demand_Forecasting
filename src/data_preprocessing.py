import pandas as pd


def load_data(train_path, stores_path, features_path):
    """
    Load Walmart dataset.
    """

    train = pd.read_csv(train_path)
    stores = pd.read_csv(stores_path)
    features = pd.read_csv(features_path)

    return train, stores, features


def merge_data(train, stores, features):
    """
    Merge all datasets.
    """

    df = train.merge(stores, on="Store", how="left")
    df = df.merge(features, on=["Store", "Date", "IsHoliday"], how="left")

    return df


def clean_data(df):
    """
    Fill missing values.
    """

    markdown_cols = [
        "MarkDown1",
        "MarkDown2",
        "MarkDown3",
        "MarkDown4",
        "MarkDown5"
    ]

    for col in markdown_cols:
        df[col] = df[col].fillna(0)

    df["CPI"] = df["CPI"].fillna(df["CPI"].median())
    df["Unemployment"] = df["Unemployment"].fillna(df["Unemployment"].median())

    return df