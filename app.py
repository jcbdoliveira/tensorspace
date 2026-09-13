from flask import Flask, request, send_file, jsonify
import subprocess
import os
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = '/app/raw'
CONVERTED_FOLDER = '/app/converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# Rota simples apenas para o Render não dar erro 404 ao abrir a página inicial
@app.route('/', methods=['GET'])
def home():
    return "Conversor TensorSpace Ativo!", 200

@app.route('/convert', methods=['POST'])
def convert():
    if 'model' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['model']
    camadas = request.form.get('layers', '')
    
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)
    
    model_name = os.path.splitext(file.filename)[0]
    output_dir = os.path.join(CONVERTED_FOLDER, model_name)
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        
    try:
        # Encontra o caminho absoluto oculto do binário
        caminho_conversor = subprocess.check_output(["which", "tensorspacejs_converter"]).decode().strip()
        
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
            return jsonify({"erro": resultado.stderr, "log_interno": resultado.stdout}), 500
            
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": f"Falha na execução do sistema: {str(e)}"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
