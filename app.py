from flask import Flask, request, send_file, jsonify
import subprocess
import os
import shutil
import sys # Adicionado para mapear o caminho do Python

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
        # Encontra dinamicamente a pasta de executáveis (bin) vinculada ao Python do container
        pasta_bin = os.path.dirname(sys.executable)
        caminho_conversor = os.path.join(pasta_bin, "tensorspacejs_converter")
        
        # Garante segurança caso o executável esteja em outro local comum do Linux
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
        
        # Executa a conversão real das camadas da CNN
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            # Caso o conversor antigo rejeite a estrutura do H5, retorna o erro exato do compilador
            return jsonify({
                "erro": "O conversor do TensorSpace falhou ao processar o arquivo H5.",
                "detalhes_do_conversor": resultado.stderr
            }), 500
            
        zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
        return send_file(zip_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"erro": f"Erro interno no script de automação: {str(e)}"}), 500
