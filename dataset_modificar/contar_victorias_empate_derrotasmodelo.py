########################################################################################################
###############################  VICTORIAS - EMPATES - DERROTAS (X-O)  #################################
########################################################################################################
# Muestra las victorias, empates o derrotas por modelo y por jugador (x - o)

import pandas as pd
import ast

# === 1. Cargar CSV ===
df = pd.read_csv(r"dataset1.csv")

# === 2. Ordenar por tiempo por partida ===
df = df.sort_values(["id_match", "timestamp"])

# === 3. Función para verificar si el tablero está lleno ===
def esta_lleno(board_str):
    try:
        board = ast.literal_eval(board_str)
        for celda in board:
            if celda[0] == "cell" and celda[3] == "b":
                return False
        return True
    except Exception as e:
        print(f"Error en board: {e}")
        return False

# === 4. Procesar resultados por partida ===
resultados = []

for id_partida, grupo in df.groupby("id_match"):
    grupo_final = grupo.sort_values("timestamp").iloc[-1]
    modelos = grupo["model"].unique().tolist()

    if len(modelos) != 2:
        continue  # Omitir si no hay dos modelos distintos

    modelo_ganador = None
    modelo_perdedor = None
    empate = False

    if grupo_final["win"] == 1:
        modelo_ganador = grupo_final["model"]
        modelo_perdedor = [m for m in modelos if m != modelo_ganador][0]
    elif grupo_final["win"] == 0 and esta_lleno(grupo_final["board"]):
        empate = True
    else:
        modelo_perdedor = grupo_final["model"]
        modelo_ganador = [m for m in modelos if m != modelo_perdedor][0]

    if empate:
        for m in modelos:
            jugador = grupo[grupo["model"] == m]["player"].iloc[0]
            resultados.append({
                "id_match": id_partida,
                "model": m,
                "resultado": "Empate",
                "player": jugador
            })
    else:
        jugador_ganador = grupo[grupo["model"] == modelo_ganador]["player"].iloc[0]
        jugador_perdedor = grupo[grupo["model"] == modelo_perdedor]["player"].iloc[0]

        resultados.append({
            "id_match": id_partida,
            "model": modelo_ganador,
            "resultado": "Victoria",
            "player": jugador_ganador
        })
        resultados.append({
            "id_match": id_partida,
            "model": modelo_perdedor,
            "resultado": "Derrota",
            "player": jugador_perdedor
        })

# === 5. Crear DataFrame con resultados ===
df_resultados = pd.DataFrame(resultados)

# === 6. Contar resumen general de resultados por modelo ===
resumen = df_resultados.groupby("model")["resultado"].value_counts().unstack(fill_value=0)
resumen["Total Partidas"] = resumen.sum(axis=1)

# === 7. Función auxiliar para contar por ficha ===
def contar_por_ficha(df_resultados, tipo_resultado, nombre_columna):
    temp = df_resultados[df_resultados["resultado"] == tipo_resultado]
    conteo = temp.groupby(["model", "player"]).size().unstack(fill_value=0)
    conteo.columns = [f"{nombre_columna} con {col.upper()}" for col in conteo.columns]
    return conteo

# === 8. Contar por ficha para cada tipo de resultado ===
victorias_por_ficha = contar_por_ficha(df_resultados, "Victoria", "Victorias")
empates_por_ficha   = contar_por_ficha(df_resultados, "Empate", "Empates")
derrotas_por_ficha  = contar_por_ficha(df_resultados, "Derrota", "Derrotas")

# === 9. Unir todos los conteos al resumen principal ===
resumen_final = resumen \
    .join(victorias_por_ficha, how="left") \
    .join(empates_por_ficha, how="left") \
    .join(derrotas_por_ficha, how="left") \
    .fillna(0).astype(int)

# === 10. Mostrar y exportar ===
print("Resumen completo de partidas por modelo:")
print(resumen_final)

resumen_final.to_csv(
    r"resumen_modelos_resultados.csv",
    index=True
)
