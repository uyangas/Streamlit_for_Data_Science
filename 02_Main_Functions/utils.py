import pandas as pd
import numpy as np


def process_data(df):
    # convert date to YYYY-MM-DD format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], format="YYYY-MM-DD")
    # convert the transaction time to H-M-S format
    df['transaction_time'] = pd.to_datetime(df['transaction_time'], format="%H:%M:%S").dt.time

    return df
