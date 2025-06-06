# Use uma imagem Python leve
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia requirements.txt para instalar dependências
COPY requirements.txt .

# Instala dependências (ajusta se tiver libs específicas do sistema)
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta webapp para /app dentro do container
COPY . .

# Expõe a porta que o Dash vai rodar
EXPOSE 8050

# Comando para rodar o Dash app (ajuste para webdash.py dentro da pasta atual)
CMD ["python", "webdash.py"]