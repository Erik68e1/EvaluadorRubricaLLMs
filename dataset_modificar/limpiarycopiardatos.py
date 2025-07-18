########################################################################################################
##################################  LIMPIEZA DE FORMATO DE RESPUESTA  ##################################
########################################################################################################
# Este script limpia y reestructura un archivo CSV generado por modelos LLM, separando correctamente las columnas de evaluación.
# Además, copia la columna del dataset original de jugadas hacia el archivo evaluado para su posterior análisis.

import csv
import pandas as pd

def limpiar_comillas(texto):
    return texto.replace('"', '').strip()

def procesar_csv(entrada, salida):
    with open(entrada, 'r', encoding='utf-8') as f_in, \
         open(salida, 'w', encoding='utf-8', newline='') as f_out:

        lector = csv.reader(f_in, delimiter=',', quotechar='"')
        escritor = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        encabezado = next(lector)
        escritor.writerow([limpiar_comillas(c) for c in encabezado])

        for i, fila in enumerate(lector, start=2):
            # Limpiamos todas las columnas de comillas dobles
            fila_limpia = [limpiar_comillas(c) for c in fila]

            if len(fila_limpia) > 7:
                id_partida = fila_limpia[0]
                modelo = fila_limpia[1]
                jugador = fila_limpia[2]
                estado = fila_limpia[3]
                timestamp = fila_limpia[-1]

                intermedios = fila_limpia[4:-1]
                texto_intermedio = ','.join(intermedios)

                # Dividir en rubrica y explicacion basado en el primer cierre de '}'
                try:
                    cierre_rubrica = texto_intermedio.index('}') + 1
                    rubrica_raw = texto_intermedio[:cierre_rubrica].strip()
                    explicacion_raw = texto_intermedio[cierre_rubrica:].strip().lstrip(',')
                except ValueError:
                    rubrica_raw = texto_intermedio
                    explicacion_raw = ""

                escritor.writerow([
                    id_partida, modelo, jugador, estado, rubrica_raw, explicacion_raw, timestamp
                ])
            elif len(fila_limpia) == 7:
                escritor.writerow(fila_limpia)
            else:
                print(f"Fila {i} con columnas inesperadas: {len(fila_limpia)} - {fila_limpia}")


if __name__ == "__main__":
    entrada = r"gemini_evaluado.csv"
    salida  = r"gemini_evaluado_sincomillas.csv"

    df1 = pd.read_csv(r'partidas_validas_2025-07-06.csv')   
    df2 = pd.read_csv(r'evaluadoDeepseek.csv')   

    # Copiar la columna deseada del primer DataFrame al segundo
    df2['valid'] = df1['valid'] 

    df2.to_csv(r'evaluadoDeepseek.csv', index=False)  