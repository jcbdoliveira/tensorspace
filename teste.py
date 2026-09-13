import requests
import time
import os

# 1. Altere para a URL pública gerada pelo seu painel do Render
url_render_base = "https://tensorspace.onrender.com"
url_conversor = f"{url_render_base}/convert"

# 2. Configurações dos seus arquivos locais
caminho_modelo = "model.weights.h5"
camadas_alvo = "conv_1,maxpool_1,flatten,saida"  # Substitua pelos nomes reais da sua CNN

def acordar_servidor():
    print("Verificando se o servidor no Render está acordado...")
    try:
        # Tenta dar um "ping" na URL. Se estiver dormindo, essa linha vai esperar o Render ligar
        requests.get(url_render_base, timeout=120)
        print("Servidor ativo e pronto!")
    except Exception as e:
        print("Aguardando o servidor inicializar (isso pode levar cerca de 1 minuto)...")
        time.sleep(30)

def enviar_e_converter():
    if not os.path.exists(caminho_modelo):
        print(f"Erro: O arquivo '{caminho_modelo}' não foi encontrado na pasta atual!")
        return

    acordar_servidor()
    print("\nEnviando o modelo .h5 e iniciando a conversão no ambiente isolado...")
    
    # Prepara o arquivo binário e as variáveis de texto para o envio via POST
    with open(caminho_modelo, "rb") as f:
        arquivos = {"model": f}
        dados = {"layers": camadas_alvo}
        
        try:
            resposta = requests.post(url_conversor, files=arquivos, data=dados, timeout=300)
            
            # Se o status for 200, o Render devolveu o arquivo compactado com sucesso
            if resposta.status_code == 200:
                nome_zip_saida = "resultado_tensorspace.zip"
                with open(nome_zip_saida, "wb") as saida:
                    saida.write(resposta.content)
                print(f"\nSucesso total! Arquivo '{nome_zip_saida}' baixado e salvo localmente.")
                print("Dica: Extraia o arquivo ZIP para obter o 'model.json' e os pesos binários para o TensorSpace.js.")
            else:
                print("\nFalha na conversão dentro do container do Render:")
                print(resposta.text)
                
        except requests.exceptions.Timeout:
            print("\nErro: A conversão demorou demais e a conexão local caiu (Timeout).")
        except Exception as e:
            print(f"\nErro de conexão ao tentar falar com o Render: {e}")

if __name__ == "__main__":
    enviar_e_converter()
