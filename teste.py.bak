import requests

url_render = "https://onrender.com"
caminho_modelo = "sua_cnn.keras"

print("Enviando modelo... O Render vai extrair as camadas e converter tudo.")
with open(caminho_modelo, "rb") as f:
    arquivos = {"model": f}
    # N�O precisa mais passar o dicion�rio 'data={"layers": ...}'
    resposta = requests.post(url_render, files=arquivos)

if resposta.status_code == 200:
    with open("resultado_tensorspace.zip", "wb") as saida:
        saida.write(resposta.content)
    print("Sucesso! Arquivo pronto baixado.")
else:
    print(f"Erro: {resposta.text}")

