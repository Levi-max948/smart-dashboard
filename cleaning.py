import pandas as pd

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(df.mean(numeric_only=True))
    return df