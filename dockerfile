dockerfile
# Troque a versão antiga por uma ligeiramente mais recente que ainda aceite as dependências
FROM python:3.8-slim

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
