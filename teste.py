import os
import shutil
import zipfile
import json

caminho_modelo_keras = "cnn_mnist.keras"
pasta_destino = "./modelo_tensorspace_pronto"

print("1. Abrindo o arquivo .keras sem usar o TensorFlow (Evitando conflito de versao)...")

if not os.path.exists(caminho_modelo_keras):
    print(f"Erro: O arquivo '{caminho_modelo_keras}' nao foi encontrado nesta pasta.")
    exit(1)

try:
    # 1. Cria a pasta de destino limpa
    if os.path.exists(pasta_destino):
        shutil.rmtree(pasta_destino)
    os.makedirs(pasta_destino, exist_ok=True)

    # 2. Abre o arquivo .keras como o arquivo ZIP que ele eh por dentro
    with zipfile.ZipFile(caminho_modelo_keras, 'r') as arquivo_zip:
        lista_arquivos = arquivo_zip.namelist()
        print("-> Estrutura interna detectada com sucesso!")

        # 3. Busca o arquivo de configuracao da arquitetura
        config_path = [f for f in lista_arquivos if 'config.json' in f]
        
        if config_path:
            # Extrai e le a arquitetura para descobrir as camadas
            with arquivo_zip.open(config_path[0]) as f_json:
                dados_modelo = json.loads(f_json.read().decode('utf-8'))
                
                # Extrai os nomes das camadas de forma inteligente adaptada para Keras 3
                camadas = []
                if 'config' in dados_modelo and 'layers' in dados_modelo['config']:
                    camadas = [layer['config'].get('name', 'camada') for layer in dados_modelo['config']['layers']]
                
                camadas_str = ",".join(camadas)
                print(f"-> Camadas detectadas automaticamente: {camadas_str}")
        else:
            print("-> Aviso: Nao foi possivel listar os nomes das camadas automaticamente.")

        print("4. Extraindo e estruturando pesos para o formato Web...")
        # 4. Extrai todos os arquivos internos direto para a pasta final
        for arquivo in lista_arquivos:
            # Ignora metadados do Keras e extrai o json e arquivos h5/bin de pesos
            if not arquivo.endswith('/'):
                nome_final = os.path.basename(arquivo)
                if nome_final == "config.json":
                    nome_final = "model.json" # Altera para o padrao que o TensorSpace busca
                
                with arquivo_zip.open(arquivo) as fonte, open(os.path.join(pasta_destino, nome_final), 'wb') as destino:
                    shutil.copyfileobj(fonte, destino)

    print(f"\n[SUCESSO] Pasta criada com sucesso em: {os.path.abspath(pasta_destino)}")
    print("Arquivos prontos extraidos:")
    for item in os.listdir(pasta_destino):
        print(f" -> {item}")

except Exception as e:
    print(f"\n[ERRO] Falha ao descompactar e extrair o modelo: {e}")
