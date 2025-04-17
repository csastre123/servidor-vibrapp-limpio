import json
import sys
from collections import Counter

def simplificar_melodia(json_entrada, json_salida, ventana_ms=100):
    with open(json_entrada, 'r') as f:
        datos = json.load(f)

    simplificado = {
        "notas_simplificadas": []
    }

    bloque = []
    bloque_tiempos = []
    tiempo_anterior = datos[0]["tiempo"]

    for entrada in datos:
        tiempo = entrada["tiempo"]
        nota = entrada["nota"]
        bloque.append(nota)
        bloque_tiempos.append(tiempo)

        if tiempo - tiempo_anterior >= ventana_ms / 1000.0:
            notas_validas = [n for n in bloque if n != "N"]
            nota_frecuente = Counter(notas_validas).most_common(1)[0][0] if notas_validas else "N"
            simplificado["notas_simplificadas"].append({
                "inicio": round(bloque_tiempos[0], 3),
                "fin": round(bloque_tiempos[-1], 3),
                "nota": nota_frecuente
            })
            bloque = []
            bloque_tiempos = []
            tiempo_anterior = tiempo

    # Guardar resultado
    with open(json_salida, 'w') as f:
        json.dump(simplificado, f, indent=2)

    print(f"✅ Archivo simplificado guardado en: {json_salida}")

# Uso desde terminal
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python simplificar_melodia.py entrada.json salida.json")
    else:
        simplificar_melodia(sys.argv[1], sys.argv[2])
