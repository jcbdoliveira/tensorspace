from flask import Flask, request, send_file, jsonify
import subprocess
import os
import shutil
import sys

# 1. DEFINIÇÃO DO APP (Deve vir antes de qualquer rota)
app = Flask(__name__)

UPLOAD_FOLDER = '/app/raw'
CONVERTED_FOLDER = '/app/converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Rota de teste padrão para checar se o servidor está online
@app.route('/', methods=['GET'])
def home():
    return "Conversor TensorSpace Ativo!", 200

# Rota principal que recebe a requisição do seu Python 3.11 local
@app.route('/convert', methods=['POST'])
def convert():
    if 'model' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['model']
    camadas = request.form.get('layers', '')
    
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    
    # Extrai o nome do arquivo para criar uma pasta organizada
    model_name = os.path.splitext(file.filename)[0]
    output_dir = os.path.join(CONVERTED_FOLDER, model_name)
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    try:
        # Localiza a pasta binária interna do Python do container
        pasta_bin = os.path.dirname(sys.executable)
        caminho_conversor = os.path.join(pasta_bin, "tensorspacejs_converter")
        
        # Fallback de segurança para o caminho padrão Linux
        if not os.path.exists(caminho_conversor):
            caminho_conversor = "/usr/local/bin/tensorspacejs_converter"

        comando = [
            caminho_conversor,
            "--input_model_from=keras",
            "--input_model_format=topology_weights_combined",
            f"--output_layer_names={camadas}",
            input_path,
            output_dir
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            return jsonify({
                "erro": "O conversor interno falhou.",
                "detalhes": resultado.stderr
            }), 500
            
        # Compacta a pasta de saída em um único .zip
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno na automação: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
