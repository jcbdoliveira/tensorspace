# tensorspace_compiler/main.py
import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Conversor TensorSpace para Python 3.11")
    parser.add_init = parser.add_argument('--init', action='store_true', help='Inicializa dependencias')
    parser.add_argument('--input_model_from', type=str, default='keras')
    parser.add_argument('--input_model_format', type=str, default='topology_weights_combined')
    parser.add_argument('--output_layer_names', type=str, required=False)
    parser.add_argument('input_path', type=str, nargs='?')
    parser.add_argument('output_dir', type=str, nargs='?')

    args = parser.parse_args()

    # O TensorSpace usa o pacote do Google por baixo dos panos
    if args.output_layer_names:
        comando = [
            "tensorflowjs_converter",
            f"--input_format={args.input_model_format}",
            f"--output_layer_names={args.output_layer_names}",
            args.input_path,
            args.output_dir
        ]
        print(f"Executando: {' '.join(comando)}")
        subprocess.run(comando, check=True)
    else:
        print("Forneça o parâmetro --output_layer_names com as camadas da sua CNN.")

if __name__ == "__main__":
    main()
