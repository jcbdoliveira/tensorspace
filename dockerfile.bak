# Usa uma imagem oficial antiga do Python 3.6 baseada em Debian
FROM python:3.6-slim

# Instala dependências do sistema necessárias para compilar bibliotecas antigas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala o Flask para criarmos uma API de conversão e o conversor do TensorSpace
RUN pip install --no-cache-dir flask tensorspacejs

# Cria pastas para os modelos brutos e convertidos
RUN mkdir -p /app/raw /app/converted

# Copia o código da nossa mini-API (passo abaixo)
COPY app.py /app/app.py

# Porta padrão que o Render exige para Web Services
EXPOSE 10000

CMD ["python", "app.py"]
