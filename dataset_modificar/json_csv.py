########################################################################################################
###################################  CARPETA DE JSON A UN SOLO .CSV  ###################################
########################################################################################################
# SE REALIZA VARIOS FILTROS LOS CUALES TODOS LOS TURNOS QUE CUMPLAN SE VAN A UN .CSV Y LOS DESCARTADOS A OTRO .CSV

import os
import json
import pandas as pd
from datetime import datetime

def limpiar_texto(texto):
    """Elimina saltos de línea, dobles espacios y recorta espacios extremos."""
    if isinstance(texto, str):
        return ' '.join(texto.split())
    return texto

def procesar_todas_las_partidas(ruta_principal, nombre_csv_validas, nombre_csv_descartadas):
    todas_las_jugadas_validas = []
    todas_las_jugadas_descartadas = []

    for carpeta_raiz, _, archivos in os.walk(ruta_principal):
        for archivo in archivos:
            if archivo.endswith(".json"):
                ruta_archivo = os.path.join(carpeta_raiz, archivo)
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    try:
                        partida = json.load(f)

                        jugadas_filtradas = []
                        jugadas_validas = 0
                        win_encontrado = False
                        consecutivos_invalidos = 0
                        invalidos_iniciales = True

                        sobrantes_descartados = []

                        for idx, turno in enumerate(partida):
                            valid = turno.get("valid", 0)

                            if invalidos_iniciales and valid == 0:
                                consecutivos_invalidos += 1
                                if consecutivos_invalidos >= 5:
                                    jugadas_filtradas = []
                                    break
                            else:
                                invalidos_iniciales = False

                            reason_cruda = turno.get("reason", "N/A")
                            razon_limpia = limpiar_texto(reason_cruda)
                            razon_lista = [razon_limpia] if isinstance(razon_limpia, str) else []

                            t = {
                                "id_match": limpiar_texto(turno.get("id_match", "N/A")),
                                "board": limpiar_texto(str(turno.get("board", "N/A"))),
                                "move": limpiar_texto(str(turno.get("move", "N/A"))),
                                "win": turno.get("win", 0),
                                "player": limpiar_texto(turno.get("player", "N/A")),
                                "model": limpiar_texto(turno.get("model", "N/A")),
                                "reason": razon_lista,
                                "timestamp": limpiar_texto(turno.get("timestamp", {}).get("$date", "N/A")),
                                "valid": valid,
                                "execution_time": turno.get("execution_time", None)  
                            }

                            if not win_encontrado:
                                jugadas_filtradas.append(t)
                            else:
                                sobrantes_descartados.append(t)

                            if valid == 1:
                                jugadas_validas += 1

                            if turno.get("win", 0) == 1:
                                win_encontrado = True

                        if win_encontrado and jugadas_validas <= 9:
                            todas_las_jugadas_validas.extend(jugadas_filtradas)
                            todas_las_jugadas_descartadas.extend(sobrantes_descartados)
                        elif not win_encontrado and jugadas_validas == 9:
                            todas_las_jugadas_validas.extend(jugadas_filtradas)
                            # no sobrantes en este caso, pero por si acaso:
                            todas_las_jugadas_descartadas.extend(sobrantes_descartados)
                        else:
                            # Partida descartada completa: guardamos todos sus turnos
                            for turno in partida:
                                reason_cruda = turno.get("reason", "N/A")
                                razon_limpia = limpiar_texto(reason_cruda)
                                razon_lista = [razon_limpia] if isinstance(razon_limpia, str) else []

                                t_desc = {
                                    "id_match": limpiar_texto(turno.get("id_match", "N/A")),
                                    "board": limpiar_texto(str(turno.get("board", "N/A"))),
                                    "move": limpiar_texto(str(turno.get("move", "N/A"))),
                                    "win": turno.get("win", 0),
                                    "player": limpiar_texto(turno.get("player", "N/A")),
                                    "model": limpiar_texto(turno.get("model", "N/A")),
                                    "reason": razon_lista,
                                    "timestamp": limpiar_texto(turno.get("timestamp", {}).get("$date", "N/A")),
                                    "valid": turno.get("valid", 0),
                                    "execution_time": turno.get("execution_time", None)
                                }
                                todas_las_jugadas_descartadas.append(t_desc)

                    except json.JSONDecodeError:
                        print(f"⚠️ Error leyendo archivo {archivo}")

    # Guardar archivos
    def guardar_csv(datos, ruta_csv, nombre):
        if datos:
            try:
                df = pd.DataFrame(datos)[["id_match", "board", "move", "win", "player", "model", "reason", "timestamp", "valid", "execution_time"]]
                df.to_csv(ruta_csv, index=False, encoding="utf-8")
                print(f"CSV {nombre} generado: {ruta_csv}")
            except PermissionError:
                print(f"Error: No se pudo guardar {ruta_csv}. ¿Está abierto el archivo?")
        else:
            print(f"No se encontraron partidas {nombre.lower()} para guardar.")

    guardar_csv(todas_las_jugadas_validas, nombre_csv_validas, "partidas válidas")
    guardar_csv(todas_las_jugadas_descartadas, nombre_csv_descartadas, "partidas descartadas")

data = r"dataset\tictactoe"
fecha_actual = datetime.now().strftime("%Y-%m-%d")
csv_validas = os.path.join(data, f"partidas_validas_{fecha_actual}.csv")
csv_descartadas = os.path.join(data, f"partidas_descartadas_{fecha_actual}.csv")

procesar_todas_las_partidas(data, csv_validas, csv_descartadas)
