import requests
import zipfile
import io
import os

# 1. CORREÇÃO DA URL: Adicionado o /convert no final
url_render = "https://tensorspace.onrender.com"
caminho_modelo = "cnn_mnist.keras"

# Pasta local onde os arquivos descompactados serão salvos
pasta_destino = "./modelo_tensorspace_pronto"

print("Enviando modelo... O Render vai extrair as camadas e converter tudo.")

try:
    with open(caminho_modelo, "rb") as f:
        arquivos = {"model": f}
        resposta = requests.post(url_render, files=arquivos)

    if resposta.status_code == 200:
        print("Conversão concluída! Descompactando arquivos localmente...")
        
        # Abre o zip recebido direto da memória RAM e extrai na pasta
        zip_arquivos = zipfile.ZipFile(io.BytesIO(resposta.content))
        os.makedirs(pasta_destino, exist_ok=True)
        zip_arquivos.extractall(pasta_destino)
        
        print(f"\n[SUCESSO] Arquivos salvos na pasta: {os.path.abspath(pasta_destino)}")
        print("Conteúdo gerado para usar no seu HTML:")
        for item in os.listdir(pasta_destino):
            print(f" -> {item}")
    else:
        print(f"\nErro no servidor (Status {resposta.status_code}):")
        print(resposta.text)

except Exception as e:
    print(f"\nErro ao conectar com o Render: {e}")


