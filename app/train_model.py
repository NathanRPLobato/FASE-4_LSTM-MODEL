import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Configurações
data_path = 'app/data/data_scaled.npy'
model_path = 'app/models/lstm_model.h5'
sequence_length = 120

data = np.load(data_path)

def create_sequences(data, seq_len):
    X, y = [], []
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i])
        y.append(data[i])
    return np.array(X), np.array(y)

X, y = create_sequences(data, sequence_length)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Callback para calcular MAE e RMSE após cada época no conjunto de validação
class MetricsCallback(Callback):
    def __init__(self, validation_data):
        super().__init__()
        self.X_val, self.y_val = validation_data

    def on_epoch_end(self, epoch, logs=None):
        preds = self.model.predict(self.X_val)
        mae = mean_absolute_error(self.y_val, preds)
        mse = mean_squared_error(self.y_val, preds)
        rmse = mse ** 0.5
        print(f" — Val MAE: {mae:.4f} | Val RMSE: {rmse:.4f}")

# Dividir dados para treino e validação manualmente
val_split = 0.1
val_size = int(len(X) * val_split)
X_train, X_val = X[:-val_size], X[-val_size:]
y_train, y_val = y[:-val_size], y[-val_size:]

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))

optimizer = Adam(learning_rate=0.0005)
model.compile(optimizer=optimizer, loss='mean_squared_error')

metrics_cb = MetricsCallback(validation_data=(X_val, y_val))

model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=16,
    validation_data=(X_val, y_val),
    callbacks=[metrics_cb],
    verbose=1
)

os.makedirs(os.path.dirname(model_path), exist_ok=True)
model.save(model_path)

print("Modelo treinado e salvo com sucesso em:", model_path)

