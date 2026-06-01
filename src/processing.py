import pandas as pd


def load_data(path):
    df = pd.read_csv(path, engine="python", on_bad_lines="skip")
    return df


def clean_data(df):
    df = df.copy()
    return df


def get_metrics(df):
    total_movies = df.shape[0]
    return total_movies
