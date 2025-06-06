Previsão de Preço de Ações com LSTM
Projeto que combina inteligência artificial e visualização interativa para prever preços de ações em tempo real. Utiliza um modelo LSTM treinado, disponibilizado via API REST Flask, e uma interface web com Dash para consulta e análise das previsões.

📂 Estrutura do Projeto
/app
 ├─ app.py # Backend Flask da API REST
 ├─ models/
  └─ lstm_model.h5 # Modelo LSTM treinado
 └─ data/ # Dados financeiros para avaliação local

/webapp
 └─ webdash.py # Aplicação Dash para interface gráfica

⚙️ Pré-requisitos
Python 3.8 ou superior

pip

Opcional: Docker e Docker Compose (para ambiente containerizado)

🚀 Como executar localmente
Clone o repositório:
git clone https://seu-repositorio.git
cd seu-repositorio

Crie e ative um ambiente virtual:
python -m venv venv

No Windows:
venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

Instale as dependências:
pip install -r requirements.txt

Inicie a API Flask:
python app/app.py

Em outro terminal, rode a aplicação Dash:
python webapp/webdash.py

Acesse a interface no navegador:
http://localhost:8050

🔗 Endpoints da API
POST /predict

Payload JSON:
{
  "ticker": "PETR4.SA"
}

Resposta: Previsão do preço de fechamento para o ticker informado.

🖥️ Uso do WebDash
Insira o ticker da ação no campo de texto (exemplo: PETR4.SA).

Clique em Prever.

Veja:

Previsão do preço de fechamento.

Métricas do modelo (MAE e RMSE).

Tempo de resposta da API.

Visualize o gráfico com histórico e previsão de preços.

🐳 Executando via Docker
Utilize o arquivo docker-compose.yml para rodar ambos os serviços:
docker-compose up --build

Após a inicialização, acesse:

API: http://localhost:5000

WebDash: http://localhost:8050

📊 Métricas do Modelo
MAE (Erro Absoluto Médio)

RMSE (Raiz do Erro Quadrático Médio)

Essas métricas avaliam a precisão da previsão do modelo.

⚠️ Considerações Importantes
O modelo foi treinado com dados históricos até uma data fixa.

Previsões futuras podem variar conforme condições reais do mercado.

Tickers com dados insuficientes retornam erro.

📞 Contato
Nathan Rafael Pedroso Lobato
E-mail: nathan.lobato@outlook.com.br

André Vicente Torres Martins
E-mail: andrasno@gmail.com

📄 Licença
Este projeto está licenciado sob a Licença MIT, permitindo uso, modificação e distribuição livre.