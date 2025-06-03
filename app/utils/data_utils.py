import numpy as np
import pandas as pd

def prepare_input(data, scaler, window_size=60):
    df = pd.DataFrame(data)
    df_scaled = scaler.transform(df)
    X = []
    for i in range(len(df_scaled) - window_size + 1):
        X.append(df_scaled[i:i + window_size])
    return np.array(X)
