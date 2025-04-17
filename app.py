from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar():
    archivo = request.files['archivo']
    nombre_base = str(uuid.uuid4())
    carpeta = f"./temp/{nombre_base}"
    os.makedirs(carpeta, exist_ok=True)

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

        subprocess.run([
            "python3", "extraer_tarareo.py",
            ruta_vocals,
            f"{carpeta}/melodia.json"
        ], check=True)

        subprocess.run([
            "python3", "simplificar_melodia.py",
            f"{carpeta}/melodia.json",
            f"{carpeta}/melodia_simplificada.json"
        ], check=True)

        return send_file(f"{carpeta}/melodia_simplificada.json", as_attachment=True)

    except subprocess.CalledProcessError as e:
        return f"❌ Error durante el análisis: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
