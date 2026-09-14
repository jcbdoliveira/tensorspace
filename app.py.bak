import os
# IMPORTANTE: Força o TensorFlow a usar apenas a CPU e silencia avisos pesados de CUDA
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import shutil
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = '/app/raw'
CONVERTED_FOLDER = '/app/converted'

# Garante que o Linux crie as pastas se elas não existirem no build
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert():
    if 'model' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['model']
    
    keras_zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(keras_zip_path)
    
    model_base_name = os.path.splitext(file.filename)[0]
    legacy_h5_path = os.path.join(UPLOAD_FOLDER, f"{model_base_name}_legacy.h5")
    output_dir = os.path.join(CONVERTED_FOLDER, model_base_name)
    
    try:
        # IMPORTAÇÃO ATRASADA (Lazy Import): O TensorFlow só é carregado na RAM quando
        # uma requisição chega. Isso evita que o Render derrube o app no início por falta de memória.
        import tensorflow as tf
        
        modelo_carregado = tf.keras.models.load_model(keras_zip_path)
        
        nomes_camadas = [layer.name for layer in modelo_carregado.layers]
        camadas_str = ",".join(nomes_camadas)
        print(f"Camadas detectadas automaticamente: {camadas_str}")
        
        modelo_carregado.save(legacy_h5_path, save_format="h5")
        
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            
        comando = [
            "python", "-m", "tensorspace_compiler.main",
            "--input_model_format=keras",
            f"--output_layer_names={camadas_str}",
            legacy_h5_path,
            output_dir
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Limpeza imediata de arquivos pesados para liberar espaço em disco
        if os.path.exists(keras_zip_path): os.remove(keras_zip_path)
        if os.path.exists(legacy_h5_path): os.remove(legacy_h5_path)
        
        if resultado.returncode != 0:
            return jsonify({"erro": "Falha no tensorflowjs", "detalhes": resultado.stderr}), 500
            
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": "Falha na extracao automatica", "detalhes": str(e)}), 500

if __name__ == '__main__':
    porta = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=porta, debug=False)
