# prepare_data.py
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
import os

def prepare_data(csv_path='app/data/finance_data.csv', scaler_path='app/models/scaler.gz'):
    df = pd.read_csv(csv_path, index_col=0)

    if 'Close' not in df.columns:
        raise ValueError("A coluna 'Close' não foi encontrada no arquivo CSV.")

    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df.dropna(subset=['Close'], inplace=True)

    data = df['Close'].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(scaler, scaler_path)

    return data_scaled, scaler
