######################################################################################################
################################     PROMEDIO TIEMPO DE EJECUCION     ################################
######################################################################################################
# Muestra y guarda el tiempo promedio que demoró cada modelo en responder en un archivo .xlsx

import pandas as pd

archivo = r"dataset1.csv"  
df = pd.read_csv(archivo)

# === 2. Asegurar que execution_time sea tipo numérico ===
df['execution_time'] = pd.to_numeric(df['execution_time'], errors='coerce')

# === 3. Agrupar por modelo y calcular promedio de tiempo de ejecución ===
promedios = df.groupby('model')['execution_time'].mean().reset_index()

salida_excel = r"C:\Users\Erik_\OneDrive\Desktop\evaluadoresLLMs\rubrica csv\resultados_resumen\promedios_tiempo_respuesta.xlsx"
promedios.to_excel(salida_excel, index=False)

print("Promedio de tiempo de respuesta por modelo (en segundos):\n")
print(promedios.to_string(index=False))
print(f"\nArchivo guardado en: {salida_excel}")
