import numpy as np
import joblib
from tensorflow.keras.models import load_model
from app.utils.data_utils import prepare_input

model = load_model("app/model/lstm_model.keras")
scaler = joblib.load("app/model/scaler.gz")

def predict_prices(data):
    X = prepare_input(data, scaler)
    pred = model.predict(X)
    result = scaler.inverse_transform(pred)
    return result.flatten().tolist()
