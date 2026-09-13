# Usa uma imagem oficial que já vem com Python 3.8 e Node.js instalados de fábrica
FROM nikolaik/python-nodejs:python3.8-nodejs14-slim

WORKDIR /app

# Instala ferramentas essenciais de compilação do Linux exigidas por pacotes C antigos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Atualiza os gerenciadores de pacotes internos
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instala o Flask e o conversor do TensorSpace
RUN pip install --no-cache-dir flask tensorspacejs

# Inicializa as dependências de Node internas do TensorSpace Converter
RUN tensorspacejs_converter -init

# Organiza os arquivos da aplicação
RUN mkdir -p /app/raw /app/converted
COPY app.py /app/app.py

EXPOSE 10000

CMD ["python", "app.py"]
