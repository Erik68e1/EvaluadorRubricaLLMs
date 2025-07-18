########################################################################################################
###################################   VERIFICAR PARTIDAS Y TURNOS    ###################################
########################################################################################################
# AL TRANSFORMAR A .CSV ESTE CODIGO ES PARA VERIFICAR QUE EL TOTAL DE LOS DOS ARCHIVOS SEA CORRECTO CON 
# EL ORIGINAL EN PARTIDAS COMO EN TURNOS

import pandas as pd

# Rutas de los archivos CSV
ruta_csv1 = r"partidas_validas_2025-07-06.csv"
ruta_csv2 = r"partidas_descartadas_2025-07-06.csv"

# Leer ambos archivos
df1 = pd.read_csv(ruta_csv1)
df2 = pd.read_csv(ruta_csv2)

# Verificar existencia de columna 'id_match'
if 'id_match' in df1.columns and 'id_match' in df2.columns:
    # === Análisis por archivo ===
    ids1 = df1['id_match'].dropna().unique()
    ids2 = df2['id_match'].dropna().unique()

    total_turnos_1 = len(df1)
    total_turnos_2 = len(df2)

    # Unir todos los IDs para obtener partidas únicas en total
    ids_total = pd.Series(list(ids1) + list(ids2)).dropna().unique()

    print("RESULTADOS DEL ANÁLISIS\n")
    print(f"Archivo 1 (válidas):")
    print(f"   - Partidas únicas: {len(ids1)}")
    print(f"   - Turnos totales: {total_turnos_1}\n")

    print(f"Archivo 2 (descartadas):")
    print(f"   - Partidas únicas: {len(ids2)}")
    print(f"   - Turnos totales: {total_turnos_2}\n")

    print(f"TOTAL GENERAL:")
    print(f"   - Partidas únicas combinadas: {len(ids_total)}")
    print(f"   - Turnos combinados: {total_turnos_1 + total_turnos_2}")
else:
    print("Alguno de los archivos no contiene la columna 'id_match'.")
