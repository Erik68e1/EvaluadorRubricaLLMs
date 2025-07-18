########################################################################################################
################################  VISUALIZAR LAS DIMENSIONES PROMEDIO  #################################
########################################################################################################
# EL promedio general de cada dimension por modelo y un promedio general 

import pandas as pd
import json
import re

def parsear_campo_diccionario(texto):
    try:
        texto = re.sub(r'([{,])\s*([^:{",]+)\s*:', r'\1 "\2":', texto)
        return json.loads(texto)
    except Exception as e:
        print(f"Error: {e}\nTexto problemático: {texto}")
        return {}

ruta_csv = r"evaluadoDeepseek.csv"
ruta_salida_excel = r"resumen_deepseek.xlsx"

df = pd.read_csv(ruta_csv)
df["rubrica"] = df["rubrica"].apply(parsear_campo_diccionario)

dimensiones = [
    'Comprensión de Reglas', 'Validez y Legalidad', 'Razonamiento Estratégico',
    'Factualidad', 'Coherencia Explicativa', 'Claridad Lingüística', 'Adaptabilidad'
]

# Extraer cada dimensión como columna
for dim in dimensiones:
    df[dim] = df["rubrica"].apply(lambda d: d.get(dim, None))

# Calcular promedio por modelo
tabla_promedios = df.groupby("modelo")[dimensiones].mean().round(2).reset_index()

# Agregar columna de media general
tabla_promedios["Promedio General"] = tabla_promedios[dimensiones].mean(axis=1).round(2)

# Exportar a Excel
tabla_promedios.to_excel(ruta_salida_excel, index=False)

print(f"Archivo Excel generado en:\n{ruta_salida_excel}", tabla_promedios)
