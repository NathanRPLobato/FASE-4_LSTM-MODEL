# 📈 Previsão de Preço de Ações com LSTM

Projeto que une inteligência artificial e visualização interativa para prever preços de ações em tempo real. Utiliza modelo LSTM via API REST Flask e interface web Dash para consulta e análise das previsões.

---

## 📂 Estrutura do Projeto

```
/app
  ├── app.py              # Backend Flask da API REST
  ├── models/
  │     └── lstm_model.h5 # Modelo LSTM treinado
  └── data/               # Dados financeiros para avaliação local

/webapp
  └── webdash.py          # Aplicação Dash para interface gráfica
```
---

## ⚙️ Pré-requisitos

- Python 3.8+  
- pip  
- (Opcional) Docker e Docker Compose

---

## 🚀 Execução Local

1. Clone o repositório e acesse a pasta:

   ```bash
   git clone https://seu-repositorio.git
   cd seu-repositorio
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a API Flask:

   ```bash
   python app/app.py
   ```

5. Em outro terminal, inicie a aplicação Dash:

   ```bash
   python webapp/webdash.py
   ```

6. Acesse a aplicação no navegador:

   ```
   http://localhost:8050
   ```

---

## 🔗 API REST

**Endpoint:** `POST /predict`

**Payload JSON:**

```json
{
  "ticker": "PETR4.SA"
}
```

**Retorno:** Previsão do preço de fechamento para o ticker informado.

---

## 🖥️ Uso do WebDash

- Insira o ticker da ação (exemplo: `PETR4.SA`)  
- Clique em **Prever**  
- Visualize:  
  - Previsão do preço  
  - Métricas do modelo (MAE e RMSE)  
  - Tempo de resposta da API  
- Veja o gráfico com histórico e previsão de preços

---

## 🐳 Executando com Docker

Para rodar API e WebDash via Docker Compose:

```bash
docker-compose up --build
```

Acesse após iniciar:  

- API: `http://localhost:5000`  
- WebDash: `http://localhost:8050`

---

## 📊 Métricas do Modelo

- **MAE** (Erro Absoluto Médio)  
- **RMSE** (Raiz do Erro Quadrático Médio)  

Indicadores da qualidade das previsões.

---

## ⚠️ Avisos Importantes

- Modelo treinado com dados históricos até uma data fixa  
- Previsões futuras podem variar conforme o mercado  
- Tickers com dados insuficientes retornam erro

---

## 📞 Contato

**Nathan Rafael Pedroso Lobato**  
✉️ nathan.lobato@outlook.com.br

**André Vicente Torres Martins**  
✉️ andrasno@gmail.com

---

## 📄 Licença

Este projeto está sob a licença **MIT** — livre para uso, modificação e distribuição.
