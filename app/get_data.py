import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def download_data():
    ticker = "AAPL"
    start_date = datetime.now() - timedelta(days=365 * 3)
    end_date = datetime.now()

    df = yf.download(ticker, start=start_date, end=end_date)

    # Cria diretório se não existir
    os.makedirs("app/data", exist_ok=True)

    # Salva CSV com caminho seguro
    df.to_csv("app/data/finance_data.csv")
    print("Dados salvos com sucesso!")

download_data()
