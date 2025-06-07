from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
from datetime import datetime, timedelta
import yfinance as yf
import os

from prepare_data import prepare_data

app = Flask(__name__)

model = load_model("app/models/lstm_model.h5")
SEQ_LEN = 120
CSV_PATH = "app/data/finance_data.csv"
SCALER_PATH = "app/models/scaler.gz"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or 'ticker' not in data:
        return jsonify({"error": "Ticker não fornecido no corpo da requisição."}), 400

    ticker = data['ticker'].upper()
    end = datetime.today()
    start = end - timedelta(days=SEQ_LEN * 2)

    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    if df.empty:
        return jsonify({"error": f"Nenhum dado encontrado para o ticker {ticker}."}), 404

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    df.to_csv(CSV_PATH)

    try:
        data_scaled, scaler = prepare_data(csv_path=CSV_PATH, scaler_path=SCALER_PATH)
    except Exception as e:
        return jsonify({"error": f"Erro no processamento dos dados: {str(e)}"}), 500

    if data_scaled.shape[0] < SEQ_LEN:
        return jsonify({"error": "Não há dados suficientes para previsão."}), 400

    sequence = data_scaled[-SEQ_LEN:].reshape(1, SEQ_LEN, 1)
    prediction = model.predict(sequence)
    predicted_price = scaler.inverse_transform(prediction)[0][0]

    return jsonify({
        "ticker": ticker,
        "predicted_close_price": round(float(predicted_price), 2)
    })

@app.route("/")
def index():
    return "API de Previsão de Preço com LSTM está no ar!"

if __name__ == "__main__":
    app.run(debug=True)
