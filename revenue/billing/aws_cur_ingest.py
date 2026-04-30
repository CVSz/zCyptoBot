import pandas as pd


def load_cur(path: str):
    df = pd.read_csv(path)
    return df[["lineItem/UsageAmount", "lineItem/BlendedCost"]]


def total_cost(df):
    return float(df["lineItem/BlendedCost"].sum())
