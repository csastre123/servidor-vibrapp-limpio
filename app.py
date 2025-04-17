from flask import Flask, request, send_file, after_this_request
import subprocess
import os
import uuid
import shutil

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    archivo = request.files['archivo']

    # Validar que el archivo sea un MP3
    if not archivo.filename.lower().endswith('.mp3'):
        return "⚠️ El archivo debe tener formato .mp3", 400

    # Crear carpeta temporal única
    nombre_base = str(uuid.uuid4())
    carpeta = f"./temp/{nombre_base}"
    os.makedirs(carpeta, exist_ok=True)

    # Asegurar limpieza después del envío
    @after_this_request
    def cleanup(response):
        shutil.rmtree(carpeta)
        return response

    ruta_mp3 = os.path.join(carpeta, "cancion.mp3")
    archivo.save(ruta_mp3)

    try:
        subprocess.run([
            "spleeter", "separate",
            "-p", "spleeter:2stems",
            "-o", carpeta,
            ruta_mp3
        ], check=True)

        ruta_vocals = os.path.join(carpeta, "cancion", "vocals.wav")

        result = subprocess.run(
            ["python3", "extraer_tarareo.py", ruta_vocals, f"{carpeta}/melodia.json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return f"❌ Error extraer_tarareo.py:\n{result.stderr}", 500



        subprocess.run([
            "python3", "simplificar_melodia.py",
            f"{carpeta}/melodia.json",
            f"{carpeta}/melodia_simplificada.json"
        ], check=True)

        return send_file(f"{carpeta}/melodia_simplificada.json", as_attachment=True)

    except subprocess.CalledProcessError as e:
        return f"❌ Error durante el análisis: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
