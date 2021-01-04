import pandas as pd
from app.core import config


def get_impressions_data_frame(index=1):
    return pd.read_csv(
        f'{config.CSV_FILES_PATH}/{index}/impressions_{index}.csv'
    )


def get_clicks_data_frame(index=1):
    return pd.read_csv(f'{config.CSV_FILES_PATH}/{index}/clicks_{index}.csv')


def get_conversions_data_frame(index=1):
    return pd.read_csv(
        f'{config.CSV_FILES_PATH}/{index}/conversions_{index}.csv'
    )
