# app.py (Versão que extrai as camadas do .keras de forma 100% automática)
import tensorflow as tf
import os
import shutil
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = '/app/raw'
CONVERTED_FOLDER = '/app/converted'

@app.route('/convert', methods=['POST'])
def convert():
    if 'model' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['model']
    
    # Salva o arquivo .keras temporário enviado pela sua máquina
    keras_zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(keras_zip_path)
    
    model_base_name = os.path.splitext(file.filename)[0]
    legacy_h5_path = os.path.join(UPLOAD_FOLDER, f"{model_base_name}_legacy.h5")
    output_dir = os.path.join(CONVERTED_FOLDER, model_base_name)
    
    try:
        # 1. Carrega o modelo usando o TensorFlow do container
        modelo_carregado = tf.keras.models.load_model(keras_zip_path)
        
        # 2. AUTOMAÇÃO: Descobre todas as camadas do seu .keras sozinho
        nomes_camadas = [layer.name for layer in modelo_carregado.layers]
        camadas_str = ",".join(nomes_camadas)
        print(f"Camadas detectadas automaticamente: {camadas_str}")
        
        # 3. Salva no formato HDF5 legado puro combinado
        modelo_carregado.save(legacy_h5_path, save_format="h5")
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            
        # 4. Aciona o conversor usando as camadas extraídas de forma nativa
        comando = [
            "python", "-m", "tensorspace_compiler.main",
            "--input_model_format=keras",
            f"--output_layer_names={camadas_str}", # Injetado automaticamente pelo servidor
            legacy_h5_path,
            output_dir
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Limpeza de arquivos temporários do servidor
        if os.path.exists(keras_zip_path): os.remove(keras_zip_path)
        if os.path.exists(legacy_h5_path): os.remove(legacy_h5_path)
        
        if resultado.returncode != 0:
            return jsonify({"erro": "Falha no tensorflowjs", "detalhes": resultado.stderr}), 500
            
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": "Falha na extração automática", "detalhes": str(e)}), 500
