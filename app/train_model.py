import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib

# --- CONFIGURAÇÕES ---
data_path = 'app/data/data_scaled.npy'
model_path = 'app/models/lstm_model.h5'
scaler_path = 'app/models/scaler.gz'
sequence_length = 60  # nº de dias anteriores usados para prever o próximo

# --- CARREGAR OS DADOS ESCALADOS ---
data = np.load(data_path)

# --- GERAR SEQUÊNCIAS PARA LSTM ---
def create_sequences(data, seq_len):
    X, y = [], []
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i])
        y.append(data[i])
    return np.array(X), np.array(y)

X, y = create_sequences(data, sequence_length)

print("Shape das sequências de entrada (X):", X.shape)
print("Shape dos rótulos (y):", y.shape)

# --- DEFINIR MODELO LSTM ---
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))  # saída: valor de fechamento previsto

model.compile(optimizer='adam', loss='mean_squared_error')

# --- TREINAR MODELO ---
early_stop = EarlyStopping(monitor='loss', patience=5)

model.fit(X, y, epochs=50, batch_size=32, callbacks=[early_stop], verbose=1)

# --- SALVAR MODELO ---
os.makedirs(os.path.dirname(model_path), exist_ok=True)
model.save(model_path)

print("Modelo treinado e salvo com sucesso em:", model_path)
