import librosa
import json
import numpy as np

A4 = 440.0
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def frecuencia_a_nota(frec):
    if frec is None or np.isnan(frec):
        return "Silencio"
    semitonos = int(round(12 * np.log2(frec / A4)))
    nota = NOTAS[semitonos % 12]
    octava = 4 + semitonos // 12
    return f"{nota}{octava}"

def extraer_melodia(ruta_audio, ruta_salida_json):
    print("🎼 Cargando archivo de voz...")
    y, sr = librosa.load(ruta_audio, sr=None)

    print("🎯 Extrayendo tono principal...")
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        sr=sr,
        fmin=librosa.note_to_hz('F2'),
        fmax=librosa.note_to_hz('C7'),
        frame_length=1024,       # REDUCIDO para evitar el error
        hop_length=256           # más precisión temporal
    )

    print("🧠 Convirtiendo a notas musicales...")
    tiempos = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=256)
    melodia = []

    for t, f in zip(tiempos, f0):
        nota = frecuencia_a_nota(f)
        melodia.append({"tiempo": round(t, 3), "nota": nota})

    with open(ruta_salida_json, 'w', encoding='utf-8') as f:
        json.dump(melodia, f, indent=2, ensure_ascii=False)

    print(f"✅ Melodía extraída y guardada en '{ruta_salida_json}'")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Uso: python extraer_tarareo.py <ruta_audio.wav> <salida.json>")
        sys.exit(1)

    ruta_vocals = sys.argv[1]
    ruta_json_salida = sys.argv[2]
    extraer_melodia(ruta_vocals, ruta_json_salida)
