# Usa o Python 3.11 moderno de forma nativa
FROM python:3.11-slim

WORKDIR /app

# Instala o compilador do Google (tensorflowjs) compatível com Python 3.11
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir flask tensorflowjs>=4.10.0

# Cria as pastas necessárias
RUN mkdir -p /app/raw /app/converted

# Copia os códigos do repositório para dentro do container
COPY tensorspace_compiler/ /app/tensorspace_compiler/
COPY app.py /app/app.py

EXPOSE 10000

CMD ["python", "app.py"]
