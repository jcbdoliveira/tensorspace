# Usa uma imagem do Python estável e compatível
FROM python:3.8-slim

WORKDIR /app

# 1. Instala ferramentas de compilação do Linux, curl e o Node.js v12 com NPM legados
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && curl -sL https://nodesource.com | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala o Flask para a API e o pacote do TensorSpace
RUN pip install --no-cache-dir flask tensorspacejs

# 3. PASSO CRUCIAL: Inicializa as dependências Node internas do TensorSpace Converter
RUN tensorspacejs_converter -init

# 4. Estrutura os diretórios de trabalho da aplicação
RUN mkdir -p /app/raw /app/converted
COPY app.py /app/app.py

EXPOSE 10000

CMD ["python", "app.py"]
