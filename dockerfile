# Usa a imagem estável com Python 3.8 e Node.js de fábrica
FROM nikolaik/python-nodejs:python3.8-nodejs14-slim

WORKDIR /app

# CORREÇÃO: Remove as fontes antigas do Yarn que quebram o apt-get devido à chave GPG expirada
RUN rm -f /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Atualiza os gerenciadores internos de módulos
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instala o Flask para a comunicação de dados e o conversor legado
RUN pip install --no-cache-dir flask tensorspacejs

# Inicializa as rotinas e dependências de Node do próprio ecossistema TensorSpace
RUN tensorspacejs_converter -init

# Prepara a árvore de diretórios do servidor Render
RUN mkdir -p /app/raw /app/converted
COPY app.py /app/app.py

EXPOSE 10000

CMD ["python", "app.py"]
