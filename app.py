from flask import Flask, request, send_file, jsonify
import subprocess
import os
import shutil
import sys

app = Flask(__name__)

UPLOAD_FOLDER = '/app/raw'
CONVERTED_FOLDER = '/app/converted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

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
        # --- BUSCA INTELIGENTE PELO EXECUTÁVEL ---
        caminhos_possiveis = [
            os.path.join(os.path.dirname(sys.executable), "tensorspacejs_converter"),
            "/usr/local/bin/tensorspacejs_converter",
            "/root/.local/bin/tensorspacejs_converter",
            "/usr/bin/tensorspacejs_converter"
        ]
        
        caminho_conversor = None
        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                caminho_conversor = caminho
                break
                
        # Se mesmo assim não achar na marra, tenta disparar o comando cru puro
        if not caminho_conversor:
            caminho_conversor = "tensorspacejs_converter"
        # ----------------------------------------

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
                "erro": "O conversor do TensorSpace falhou internamente.",
                "detalhes_do_conversor_stderr": resultado.stderr,
                "detalhes_do_conversor_stdout": resultado.stdout
            }), 500
            
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno na automação do servidor: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
