# Usa a imagem estável do Python 3.6
FROM python:3.6-slim

# Altera as fontes do apt-get para apontar para o repositório de arquivos mortos (archive)
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

# Agora o apt-get update vai funcionar sem o erro 100
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Atualiza ferramentas essenciais de pacotes e instala o conversor
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir flask tensorspacejs

RUN mkdir -p /app/raw /app/converted
COPY app.py /app/app.py

EXPOSE 10000

CMD ["python", "app.py"]
