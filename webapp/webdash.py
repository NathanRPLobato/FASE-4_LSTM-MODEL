# webapp/webdash.py
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import yfinance as yf
import requests
import plotly.graph_objs as go
import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import time

# URL da sua API Flask
API_URL = "http://127.0.0.1:5000/predict"

# Inicializa o app Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Previsão de Ações"
)

app.layout = dbc.Container([
    html.H1("Previsão de Preço de Ações com LSTM", className="text-center my-4"),

    dbc.Row([
        dbc.Col([
            dbc.Input(id="input-ticker", placeholder="Digite o ticker da ação (ex: PETR4.SA)", type="text")
        ], width=8),

        dbc.Col([
            dbc.Button("Prever", id="btn-predict", color="primary")
        ], width=4)
    ], className="mb-3"),

    html.Div(id="output-prediction", className="fs-4 text-success mb-3"),
    dcc.Graph(id="price-graph"),

    html.Hr(),
    html.H4("Métricas do Modelo (MAE & RMSE)", className="mt-4"),
    html.Div(id="model-metrics", className="fs-5 text-dark mb-3"),

    html.H4("Tempo de Resposta da API", className="mt-4"),
    html.Div(id="api-timing", className="fs-5 text-primary")
])

@app.callback(
    Output("output-prediction", "children"),
    Output("price-graph", "figure"),
    Output("model-metrics", "children"),
    Output("api-timing", "children"),
    Input("btn-predict", "n_clicks"),
    State("input-ticker", "value"),
    prevent_initial_call=True
)
def prever_acao(n_clicks, ticker):
    if not ticker:
        return "Por favor, digite o ticker da ação.", go.Figure(), "", ""

    try:
        ticker = ticker.strip().upper()
        df = yf.download(ticker, period="3mo", interval="1d")

        if df.empty or len(df) < 60:
            return "Erro: dados insuficientes para esta ação.", go.Figure(), "", ""

        start_time = time.time()
        response = requests.post(API_URL, json={"ticker": ticker})
        elapsed_time = time.time() - start_time

        if response.status_code != 200:
            return f"Erro da API: {response.status_code}", go.Figure(), "", f"{elapsed_time:.3f} segundos"

        result = response.json()
        prediction = result.get("predicted_close_price")
        if prediction is None:
            return "Erro: resposta inválida da API.", go.Figure(), "", f"{elapsed_time:.3f} segundos"

        # Avaliação do modelo (apenas local, com o mesmo CSV base)
        df_csv = pd.read_csv("app/data/finance_data.csv", index_col=0)
        df_csv['Close'] = pd.to_numeric(df_csv['Close'], errors='coerce')
        df_csv.dropna(subset=['Close'], inplace=True)
        last_60 = df_csv['Close'].values[-60:]

        data = df_csv['Close'].values.reshape(-1, 1)

        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)

        X, y = [], []
        for i in range(60, len(data_scaled)):
            X.append(data_scaled[i-60:i])
            y.append(data_scaled[i])
        X, y = np.array(X), np.array(y)

        from tensorflow.keras.models import load_model
        model = load_model("app/models/lstm_model.h5")
        predictions = model.predict(X)

        predicted_prices = scaler.inverse_transform(predictions)
        true_prices = scaler.inverse_transform(y)

        mae = mean_absolute_error(true_prices, predicted_prices)
        rmse = np.sqrt(mean_squared_error(true_prices, predicted_prices))


        metrics_text = f"MAE: {mae:.2f} | RMSE: {rmse:.2f}"
        timing_text = f"{elapsed_time:.3f} segundos"

        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=last_60, mode="lines+markers", name="Histórico"))
        fig.add_trace(go.Scatter(y=[None]*59 + [prediction], mode="markers+text", name="Previsão",
                                 marker=dict(size=12, color="red"),
                                 text=["Previsão"]*60, textposition="top center"))
        fig.update_layout(title=f"Histórico de Fechamento - {ticker}",
                          xaxis_title="Dias",
                          yaxis_title="Preço (R$)",
                          template="plotly_white")

        return f"Previsão de fechamento para {ticker}: R$ {round(prediction, 2)}", fig, metrics_text, timing_text

    except Exception as e:
        return f"Erro: {str(e)}", go.Figure(), "", ""

if __name__ == "__main__":
    app.run(debug=True, port=8050)
